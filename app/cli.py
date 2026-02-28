"""Typer CLI: review, mock, stats, fix-figures."""
from __future__ import annotations
import json
import random
import time
import uuid
from datetime import date, datetime
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich import print as rprint

from app.config import MISTAKES_DIR, PROBLEMS_DIR
from app import db, srs, notes, note_chunker, figures as fig_mod
from app.agents import TutorAgent, InterviewerAgent, GraderAgent
from app.llm.factory import get_llm
from app.llm.logging_llm import LoggingLLM
from app.schemas import Problem

app = typer.Typer(
    name="app",
    help="Interview Prep Agent — 八股 + Algorithm mock sessions",
    no_args_is_help=True,
)
console = Console()

review_app = typer.Typer(help="Topic review commands")
app.add_typer(review_app, name="review")


# ---------- helpers ----------

def _now_ts() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _load_problem(path: Path) -> Problem:
    data = json.loads(path.read_text(encoding="utf-8"))
    return Problem(**data)


def _list_problems(tag: str = "", difficulty: str = "") -> list[Path]:
    if not PROBLEMS_DIR.exists():
        return []
    probs = list(PROBLEMS_DIR.glob("*.json"))
    if tag or difficulty:
        filtered = []
        for p in probs:
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
                if tag and tag not in data.get("tags", []):
                    continue
                if difficulty and data.get("difficulty", "").lower() != difficulty.lower():
                    continue
                filtered.append(p)
            except Exception:
                pass
        return filtered
    return probs


def _write_mistake_log(
    timestamp: str,
    topic_or_problem: str,
    prompt_subject: str,
    first_reaction: str,
    trigger_words: str,
    self_questions: list[str],
    next_review_date: date,
) -> Path:
    MISTAKES_DIR.mkdir(parents=True, exist_ok=True)
    filename = MISTAKES_DIR / f"{timestamp}_{topic_or_problem[:20].replace('/', '_')}.md"
    questions_md = "\n".join(f"{i+1}. {q}" for i, q in enumerate(self_questions))
    content = f"""## Session: {timestamp} – {topic_or_problem}
**Prompt / Subject**: {prompt_subject}
**My First Reaction**: {first_reaction}
**Correct Trigger Words**: {trigger_words}
**Next-Time Self-Questions**:
{questions_md}
**Next Review Date**: {next_review_date.isoformat()}
"""
    filename.write_text(content, encoding="utf-8")
    return filename


def _render_score_table(grade, title: str = "评分结果") -> None:
    table = Table(title=title, show_header=True, header_style="bold cyan")
    table.add_column("维度", style="white")
    table.add_column("得分", style="green")
    table.add_column("满分", style="yellow")
    for key, score in grade.score_breakdown.items():
        max_s = grade.max_score  # approximation; real max per-category not stored here
        table.add_row(key, str(score), "-")
    table.add_row("[bold]总分[/bold]", f"[bold]{grade.total}[/bold]", f"[bold]{grade.max_score}[/bold]")
    console.print(table)

    if grade.missed_points:
        console.print("\n[bold red]遗漏要点：[/bold red]")
        for pt in grade.missed_points:
            console.print(f"  • {pt}")

    if grade.model_answer_structure:
        console.print(Panel(grade.model_answer_structure, title="标准答题框架", border_style="blue"))

    if grade.next_drills:
        console.print("\n[bold yellow]推荐练习：[/bold yellow]")
        for d in grade.next_drills:
            console.print(f"  → {d}")


def _collect_mistake_info() -> tuple[str, str, list[str]]:
    """Interactively collect mistake log fields from user."""
    console.print("\n[bold]记录错题（直接回车跳过）[/bold]")
    first_reaction = Prompt.ask("我的第一反应", default="")
    trigger_words = Prompt.ask("正确触发关键词", default="")
    console.print("下次自问（每行一条，空行结束）：")
    self_questions = []
    while True:
        q = input("  > ").strip()
        if not q:
            break
        self_questions.append(q)
    return first_reaction, trigger_words, self_questions


# ---------- token summary ----------

