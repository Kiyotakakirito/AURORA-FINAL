import React, { useState, useRef } from 'react';
import { useDropzone } from 'react-dropzone';
import { useNavigate } from 'react-router-dom';
import {
  Upload, FileText, AlertCircle, CheckCircle, Github,
  Loader2, Zap, ChevronRight, X, Sparkles,
  Code2, BarChart3, MessageSquare, ClipboardList,
} from 'lucide-react';
import { submitProject, createEvaluationSocket } from '../lib/api';
import { useAuroraStore, ProgressEvent, EvaluationResult } from '../lib/store';

/* ─── design tokens (mirrors index.css vars) ─── */
const S = {
  bg:        '#07071a',
  bgCard:    'rgba(14,12,40,0.88)',
  bgSurface: 'rgba(22,18,62,0.6)',
  border:    'rgba(124,58,237,0.22)',
  borderHov: 'rgba(124,58,237,0.5)',
  accent:    '#7c3aed',
  accent2:   '#a78bfa',
  glow:      'rgba(124,58,237,0.38)',
  green:     '#22c55e',
  yellow:    '#eab308',
  red:       '#ef4444',
  text:      '#e2e8f0',
  muted:     '#7c84a6',
  radius:    '14px',
  radiusSm:  '9px',
} as const;

/* ─── Stage config ─── */
const STAGES = [
  { key: 'uploading', label: 'Upload',   Icon: Upload },
  { key: 'parsing',   label: 'Parse',    Icon: FileText },
  { key: 'analyzing', label: 'Analyze',  Icon: Code2 },
  { key: 'scoring',   label: 'Score',    Icon: BarChart3 },
  { key: 'feedback',  label: 'Feedback', Icon: MessageSquare },
  { key: 'complete',  label: 'Done',     Icon: CheckCircle },
];
const stageIndex = (s: string) => STAGES.findIndex((x) => x.key === s);

/* ─── Inline keyframes injected once ─── */
const KEYFRAMES = `
@keyframes auroraShift {
  0%,100% { background-position: 0% 50%; }
  50%      { background-position: 100% 50%; }
}
@keyframes floatUp {
  0%   { opacity:0; transform:translateY(18px) scale(.96); }
  100% { opacity:1; transform:translateY(0)   scale(1);    }
}
@keyframes pulseGlow {
  0%,100% { box-shadow: 0 0 14px ${S.glow}; }
  50%     { box-shadow: 0 0 32px ${S.glow}, 0 0 60px rgba(124,58,237,.18); }
}
@keyframes spin { to { transform:rotate(360deg); } }
@keyframes pop  { from{transform:scale(0)} to{transform:scale(1)} }
@keyframes shimmer {
  0%   { background-position: -200% center; }
  100% { background-position:  200% center; }
}
@keyframes dash {
  to { stroke-dashoffset: 0; }
}
`;

/* ─── Progress Stepper ─── */
const ProgressStepper: React.FC<{ stage: string; percent: number; message: string }> = ({
  stage, percent, message,
}) => {
  const current = stageIndex(stage);
  return (
    <div style={{ width: '100%' }}>
      {/* Steps row */}
      <div style={{ display:'flex', alignItems:'center', marginBottom:20 }}>
        {STAGES.map((s, i) => {
          const done    = i < current;
          const active  = i === current;
          const { Icon } = s;
          return (
            <React.Fragment key={s.key}>
              <div style={{ display:'flex', flexDirection:'column', alignItems:'center', gap:6 }}>
                <div style={{
                  width:38, height:38, borderRadius:'50%', display:'flex',
                  alignItems:'center', justifyContent:'center', flexShrink:0,
                  background: done   ? 'rgba(34,197,94,.2)'   :
                               active ? 'rgba(124,58,237,.3)'  :
                                        'rgba(22,18,62,.6)',
                  border: `2px solid ${done ? S.green : active ? S.accent : S.border}`,
                  color:   done ? S.green : active ? S.accent2 : S.muted,
                  transition: 'all .3s ease',
                  boxShadow: active ? `0 0 18px ${S.glow}` : 'none',
                  animation: active ? 'pulseGlow 1.8s ease infinite' : 'none',
                }}>
                  {done ? <CheckCircle size={16} /> : <Icon size={15} />}
                </div>
                <span style={{
                  fontSize:10, fontWeight:600, letterSpacing:.6,
                  textTransform:'uppercase',
                  color: active ? S.accent2 : done ? S.green : S.muted,
                  transition:'color .3s',
                }}>{s.label}</span>
              </div>
              {i < STAGES.length - 1 && (
                <div style={{
                  flex:1, height:2, margin:'0 4px', marginBottom:22,
                  background: i < current
                    ? `linear-gradient(90deg,${S.green},${S.accent})`
                    : S.border,
                  borderRadius:999, transition:'background .4s ease',
                  boxShadow: i < current ? `0 0 8px ${S.glow}` : 'none',
                }} />
              )}
            </React.Fragment>
          );
        })}
      </div>

      {/* Bar */}
      <div style={{
        height:5, background:'rgba(22,18,62,.8)',
        borderRadius:999, overflow:'hidden', marginBottom:12,
      }}>
        <div style={{
          height:'100%', width:`${percent}%`,
          background:`linear-gradient(90deg,${S.accent},${S.accent2},#2563eb)`,
          backgroundSize:'200% 100%',
          animation:'shimmer 2s linear infinite',
          borderRadius:999,
          boxShadow:`0 0 10px ${S.glow}`,
          transition:'width .5s cubic-bezier(.4,0,.2,1)',
        }} />
      </div>

      <p style={{ fontSize:13, color:S.muted, textAlign:'center', minHeight:20 }}>{message}</p>
    </div>
  );
};

