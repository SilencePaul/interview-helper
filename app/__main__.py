from __future__ import annotations

import json
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path


def _strip_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def _load_dotenv() -> None:
    env_file = Path(".env")
    if not env_file.exists():
        return
    for raw_line in env_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export "):].strip()
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip()
        if not key:
            continue
        quoted = len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}
        if not quoted and " #" in value:
            value = value.split(" #", 1)[0].rstrip()
        value = _strip_quotes(value)
        os.environ.setdefault(key, value)


_load_dotenv()

_NOTES_DIR = "notes_clean_v2"
_INDEX_PATH = "data/concepts_index.json"
_DATA_DIR = Path("data")
_HISTORY_DIR = _DATA_DIR / "history"
_SUMMARY_DIR = _DATA_DIR / "summaries"
_VALID_PROVIDERS = {"anthropic", "openai", "ollama", "siliconflow"}
_PROVIDER_ENV = {
    "anthropic": ["ANTHROPIC_API_KEY"],
    "openai": ["OPENAI_API_KEY"],
    "ollama": [],
    "siliconflow": ["SILICONFLOW_API_KEY"],
}
_PROVIDER_BASE_URL_ENV = {"ollama": "OLLAMA_BASE_URL", "siliconflow": "SILICONFLOW_BASE_URL"}
_PROVIDER_DEFAULT_BASE_URL = {"ollama": "http://localhost:11434/v1", "siliconflow": "https://api.siliconflow.cn/v1"}
_DIMENSION_LABELS = {"accuracy": "准确性", "completeness": "完整性", "practicality": "场景意识", "clarity": "表达清晰度"}
_LOW_SCORE_THRESHOLD = 6


class ConfigError(RuntimeError):
    pass


def main() -> None:
    args = sys.argv[1:]
    if not args:
        _usage()
        sys.exit(1)
    command = args[0]
    try:
        if command == "build-index":
            _cmd_build_index()
        elif command == "doctor":
            _cmd_doctor()
        elif command == "smoke":
            mode = "prod" if "--prod" in args else "dev"
            _cmd_smoke(mode)
        elif command == "stats":
            limit = _get_int_flag(args, "--limit", 20)
            module = _get_flag(args, "--module")
            as_json = "--json" in args
            _cmd_stats(limit, module=module, as_json=as_json)
        elif command == "history":
            limit = _get_int_flag(args, "--limit", 10)
            latest = "--latest" in args
            low_score_only = "--low-score" in args
            full = "--full" in args
            module = _get_flag(args, "--module")
            as_json = "--json" in args
            _cmd_history(limit=limit, latest=latest, low_score_only=low_score_only, full=full, module=module, as_json=as_json)
        elif command == "summary":
            limit = _get_int_flag(args, "--limit", 10)
            latest = "--latest" in args
            as_json = "--json" in args
            _cmd_summary(limit=limit, latest=latest, as_json=as_json)
        elif command == "study-init":
            base_dir = _get_flag(args, "--dir") or "study"
            _cmd_study_init(base_dir)
        elif command == "study-import":
            source = _get_flag(args, "--file")
            if not source:
                raise ConfigError("study-import requires --file <path>")
            category = _get_flag(args, "--category") or "未分类"
            base_dir = _get_flag(args, "--dir") or "study"
            _cmd_study_import(source, category=category, base_dir=base_dir)
        elif command == "study-import-dir":
            source_dir = _get_flag(args, "--dir")
            if not source_dir:
                raise ConfigError("study-import-dir requires --dir <path>")
            category = _get_flag(args, "--category") or "未分类"
            base_dir = _get_flag(args, "--out") or "study"
            recursive = "--no-recursive" not in args
            _cmd_study_import_dir(source_dir, category=category, base_dir=base_dir, recursive=recursive)
        elif command == "interview":
            mode = "prod" if "--prod" in args else "dev"
            module = _get_flag(args, "--module")
            file = _get_flag(args, "--file")
            review_wrong = "--review-wrong" in args
            no_followup = "--no-followup" in args
            count = _get_int_flag(args, "--count", 1)
            _cmd_interview(mode, module, file, review_wrong, no_followup, count)
        else:
            print(f"Unknown command: {command!r}")
            _usage()
            sys.exit(1)
    except ConfigError as exc:
        print(f"Configuration error: {exc}")
        sys.exit(2)
    except FileNotFoundError as exc:
        print(f"File error: {exc}")
        sys.exit(4)
    except KeyboardInterrupt:
        print("\nInterrupted.")
        sys.exit(130)
    except Exception as exc:
        print(f"Runtime error: {exc}")
        sys.exit(3)