def _print_token_summary(llm: LoggingLLM) -> None:
    """Print a Rich table summarising all LLM calls made during the session."""
    calls = llm.session_summary()
    if not calls:
        return

    table = Table(title="LLM Call Summary", show_header=True, header_style="bold magenta")
    table.add_column("Tag", style="cyan")
    table.add_column("Model", style="white")
    table.add_column("Input tok", justify="right", style="green")
    table.add_column("Output tok", justify="right", style="yellow")
    table.add_column("Latency", justify="right", style="dim")

    for call in calls:
        table.add_row(
            call["tag"] or "—",
            call["model"],
            str(call["input_tokens"]),
            str(call["output_tokens"]),
            f"{call['latency_s']:.3f}s",
        )

    total_in, total_out = llm.total_tokens()
    table.add_row(
        "[bold]TOTAL[/bold]",
        "[bold]—[/bold]",
        f"[bold]{total_in}[/bold]",
        f"[bold]{total_out}[/bold]",
        "[bold]—[/bold]",
    )
    console.print(table)


# ---------- review t <topic> ----------

@review_app.command("t")
def review_topic(
    topic: str = typer.Argument(..., help="Topic name (supports fuzzy match)"),
):
    """Topic review: active recall + grading + spaced repetition."""
    db.init_db()
    ts = _now_ts()

    # 1. Find note
    matches = notes.find_notes(topic)
    if not matches:
        console.print(f"[red]未找到匹配「{topic}」的笔记[/red]")
        raise typer.Exit(1)

    if len(matches) == 1:
        note_path, display = matches[0]
    else:
        console.print("[bold]找到多个匹配：[/bold]")
        for i, (_, d) in enumerate(matches[:5], 1):
            console.print(f"  {i}. {d}")
        idx = Prompt.ask("选择编号", default="1")
        try:
            note_path, display = matches[int(idx) - 1]
        except (ValueError, IndexError):
            note_path, display = matches[0]

    console.print(f"\n[green]已加载：{display}[/green]")

    # 2. Chunk and show outline
    content = notes.load_note(note_path)
    chunks = note_chunker.chunk_note(content)
    outline = note_chunker.build_outline(chunks)
    console.print(Panel(outline, title="笔记目录", border_style="cyan"))

    # 3. Select subtopic
    item_id = display.replace("/", "_")
    weakest_id = srs.get_weakest_item([f"{item_id}_chunk_{c.index}" for c in chunks])

    console.print("\n输入子主题关键词（直接回车=全部，'auto'=自动选最弱）：", end=" ")
    hint = input().strip()

    if hint.lower() == "auto":
        # Auto-pick weakest chunk
        if weakest_id:
            chunk_idx = int(weakest_id.split("_chunk_")[-1])
            selected = [c for c in chunks if c.index == chunk_idx] or chunks
        else:
            selected = chunks
    else:
        selected = note_chunker.select_chunks(chunks, hint)

    selected = note_chunker.chunks_for_prompt(selected, max_tokens=2000)
    chunks_text = note_chunker.format_chunks(selected)

    # 4. TutorAgent: generate questions
    llm = get_llm()
    tutor = TutorAgent(llm)
    with console.status("[cyan]生成复习问题...[/cyan]"):
        questions = tutor.start_session(outline, chunks_text)

    console.print(Panel(
        "\n".join(questions),
        title="主动回忆问题",
        border_style="green",
    ))

    # 5. Answer loop
    console.print("\n[dim]回答问题（输入 'grade' 开始评分，'quit' 退出）[/dim]")
    while True:
        user_input = Prompt.ask("[bold]你的回答[/bold]")
        if user_input.lower() in ("grade", "评分", "done"):
            break
        if user_input.lower() in ("quit", "exit", "退出"):
            raise typer.Exit(0)
        with console.status("[cyan]Tutor 思考中...[/cyan]"):
            response = tutor.answer(user_input)
        console.print(Panel(response, title="Tutor", border_style="yellow"))

    # 6. Grade
    grader = GraderAgent(llm)
    with console.status("[cyan]评分中...[/cyan]"):
        grade = grader.grade_topic(outline, chunks_text, tutor.get_transcript())

    _render_score_table(grade, "主题复习评分")

    # 7. SRS update
    scores = grade.score_breakdown
    # key_concepts_missed is a count, not a score
    kc_missed = scores.pop("key_concepts_missed", 0)
    srs_scores = {**scores, "key_concepts_missed": kc_missed}
    max_scores = {"accuracy": 4, "completeness": 3, "clarity": 2, "key_concepts_missed": 0}

    next_date = srs.update_schedule(
        item_id=item_id,
        item_type="topic",
        scores=srs_scores,
        max_scores=max_scores,
        session_type="topic",
    )
    console.print(f"\n[bold green]下次复习日期: {next_date}[/bold green]")

    # 8. Save session
    session_id = str(uuid.uuid4())
    db.insert_session(
        session_id=session_id,
        timestamp=ts,
        session_type="topic",
        item_id=item_id,
        total_score=grade.total,
        max_score=grade.max_score,
        scores=grade.score_breakdown,
        missed=grade.missed_points,
    )

    # 9. Mistake log
    first_reaction, trigger_words, self_questions = _collect_mistake_info()
    log_path = _write_mistake_log(
        ts, display,
        prompt_subject=", ".join(q for q in questions),
        first_reaction=first_reaction,
        trigger_words=trigger_words,
        self_questions=self_questions if self_questions else grade.next_drills,
        next_review_date=next_date,
    )
    db.insert_mistake(session_id, item_id, ", ".join(questions),
                      first_reaction, trigger_words,
                      self_questions or grade.next_drills,
                      next_date.isoformat())
    console.print(f"[dim]错题记录已保存: {log_path}[/dim]")
    _print_token_summary(llm)