/* ─── Score Badge ─── */
const GRADE_COLOR: Record<string,string> = { 'A+':'#22c55e','A':'#4ade80','B':'#a78bfa','C':'#eab308','D':'#ef4444' };

const ScoreBadge: React.FC<{ label:string; score?:number; accent?:string }> = ({
  label, score, accent = S.accent,
}) => {
  if (score == null) return null;
  const grade = score>=90?'A+': score>=80?'A': score>=70?'B': score>=60?'C':'D';
  const pct   = Math.min(score,100);
  return (
    <div style={{
      background: S.bgCard, border:`1px solid ${S.border}`,
      borderRadius:S.radius, padding:'18px 16px',
      display:'flex', flexDirection:'column', alignItems:'center', gap:8,
      transition:'all .2s', backdropFilter:'blur(8px)',
    }}
      onMouseEnter={e=>(e.currentTarget.style.borderColor=S.borderHov)}
      onMouseLeave={e=>(e.currentTarget.style.borderColor=S.border)}
    >
      {/* mini arc */}
      <svg width={80} height={46} viewBox="0 0 80 46">
        <path d="M6 44 A34 34 0 0 1 74 44" fill="none" stroke="rgba(22,18,62,.8)" strokeWidth={6} strokeLinecap="round"/>
        <path d="M6 44 A34 34 0 0 1 74 44" fill="none" stroke={accent} strokeWidth={6} strokeLinecap="round"
          strokeDasharray={`${pct * 1.068} 107`}
          style={{ filter:`drop-shadow(0 0 4px ${accent})` }}/>
      </svg>
      <div style={{ fontSize:22, fontWeight:800, lineHeight:1, color:'#fff', marginTop:-8 }}>
        {Math.round(score)}
      </div>
      <div style={{
        display:'inline-block', padding:'2px 10px', borderRadius:999,
        fontSize:11, fontWeight:700, letterSpacing:.4,
        background:`${GRADE_COLOR[grade]}22`, color:GRADE_COLOR[grade],
        border:`1px solid ${GRADE_COLOR[grade]}55`,
      }}>{grade}</div>
      <div style={{ fontSize:11.5, color:S.muted, textAlign:'center', fontWeight:500 }}>{label}</div>
    </div>
  );
};