def _cmd_build_index() -> None:
    from knowledge.indexer import build_index
    count = build_index(_NOTES_DIR, _INDEX_PATH)
    print(f"Indexed {count} concepts → {_INDEX_PATH}")


def _get_flag(args: list[str], flag: str) -> str | None:
    try:
        return args[args.index(flag) + 1]
    except (ValueError, IndexError):
        return None


def _get_int_flag(args: list[str], flag: str, default: int) -> int:
    value = _get_flag(args, flag)
    return default if value is None else int(value)


def _validate_runtime(mode: str) -> list[str]:
    issues: list[str] = []
    if not Path(_NOTES_DIR).exists():
        issues.append(f"Notes directory not found: {_NOTES_DIR}")
    if mode == "prod":
        provider = os.environ.get("LLM_PROVIDER", "anthropic").strip().lower()
        if provider not in _VALID_PROVIDERS:
            issues.append("LLM_PROVIDER must be one of: " + " | ".join(sorted(_VALID_PROVIDERS)) + f" (got {provider!r})")
        else:
            for env_name in _PROVIDER_ENV[provider]:
                if not os.environ.get(env_name, "").strip():
                    issues.append(f"{env_name} is required when LLM_PROVIDER={provider}")
            model = os.environ.get("MODEL_INTERVIEWER", "").strip()
            if not model:
                issues.append("MODEL_INTERVIEWER is required in prod mode")
            base_url_env = _PROVIDER_BASE_URL_ENV.get(provider)
            if base_url_env:
                base_url = os.environ.get(base_url_env, _PROVIDER_DEFAULT_BASE_URL[provider]).strip()
                if not (base_url.startswith("http://") or base_url.startswith("https://")):
                    issues.append(f"{base_url_env} must start with http:// or https://")
    return issues


def _ensure_runtime_ok(mode: str, *, require_index: bool = False) -> None:
    issues = _validate_runtime(mode)
    if require_index and not Path(_INDEX_PATH).exists():
        issues.append(f"Index not found: {_INDEX_PATH}. Run `python -m app build-index` first.")
    if issues:
        raise ConfigError("; ".join(issues))


def _cmd_doctor() -> None:
    print("== interview-helper doctor ==")
    print(f"Project root     : {Path.cwd()}")
    print(f"Notes dir        : {_NOTES_DIR} ({'ok' if Path(_NOTES_DIR).exists() else 'missing'})")
    print(f"Index file       : {_INDEX_PATH} ({'ok' if Path(_INDEX_PATH).exists() else 'missing'})")
    print(f"Dotenv file      : .env ({'ok' if Path('.env').exists() else 'missing'})")
    provider = os.environ.get("LLM_PROVIDER", "anthropic").strip().lower()
    model = os.environ.get("MODEL_INTERVIEWER", "").strip()
    print(f"Provider         : {provider}")
    print(f"Model            : {model or '<missing>'}")
    if provider in _PROVIDER_ENV:
        for env_name in _PROVIDER_ENV[provider]:
            print(f"{env_name:<17}: {'set' if bool(os.environ.get(env_name, '').strip()) else 'missing'}")
    base_url_env = _PROVIDER_BASE_URL_ENV.get(provider)
    if base_url_env:
        print(f"{base_url_env:<17}: {os.environ.get(base_url_env, _PROVIDER_DEFAULT_BASE_URL[provider])}")
    issues = _validate_runtime("prod")
    if issues:
        print("\nDoctor result    : FAIL")
        for issue in issues:
            print(f"- {issue}")
        return
    print("\nDoctor result    : OK")


def _load_json_dir(directory: Path, pattern: str, limit: int | None = None) -> list[dict]:
    if not directory.exists():
        return []
    items = []
    for path in sorted(directory.glob(pattern), reverse=True):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        data["__path"] = str(path)
        items.append(data)
        if limit is not None and len(items) >= limit:
            break
    return items


def _load_history(limit: int | None = None) -> list[dict]:
    return _load_json_dir(_HISTORY_DIR, "session-*.json", limit)


def _load_summaries(limit: int | None = None) -> list[dict]:
    return _load_json_dir(_SUMMARY_DIR, "summary-*.json", limit)