# ---------- mock algo ----------

@app.command("mock")
def mock_algo(
    tag: Optional[str] = typer.Option(None, "--tag", "-t", help="Algorithm pattern tag"),
    difficulty: Optional[str] = typer.Option(None, "--difficulty", "-d", help="easy|medium|hard"),
):
    """Algorithm mock interview session."""
    db.init_db()
    ts = _now_ts()

    prob_paths = _list_problems(tag or "", difficulty or "")
    if not prob_paths:
        console.print("[red]没有符合条件的题目[/red]")
        raise typer.Exit(1)

    # Let user pick or random
    if len(prob_paths) == 1:
        prob_path = prob_paths[0]
    else:
        console.print("[bold]可用题目：[/bold]")
        for i, p in enumerate(prob_paths, 1):
            try:
                d = json.loads(p.read_text(encoding="utf-8"))
                console.print(f"  {i}. {d.get('title','?')} ({d.get('difficulty','?')})")
            except Exception:
                console.print(f"  {i}. {p.stem}")
        idx = Prompt.ask("选择题号（回车随机）", default="")
        if idx.strip().isdigit():
            chosen = int(idx) - 1
            prob_path = prob_paths[chosen] if 0 <= chosen < len(prob_paths) else random.choice(prob_paths)
        else:
            prob_path = random.choice(prob_paths)

    problem = _load_problem(prob_path)

    # Present problem
    llm = get_llm()
    interviewer = InterviewerAgent(llm)
    with console.status("[cyan]准备题目...[/cyan]"):
        presentation = interviewer.present(problem)
    console.print(Panel(presentation, title=f"面试题：{problem.title}", border_style="green"))
    console.print(f"[dim]时间限制: {problem.time_limit_sec // 60} 分钟[/dim]")
    console.print("[dim]输入 'done' 结束作答[/dim]\n")

    # Timer + answer loop
    start_time = time.time()
    while True:
        elapsed = int(time.time() - start_time)
        mins, secs = divmod(elapsed, 60)
        user_input = Prompt.ask(f"[bold][{mins:02d}:{secs:02d}] 你[/bold]")
        if user_input.lower() in ("done", "完成", "finish"):
            break
        with console.status("[cyan]面试官思考中...[/cyan]"):
            response = interviewer.probe(user_input, elapsed)
        console.print(Panel(response, title="面试官", border_style="yellow"))

    # Grade
    grader = GraderAgent(llm)
    with console.status("[cyan]评分中...[/cyan]"):
        grade = grader.grade_algo(problem, interviewer.get_transcript())

    _render_score_table(grade, f"算法面试评分 — {problem.title}")

    # SRS
    rubric = problem.rubric or {
        "recognize_pattern": 3, "correctness": 4,
        "complexity": 2, "edge_cases": 1, "pattern_articulation": 2,
    }
    next_date = srs.update_schedule(
        item_id=problem.id,
        item_type="algo",
        scores=grade.score_breakdown,
        max_scores=rubric,
        session_type="algo",
    )
    console.print(f"\n[bold green]下次复习日期: {next_date}[/bold green]")

    # Save session
    session_id = str(uuid.uuid4())
    db.insert_session(
        session_id=session_id,
        timestamp=ts,
        session_type="algo",
        item_id=problem.id,
        total_score=grade.total,
        max_score=grade.max_score,
        scores=grade.score_breakdown,
        missed=grade.missed_points,
    )

    # Mistake log
    first_reaction, trigger_words, self_questions = _collect_mistake_info()
    log_path = _write_mistake_log(
        ts, problem.id,
        prompt_subject=problem.title,
        first_reaction=first_reaction,
        trigger_words=trigger_words,
        self_questions=self_questions or grade.next_drills,
        next_review_date=next_date,
    )
    db.insert_mistake(session_id, problem.id, problem.title,
                      first_reaction, trigger_words,
                      self_questions or grade.next_drills,
                      next_date.isoformat())
    console.print(f"[dim]错题记录已保存: {log_path}[/dim]")
    _print_token_summary(llm)