/* ─── Result Panel ─── */
const ResultPanel: React.FC<{ result:EvaluationResult }> = ({ result }) => {
  const [tab, setTab] = useState<'summary'|'analysis'|'feedback'>('summary');
  const analysis = result.comprehensive_analysis as any;
  const score    = Math.round(result.overall_score || 0);
  const pct      = Math.min(score, 100);
  const circumference = 2 * Math.PI * 42; // r=42

  return (
    <div style={{ animation:'floatUp .5s ease both' }}>
      {/* Hero */}
      <div style={{
        background:'linear-gradient(135deg,rgba(124,58,237,.18) 0%,rgba(79,70,229,.12) 100%)',
        border:`1px solid ${S.border}`, borderRadius:S.radius,
        padding:'32px 28px', marginBottom:20,
        display:'flex', alignItems:'center', gap:32, flexWrap:'wrap',
        backdropFilter:'blur(12px)',
      }}>
        {/* circular score */}
        <div style={{ position:'relative', width:130, height:130, flexShrink:0 }}>
          <svg width={130} height={130} viewBox="0 0 100 100" style={{ transform:'rotate(-90deg)' }}>
            <defs>
              <linearGradient id="sg" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%"   stopColor="#7c3aed"/>
                <stop offset="100%" stopColor="#2563eb"/>
              </linearGradient>
            </defs>
            <circle cx={50} cy={50} r={42} fill="none" stroke="rgba(22,18,62,.9)" strokeWidth={8}/>
            <circle cx={50} cy={50} r={42} fill="none" stroke="url(#sg)" strokeWidth={8}
              strokeLinecap="round"
              strokeDasharray={`${(pct/100)*circumference} ${circumference}`}
              style={{ filter:`drop-shadow(0 0 6px ${S.glow})`, transition:'stroke-dasharray .8s ease' }}/>
          </svg>
          <div style={{
            position:'absolute', inset:0,
            display:'flex', flexDirection:'column', alignItems:'center', justifyContent:'center',
          }}>
            <span style={{ fontSize:30, fontWeight:800 }}>{score}</span>
            <span style={{ fontSize:11, color:S.muted }}>/100</span>
          </div>
        </div>

        <div style={{ flex:1, minWidth:180 }}>
          <div style={{
            display:'inline-flex', alignItems:'center', gap:6, marginBottom:10,
            background:'rgba(124,58,237,.18)', border:`1px solid rgba(124,58,237,.35)`,
            borderRadius:999, padding:'4px 12px',
            fontSize:11, fontWeight:700, letterSpacing:.6, color:S.accent2,
          }}>
            <Sparkles size={12}/> Evaluation Complete
          </div>
          <h2 style={{ fontSize:22, fontWeight:700, marginBottom:10, color:'#fff' }}>
            {result.project_id ? `Project #${result.project_id}` : 'Your Project'}
          </h2>
          <div style={{ display:'flex', flexWrap:'wrap', gap:8 }}>
            {result.ai_model_used && (
              <span style={{
                background:S.bgSurface, border:`1px solid ${S.border}`,
                borderRadius:S.radiusSm, padding:'4px 10px',
                fontSize:12, color:S.muted,
              }}>🤖 {result.ai_model_used}</span>
            )}
            {result.evaluation_time && (
              <span style={{
                background:S.bgSurface, border:`1px solid ${S.border}`,
                borderRadius:S.radiusSm, padding:'4px 10px',
                fontSize:12, color:S.muted,
              }}>⏱ {result.evaluation_time.toFixed(1)}s</span>
            )}
          </div>
        </div>
      </div>

      {/* Sub-scores */}
      <div style={{
        display:'grid', gridTemplateColumns:'repeat(auto-fit,minmax(130px,1fr))',
        gap:14, marginBottom:22,
      }}>
        <ScoreBadge label="Code Quality"  score={result.code_quality_score}   accent="#7c3aed"/>
        <ScoreBadge label="Functionality" score={result.functionality_score}   accent="#2563eb"/>
        <ScoreBadge label="Documentation" score={result.documentation_score}   accent="#0891b2"/>
        <ScoreBadge label="Innovation"    score={result.innovation_score}      accent="#059669"/>
      </div>

      {/* Tabs */}
      <div style={{
        display:'flex', gap:4, marginBottom:16,
        background:S.bgCard, border:`1px solid ${S.border}`,
        borderRadius:S.radiusSm, padding:4, width:'fit-content',
      }}>
        {(['summary','analysis','feedback'] as const).map((t) => (
          <button key={t} onClick={()=>setTab(t)} style={{
            padding:'8px 20px', borderRadius:7, border:'none', cursor:'pointer',
            fontSize:13, fontWeight:tab===t?700:500,
            background: tab===t ? 'rgba(124,58,237,.2)'  : 'transparent',
            color:       tab===t ? S.accent2              : S.muted,
            borderTop:   tab===t ? `1px solid rgba(124,58,237,.3)` : '1px solid transparent',
            transition:'all .2s',
          }}>
            {t.charAt(0).toUpperCase()+t.slice(1)}
          </button>
        ))}
      </div>

      {/* Tab body */}
      <div style={{ background:S.bgCard, border:`1px solid ${S.border}`, borderRadius:S.radius, padding:'22px 24px', backdropFilter:'blur(8px)' }}>
        {tab==='summary' && (
          <div style={{ display:'grid', gridTemplateColumns:'repeat(auto-fit,minmax(240px,1fr))', gap:16 }}>
            {result.strengths?.length && (
              <FeedbackBlock variant="strengths" title="Strengths" items={result.strengths}/>)}
            {result.weaknesses?.length && (
              <FeedbackBlock variant="weaknesses" title="Areas for Improvement" items={result.weaknesses}/>)}
            {result.recommendations?.length && (
              <FeedbackBlock variant="recommendations" title="Recommendations" items={result.recommendations}/>)}
          </div>
        )}
        {tab==='analysis' && (
          analysis
            ? <pre style={{ fontSize:11.5, color:S.accent2, fontFamily:"'Fira Code',monospace", lineHeight:1.7, whiteSpace:'pre-wrap', maxHeight:500, overflow:'auto' }}>
                {JSON.stringify(analysis?.ultra_detailed_analysis || analysis, null, 2)}
              </pre>
            : <p style={{ color:S.muted, textAlign:'center', padding:'40px 0' }}>No detailed analysis data available.</p>
        )}
        {tab==='feedback' && (
          result.feedback
            ? <div style={{ fontSize:14, color:S.text, lineHeight:1.8 }}>{result.feedback}</div>
            : <p style={{ color:S.muted, textAlign:'center', padding:'40px 0' }}>No written feedback generated.</p>
        )}
      </div>
    </div>
  );
};

