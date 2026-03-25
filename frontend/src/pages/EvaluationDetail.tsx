import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  ArrowLeft, Star, Code, FileText, Lightbulb, Zap,
  AlertTriangle, CheckCircle, ThumbsUp, Clock, Cpu,
} from 'lucide-react';
import {
  RadarChart, Radar, PolarGrid, PolarAngleAxis,
  ResponsiveContainer, Tooltip,
} from 'recharts';
import { getEvaluation } from '../lib/api';
import { useAuroraStore, EvaluationResult } from '../lib/store';

/* ── design tokens ── */
const S = {
  bgCard:    'rgba(14,12,40,0.88)',
  bgSurface: 'rgba(22,18,62,0.55)',
  border:    'rgba(124,58,237,0.2)',
  borderHov: 'rgba(124,58,237,0.48)',
  accent:    '#7c3aed',
  accent2:   '#a78bfa',
  glow:      'rgba(124,58,237,0.35)',
  cyan:      '#00d4ff',
  green:     '#22c55e',
  yellow:    '#eab308',
  red:       '#ef4444',
  text:      '#e2e8f0',
  muted:     '#7c84a6',
  radius:    '14px',
  radiusSm:  '9px',
} as const;

const scoreColor = (s: number) => s >= 80 ? S.green : s >= 60 ? S.yellow : S.red;

const KF = `
@keyframes floatUp{0%{opacity:0;transform:translateY(18px) scale(.97)}100%{opacity:1;transform:none}}
@keyframes spin{to{transform:rotate(360deg)}}
`;

const formatDate = (iso: string) => {
  try {
    return new Date(iso).toLocaleString('en-US', {
      weekday: 'long', year: 'numeric', month: 'long', day: 'numeric',
      hour: '2-digit', minute: '2-digit',
    });
  } catch { return iso; }
};

/* ── Arc gauge ── */
const ArcGauge: React.FC<{ score: number; label: string; icon: React.ReactNode }> = ({ score, label, icon }) => {
  const c = scoreColor(score);
  const dash = (score / 100) * 220;
  return (
    <div style={{
      background: S.bgCard, border: `1px solid ${S.border}`, borderRadius: S.radius,
      padding: '18px 12px', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 6,
      backdropFilter: 'blur(10px)', flex: '1 1 130px', minWidth: 120,
      transition: 'border-color .2s, box-shadow .2s',
    }}
      onMouseEnter={e => { e.currentTarget.style.borderColor = c; e.currentTarget.style.boxShadow = `0 0 20px ${c}22`; }}
      onMouseLeave={e => { e.currentTarget.style.borderColor = S.border; e.currentTarget.style.boxShadow = 'none'; }}
    >
      <svg viewBox="0 0 100 60" style={{ width: 110, height: 66 }}>
        <path d="M 10 55 A 40 40 0 0 1 90 55" fill="none" stroke="#1e1b4b" strokeWidth="8" strokeLinecap="round" />
        <path d="M 10 55 A 40 40 0 0 1 90 55" fill="none" stroke={c} strokeWidth="8"
          strokeLinecap="round" strokeDasharray={`${dash} 220`} />
      </svg>
      <div style={{ color: c, marginTop: -18 }}>{icon}</div>
      <div style={{ fontSize: 22, fontWeight: 800, color: c, lineHeight: 1 }}>{Math.round(score)}</div>
      <div style={{ fontSize: 11.5, color: S.muted, fontWeight: 600 }}>{label}</div>
    </div>
  );
};

/* ── Feedback block ── */
const FeedbackBlock: React.FC<{ title: string; icon: React.ReactNode; items?: string[]; text?: string; accent: string }> = ({
  title, icon, items, text, accent,
}) => (
  <div style={{
    background: S.bgCard, border: `1px solid ${accent}2a`,
    borderLeft: `3px solid ${accent}`, borderRadius: S.radiusSm,
    padding: '16px 18px', backdropFilter: 'blur(10px)',
  }}>
    <h4 style={{ display: 'flex', alignItems: 'center', gap: 7, fontSize: 13, fontWeight: 700, color: accent, marginBottom: 10 }}>
      {icon} {title}
    </h4>
    {items && items.length > 0 && (
      <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: 6 }}>
        {items.map((s, i) => (
          <li key={i} style={{ display: 'flex', gap: 8, fontSize: 13, color: S.text, lineHeight: 1.6 }}>
            <span style={{ color: accent, flexShrink: 0, marginTop: 2 }}>▸</span>
            {s}
          </li>
        ))}
      </ul>
    )}
    {text && <p style={{ fontSize: 13, color: S.text, lineHeight: 1.7 }}>{text}</p>}
  </div>
);