# ---------- stats ----------

@app.command("stats")
def stats():
    """Show session history, average scores, and due reviews."""
    db.init_db()
    today = date.today().isoformat()

    sessions = db.get_sessions(limit=50)
    schedule = db.get_all_schedule()
    due = db.get_due_items(today)

    # Sessions this week
    from datetime import timedelta
    week_ago = (date.today() - timedelta(days=7)).strftime("%Y%m%d")

    table = Table(title="最近会话记录", show_header=True, header_style="bold cyan")
    table.add_column("时间", style="dim")
    table.add_column("类型")
    table.add_column("主题/题目")
    table.add_column("得分")
    table.add_column("满分")
    table.add_column("质量")

    for s in sessions[:20]:
        ts = s["timestamp"]
        quality = "N/A"
        sched = next((x for x in schedule if x["item_id"] == s["item_id"]), None)
        if sched:
            quality = f"{sched['last_quality']:.1f}"
        table.add_row(
            ts[:15], s["session_type"], s["item_id"],
            str(s["total_score"]), str(s["max_score"]), quality,
        )
    console.print(table)

    # Due items
    if due:
        due_table = Table(title=f"今日到期复习 ({len(due)} 项)", header_style="bold red")
        due_table.add_column("项目")
        due_table.add_column("类型")
        due_table.add_column("上次质量")
        for item in due:
            due_table.add_row(
                item["item_id"], item["item_type"], f"{item['last_quality']:.1f}"
            )
        console.print(due_table)
    else:
        console.print("[green]今日暂无到期复习[/green]")

    # Schedule summary
    sched_table = Table(title="全部复习计划", header_style="bold yellow")
    sched_table.add_column("项目")
    sched_table.add_column("下次复习")
    sched_table.add_column("间隔(天)")
    sched_table.add_column("EF")
    sched_table.add_column("重复次数")
    for item in schedule:
        sched_table.add_row(
            item["item_id"], item["next_review"],
            f"{item['interval_days']:.0f}", f"{item['ease_factor']:.2f}",
            str(item["repetitions"]),
        )
    console.print(sched_table)


# ---------- fix-figures ----------

@app.command("fix-figures")
def fix_figures(
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview only, do not write"),
):
    """Scan notes for missing figures and generate replacements."""
    with console.status("[cyan]扫描图片占位符...[/cyan]"):
        placeholders = fig_mod.scan_all_notes()

    if not placeholders:
        console.print("[green]未发现图片占位符[/green]")
        return

    console.print(f"[bold]发现 {len(placeholders)} 个占位符[/bold]\n")

    for ph in placeholders:
        console.print(f"[dim]{ph.file}:{ph.line_num}[/dim]  →  {ph.raw_text!r}")

    llm = get_llm()
    console.print()
    for i, ph in enumerate(placeholders, 1):
        console.print(f"\n[bold cyan]占位符 {i}/{len(placeholders)}[/bold cyan]")
        console.print(f"文件: {ph.file}")
        console.print(f"行号: {ph.line_num}")
        console.print(f"原内容: {ph.raw_text!r}")

        with console.status("[cyan]生成替换内容...[/cyan]"):
            try:
                replacement = fig_mod.generate_replacement(ph.context_window, ph.raw_text, llm)
            except Exception as e:
                console.print(f"[red]生成失败: {e}[/red]")
                continue

        diff = fig_mod.preview_diff(ph.file, ph.line_num, ph.raw_text, replacement)
        console.print(Panel(diff, title="Diff 预览", border_style="yellow"))

        if dry_run:
            console.print("[dim]--dry-run 模式，跳过写入[/dim]")
            continue

        if Confirm.ask("应用此替换？", default=False):
            fig_mod.apply_patch(ph.file, ph.line_num, ph.raw_text, replacement)
            console.print("[green]已应用[/green]")
        else:
            console.print("[dim]已跳过[/dim]")
    _print_token_summary(llm)