const VARIANT_STYLES: Record<string,{ bg:string; border:string; color:string; bullet:string }> = {
  strengths:      { bg:'rgba(34,197,94,.08)',  border:'rgba(34,197,94,.25)',  color:'#22c55e', bullet:'✓' },
  weaknesses:     { bg:'rgba(234,179,8,.08)',  border:'rgba(234,179,8,.25)',  color:'#eab308', bullet:'⚠' },
  recommendations:{ bg:'rgba(124,58,237,.08)', border:'rgba(124,58,237,.3)',  color:'#a78bfa', bullet:'→' },
};

const FeedbackBlock: React.FC<{ variant:string; title:string; items:string[] }> = ({ variant,title,items }) => {
  const v=VARIANT_STYLES[variant]??VARIANT_STYLES.recommendations;
  return (
    <div style={{ background:v.bg, border:`1px solid ${v.border}`, borderRadius:S.radiusSm, padding:'16px 18px' }}>
      <h4 style={{ fontSize:13, fontWeight:700, color:v.color, marginBottom:10 }}>{title}</h4>
      <ul style={{ display:'flex', flexDirection:'column', gap:6 }}>
        {items.map((item,i)=>(
          <li key={i} style={{ fontSize:13, color:S.muted, paddingLeft:18, position:'relative', lineHeight:1.5 }}>
            <span style={{ position:'absolute', left:0, color:v.color, fontSize:11, top:2 }}>{v.bullet}</span>
            {item}
          </li>
        ))}
      </ul>
    </div>
  );
};

