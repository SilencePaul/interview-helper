from __future__ import annotations

import json
import uuid
from dataclasses import asdict
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from app.__main__ import _INDEX_PATH, _build_stats_payload, _load_history, _load_summaries
from interviewer.interviewer import HistoryRound, InterviewerAgent
from knowledge.indexer import load_index
from llm.factory import get_llm

_SESSIONS: dict[str, dict] = {}

HTML = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>interview-helper UI</title>
  <style>
    body { font-family: system-ui, sans-serif; margin: 0; background: #0b1020; color: #e8ecf1; }
    .wrap { max-width: 1180px; margin: 0 auto; padding: 24px; }
    h1,h2,h3 { margin: 0 0 12px; }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px; }
    .card { background: #121933; border: 1px solid #23305f; border-radius: 14px; padding: 16px; box-shadow: 0 6px 24px rgba(0,0,0,.25); }
    .muted { color: #9aa6c2; }
    .big { font-size: 30px; font-weight: 700; }
    .row { display: flex; justify-content: space-between; gap: 12px; margin: 8px 0; align-items: center; }
    .pill { display:inline-block; padding: 4px 10px; border-radius: 999px; background:#1d2852; color:#b7c6ff; font-size:12px; }
    pre { white-space: pre-wrap; word-break: break-word; background:#0c1330; padding: 12px; border-radius: 10px; overflow:auto; }
    table { width:100%; border-collapse: collapse; }
    td,th { padding: 8px; border-bottom: 1px solid #23305f; text-align:left; vertical-align: top; }
    a { color:#8fb3ff; cursor:pointer; text-decoration: underline; }
    input,button,select,textarea,label { font: inherit; }
    input,button,select,textarea { background:#0c1330; color:#e8ecf1; border:1px solid #33437a; border-radius:10px; padding:8px 10px; }
    textarea { width:100%; min-height:140px; }
    button { cursor:pointer; }
    .form-grid { display:grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap:12px; }
    .checks { display:flex; gap:16px; flex-wrap:wrap; align-items:center; }
    .checks label { display:flex; gap:8px; align-items:center; color:#d7def0; }
    .mono { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }
    .ok { color:#73e2a7; }
    .warn { color:#ffd166; }
    .err { color:#ff7b7b; }
    ul { margin: 8px 0 0 18px; }
    .score-grid { display:grid; grid-template-columns: 130px 1fr 56px; gap:10px; align-items:center; margin-top:8px; }
    .bar { height:10px; background:#0c1330; border-radius:999px; overflow:hidden; border:1px solid #23305f; }
    .fill { height:100%; background:linear-gradient(90deg,#6ea8fe,#73e2a7); }
    .meta-grid { display:grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap:10px; margin-top:10px; }
    .subcard { background:#0c1330; border:1px solid #23305f; border-radius:12px; padding:12px; }
  </style>
</head>
<body>
<div class="wrap">
  <h1>interview-helper UI</h1>
  <p class="muted">轻量 Web 面板：在线答题、训练统计、最近历史、最近 summary。</p>

  <div class="card" style="margin-bottom:16px;">
    <div class="row"><h2>在线答题</h2><span class="pill">可直接作答</span></div>
    <div class="form-grid">
      <div>
        <div class="muted">模式</div>
        <select id="mode"><option value="dev">dev</option><option value="prod">prod</option></select>
      </div>
      <div>
        <div class="muted">模块</div>
        <select id="module"><option value="">随机</option></select>
      </div>
      <div>
        <div class="muted">会话</div>
        <div id="session-pill" class="pill">未开始</div>
      </div>
      <div>
        <div class="muted">当前状态</div>
        <div id="qa-status" class="pill">待开始</div>
      </div>
    </div>
    <div class="checks" style="margin-top:12px;">
      <label><input id="reviewWrong" type="checkbox" /> review-wrong</label>
      <label><input id="noFollowup" type="checkbox" /> no-followup</label>
      <button onclick="startSession()">开始答题</button>
    </div>
    <div id="qa-box" style="margin-top:16px; display:none;">
      <div class="row"><div class="muted">当前题目</div><div id="topic-pill" class="pill">—</div></div>
      <pre id="question-box"></pre>
      <div class="muted">你的回答</div>
      <textarea id="answer-box" placeholder="在这里输入回答..."></textarea>
      <div style="margin-top:12px; display:flex; gap:10px; flex-wrap:wrap;">
        <button id="submit-btn" onclick="submitAnswer()">提交答案</button>
        <button id="next-btn" onclick="startSession()" style="display:none;">下一题</button>
      </div>
      <div class="muted" style="margin-top:12px;">结果</div>
      <div id="result-box" class="card" style="margin-top:8px;">等待作答…</div>
    </div>
  </div>

  <div class="grid" id="stats"></div>

  <div class="grid" style="margin-top:16px;">
    <div class="card">
      <div class="row"><h2>最近 History</h2><span class="pill" id="history-count"></span></div>
      <table id="history-table"></table>
    </div>
    <div class="card">
      <div class="row"><h2>最近 Summary</h2><span class="pill" id="summary-count"></span></div>
      <table id="summary-table"></table>
    </div>
  </div>

  <div class="grid" style="margin-top:16px; grid-template-columns: 1fr 1fr;">
    <div class="card">
      <div class="row"><h2>详情</h2><span class="pill">history / summary</span></div>
      <div id="detail-box">点击上面的 Topic 或 Summary 行查看详情。</div>
    </div>
    <div class="card">
      <div class="row"><h2>JSON 预览</h2>
        <div>
          <button onclick="loadJson('stats')">stats</button>
          <button onclick="loadJson('history')">history</button>
          <button onclick="loadJson('summary')">summary</button>
        </div>
      </div>
      <pre id="json-box">点击上面的按钮查看 JSON。</pre>
    </div>
  </div>
</div>
<script>
let currentSessionId = null;
async function j(url, options){ const r = await fetch(url, options); return await r.json(); }
function card(title, value, extra='') { return `<div class="card"><div class="muted">${title}</div><div class="big">${value}</div><div class="muted">${extra}</div></div>`; }
function esc(s){ return String(s ?? '').replaceAll('&','&amp;').replaceAll('<','&lt;'); }
async function refreshDashboard(first=false){
  const stats = await j('/api/stats?limit=20');
  const history = await j('/api/history?limit=8');
  const summary = await j('/api/summary?limit=8');
  if (first) {
    const modules = await j('/api/modules');
    const modSel = document.getElementById('module');
    modules.forEach(name => { const opt = document.createElement('option'); opt.value = name; opt.textContent = name; modSel.appendChild(opt); });
  }
  document.getElementById('stats').innerHTML = [
    card('平均分', (stats.averageScore ?? 0).toFixed(2) + '/10', 'samples=' + stats.samples),
    card('低分率', Math.round((stats.lowScoreRate ?? 0) * 100) + '%', 'count=' + (stats.lowScoreCount ?? 0)),
    card('最弱维度', stats.weakestDimension?.label ?? '—', (stats.weakestDimension?.value ?? 0).toFixed(2)),
    card('Top Missing', stats.topMissingPoints?.[0]?.text ?? '—', '出现 ' + (stats.topMissingPoints?.[0]?.count ?? 0) + ' 次'),
  ].join('');
  document.getElementById('history-count').textContent = String(history.length);
  document.getElementById('history-table').innerHTML = '<tr><th>Topic</th><th>分数</th><th>Missing</th></tr>' + history.map((x,i)=>`<tr><td><a onclick="showHistory(${i})">[${esc(x.topic?.category)}] ${esc(x.topic?.title)}</a></td><td>${esc(x.score)}/10</td><td>${esc(x.topMissing||'')}</td></tr>`).join('');
  window.__history = history;
  document.getElementById('summary-count').textContent = String(summary.length);
  document.getElementById('summary-table').innerHTML = '<tr><th>平均分</th><th>最弱维度</th><th>建议</th></tr>' + summary.map((x,i)=>`<tr><td><a onclick="showSummary(${i})">${(x.averageScore ?? 0).toFixed(2)}/10</a></td><td>${esc(x.weakestDimension?.label || '')}</td><td>${esc(x.suggestion || '')}</td></tr>`).join('');
  window.__summary = summary;
}
async function boot(){ await refreshDashboard(true); }
async function startSession(){
  const payload = {
    mode: document.getElementById('mode').value,
    module: document.getElementById('module').value,
    reviewWrong: document.getElementById('reviewWrong').checked,
    noFollowup: document.getElementById('noFollowup').checked,
  };
  const data = await j('/api/session/start', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload)});
  currentSessionId = data.sessionId;
  document.getElementById('session-pill').textContent = data.sessionId;
  document.getElementById('qa-status').textContent = '第 1 轮';
  document.getElementById('qa-box').style.display = 'block';
  document.getElementById('topic-pill').textContent = `[${data.topic?.category || '未知'}] ${data.topic?.title || '未知题目'}`;
  document.getElementById('question-box').textContent = data.question;
  document.getElementById('answer-box').value = '';
  document.getElementById('result-box').textContent = '等待作答…';
  document.getElementById('submit-btn').disabled = false;
  document.getElementById('submit-btn').textContent = '提交答案';
  document.getElementById('next-btn').style.display = 'none';
}
function renderResult(data){
  if (data.error) {
    document.getElementById('result-box').innerHTML = `<div class="err">${esc(data.error)}</div>`;
    return;
  }
  const r = data.result || {};
  const dims = r.dimensions || {};
  const strengths = (r.strengths || []).map(x => `<li>${esc(x)}</li>`).join('');
  const missing = (r.missingPoints || []).map(x => `<li>${esc(x)}</li>`).join('');
  const statusLine = data.status === 'followup'
    ? `<div class="warn"><strong>需要追问：</strong>当前分数偏低，下面是追问题目。</div>`
    : `<div class="ok"><strong>本轮完成。</strong>${data.historyPath ? ` 已保存到 <span class="mono">${esc(data.historyPath)}</span>` : ''}</div>`;
  const bars = [
    ['准确性', dims.accuracy ?? 0, 4],
    ['完整性', dims.completeness ?? 0, 3],
    ['场景意识', dims.practicality ?? 0, 2],
    ['表达清晰度', dims.clarity ?? 0, 1],
  ].map(([label, value, max]) => `
    <div class="score-grid">
      <div class="muted">${label}</div>
      <div class="bar"><div class="fill" style="width:${(Number(value) / Number(max)) * 100}%"></div></div>
      <div>${value}/${max}</div>
    </div>
  `).join('');
  document.getElementById('result-box').innerHTML = `
    ${statusLine}
    <div class="meta-grid">
      <div class="subcard"><div class="muted">总分</div><div class="big">${esc(r.score ?? '-')}</div></div>
      <div class="subcard"><div class="muted">当前状态</div><div>${data.status === 'followup' ? '待追问' : '已完成'}</div></div>
      <div class="subcard"><div class="muted">会话</div><div>${esc(document.getElementById('session-pill').textContent)}</div></div>
    </div>
    <div style="margin-top:10px;"><strong>维度分</strong>${bars}</div>
    <div style="margin-top:10px;"><strong>Strengths</strong><ul>${strengths || '<li>—</li>'}</ul></div>
    <div style="margin-top:10px;"><strong>Missing Points</strong><ul>${missing || '<li>—</li>'}</ul></div>
    <div style="margin-top:10px;"><strong>Ideal Answer</strong><pre>${esc(r.idealAnswer || '')}</pre></div>
  `;
}
async function submitAnswer(){
  if(!currentSessionId) return;
  const btn = document.getElementById('submit-btn');
  btn.disabled = true;
  btn.textContent = '提交中...';
  const answer = document.getElementById('answer-box').value;
  const data = await j('/api/session/answer', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({sessionId: currentSessionId, answer})});
  renderResult(data);
  if (data.nextQuestion) {
    document.getElementById('qa-status').textContent = '第 2 轮（追问）';
    document.getElementById('question-box').textContent = data.nextQuestion;
    document.getElementById('answer-box').value = '';
    btn.disabled = false;
    btn.textContent = '提交答案';
  } else if (data.status === 'done') {
    document.getElementById('session-pill').textContent = '已完成';
    document.getElementById('qa-status').textContent = '本轮完成';
    document.getElementById('next-btn').style.display = 'inline-block';
    btn.disabled = false;
    btn.textContent = '提交答案';
    await refreshDashboard(false);
  } else {
    btn.disabled = false;
    btn.textContent = '提交答案';
  }
}
async function loadJson(kind){
  const url = kind === 'stats' ? '/api/stats?limit=20' : kind === 'history' ? '/api/history?limit=5' : '/api/summary?limit=5';
  const data = await j(url);
  document.getElementById('json-box').textContent = JSON.stringify(data, null, 2);
}
function showHistory(i){
  const x = window.__history[i];
  const rounds = (x.rounds || []).map((r, idx) => `
    <div class="card" style="margin-top:10px;">
      <div><strong>Round ${idx + 1}</strong></div>
      <div class="muted">Question</div><pre>${esc(r.question || '')}</pre>
      <div class="muted">Answer</div><pre>${esc(r.answer || '')}</pre>
      <div class="muted">Score</div><div>${esc(r.score || '')}/10</div>
      <div class="muted">Missing</div><ul>${(r.missing_points || []).map(m => `<li>${esc(m)}</li>`).join('') || '<li>—</li>'}</ul>
      <div class="muted">Ideal Answer</div><pre>${esc(r.ideal_answer || '')}</pre>
    </div>
  `).join('');
  document.getElementById('detail-box').innerHTML = `
    <div class="card">
      <div class="row"><strong>[${esc(x.topic?.category)}] ${esc(x.topic?.title)}</strong><span class="pill">${esc(x.score)}/10</span></div>
      <div class="muted">Scope: ${esc(x.scope || 'Random')}</div>
      <div class="muted">Path: ${esc(x.path || '')}</div>
      ${rounds || '<div class="muted">无详情</div>'}
    </div>
  `;
}
function showSummary(i){
  const x = window.__summary[i];
  const topics = (x.topics || []).map(t => `<li>[${esc(t.category)}] ${esc(t.title)} (${esc(t.score)}/10)</li>`).join('');
  document.getElementById('detail-box').innerHTML = `
    <div class="card">
      <div class="row"><strong>Session Summary</strong><span class="pill">${(x.averageScore ?? 0).toFixed(2)}/10</span></div>
      <div class="muted">Completed: ${esc(x.completed)}</div>
      <div class="muted">Low-score rounds: ${esc(x.lowScoreRounds)}</div>
      <div class="muted">Weakest: ${esc(x.weakestDimension?.label || '')}</div>
      <div class="muted">Best topic: [${esc(x.bestTopic?.category || '')}] ${esc(x.bestTopic?.title || '')}</div>
      <div class="muted">Worst topic: [${esc(x.worstTopic?.category || '')}] ${esc(x.worstTopic?.title || '')}</div>
      <div class="muted">Top missing</div><pre>${esc(x.topMissing || '')}</pre>
      <div class="muted">Suggestion</div><pre>${esc(x.suggestion || '')}</pre>
      <div class="muted">Topics</div><ul>${topics || '<li>—</li>'}</ul>
    </div>
  `;
}
boot();
</script>
</body>
</html>
"""


def _history_item(s: dict) -> dict:
    concept = s.get("concept", {})
    rounds = s.get("rounds", [])
    last = rounds[-1] if rounds else {}
    return {
        "savedAt": s.get("saved_at"),
        "path": s.get("__path"),
        "topic": {"category": concept.get("category"), "title": concept.get("title")},
        "score": s.get("final_score"),
        "dimensions": s.get("final_dimensions") or {},
        "topMissing": (last.get("missing_points") or [None])[0],
        "rounds": rounds,
        "scope": s.get("scope"),
    }


def _start_session(payload: dict) -> dict:
    mode = payload.get("mode", "dev")
    llm = get_llm(mode)
    agent = InterviewerAgent(llm=llm, notes_dir="notes_clean_v2", index_path=_INDEX_PATH)
    pool = agent._index
    module = payload.get("module") or None
    if module:
        pool = [e for e in pool if e.category == module]
    if payload.get("reviewWrong"):
        review_pool = agent.load_review_candidates(pool)
        if review_pool:
            pool = review_pool
    concept = agent.pick_concept(pool)
    question = agent.generate_question(concept)
    session_id = str(uuid.uuid4())[:8]
    _SESSIONS[session_id] = {
        "agent": agent,
        "mode": mode,
        "module": module,
        "concept": concept,
        "question": question,
        "round": 1,
        "rounds": [],
        "noFollowup": bool(payload.get("noFollowup")),
        "done": False,
    }
    return {"sessionId": session_id, "question": question, "topic": {"category": concept.category, "title": concept.title}}


def _score_payload(result) -> dict:
    return {
        "score": result.score,
        "dimensions": result.dimensions,
        "strengths": result.strengths,
        "missingPoints": result.missing_points,
        "idealAnswer": result.ideal_answer,
    }


def _answer_session(payload: dict) -> dict:
    session_id = payload["sessionId"]
    state = _SESSIONS.get(session_id)
    if not state:
        return {"error": "session not found"}
    if state["done"]:
        return {"error": "session already finished"}
    answer = (payload.get("answer") or "").strip()
    if not answer:
        return {"error": "answer is empty"}

    agent = state["agent"]
    concept = state["concept"]
    question = state["question"]
    result = agent.evaluate_answer(question, answer, concept)
    state["rounds"].append(HistoryRound(state["round"], question, answer, result.score, result.dimensions, result.strengths, result.missing_points, result.ideal_answer))

    if result.score < 6 and not state["noFollowup"] and state["round"] == 1:
        followup = agent.generate_followup(concept, question, answer, result.missing_points, result.dimensions)
        state["question"] = followup
        state["round"] = 2
        return {"status": "followup", "result": _score_payload(result), "nextQuestion": followup}

    saved = agent.save_history(mode=state["mode"], scope=state["module"] or "Random", concept=concept, rounds=state["rounds"])
    state["done"] = True
    return {"status": "done", "result": _score_payload(result), "historyPath": str(saved)}


class Handler(BaseHTTPRequestHandler):
    def _send_json(self, payload: object, status: int = 200) -> None:
        data = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _send_html(self, html: str, status: int = 200) -> None:
        data = html.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        limit = int(query.get("limit", ["10"])[0])
        if parsed.path == "/":
            self._send_html(HTML); return
        if parsed.path == "/api/modules":
            try:
                names = sorted({entry.category for entry in load_index(_INDEX_PATH)})
            except Exception:
                names = []
            self._send_json(names); return
        if parsed.path == "/api/stats":
            self._send_json(_build_stats_payload(limit) or {"error": "no stats"}); return
        if parsed.path == "/api/history":
            self._send_json([_history_item(s) for s in _load_history(limit)]); return
        if parsed.path == "/api/summary":
            self._send_json(_load_summaries(limit)); return
        self._send_json({"error": "not found"}, status=HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        length = int(self.headers.get("Content-Length", "0"))
        payload = json.loads(self.rfile.read(length) or b"{}")
        if parsed.path == "/api/session/start":
            self._send_json(_start_session(payload), status=HTTPStatus.CREATED); return
        if parsed.path == "/api/session/answer":
            result = _answer_session(payload)
            self._send_json(result, status=200 if "error" not in result else 400); return
        self._send_json({"error": "not found"}, status=HTTPStatus.NOT_FOUND)


def main(host: str = "127.0.0.1", port: int = 8008) -> None:
    server = ThreadingHTTPServer((host, port), Handler)
    print(f"interview-helper UI: http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
