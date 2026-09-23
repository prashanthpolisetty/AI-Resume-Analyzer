import React, { useMemo, useState } from 'react'
import {
  ArrowRight, BarChart3, CheckCircle2, FileText, History, Lightbulb,
  MessageCircle, RefreshCw, Sparkles, Target, Upload, WandSparkles, X,
} from 'lucide-react'
import './styles.css'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

async function api(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, options)
  const data = await response.json().catch(() => ({}))
  if (!response.ok) throw new Error(data.detail || 'Something went wrong. Please try again.')
  return data
}

function ScoreRing({ score }) {
  return <div className="score-ring" style={{ '--score': `${score * 3.6}deg` }}>
    <div><strong>{score}</strong><span>/100</span></div>
  </div>
}

function App() {
  const [mode, setMode] = useState('targeted')
  const [email, setEmail] = useState('')
  const [jobTitle, setJobTitle] = useState('')
  const [jobDescription, setJobDescription] = useState('')
  const [file, setFile] = useState(null)
  const [report, setReport] = useState(null)
  const [history, setHistory] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [activeTool, setActiveTool] = useState(null)
  const [toolInput, setToolInput] = useState('')
  const [toolResult, setToolResult] = useState(null)

  const headline = mode === 'targeted' ? 'Make your resume match the role.' : 'Build a resume that gets noticed.'
  const subhead = mode === 'targeted'
    ? 'Paste a job description to find missing keywords, skill gaps, and practical next steps.'
    : 'Get a clear health check for grammar, formatting, impact, and ATS readability.'

  const canAnalyze = file && email && (mode === 'general' || jobDescription.trim())
  const scoreColor = useMemo(() => report?.score >= 75 ? 'good' : report?.score >= 50 ? 'okay' : 'needs-work', [report])

  async function analyze(e) {
    e.preventDefault(); setError(''); setReport(null); setLoading(true)
    try {
      const body = new FormData()
      body.append('resume_file', file); body.append('email', email)
      body.append('jd', mode === 'targeted' ? jobDescription : '')
      body.append('job_title', mode === 'targeted' ? jobTitle : '')
      setReport(await api('/analyze', { method: 'POST', body }))
      loadHistory(email)
    } catch (err) { setError(err.message) } finally { setLoading(false) }
  }

  async function loadHistory(value = email) {
    if (!value) return
    try { setHistory(await api(`/history/${encodeURIComponent(value)}`)) } catch (err) { setError(err.message) }
  }

  async function runTool(path, body) {
    setError(''); setToolResult(null)
    try { setToolResult(await api(path, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) })) }
    catch (err) { setError(err.message) }
  }

  function openTool(tool) { setActiveTool(tool); setToolInput(''); setToolResult(null) }

  return <div className="app-shell">
    <header className="topbar"><a className="brand" href="#top"><span className="brand-mark"><Sparkles size={18} /></span> resumate</a><nav><a href="#tools">Tools</a><a href="#history">History</a><a href="#how-it-works">How it works</a></nav><button className="ghost-button" onClick={() => document.querySelector('#analyzer').scrollIntoView()}>Analyze resume <ArrowRight size={16} /></button></header>

    <main id="top">
      <section className="hero"><div className="eyebrow"><span className="pulse" /> Built for students and early-career talent</div><h1>{headline}<br /><em>Know exactly what to fix.</em></h1><p>{subhead}</p><div className="hero-stats"><span><CheckCircle2 size={17} /> Practical feedback</span><span><CheckCircle2 size={17} /> No file storage</span><span><CheckCircle2 size={17} /> Track progress</span></div></section>

      <section id="analyzer" className="workspace">
        <div className="panel form-panel"><div className="panel-heading"><div><span className="step-label">01 / Upload</span><h2>Start with your resume</h2></div><FileText className="heading-icon" /></div>
          <div className="mode-switch"><button className={mode === 'targeted' ? 'active' : ''} onClick={() => setMode('targeted')}><Target size={17} /> Match a job</button><button className={mode === 'general' ? 'active' : ''} onClick={() => setMode('general')}><BarChart3 size={17} /> General check</button></div>
          <form onSubmit={analyze}>
            <label className="dropzone">{file ? <><CheckCircle2 className="upload-success" size={27} /><strong>{file.name}</strong><small>Click to replace</small></> : <><Upload size={27} /><strong>Drop your resume here</strong><small>PDF, DOCX, or TXT · Max 10 MB</small></>}<input type="file" accept=".pdf,.docx,.txt" onChange={e => setFile(e.target.files?.[0])} /></label>
            <label>Email <span className="required">Required for your private history</span><input type="email" required value={email} onChange={e => setEmail(e.target.value)} placeholder="you@example.com" /></label>
            {mode === 'targeted' && <><label>Target role <span className="optional">Optional</span><input value={jobTitle} onChange={e => setJobTitle(e.target.value)} placeholder="e.g. Frontend Developer Intern" /></label><label>Job description <span className="required">Required</span><textarea required value={jobDescription} onChange={e => setJobDescription(e.target.value)} placeholder="Paste the job description here..." rows="6" /></label></>}
            <button className="primary-button" disabled={!canAnalyze || loading}>{loading ? <><RefreshCw className="spin" size={17} /> Analyzing your resume...</> : <>Get my feedback <ArrowRight size={17} /></>}</button>
          </form>
          {error && <div className="error"><X size={17} /> {error}</div>}
        </div>
        <div className="panel result-panel">{report ? <><div className="result-top"><div><span className="step-label">Your report is ready</span><h2>{report.mode === 'targeted' ? 'Role match' : 'Resume health'}</h2></div><span className={`score-badge ${scoreColor}`}>{report.score >= 75 ? 'Strong start' : report.score >= 50 ? 'On the way' : 'Room to grow'}</span></div><div className="score-summary"><ScoreRing score={report.score} /><div><h3>{report.score}/100</h3><p>{report.mode === 'targeted' ? 'match score for this role' : 'overall resume score'}</p></div></div><Feedback report={report} /></> : <div className="empty-result"><div className="empty-icon"><WandSparkles size={28} /></div><h2>Your feedback will appear here</h2><p>Upload a resume and complete the form to get clear, actionable recommendations.</p><div className="mini-checks"><span><CheckCircle2 size={16} /> What’s working</span><span><CheckCircle2 size={16} /> What to improve</span><span><CheckCircle2 size={16} /> Your next steps</span></div></div>}</div>
      </section>

      <section id="tools" className="tools-section"><div className="section-intro"><span className="eyebrow">Go beyond a score</span><h2>Small tools. Big improvements.</h2><p>Turn vague feedback into something you can act on today.</p></div><div className="tool-grid"><Tool icon={<FileText />} title="ATS text check" text="See the plain text an ATS actually reads." action={() => openTool('ats')} /><Tool icon={<Lightbulb />} title="Project booster" text="Turn rough notes into stronger bullets." action={() => openTool('project')} /><Tool icon={<Target />} title="Skill proof checker" text="Find claims that need evidence." action={() => openTool('skills')} /><Tool icon={<WandSparkles />} title="Buzzword detector" text="Replace clichés with proof." action={() => openTool('buzzwords')} /></div></section>

      <section id="history" className="history-section"><div className="section-intro"><span className="eyebrow">Your progress</span><h2>Keep getting better.</h2><p>Enter your email to see your past reports and score changes.</p></div><div className="history-card"><div className="history-search"><input type="email" value={email} onChange={e => setEmail(e.target.value)} placeholder="you@example.com" /><button className="secondary-button" onClick={() => loadHistory()}>View history <History size={16} /></button></div>{history?.analyses?.length ? <div className="history-list">{history.analyses.map(item => <div className="history-row" key={item.id}><div><strong>{item.job_title || (item.mode === 'targeted' ? 'Targeted analysis' : 'General health check')}</strong><small>{new Date(item.created_at).toLocaleDateString()} · {item.filename}</small></div><b className={item.score >= 75 ? 'green' : ''}>{item.score}/100</b></div>)}</div> : <div className="history-empty"><History size={22} /><span>Your saved reports will show up here.</span></div>}</div></section>
    </main>

    <footer><span className="brand"><span className="brand-mark"><Sparkles size={15} /></span> resumate</span><span>Build a resume you’re proud to send.</span></footer>
    {activeTool && <ToolModal tool={activeTool} input={toolInput} setInput={setToolInput} result={toolResult} close={() => setActiveTool(null)} run={runTool} />}
  </div>
}