/* ─────────────────────────────────────────────────────────── */
/*  MAIN PAGE                                                   */
/* ─────────────────────────────────────────────────────────── */
export const SubmitProject: React.FC = () => {
  const navigate = useNavigate();
  const { isSubmitting, setIsSubmitting, setProgress, resetProgress, addEvaluation } = useAuroraStore();

  const [submissionType, setSubmissionType] = useState<'github'|'zip'>('github');
  const [formData, setFormData] = useState({ name:'', studentName:'', studentEmail:'', githubUrl:'' });
  const [pdfFile,  setPdfFile]  = useState<File|null>(null);
  const [zipFile,  setZipFile]  = useState<File|null>(null);
  const [status,   setStatus]   = useState<'idle'|'connecting'|'processing'|'success'|'error'>('idle');
  const [prog,     setProg]     = useState({ stage:'', percent:0, message:'' });
  const [result,   setResult]   = useState<EvaluationResult|null>(null);
  const [err,      setErr]      = useState<string|null>(null);
  const socketRef = useRef<WebSocket|null>(null);

  const { getRootProps:pdfRoot, getInputProps:pdfIn, isDragActive:pdfDrag } = useDropzone({
    onDrop:(f)=>{ if(f[0]) setPdfFile(f[0]); },
    accept:{'application/pdf':['.pdf']}, maxFiles:1, maxSize:20*1024*1024,
  });
  const { getRootProps:zipRoot, getInputProps:zipIn, isDragActive:zipDrag } = useDropzone({
    onDrop:(f)=>{ if(f[0]) setZipFile(f[0]); },
    accept:{'application/zip':['.zip'],'application/x-zip-compressed':['.zip']}, maxFiles:1, maxSize:100*1024*1024,
  });

  const handleInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((p)=>({...p,[name]:value}));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErr(null); resetProgress();

    if (!formData.name.trim())         return setErr('Project name is required.');
    if (!formData.studentName.trim())  return setErr('Student name is required.');
    if (!pdfFile)                      return setErr('PDF report is required.');
    if (submissionType==='github' && !formData.githubUrl.trim()) return setErr('GitHub URL is required.');
    if (submissionType==='zip'    && !zipFile)                   return setErr('ZIP file is required.');

    const jobId = `job-${Date.now()}-${Math.random().toString(36).slice(2,8)}`;
    setStatus('connecting');
    setProg({ stage:'uploading', percent:5, message:'Connecting to evaluation service...' });

    const ws = createEvaluationSocket(jobId);
    socketRef.current = ws;
    ws.onopen    = () => setStatus('processing');
    ws.onmessage = (ev) => {
      try {
        const msg: ProgressEvent = JSON.parse(ev.data);
        if (msg.type==='heartbeat') return;
        setProgress(msg);
        setProg({ stage:msg.stage||'', percent:msg.percent||0, message:msg.message||'' });
        if (msg.type==='complete' && msg.data) { setResult(msg.data); addEvaluation(msg.data); setStatus('success'); }
        if (msg.type==='error')                { setErr(msg.message||'Evaluation failed');      setStatus('error');   }
      } catch(_){}
    };
    ws.onerror = () => setErr('WebSocket connection failed. The evaluation will still proceed.');
    ws.onclose = () => { socketRef.current=null; };

    setIsSubmitting(true);
    try {
      const fd = new FormData();
      fd.append('name',            formData.name);
      fd.append('student_name',    formData.studentName);
      fd.append('student_email',   formData.studentEmail);
      fd.append('submission_type', submissionType);
      if (submissionType==='github') fd.append('github_url', formData.githubUrl);
      if (submissionType==='zip' && zipFile) fd.append('file', zipFile);
      fd.append('pdf_file', pdfFile);
      fd.append('job_id',   jobId);

      const response = await submitProject(fd);
      const data     = response.data;
      if (status!=='success' && data) {
        const evalResult: EvaluationResult = {
          project_id: data.project_id, evaluation_id: data.evaluation_id,
          overall_score: data.overall_score, comprehensive_analysis: data.comprehensive_analysis,
          message: data.message, status: data.status,
        };
        setResult(evalResult); addEvaluation(evalResult); setStatus('success');
      }
    } catch(e:any) {
      setErr(e.message||'Submission failed'); setStatus('error');
    } finally {
      setIsSubmitting(false);
    }
  };

  const resetForm = () => {
    setStatus('idle'); setResult(null); setErr(null); resetProgress();
    setProg({ stage:'', percent:0, message:'' }); socketRef.current?.close();
  };

  /* shared field style */
  const fieldStyle: React.CSSProperties = {
    width:'100%', background:'rgba(10,8,32,.7)', border:`1px solid ${S.border}`,
    borderRadius:S.radiusSm, color:S.text, padding:'11px 14px',
    fontSize:14, outline:'none', transition:'all .2s',
    fontFamily:'inherit',
  };

  return (
    <>
      {/* inject keyframes once */}
      <style>{KEYFRAMES}</style>

      <div style={{ maxWidth:860, margin:'0 auto', animation:'floatUp .45s ease both' }}>

        {/* ── HERO HEADER ── */}
        <div style={{
          position:'relative', borderRadius:S.radius, overflow:'hidden',
          marginBottom:28, padding:'36px 32px',
          background:`linear-gradient(135deg,rgba(124,58,237,.25) 0%,rgba(79,70,229,.18) 50%,rgba(37,99,235,.2) 100%)`,
          border:`1px solid rgba(124,58,237,.35)`,
          backdropFilter:'blur(16px)',
        }}>
          {/* decorative orbs */}
          <div style={{ position:'absolute', top:-40, right:-40, width:180, height:180, borderRadius:'50%', background:'radial-gradient(circle,rgba(124,58,237,.3) 0%,transparent 70%)', pointerEvents:'none' }}/>
          <div style={{ position:'absolute', bottom:-30, left:-20, width:120, height:120, borderRadius:'50%', background:'radial-gradient(circle,rgba(37,99,235,.25) 0%,transparent 70%)', pointerEvents:'none' }}/>

          <div style={{ position:'relative', zIndex:1 }}>
            <div style={{
              display:'inline-flex', alignItems:'center', gap:7, marginBottom:14,
              background:'rgba(124,58,237,.22)', border:`1px solid rgba(124,58,237,.4)`,
              borderRadius:999, padding:'5px 14px',
              fontSize:11.5, fontWeight:700, letterSpacing:.8, color:S.accent2,
            }}>
              <Zap size={12} style={{ fill:S.accent2 }}/> AI-POWERED EVALUATION
            </div>
            <h1 style={{ fontSize:28, fontWeight:800, marginBottom:8, color:'#fff', letterSpacing:-.3 }}>
              Submit Your Project
            </h1>
            <p style={{ fontSize:14, color:S.muted, maxWidth:500 }}>
              Upload your code and PDF report. Our AI will analyze everything — code quality, documentation, innovation — within minutes.
            </p>
          </div>
        </div>

        {/* ── EVALUATING OVERLAY ── */}
        {(status==='connecting'||status==='processing') && (
          <div style={{
            background:S.bgCard, border:`1px solid ${S.border}`,
            borderRadius:S.radius, padding:'48px 36px',
            backdropFilter:'blur(16px)', textAlign:'center',
            animation:'floatUp .4s ease both',
          }}>
            {/* Animated rings */}
            <div style={{ position:'relative', width:80, height:80, margin:'0 auto 28px' }}>
              <div style={{ position:'absolute', inset:0, borderRadius:'50%', border:`3px solid ${S.border}` }}/>
              <div style={{
                position:'absolute', inset:0, borderRadius:'50%',
                border:`3px solid transparent`,
                borderTopColor: S.accent,
                borderRightColor: S.accent2,
                animation:'spin .9s linear infinite',
              }}/>
              <div style={{
                position:'absolute', inset:8, borderRadius:'50%',
                border:`2px solid transparent`,
                borderTopColor:'rgba(37,99,235,.6)',
                animation:'spin 1.4s linear infinite reverse',
              }}/>
              <div style={{
                position:'absolute', inset:0, display:'flex', alignItems:'center', justifyContent:'center',
              }}>
                <Sparkles size={20} color={S.accent2}/>
              </div>
            </div>
            <h3 style={{ fontSize:18, fontWeight:700, marginBottom:6, color:'#fff' }}>Evaluating Your Project</h3>
            <p style={{ fontSize:13, color:S.muted, marginBottom:28 }}>This usually takes 30–90 seconds</p>
            <ProgressStepper stage={prog.stage} percent={prog.percent} message={prog.message||'Processing…'}/>
          </div>
        )}

        {/* ── SUCCESS ── */}
        {status==='success' && result && (
          <div style={{ animation:'floatUp .4s ease both' }}>
            <ResultPanel result={result}/>
            <div style={{ display:'flex', gap:12, marginTop:20, flexWrap:'wrap' }}>
              <button onClick={resetForm} style={{
                flex:1, minWidth:180,
                background:`linear-gradient(135deg,${S.accent},#4f46e5)`,
                color:'#fff', border:'none', borderRadius:S.radiusSm,
                padding:'13px 22px', fontSize:14, fontWeight:700, cursor:'pointer',
                display:'flex', alignItems:'center', justifyContent:'center', gap:8,
                boxShadow:`0 0 22px ${S.glow}`, transition:'all .2s',
              }}
                onMouseEnter={e=>(e.currentTarget.style.boxShadow=`0 0 36px ${S.glow}`)}
                onMouseLeave={e=>(e.currentTarget.style.boxShadow=`0 0 22px ${S.glow}`)}
              >
                <Upload size={16}/> Submit Another
              </button>
              {result.evaluation_id && (
                <button onClick={()=>navigate(`/evaluations/${result.evaluation_id}`)} style={{
                  flex:1, minWidth:180,
                  background:S.bgSurface, border:`1px solid ${S.border}`,
                  color:S.text, borderRadius:S.radiusSm,
                  padding:'12px 22px', fontSize:14, fontWeight:600, cursor:'pointer',
                  display:'flex', alignItems:'center', justifyContent:'center', gap:8, transition:'all .2s',
                }}
                  onMouseEnter={e=>{ e.currentTarget.style.borderColor=S.borderHov; e.currentTarget.style.background='rgba(124,58,237,.1)'; }}
                  onMouseLeave={e=>{ e.currentTarget.style.borderColor=S.border;    e.currentTarget.style.background=S.bgSurface; }}
                >
                  View Full Report <ChevronRight size={16}/>
                </button>
              )}
            </div>
          </div>
        )}

        {/* ── FORM ── */}
        {(status==='idle'||status==='error') && (
          <form onSubmit={handleSubmit} style={{ display:'flex', flexDirection:'column', gap:18 }}>

            {/* Error banner */}
            {err && (
              <div style={{
                background:'rgba(239,68,68,.1)', border:'1px solid rgba(239,68,68,.3)',
                borderRadius:S.radiusSm, padding:'12px 16px',
                display:'flex', alignItems:'center', gap:10, color:'#f87171', fontSize:13,
                animation:'floatUp .3s ease both',
              }}>
                <AlertCircle size={16} style={{ flexShrink:0 }}/>
                <span style={{ flex:1 }}>{err}</span>
                <button type="button" onClick={()=>setErr(null)} style={{ color:'#f87171', background:'none', border:'none', cursor:'pointer', padding:2 }}>
                  <X size={14}/>
                </button>
              </div>
            )}

            {/* ── Submission type toggle ── */}
            <GlassCard>
              <CardLabel>Submission Type</CardLabel>
              <div style={{ display:'flex', gap:10, marginTop:10 }}>
                {(['github','zip'] as const).map((t)=>(
                  <button key={t} type="button" onClick={()=>setSubmissionType(t)} style={{
                    flex:1, padding:'11px 16px', borderRadius:S.radiusSm, cursor:'pointer',
                    display:'flex', alignItems:'center', justifyContent:'center', gap:8,
                    fontSize:13.5, fontWeight:600, transition:'all .22s',
                    border: submissionType===t
                      ? `1px solid rgba(124,58,237,.55)`
                      : `1px solid ${S.border}`,
                    background: submissionType===t
                      ? 'rgba(124,58,237,.22)'
                      : S.bgSurface,
                    color: submissionType===t ? S.accent2 : S.muted,
                    boxShadow: submissionType===t ? `0 0 14px ${S.glow}` : 'none',
                  }}>
                    {t==='github' ? <Github size={16}/> : <Upload size={16}/>}
                    {t==='github' ? 'GitHub URL' : 'ZIP File'}
                  </button>
                ))}
              </div>
            </GlassCard>

            {/* ── Project details ── */}
            <GlassCard>
              <SectionTitle icon={<ClipboardList size={16}/>} title="Project Details"/>
              <div style={{ display:'grid', gridTemplateColumns:'repeat(auto-fit,minmax(200px,1fr))', gap:14, marginTop:16 }}>
                <FieldWrap label="Project Name" required>
                  <input style={fieldStyle} name="name" value={formData.name} onChange={handleInput}
                    placeholder="Smart Library Management System"
                    onFocus={e=>{ e.target.style.borderColor=S.accent; e.target.style.boxShadow=`0 0 0 3px ${S.glow}`; }}
                    onBlur={e=>{  e.target.style.borderColor=S.border;  e.target.style.boxShadow='none'; }}/>
                </FieldWrap>
                <FieldWrap label="Student Name" required>
                  <input style={fieldStyle} name="studentName" value={formData.studentName} onChange={handleInput}
                    placeholder="Full name"
                    onFocus={e=>{ e.target.style.borderColor=S.accent; e.target.style.boxShadow=`0 0 0 3px ${S.glow}`; }}
                    onBlur={e=>{  e.target.style.borderColor=S.border;  e.target.style.boxShadow='none'; }}/>
                </FieldWrap>
                <FieldWrap label="Student Email">
                  <input style={fieldStyle} type="email" name="studentEmail" value={formData.studentEmail} onChange={handleInput}
                    placeholder="student@university.edu"
                    onFocus={e=>{ e.target.style.borderColor=S.accent; e.target.style.boxShadow=`0 0 0 3px ${S.glow}`; }}
                    onBlur={e=>{  e.target.style.borderColor=S.border;  e.target.style.boxShadow='none'; }}/>
                </FieldWrap>
                {submissionType==='github' && (
                  <FieldWrap label="GitHub Repository URL" required style={{ gridColumn:'1/-1' }}>
                    <div style={{ position:'relative' }}>
                      <Github size={15} style={{ position:'absolute', left:12, top:'50%', transform:'translateY(-50%)', color:S.muted, pointerEvents:'none' }}/>
                      <input style={{ ...fieldStyle, paddingLeft:36 }} name="githubUrl" value={formData.githubUrl} onChange={handleInput}
                        placeholder="https://github.com/username/repository"
                        onFocus={e=>{ e.target.style.borderColor=S.accent; e.target.style.boxShadow=`0 0 0 3px ${S.glow}`; }}
                        onBlur={e=>{  e.target.style.borderColor=S.border;  e.target.style.boxShadow='none'; }}/>
                    </div>
                  </FieldWrap>
                )}
              </div>
            </GlassCard>

            {/* ── ZIP upload ── */}
            {submissionType==='zip' && (
              <GlassCard>
                <SectionTitle icon={<Upload size={16}/>} title="Project ZIP File" required/>
                <Dropzone
                  getRootProps={zipRoot} getInputProps={zipIn} isDrag={zipDrag}
                  file={zipFile} onRemove={()=>setZipFile(null)}
                  icon={<Upload size={36}/>}
                  hint="Drop your ZIP here or browse"
                  maxLabel="Max 100 MB"
                />
              </GlassCard>
            )}

            {/* ── PDF upload ── */}
            <GlassCard>
              <SectionTitle icon={<FileText size={16}/>} title="Project Report (PDF)" required/>
              <Dropzone
                getRootProps={pdfRoot} getInputProps={pdfIn} isDrag={pdfDrag}
                file={pdfFile} onRemove={()=>setPdfFile(null)}
                icon={<FileText size={36}/>}
                hint="Drop your PDF report here or browse"
                maxLabel="Max 20 MB"
              />
            </GlassCard>

            {/* ── Submit ── */}
            <button type="submit" disabled={isSubmitting} style={{
              width:'100%', padding:'15px 24px',
              background:`linear-gradient(135deg,${S.accent} 0%,#4f46e5 60%,#2563eb 100%)`,
              backgroundSize:'200% 200%',
              color:'#fff', border:'none', borderRadius:S.radiusSm,
              fontSize:15.5, fontWeight:700, cursor:'pointer',
              display:'flex', alignItems:'center', justifyContent:'center', gap:10,
              transition:'all .25s', boxShadow:`0 0 24px ${S.glow}`,
              animation:'auroraShift 4s ease infinite',
              opacity: isSubmitting ? .55 : 1,
            }}
              onMouseEnter={e=>{ if(!isSubmitting) e.currentTarget.style.boxShadow=`0 0 42px ${S.glow},0 0 80px rgba(124,58,237,.2)`; }}
              onMouseLeave={e=>{ e.currentTarget.style.boxShadow=`0 0 24px ${S.glow}`; }}
            >
              {isSubmitting
                ? <><Loader2 size={18} style={{ animation:'spin .8s linear infinite' }}/> Evaluating…</>
                : <><Zap size={18} style={{ fill:'#fff' }}/> Evaluate Project</>
              }
            </button>
          </form>
        )}
      </div>
    </>
  );
};