def _build_stats_payload(limit: int, module: str | None = None) -> dict | None:
    sessions = _load_history(limit)
    if module:
        sessions = [s for s in sessions if s.get("concept", {}).get("category") == module]
    if not sessions:
        return None
    total = len(sessions)
    avg_score = sum(int(s.get("final_score", 0) or 0) for s in sessions) / total
    low_count = sum(1 for s in sessions if int(s.get("final_score", 0) or 0) < _LOW_SCORE_THRESHOLD)
    dimension_totals = defaultdict(float)
    dimension_counts = defaultdict(int)
    category_scores = defaultdict(list)
    missing_counter = Counter()
    for session in sessions:
        concept = session.get("concept", {})
        category_scores[concept.get("category", "未知")].append(int(session.get("final_score", 0) or 0))
        dimensions = session.get("final_dimensions") or {}
        for key in _DIMENSION_LABELS:
            if key in dimensions:
                dimension_totals[key] += float(dimensions[key])
                dimension_counts[key] += 1
        rounds = session.get("rounds", [])
        if rounds:
            for item in rounds[-1].get("missing_points", [])[:3]:
                missing_counter[item] += 1
    avg_dimensions = {key: (0.0 if dimension_counts[key] == 0 else dimension_totals[key] / dimension_counts[key]) for key in _DIMENSION_LABELS}
    weakest_key = min(avg_dimensions, key=avg_dimensions.get)
    category_averages = [{"category": c, "avgScore": sum(scores) / len(scores), "count": len(scores)} for c, scores in category_scores.items()]
    category_averages.sort(key=lambda item: item["avgScore"])
    return {
        "samples": total,
        "limit": limit,
        "module": module,
        "averageScore": avg_score,
        "lowScoreRate": low_count / total,
        "lowScoreCount": low_count,
        "averageDimensions": avg_dimensions,
        "weakestDimension": {"key": weakest_key, "label": _DIMENSION_LABELS[weakest_key], "value": avg_dimensions[weakest_key]},
        "categoryAverages": category_averages,
        "topMissingPoints": [{"text": text, "count": count} for text, count in missing_counter.most_common(5)],
    }


def _cmd_stats(limit: int, module: str | None = None, as_json: bool = False) -> None:
    payload = _build_stats_payload(limit, module=module)
    if payload is None:
        print("No history found. Run `python -m app interview` first.")
        return
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    print("== interview-helper stats ==")
    print(f"Samples          : {payload['samples']} (latest {payload['limit']})")
    print(f"Average score    : {payload['averageScore']:.2f}/10")
    print(f"Low-score rate   : {payload['lowScoreCount']}/{payload['samples']} ({payload['lowScoreRate']:.0%})")
    print("\nAverage dimensions:")
    for key, label in _DIMENSION_LABELS.items():
        print(f"  - {label}: {payload['averageDimensions'][key]:.2f}")
    print(f"Weakest dimension: {payload['weakestDimension']['label']} ({payload['weakestDimension']['value']:.2f})")
    print("\nCategory averages:")
    for item in payload["categoryAverages"][:10]:
        print(f"  - {item['category']}: {item['avgScore']:.2f}/10 ({item['count']})")
    print("\nTop missing points:")
    for item in payload["topMissingPoints"]:
        print(f"  - {item['text']} ({item['count']})")


def _history_summary(session: dict) -> dict:
    concept = session.get("concept", {})
    dims = session.get("final_dimensions") or {}
    rounds = session.get("rounds", [])
    last_round = rounds[-1] if rounds else {}
    return {
        "savedAt": session.get("saved_at"),
        "path": session.get("__path"),
        "topic": {"category": concept.get("category"), "title": concept.get("title")},
        "score": session.get("final_score"),
        "dimensions": dims,
        "scope": session.get("scope", "Random"),
        "rounds": session.get("round_count", len(rounds)),
        "question": last_round.get("question"),
        "topMissing": (last_round.get("missing_points") or [None])[0],
    }