function Feedback({ report }) { const items = report.mode === 'targeted' ? [['Missing keywords', report.missing_keywords], ['Skill gaps', report.skill_gaps]] : [['Grammar notes', report.grammar_issues], ['Sections found', report.sections_found]]; return <div className="feedback"><h3>Start here</h3>{report.feedback?.map((item, i) => <div className="feedback-line" key={i}><CheckCircle2 size={17} />{item}</div>)}{items.map(([title, list]) => <div className="feedback-group" key={title}><div><strong>{title}</strong><span>{list?.length || 0}</span></div>{list?.length ? <p>{list.slice(0, 7).join(' · ')}</p> : <p className="positive">Nothing flagged here.</p>}</div>)}<h3 className="next-title">Your next steps</h3>{report.next_steps?.map((item, i) => <div className="next-step" key={i}><b>{i + 1}</b>{item}</div>)}</div> }
function Tool({ icon, title, text, action }) { return <button className="tool-card" onClick={action}><div className="tool-icon">{icon}</div><h3>{title}</h3><p>{text}</p><span>Try it <ArrowRight size={15} /></span></button> }
function ToolModal({ tool, input, setInput, result, close, run }) { const config = { ats: ['ATS text check', 'Paste extracted resume text or a resume summary.', null], project: ['Project booster', 'What did you build? Include tools, users, or an outcome if you have them.', '/boost-project'], skills: ['Skill proof checker', 'Paste your resume text. Add claimed skills separated by commas above.', '/validate-skills'], buzzwords: ['Buzzword detector', 'Paste the resume text you want to improve.', '/check-buzzwords'] }[tool]; const [skills, setSkills] = useState(''); const submit = () => { if (tool === 'project') run('/boost-project', { notes: input }); if (tool === 'skills') run('/validate-skills', { skills: skills.split(','), resume_text: input }); if (tool === 'buzzwords') run('/check-buzzwords', { resume_text: input }); if (tool === 'ats') run('/boost-project', { notes: input }) }; return <div className="modal-backdrop" onClick={close}><div className="modal" onClick={e => e.stopPropagation()}><button className="modal-close" onClick={close}><X /></button><span className="eyebrow">Helpful tool</span><h2>{config[0]}</h2><p>{config[1]}</p>{tool === 'skills' && <input className="modal-input" value={skills} onChange={e => setSkills(e.target.value)} placeholder="Python, React, SQL" />}<textarea className="modal-textarea" value={input} onChange={e => setInput(e.target.value)} placeholder={tool === 'project' ? 'Built a campus events app...' : 'Paste text here...'} rows="8" /><button className="primary-button" onClick={submit}>Get suggestions <Sparkles size={16} /></button>{result && <div className="tool-result"><strong>Suggestions</strong><pre>{JSON.stringify(result, null, 2)}</pre></div>}</div></div> }

export default App
