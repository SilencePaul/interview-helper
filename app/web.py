from __future__ import annotations

import json
import uuid
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
    :root {
      --bg: #1a1a1a;
      --panel: #262626;
      --panel-2: #2f2f2f;
      --line: #3a3a3a;
      --text: #f5f5f5;
      --muted: #b8b8b8;
      --green: #2ecc71;
      --yellow: #f7c948;
      --red: #ff6b6b;
      --blue: #0ea5e9;
      --blue-2: #38bdf8;
      --accent: #ffa116;
      --shadow: 0 10px 30px rgba(0,0,0,.28);
      --radius: 14px;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    .app { max-width: 1380px; margin: 0 auto; padding: 20px; }
    .topbar {
      display: flex; align-items: center; justify-content: space-between; gap: 16px;
      padding: 14px 18px; border: 1px solid var(--line); background: #202020; border-radius: 16px; box-shadow: var(--shadow);
      margin-bottom: 18px;
    }
    .brand h1 { margin: 0; font-size: 22px; font-weight: 800; letter-spacing: -.02em; }
    .brand p { margin: 6px 0 0; color: var(--muted); font-size: 13px; }
    .top-actions { display:flex; gap:10px; flex-wrap: wrap; }
    .pill {
      display:inline-flex; align-items:center; gap:8px; padding: 6px 12px; border-radius: 999px;
      background: #303030; color: #f1f1f1; border: 1px solid #474747; font-size: 12px; font-weight: 600;
    }
    .layout { display:grid; grid-template-columns: 1.25fr .75fr; gap: 18px; }
    .panel {
      background: var(--panel); border: 1px solid var(--line); border-radius: 18px; box-shadow: var(--shadow);
      overflow: hidden;
    }
    .panel-head {
      display:flex; justify-content:space-between; align-items:center; gap:12px;
      padding: 16px 18px; border-bottom: 1px solid var(--line); background: linear-gradient(180deg, rgba(255,255,255,.02), rgba(255,255,255,0));
    }
    .panel-head h2, .panel-head h3 { margin: 0; font-size: 17px; }
    .panel-body { padding: 18px; }
    .meta-grid { display:grid; grid-template-columns: repeat(4, minmax(0,1fr)); gap: 10px; margin-bottom: 14px; }
    .meta-card {
      padding: 14px; border-radius: 14px; background: var(--panel-2); border: 1px solid var(--line);
    }
    .meta-card .label { color: var(--muted); font-size: 12px; margin-bottom: 8px; }
    .meta-card .value { font-size: 15px; font-weight: 700; line-height: 1.35; }
    .question-box {
      padding: 16px 18px; border-radius: 16px; background: #1f1f1f; border: 1px solid #3d3d3d;
      font-size: 18px; line-height: 1.65; margin-bottom: 14px;
    }
    .section-label { color: var(--muted); font-size: 12px; margin-bottom: 8px; text-transform: uppercase; letter-spacing: .06em; }
    textarea {
      width: 100%; min-height: 220px; resize: vertical; padding: 14px 16px; border-radius: 16px;
      background: #1e1e1e; border: 1px solid #444; color: var(--text); font: inherit; line-height: 1.6; outline: none;
    }
    textarea:focus, select:focus, button:focus { box-shadow: 0 0 0 3px rgba(255,161,22,.18); border-color: var(--accent); }
    .controls { display:grid; grid-template-columns: repeat(4, minmax(0,1fr)); gap: 10px; margin-bottom: 14px; }
    select, button {
      width: 100%; padding: 10px 12px; border-radius: 12px; border: 1px solid #4a4a4a; background: #2d2d2d; color: var(--text); font: inherit;
    }
    .checks { display:flex; gap: 14px; flex-wrap: wrap; margin: 10px 0 16px; }
    .checks label { color: var(--muted); font-size: 14px; display:flex; align-items:center; gap: 8px; }
    .action-row { display:flex; gap: 10px; margin-top: 12px; }
    .btn-primary { background: var(--accent); color: #1c1c1c; border-color: #f0a020; font-weight: 800; }
    .btn-secondary { background: #323232; color: #f3f3f3; }
    .status-banner {
      margin-bottom: 14px; padding: 12px 14px; border-radius: 14px; border:1px solid var(--line); background: #222;
      font-size: 14px; line-height: 1.5;
    }
    .status-ok { border-color: rgba(46, 204, 113, .35); background: rgba(46, 204, 113, .08); color: #c8f7db; }
    .status-warn { border-color: rgba(247, 201, 72, .35); background: rgba(247, 201, 72, .08); color: #fff1bf; }
    .status-err { border-color: rgba(255, 107, 107, .35); background: rgba(255, 107, 107, .08); color: #ffd4d4; }
    .score-hero {
      display:grid; grid-template-columns: 200px 1fr; gap: 16px; align-items: stretch; margin-bottom: 16px;
    }
    .score-card {
      border-radius: 18px; padding: 18px; background: linear-gradient(180deg, rgba(255,161,22,.18), rgba(255,161,22,.04));
      border: 1px solid rgba(255,161,22,.35);
    }
    .score-card .label { color:#ffd7a3; font-size: 12px; text-transform: uppercase; letter-spacing: .08em; }
    .score-card .score { font-size: 56px; font-weight: 900; line-height: 1; margin-top: 10px; }
    .score-card .outof { color: var(--muted); margin-top: 6px; }
    .metric-list { display:grid; gap: 10px; }
    .metric { padding: 12px 14px; border-radius: 14px; background: #202020; border: 1px solid var(--line); }
    .metric-top { display:flex; justify-content:space-between; gap: 10px; margin-bottom: 8px; font-size: 14px; }
    .bar { height: 10px; background: #151515; border-radius: 999px; overflow:hidden; border: 1px solid #373737; }
    .fill { height:100%; background: linear-gradient(90deg, var(--blue), var(--blue-2)); }
    .result-grid { display:grid; grid-template-columns: 1fr 1fr; gap: 14px; }
    .result-card {
      padding: 16px; border-radius: 16px; background: #202020; border: 1px solid var(--line);
    }
    .result-card h3 { margin: 0 0 10px; font-size: 14px; color: #f0f0f0; }
    .result-card ul { margin: 0; padding-left: 20px; line-height: 1.6; }
    pre {
      margin: 0; white-space: pre-wrap; word-break: break-word; line-height: 1.65; background: #1b1b1b; border: 1px solid #353535;
      padding: 14px; border-radius: 14px; color: #f1f1f1;
    }
    .stats-grid { display:grid; grid-template-columns: repeat(4, minmax(0,1fr)); gap: 12px; }
    .stats-card { padding: 16px; border-radius: 16px; background: #202020; border: 1px solid var(--line); }
    .stats-card .title { color: var(--muted); font-size: 12px; margin-bottom: 8px; }
    .stats-card .big { font-size: 28px; font-weight: 800; }
    .sidebar-stack { display:grid; gap: 18px; }
    table { width:100%; border-collapse: collapse; }
    th, td { text-align:left; padding: 10px 8px; border-bottom: 1px solid #343434; vertical-align: top; }
    th { color: var(--muted); font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: .05em; }
    a { color: #ffd089; text-decoration: none; cursor: pointer; }
    a:hover { text-decoration: underline; }
    .detail-card { padding: 16px; border-radius: 16px; background:#202020; border:1px solid var(--line); }
    .detail-block { margin-top: 12px; }
    .detail-title { color: var(--muted); font-size: 12px; margin-bottom: 6px; text-transform: uppercase; letter-spacing: .06em; }
    .empty { color: var(--muted); }
    .footer-note { color: var(--muted); font-size: 12px; margin-top: 10px; }
    @media (max-width: 1100px) {
      .layout { grid-template-columns: 1fr; }
      .meta-grid, .controls, .stats-grid { grid-template-columns: repeat(2, minmax(0,1fr)); }
      .score-hero, .result-grid { grid-template-columns: 1fr; }
    }
    @media (max-width: 720px) {
      .app { padding: 14px; }
      .meta-grid, .controls, .stats-grid { grid-template-columns: 1fr; }
      .topbar { flex-direction: column; align-items: stretch; }
    }
  </style>
</head>
<body>
<div class="app">
  <div class="topbar">
    <div class="brand">
      <h1>interview-helper</h1>
      <p>LeetCode 风格训练面板：做题、评分、复盘、查看历史。</p>
    </div>
    <div class="top-actions">
      <span class="pill">Online Practice</span>
      <span class="pill">History</span>
      <span class="pill">Summary</span>
    </div>
  </div>

  <div class="layout">
    <div class="panel">
      <div class="panel-head">
        <h2>在线答题</h2>
        <div class="pill" id="session-pill">未开始</div>
      </div>
      <div class="panel-body">
        <div class="controls">
          <select id="mode"><option value="dev">dev</option><option value="prod">prod</option></select>
          <select id="module"><option value="">随机模块</option></select>
          <button class="btn-secondary" onclick="startSession()">开始答题</button>
          <div class="pill" id="qa-status">待开始</div>
        </div>

        <div class="checks">
          <label><input id="reviewWrong" type="checkbox" /> 错题优先</label>
          <label><input id="noFollowup" type="checkbox" /> 跳过追问</label>
        </div>

        <div class="meta-grid">
          <div class="meta-card"><div class="label">当前 Topic</div><div class="value" id="topic-pill">—</div></div>
          <div class="meta-card"><div class="label">模式</div><div class="value" id="mode-meta">dev</div></div>
          <div class="meta-card"><div class="label">刷题策略</div><div class="value" id="strategy-meta">默认</div></div>
          <div class="meta-card"><div class="label">当前轮次</div><div class="value" id="round-meta">—</div></div>
        </div>

        <div class="section-label">Question</div>
        <div class="question-box" id="question-box">点击“开始答题”后，这里会显示题目。</div>

        <div class="section-label">Your Answer</div>
        <textarea id="answer-box" placeholder="在这里输入回答，像做 LeetCode 题解一样，尽量有结构地表达。"></textarea>

        <div class="action-row">
          <button id="submit-btn" class="btn-primary" onclick="submitAnswer()">提交答案</button>
          <button id="next-btn" class="btn-secondary" onclick="startSession()" style="display:none;">下一题</button>
        </div>

        <div class="footer-note">提示：如果不开“跳过追问”，低分题会自动进入第二轮追问。</div>

        <div style="margin-top:18px;">
          <div class="section-label">Result</div>
          <div id="result-box" class="empty">等待作答…</div>
        </div>
      </div>
    </div>

    <div class="sidebar-stack">
      <div class="panel">
        <div class="panel-head"><h3>训练统计</h3><span class="pill">Live</span></div>
        <div class="panel-body">
          <div class="stats-grid" id="stats"></div>
        </div>
      </div>

      <div class="panel">
        <div class="panel-head"><h3>最近 History</h3><span class="pill" id="history-count"></span></div>
        <div class="panel-body"><table id="history-table"></table></div>
      </div>

      <div class="panel">
        <div class="panel-head"><h3>最近 Summary</h3><span class="pill" id="summary-count"></span></div>
        <div class="panel-body"><table id="summary-table"></table></div>
      </div>
    </div>
  </div>

  <div class="layout" style="margin-top:18px;">
    <div class="panel">
      <div class="panel-head"><h3>详情</h3><span class="pill">Structured View</span></div>
      <div class="panel-body"><div id="detail-box" class="empty">点击右侧列表中的 Topic 或 Summary 查看详情。</div></div>
    </div>
    <div class="panel">
      <div class="panel-head">
        <h3>JSON 预览</h3>
        <div class="top-actions">
          <button class="btn-secondary" onclick="loadJson('stats')">stats</button>
          <button class="btn-secondary" onclick="loadJson('history')">history</button>
          <button class="btn-secondary" onclick="loadJson('summary')">summary</button>
        </div>
      </div>
      <div class="panel-body"><pre id="json-box">点击上面的按钮查看 JSON。</pre></div>
    </div>
  </div>
</div>
<script>
let currentSessionId = null;
async function j(url, options){ const r = await fetch(url, options); return await r.json(); }
function esc(s){ return String(s ?? '').replaceAll('&','&amp;').replaceAll('<','&lt;'); }
function statCard(title, value, extra=''){ return `<div class="stats-card"><div class="title">${title}</div><div class="big">${value}</div><div class="title">${extra}</div></div>`; }
function setStatus(text){ document.getElementById('qa-status').textContent = text; document.getElementById('round-meta').textContent = text; }
function setStrategyMeta(){
  const review = document.getElementById('reviewWrong').checked ? '错题优先' : '随机';
  const follow = document.getElementById('noFollowup').checked ? '跳过追问' : '允许追问';
  document.getElementById('strategy-meta').textContent = `${review} / ${follow}`;
  document.getElementById('mode-meta').textContent = document.getElementById('mode').value;
}
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
    statCard('平均分', ((stats.averageScore ?? 0).toFixed(2)) + '/10', 'samples=' + (stats.samples ?? 0)),
    statCard('低分率', Math.round((stats.lowScoreRate ?? 0) * 100) + '%', 'count=' + (stats.lowScoreCount ?? 0)),
    statCard('最弱维度', esc(stats.weakestDimension?.label ?? '—'), (stats.weakestDimension?.value ?? 0).toFixed(2)),
    statCard('Top Missing', esc(stats.topMissingPoints?.[0]?.text ?? '—'), '出现 ' + (stats.topMissingPoints?.[0]?.count ?? 0) + ' 次')
  ].join('');
  document.getElementById('history-count').textContent = String(history.length);
  document.getElementById('history-table').innerHTML = '<tr><th>Topic</th><th>分数</th><th>Missing</th></tr>' + history.map((x,i)=>`<tr><td><a onclick="showHistory(${i})">[${esc(x.topic?.category)}] ${esc(x.topic?.title)}</a></td><td>${esc(x.score)}/10</td><td>${esc(x.topMissing||'')}</td></tr>`).join('');
  window.__history = history;
  document.getElementById('summary-count').textContent = String(summary.length);
  document.getElementById('summary-table').innerHTML = '<tr><th>平均分</th><th>最弱维度</th><th>建议</th></tr>' + summary.map((x,i)=>`<tr><td><a onclick="showSummary(${i})">${(x.averageScore ?? 0).toFixed(2)}/10</a></td><td>${esc(x.weakestDimension?.label || '')}</td><td>${esc(x.suggestion || '')}</td></tr>`).join('');
  window.__summary = summary;
}
async function boot(){ setStrategyMeta(); await refreshDashboard(true); }
async function startSession(){
  setStrategyMeta();
  const payload = { mode: document.getElementById('mode').value, module: document.getElementById('module').value, reviewWrong: document.getElementById('reviewWrong').checked, noFollowup: document.getElementById('noFollowup').checked };
  const data = await j('/api/session/start', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload)});
  currentSessionId = data.sessionId;
  document.getElementById('session-pill').textContent = data.sessionId;
  setStatus('第 1 轮');
  document.getElementById('topic-pill').textContent = `[${data.topic?.category || '未知'}] ${data.topic?.title || '未知题目'}`;
  document.getElementById('question-box').textContent = data.question;
  document.getElementById('answer-box').value = '';
  document.getElementById('result-box').innerHTML = '<div class="empty">等待作答…</div>';
  document.getElementById('submit-btn').disabled = false;
  document.getElementById('submit-btn').textContent = '提交答案';
  document.getElementById('next-btn').style.display = 'none';
}
function renderResult(data){
  if (data.error) {
    document.getElementById('result-box').innerHTML = `<div class="status-banner status-err">${esc(data.error)}</div>`;
    return;
  }
  const r = data.result || {};
  const dims = r.dimensions || {};
  const strengths = (r.strengths || []).map(x => `<li>${esc(x)}</li>`).join('') || '<li>—</li>';
  const missing = (r.missingPoints || []).map(x => `<li>${esc(x)}</li>`).join('') || '<li>—</li>';
  const statusBanner = data.status === 'followup'
    ? `<div class="status-banner status-warn"><strong>需要追问：</strong>当前分数偏低，下面是追问题目。</div>`
    : `<div class="status-banner status-ok"><strong>本轮完成。</strong>${data.historyPath ? ` 已保存到 <span class="pill">${esc(data.historyPath)}</span>` : ''}</div>`;
  const bars = [
    ['准确性', dims.accuracy ?? 0, 4],
    ['完整性', dims.completeness ?? 0, 3],
    ['场景意识', dims.practicality ?? 0, 2],
    ['表达清晰度', dims.clarity ?? 0, 1],
  ].map(([label, value, max]) => `
    <div class="metric">
      <div class="metric-top"><span>${label}</span><strong>${value}/${max}</strong></div>
      <div class="bar"><div class="fill" style="width:${(Number(value) / Number(max)) * 100}%"></div></div>
    </div>
  `).join('');
  document.getElementById('result-box').innerHTML = `
    ${statusBanner}
    <div class="score-hero">
      <div class="score-card">
        <div class="label">Score</div>
        <div class="score">${esc(r.score ?? '-')}</div>
        <div class="outof">/ 10</div>
      </div>
      <div class="metric-list">${bars}</div>
    </div>
    <div class="result-grid">
      <div class="result-card"><h3>Strengths</h3><ul>${strengths}</ul></div>
      <div class="result-card"><h3>Missing Points</h3><ul>${missing}</ul></div>
    </div>
    <div class="result-card" style="margin-top:14px;"><h3>Ideal Answer</h3><pre>${esc(r.idealAnswer || '')}</pre></div>
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
    setStatus('第 2 轮（追问）');
    document.getElementById('question-box').textContent = data.nextQuestion;
    document.getElementById('answer-box').value = '';
    btn.disabled = false;
    btn.textContent = '提交答案';
  } else if (data.status === 'done') {
    document.getElementById('session-pill').textContent = '已完成';
    setStatus('本轮完成');
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
    <div class="detail-card detail-block">
      <div class="detail-title">Round ${idx + 1}</div>
      <div class="detail-title">Question</div><pre>${esc(r.question || '')}</pre>
      <div class="detail-title">Answer</div><pre>${esc(r.answer || '')}</pre>
      <div class="detail-title">Score</div><div>${esc(r.score || '')}/10</div>
      <div class="detail-title">Missing</div><ul>${(r.missing_points || []).map(m => `<li>${esc(m)}</li>`).join('') || '<li>—</li>'}</ul>
      <div class="detail-title">Ideal Answer</div><pre>${esc(r.ideal_answer || '')}</pre>
    </div>`).join('');
  document.getElementById('detail-box').innerHTML = `
    <div class="detail-card">
      <div class="row"><strong>[${esc(x.topic?.category)}] ${esc(x.topic?.title)}</strong><span class="pill">${esc(x.score)}/10</span></div>
      <div class="footer-note">Scope: ${esc(x.scope || 'Random')}</div>
      <div class="footer-note">Path: ${esc(x.path || '')}</div>
      ${rounds || '<div class="empty">无详情</div>'}
    </div>`;
}
function showSummary(i){
  const x = window.__summary[i];
  const topics = (x.topics || []).map(t => `<li>[${esc(t.category)}] ${esc(t.title)} (${esc(t.score)}/10)</li>`).join('') || '<li>—</li>';
  document.getElementById('detail-box').innerHTML = `
    <div class="detail-card">
      <div class="row"><strong>Session Summary</strong><span class="pill">${(x.averageScore ?? 0).toFixed(2)}/10</span></div>
      <div class="detail-block"><div class="detail-title">概览</div>
        <div>Completed: ${esc(x.completed)}</div>
        <div>Low-score rounds: ${esc(x.lowScoreRounds)}</div>
        <div>Weakest: ${esc(x.weakestDimension?.label || '')}</div>
      </div>
      <div class="detail-block"><div class="detail-title">Best / Worst</div>
        <div>Best: [${esc(x.bestTopic?.category || '')}] ${esc(x.bestTopic?.title || '')}</div>
        <div>Worst: [${esc(x.worstTopic?.category || '')}] ${esc(x.worstTopic?.title || '')}</div>
      </div>
      <div class="detail-block"><div class="detail-title">Top Missing</div><pre>${esc(x.topMissing || '')}</pre></div>
      <div class="detail-block"><div class="detail-title">Suggestion</div><pre>${esc(x.suggestion || '')}</pre></div>
      <div class="detail-block"><div class="detail-title">Topics</div><ul>${topics}</ul></div>
    </div>`;
}
document.getElementById('mode').addEventListener('change', setStrategyMeta);
document.getElementById('reviewWrong').addEventListener('change', setStrategyMeta);
document.getElementById('noFollowup').addEventListener('change', setStrategyMeta);
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