/* ─── Tiny shared sub-components ─────────────────────────── */

const GlassCard: React.FC<{ children:React.ReactNode }> = ({ children }) => (
  <div style={{
    background:S.bgCard, border:`1px solid ${S.border}`,
    borderRadius:S.radius, padding:'22px 24px',
    backdropFilter:'blur(10px)', transition:'border-color .2s',
  }}
    onMouseEnter={e=>(e.currentTarget.style.borderColor=S.borderHov)}
    onMouseLeave={e=>(e.currentTarget.style.borderColor=S.border)}
  >{children}</div>
);

const CardLabel: React.FC<{ children:React.ReactNode }> = ({ children }) => (
  <div style={{ fontSize:12, fontWeight:700, letterSpacing:.7, textTransform:'uppercase', color:S.muted }}>{children}</div>
);

const SectionTitle: React.FC<{ icon:React.ReactNode; title:string; required?:boolean }> = ({ icon,title,required }) => (
  <div style={{ display:'flex', alignItems:'center', gap:8, color:S.accent2, fontWeight:700, fontSize:14 }}>
    {icon} {title} {required && <span style={{ color:'#ef4444', fontSize:11 }}>*</span>}
  </div>
);

const FieldWrap: React.FC<{ label:string; required?:boolean; children:React.ReactNode; style?:React.CSSProperties }> = ({
  label, required, children, style,
}) => (
  <div style={style}>
    <label style={{ display:'block', fontSize:12, fontWeight:600, letterSpacing:.5, textTransform:'uppercase', color:S.muted, marginBottom:7 }}>
      {label}{required && <span style={{ color:'#ef4444', marginLeft:3 }}>*</span>}
    </label>
    {children}
  </div>
);