def _cmd_history(limit: int, latest: bool = False, low_score_only: bool = False, full: bool = False, module: str | None = None, as_json: bool = False) -> None:
    sessions = _load_history(None)
    if not sessions:
        print("No history found. Run `python -m app interview` first.")
        return
    if module:
        sessions = [s for s in sessions if s.get("concept", {}).get("category") == module]
    if low_score_only:
        sessions = [s for s in sessions if int(s.get("final_score", 0) or 0) < _LOW_SCORE_THRESHOLD]
    sessions = sessions[:1] if latest else sessions[:limit]
    if not sessions:
        print("No matching history sessions.")
        return
    if as_json:
        payload = sessions if full else [_history_summary(s) for s in sessions]
        print(json.dumps(payload[0] if latest else payload, ensure_ascii=False, indent=2))
        return
    print("== interview-helper history ==")
    if full and latest and sessions:
        _print_history_full(sessions[0])
        return
    for idx, session in enumerate(sessions, start=1):
        item = _history_summary(session)
        print(f"[{idx}] {item['savedAt'] or '<unknown time>'}")
        print(f"  Path     : {item['path'] or '<unknown path>'}")
        print(f"  Topic    : [{item['topic']['category'] or '未知'}] {item['topic']['title'] or '未知概念'}")
        print(f"  Score    : {item['score']}/10")
        dims = item['dimensions'] or {}
        if dims:
            print("  Dims     : "
                  f"准确性 {dims.get('accuracy', 0)}/4 | "
                  f"完整性 {dims.get('completeness', 0)}/3 | "
                  f"场景意识 {dims.get('practicality', 0)}/2 | "
                  f"表达清晰度 {dims.get('clarity', 0)}/1")
        print(f"  Scope    : {item['scope']}")
        print(f"  Rounds   : {item['rounds']}")
        if item['question']:
            print(f"  Question : {item['question']}")
        if item['topMissing']:
            print(f"  Missing  : {item['topMissing']}")
        print()


def _cmd_summary(limit: int, latest: bool = False, as_json: bool = False) -> None:
    summaries = _load_summaries(None)
    if not summaries:
        print("No summaries found. Run `python -m app interview --count N` first.")
        return
    summaries = summaries[:1] if latest else summaries[:limit]
    if as_json:
        print(json.dumps(summaries[0] if latest else summaries, ensure_ascii=False, indent=2))
        return
    print("== interview-helper summary ==")
    for idx, item in enumerate(summaries, start=1):
        weak = item.get("weakestDimension", {})
        best = item.get("bestTopic", {})
        worst = item.get("worstTopic", {})
        print(f"[{idx}] {item.get('__path', '<unknown path>')}")
        print(f"  Completed  : {item.get('completed')} ")
        print(f"  Avg score  : {item.get('averageScore', 0):.2f}/10")
        print(f"  Weakest    : {weak.get('label', '未知')} ({weak.get('value', 0):.2f})")
        print(f"  Best topic : [{best.get('category', '未知')}] {best.get('title', '未知')} ({best.get('score', '?')}/10)")
        print(f"  Worst topic: [{worst.get('category', '未知')}] {worst.get('title', '未知')} ({worst.get('score', '?')}/10)")
        print(f"  Missing    : {item.get('topMissing', '无')}")
        print(f"  Suggestion : {item.get('suggestion', '')}")
        print()


def _print_history_full(session: dict) -> None:
    concept = session.get("concept", {})
    print(f"Time     : {session.get('saved_at', '<unknown time>')}")
    print(f"Path     : {session.get('__path', '<unknown path>')}")
    print(f"Topic    : [{concept.get('category', '未知')}] {concept.get('title', '未知概念')}")
    print(f"Scope    : {session.get('scope', 'Random')}")
    print(f"Score    : {session.get('final_score', '?')}/10")
    dims = session.get('final_dimensions') or {}
    if dims:
        print("Dims     : "
              f"准确性 {dims.get('accuracy', 0)}/4 | "
              f"完整性 {dims.get('completeness', 0)}/3 | "
              f"场景意识 {dims.get('practicality', 0)}/2 | "
              f"表达清晰度 {dims.get('clarity', 0)}/1")
    print()
    for idx, rnd in enumerate(session.get('rounds', []), start=1):
        print(f"Round {idx}")
        print(f"  Question : {rnd.get('question', '')}")
        print(f"  Answer   : {rnd.get('answer', '')}")
        print(f"  Score    : {rnd.get('score', '?')}/10")
        rd = rnd.get('dimensions') or {}
        if rd:
            print("  Dims     : "
                  f"准确性 {rd.get('accuracy', 0)}/4 | "
                  f"完整性 {rd.get('completeness', 0)}/3 | "
                  f"场景意识 {rd.get('practicality', 0)}/2 | "
                  f"表达清晰度 {rd.get('clarity', 0)}/1")
        strengths = rnd.get('strengths', [])
        if strengths:
            print(f"  Strengths: {'；'.join(strengths)}")
        missing = rnd.get('missing_points', [])
        if missing:
            print(f"  Missing  : {'；'.join(missing)}")
        if rnd.get('ideal_answer'):
            print(f"  Ideal    : {rnd.get('ideal_answer')}")
        print()