export const EvaluationDetail: React.FC = () => {
  const { id }          = useParams<{ id: string }>();
  const navigate        = useNavigate();
  const { evaluations } = useAuroraStore();
  const [evaluation, setEvaluation] = useState<EvaluationResult | null>(null);
  const [loading, setLoading]       = useState(true);
  const [error, setError]           = useState<string | null>(null);
  const [tab, setTab]               = useState<'overview' | 'analysis' | 'raw'>('overview');

  useEffect(() => {
    const load = async () => {
      if (!id) return;
      const cached = evaluations.find((e) => String(e.id) === id);
      if (cached) { setEvaluation(cached); setLoading(false); return; }
      setLoading(true);
      try {
        const res = await getEvaluation(Number(id));
        setEvaluation(res.data);
      } catch (err: any) {
        setError(err.message || 'Evaluation not found');
      } finally { setLoading(false); }
    };
    load();
  }, [id]);

  if (loading) return (
    <div style={{
      display: 'flex', flexDirection: 'column', alignItems: 'center',
      justifyContent: 'center', gap: 16, minHeight: 300, color: S.muted,
    }}>
      <div style={{
        width: 48, height: 48, borderRadius: '50%',
        border: `3px solid ${S.border}`,
        borderTopColor: S.accent, borderRightColor: S.accent2,
        animation: 'spin .9s linear infinite',
      }} />
      Loading evaluation…
    </div>
  );

  if (error || !evaluation) return (
    <div style={{
      display: 'flex', flexDirection: 'column', alignItems: 'center',
      justifyContent: 'center', gap: 14, minHeight: 300, color: S.muted,
    }}>
      <AlertTriangle size={40} color={S.red} />
      <h2 style={{ color: S.text }}>Evaluation Not Found</h2>
      <p style={{ fontSize: 13 }}>{error || 'No data available.'}</p>
      <button onClick={() => navigate('/history')} style={{
        padding: '9px 18px', borderRadius: S.radiusSm, fontSize: 13, fontWeight: 700,
        background: S.bgSurface, border: `1px solid ${S.border}`, color: S.text, cursor: 'pointer',
      }}>
        ← Back to History
      </button>
    </div>
  );

  const overall = evaluation.overall_score || 0;
  const oc      = scoreColor(overall);
  const radarData = [
    { subject: 'Code Quality',   score: evaluation.code_quality_score  || 0 },
    { subject: 'Functionality',  score: evaluation.functionality_score  || 0 },
    { subject: 'Documentation',  score: evaluation.documentation_score || 0 },
    { subject: 'Innovation',     score: evaluation.innovation_score     || 0 },
  ];
  const analysis = evaluation.comprehensive_analysis as any;

  const TABS = ['overview', 'analysis', 'raw'] as const;

  return (
    <>
      <style>{KF}</style>
      <div style={{ maxWidth: 1050, margin: '0 auto', animation: 'floatUp .4s ease both' }}>

        {/* Back */}
        <button onClick={() => navigate('/history')} style={{
          display: 'inline-flex', alignItems: 'center', gap: 7, marginBottom: 20,
          background: 'transparent', border: `1px solid ${S.border}`, borderRadius: S.radiusSm,
          color: S.muted, fontSize: 13, fontWeight: 600, cursor: 'pointer', padding: '7px 14px',
          transition: 'all .2s',
        }}
          onMouseEnter={e => { e.currentTarget.style.borderColor = S.accent2; e.currentTarget.style.color = S.accent2; }}
          onMouseLeave={e => { e.currentTarget.style.borderColor = S.border;  e.currentTarget.style.color = S.muted; }}
        >
          <ArrowLeft size={14} /> Back to History
        </button>

        {/* Hero */}
        <div style={{
          display: 'grid', gridTemplateColumns: '1fr auto', gap: 24, alignItems: 'center',
          background: 'linear-gradient(135deg,rgba(124,58,237,.2) 0%,rgba(79,70,229,.12) 50%,rgba(0,212,255,.06) 100%)',
          border: `1px solid rgba(124,58,237,.32)`, borderRadius: S.radius,
          padding: '28px 28px', marginBottom: 20, backdropFilter: 'blur(16px)',
          position: 'relative', overflow: 'hidden',
        }}>
          <div style={{ position: 'absolute', top: -40, right: 220, width: 160, height: 160, borderRadius: '50%', background: 'radial-gradient(circle,rgba(124,58,237,.22) 0%,transparent 70%)', pointerEvents: 'none' }} />

          <div style={{ position: 'relative', zIndex: 1 }}>
            <div style={{
              display: 'inline-flex', alignItems: 'center', gap: 7, marginBottom: 12,
              background: 'rgba(124,58,237,.18)', border: '1px solid rgba(124,58,237,.35)',
              borderRadius: 999, padding: '3px 12px',
              fontSize: 10.5, fontWeight: 700, letterSpacing: .8, color: S.accent2,
            }}>
              Evaluation #{evaluation.id}
            </div>
            <h1 style={{ fontSize: 24, fontWeight: 800, color: '#fff', marginBottom: 10, letterSpacing: -.3 }}>
              Project #{evaluation.project_id}
            </h1>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 12 }}>
              {evaluation.created_at && (
                <span style={{ display: 'flex', alignItems: 'center', gap: 5, fontSize: 12, color: S.muted }}>
                  <Clock size={12} /> {formatDate(evaluation.created_at)}
                </span>
              )}
              {evaluation.ai_model_used && (
                <span style={{ display: 'flex', alignItems: 'center', gap: 5, fontSize: 12, color: S.muted }}>
                  <Cpu size={12} /> {evaluation.ai_model_used}
                </span>
              )}
              {evaluation.evaluation_time && (
                <span style={{ display: 'flex', alignItems: 'center', gap: 5, fontSize: 12, color: S.muted }}>
                  <Zap size={12} /> {evaluation.evaluation_time.toFixed(1)}s
                </span>
              )}
            </div>
          </div>

          {/* Big score circle */}
          <div style={{ position: 'relative', zIndex: 1, width: 120, height: 120, flexShrink: 0 }}>
            <svg viewBox="0 0 120 120" style={{ width: '100%', height: '100%' }}>
              <circle cx="60" cy="60" r="52" fill="none" stroke="#1e1b4b" strokeWidth="10" />
              <circle
                cx="60" cy="60" r="52" fill="none" stroke={oc} strokeWidth="10"
                strokeLinecap="round"
                strokeDasharray={`${(overall / 100) * 326.7} 326.7`}
                strokeDashoffset="81.68"
                transform="rotate(-90 60 60)"
                style={{ filter: `drop-shadow(0 0 8px ${oc}88)` }}
              />
            </svg>
            <div style={{
              position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column',
              alignItems: 'center', justifyContent: 'center',
            }}>
              <span style={{ fontSize: 28, fontWeight: 900, color: oc, lineHeight: 1 }}>{Math.round(overall)}</span>
              <span style={{ fontSize: 11, color: S.muted }}>/&nbsp;100</span>
            </div>
          </div>
        </div>

        {/* Sub-score gauges */}
        <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap', marginBottom: 20 }}>
          <ArcGauge score={evaluation.code_quality_score  || 0} label="Code Quality"  icon={<Code      size={15} />} />
          <ArcGauge score={evaluation.functionality_score  || 0} label="Functionality" icon={<Star      size={15} />} />
          <ArcGauge score={evaluation.documentation_score || 0} label="Documentation" icon={<FileText  size={15} />} />
          <ArcGauge score={evaluation.innovation_score    || 0} label="Innovation"    icon={<Lightbulb size={15} />} />
        </div>

        {/* Tabs */}
        <div style={{
          display: 'flex', gap: 4, marginBottom: 16,
          background: S.bgCard, border: `1px solid ${S.border}`,
          borderRadius: S.radiusSm, padding: 4, width: 'fit-content',
          backdropFilter: 'blur(10px)',
        }}>
          {TABS.map(t => (
            <button key={t} onClick={() => setTab(t)} style={{
              padding: '7px 18px', borderRadius: 7, fontSize: 13, fontWeight: 600,
              cursor: 'pointer', border: 'none', transition: 'all .2s',
              background: tab === t ? `linear-gradient(135deg,${S.accent},#4f46e5)` : 'transparent',
              color: tab === t ? '#fff' : S.muted,
              boxShadow: tab === t ? `0 0 14px ${S.glow}` : 'none',
            }}>
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>

        {/* Tab: Overview */}
        {tab === 'overview' && (
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 18, alignItems: 'start' }}>

            {/* Radar chart */}
            <div style={{
              background: S.bgCard, border: `1px solid ${S.border}`, borderRadius: S.radius,
              padding: '20px 16px', backdropFilter: 'blur(10px)',
            }}>
              <h3 style={{ fontSize: 14, fontWeight: 700, color: '#fff', marginBottom: 16 }}>Score Breakdown</h3>
              <ResponsiveContainer width="100%" height={240}>
                <RadarChart cx="50%" cy="50%" outerRadius="72%" data={radarData}>
                  <PolarGrid gridType="polygon" stroke="#2d2b55" />
                  <PolarAngleAxis dataKey="subject" tick={{ fill: '#9ca3af', fontSize: 11.5 }} />
                  <Radar name="Score" dataKey="score" stroke={S.accent} fill={S.accent} fillOpacity={0.25} strokeWidth={2} />
                  <Tooltip contentStyle={{ background: '#0f0f1a', border: `1px solid ${S.border}`, borderRadius: 8, fontSize: 12 }} />
                </RadarChart>
              </ResponsiveContainer>
            </div>

            {/* Feedback */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
              {evaluation.strengths && evaluation.strengths.length > 0 && (
                <FeedbackBlock title="Strengths" icon={<CheckCircle size={13} />} items={evaluation.strengths} accent={S.green} />
              )}
              {evaluation.weaknesses && evaluation.weaknesses.length > 0 && (
                <FeedbackBlock title="Weaknesses" icon={<AlertTriangle size={13} />} items={evaluation.weaknesses} accent={S.red} />
              )}
              {evaluation.recommendations && evaluation.recommendations.length > 0 && (
                <FeedbackBlock title="Recommendations" icon={<ThumbsUp size={13} />} items={evaluation.recommendations} accent={S.cyan} />
              )}
              {evaluation.feedback && (
                <FeedbackBlock title="AI Feedback" icon={<Star size={13} />} text={evaluation.feedback} accent={S.accent2} />
              )}
            </div>
          </div>
        )}

        {/* Tab: Analysis */}
        {tab === 'analysis' && (
          <div style={{
            background: S.bgCard, border: `1px solid ${S.border}`, borderRadius: S.radius,
            padding: '20px 22px', backdropFilter: 'blur(10px)',
          }}>
            {analysis ? (
              <div style={{ display: 'flex', flexDirection: 'column', gap: 18 }}>
                {Object.entries(analysis).map(([key, value]) => (
                  <div key={key}>
                    <h4 style={{
                      fontSize: 12.5, fontWeight: 700, color: S.accent2, marginBottom: 8,
                      textTransform: 'uppercase', letterSpacing: .7,
                    }}>
                      {key.replace(/_/g, ' ')}
                    </h4>
                    <pre style={{
                      background: 'rgba(7,7,26,.7)', border: `1px solid ${S.border}`,
                      borderRadius: S.radiusSm, padding: '14px 16px',
                      fontSize: 12, color: S.text, whiteSpace: 'pre-wrap',
                      fontFamily: "'JetBrains Mono', monospace",
                      lineHeight: 1.65, overflowX: 'auto',
                    }}>
                      {typeof value === 'string' ? value : JSON.stringify(value, null, 2)}
                    </pre>
                  </div>
                ))}
              </div>
            ) : (
              <p style={{ color: S.muted, fontSize: 14, textAlign: 'center', padding: '32px 0' }}>
                No detailed analysis data available.
              </p>
            )}
          </div>
        )}

        {/* Tab: Raw */}
        {tab === 'raw' && (
          <div style={{
            background: S.bgCard, border: `1px solid ${S.border}`, borderRadius: S.radius,
            padding: '20px 22px', backdropFilter: 'blur(10px)',
          }}>
            <pre style={{
              fontSize: 12, color: S.text, whiteSpace: 'pre-wrap',
              fontFamily: "'JetBrains Mono', monospace",
              lineHeight: 1.65, overflowX: 'auto',
            }}>
              {JSON.stringify(evaluation, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </>
  );
};