const Dropzone: React.FC<{
  getRootProps:any; getInputProps:any; isDrag:boolean;
  file:File|null; onRemove:()=>void;
  icon:React.ReactNode; hint:string; maxLabel:string;
}> = ({ getRootProps,getInputProps,isDrag,file,onRemove,icon,hint,maxLabel }) => (
  <div {...getRootProps()} style={{
    marginTop:14, border:`2px dashed ${isDrag ? S.accent : file ? 'rgba(34,197,94,.5)' : S.border}`,
    borderRadius:S.radiusSm, padding:'28px 20px', cursor:'pointer',
    background: isDrag ? 'rgba(124,58,237,.1)' : file ? 'rgba(34,197,94,.06)' : 'rgba(14,12,40,.5)',
    transition:'all .22s', textAlign:'center',
    boxShadow: isDrag ? `0 0 20px ${S.glow}` : 'none',
  }}>
    <input {...getInputProps()}/>
    {file ? (
      <div style={{ display:'flex', alignItems:'center', justifyContent:'center', gap:10, flexWrap:'wrap' }}>
        <CheckCircle size={20} color={S.green}/>
        <span style={{ fontSize:13.5, fontWeight:600, color:S.text }}>{file.name}</span>
        <span style={{ fontSize:12, color:S.muted }}>({(file.size/1024/1024).toFixed(2)} MB)</span>
        <button type="button" onClick={(e)=>{ e.stopPropagation(); onRemove(); }} style={{
          background:'rgba(239,68,68,.15)', border:'1px solid rgba(239,68,68,.3)',
          borderRadius:6, padding:'3px 7px', color:'#f87171', cursor:'pointer',
          display:'flex', alignItems:'center', gap:4, fontSize:11,
        }}>
          <X size={12}/> Remove
        </button>
      </div>
    ) : (
      <>
        <div style={{ color: isDrag ? S.accent2 : S.muted, marginBottom:10, transition:'color .2s' }}>{icon}</div>
        <p style={{ fontSize:13.5, color: isDrag ? S.text : S.muted, marginBottom:4 }}>
          {hint.split('or')[0]}or{' '}
          <span style={{ color:S.accent2, fontWeight:600 }}>browse</span>
        </p>
        <small style={{ fontSize:11, color:S.muted }}>{maxLabel}</small>
      </>
    )}
  </div>
);