def _cmd_study_init(base_dir: str = "study") -> None:
    from study_ingest.importer import setup_workspace
    paths = setup_workspace(base_dir)
    print("Study workspace initialized:")
    for key, value in paths.items():
        print(f"  {key}: {value}")


def _cmd_study_import(source: str, *, category: str = "未分类", base_dir: str = "study") -> None:
    from study_ingest.importer import import_file
    result = import_file(source, category=category, base_dir=base_dir)
    print("Study import completed:")
    for key, value in result.items():
        print(f"  {key}: {value}")


def _cmd_study_import_dir(source_dir: str, *, category: str = "未分类", base_dir: str = "study", recursive: bool = True) -> None:
    from study_ingest.importer import import_dir
    result = import_dir(source_dir, category=category, base_dir=base_dir, recursive=recursive)
    print("Study batch import completed:")
    print(f"  source_dir: {result['source_dir']}")
    print(f"  category: {result['category']}")
    print(f"  recursive: {result['recursive']}")
    print(f"  total_found: {result['total_found']}")
    print(f"  imported_count: {result['imported_count']}")
    print(f"  failed_count: {result['failed_count']}")
    if result['failed']:
        print("  failed:")
        for item in result['failed']:
            print(f"    - {item['file']}: {item['error']}")


def _cmd_interview(mode: str, module: str | None, file: str | None, review_wrong: bool = False, no_followup: bool = False, count: int = 1) -> None:
    from interviewer.interviewer import InterviewerAgent
    from llm.factory import get_llm
    _ensure_runtime_ok(mode, require_index=True)
    llm = get_llm(mode)
    agent = InterviewerAgent(llm=llm, notes_dir=_NOTES_DIR, index_path=_INDEX_PATH)
    agent.run(mode=mode, module=module, file=file, review_wrong=review_wrong, no_followup=no_followup, count=count)


def _cmd_smoke(mode: str) -> None:
    from interviewer.interviewer import InterviewerAgent
    from llm.factory import get_llm
    _ensure_runtime_ok(mode, require_index=False)
    if not Path(_INDEX_PATH).exists():
        _cmd_build_index()
    llm = get_llm(mode)
    agent = InterviewerAgent(llm=llm, notes_dir=_NOTES_DIR, index_path=_INDEX_PATH)
    concept = agent.pick_concept()
    question = agent.generate_question(concept)
    result = agent.evaluate_answer(question, "这是一次 smoke test，用来验证问答与评分链路是否可用。", concept)
    print("Smoke test passed.")
    print(f"Topic            : [{concept.category}] {concept.title}")
    print(f"Question         : {question}")
    print(f"Score            : {result.score}/10")


def _usage() -> None:
    print("Usage:")
    print("  python -m app build-index")
    print("  python -m app doctor")
    print("  python -m app smoke [--prod]")
    print("  python -m app stats [--limit N] [--module <category>] [--json]")
    print("  python -m app history [--limit N] [--latest] [--low-score] [--full] [--module <category>] [--json]")
    print("  python -m app summary [--limit N] [--latest] [--json]")
    print("  python -m app study-init [--dir study]")
    print("  python -m app study-import --file <path> [--category <name>] [--dir study]")
    print("  python -m app study-import-dir --dir <path> [--category <name>] [--out study] [--no-recursive]")
    print("  python -m app interview [--count N] [--no-followup] # random across all concepts")
    print("  python -m app interview --review-wrong       # prioritize low-score history")
    print("  python -m app interview --module <category>  # restrict to one category")
    print("  python -m app interview --file <filename.md> # restrict to one file")
    print("  python -m app interview --prod               # prod mode (reads .env)")
    print()
    print("Providers (set LLM_PROVIDER in .env):")
    print("  anthropic   — ANTHROPIC_API_KEY required")
    print("  openai      — OPENAI_API_KEY required")
    print("  ollama      — local, no API key needed")
    print("  siliconflow — SILICONFLOW_API_KEY required")


if __name__ == "__main__":
    main()
