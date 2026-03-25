import React, { useCallback, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Clock, Search, Filter, ChevronRight, Download,
  RefreshCw, TrendingUp, BarChart3, AlertCircle, Inbox,
} from 'lucide-react';
import { listEvaluations } from '../lib/api';
import { useAuroraStore } from '../lib/store';

/* ─── design tokens ─── */
const S = {
  bg:        '#07071a',
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

const KF = `
@keyframes floatUp{0%{opacity:0;transform:translateY(16px) scale(.97)}100%{opacity:1;transform:none}}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes shimmer{0%{background-position:-200% center}100%{background-position:200% center}}
@keyframes pulse{0%,100%{opacity:.6}50%{opacity:1}}
`;

const formatDate = (iso: string) => {
  try {
    return new Date(iso).toLocaleString('en-US', {
      month: 'short', day: 'numeric', year: 'numeric',
      hour: '2-digit', minute: '2-digit',
    });
  } catch { return iso; }
};

/* ── Score bar ── */
const ScoreBar: React.FC<{ value: number }> = ({ value }) => {
  const color = value >= 80 ? S.green : value >= 60 ? S.yellow : S.red;
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 10, minWidth: 140 }}>
      <div style={{ flex: 1, height: 5, background: 'rgba(22,18,62,.8)', borderRadius: 999, overflow: 'hidden' }}>
        <div style={{
          height: '100%', width: `${Math.min(value, 100)}%`,
          background: color, borderRadius: 999,
          boxShadow: `0 0 6px ${color}55`,
          transition: 'width .5s cubic-bezier(.4,0,.2,1)',
        }} />
      </div>
      <span style={{ fontSize: 13, fontWeight: 700, color, minWidth: 28, textAlign: 'right' }}>
        {Math.round(value)}
      </span>
    </div>
  );
};

/* ── Chip ── */
const Chip: React.FC<{ value?: number }> = ({ value }) => {
  if (value == null) return <span style={{ color: S.muted, fontSize: 12 }}>—</span>;
  const color = value >= 80 ? S.green : value >= 60 ? S.yellow : S.red;
  return (
    <span style={{
      display: 'inline-block', padding: '3px 10px', borderRadius: 999,
      fontSize: 11.5, fontWeight: 700,
      background: `${color}18`, color, border: `1px solid ${color}44`,
    }}>
      {Math.round(value)}
    </span>
  );
};

/* ── Stat Card ── */
const StatCard: React.FC<{ icon: React.ReactNode; label: string; value: string | number; accent: string }> = ({
  icon, label, value, accent,
}) => (
  <div style={{
    background: S.bgCard, border: `1px solid ${S.border}`,
    borderRadius: S.radius, padding: '18px 20px',
    backdropFilter: 'blur(10px)', display: 'flex', alignItems: 'center', gap: 14,
    transition: 'border-color .2s',
  }}
    onMouseEnter={e => (e.currentTarget.style.borderColor = S.borderHov)}
    onMouseLeave={e => (e.currentTarget.style.borderColor = S.border)}
  >
    <div style={{
      width: 42, height: 42, borderRadius: 10, display: 'flex',
      alignItems: 'center', justifyContent: 'center', flexShrink: 0,
      background: `${accent}1a`, color: accent,
    }}>
      {icon}
    </div>
    <div>
      <div style={{ fontSize: 22, fontWeight: 800, color: '#fff', lineHeight: 1 }}>{value}</div>
      <div style={{ fontSize: 11.5, color: S.muted, marginTop: 3 }}>{label}</div>
    </div>
  </div>
);

export const EvaluationHistory: React.FC = () => {
  const navigate = useNavigate();
  const { evaluations, setEvaluations } = useAuroraStore();
  const [loading, setLoading]   = useState(evaluations.length === 0);
  const [error, setError]       = useState<string | null>(null);
  const [search, setSearch]     = useState('');
  const [minScore, setMinScore] = useState<number>(0);
  const [sortBy, setSortBy]     = useState<'date' | 'score'>('date');

  const load = useCallback(async () => {
    setLoading(true); setError(null);
    try {
      const res = await listEvaluations(0, 100);
      setEvaluations(res.data || []);
    } catch (err: any) {
      setError(err.message || 'Failed to load evaluations');
    } finally {
      setLoading(false);
    }
  }, [setEvaluations]);

  useEffect(() => { load(); }, [load]);

  const filtered = React.useMemo(() => {
    let list = [...evaluations];
    if (search.trim()) {
      const q = search.trim().toLowerCase();
      list = list.filter(e =>
        String(e.project_id ?? '').includes(q) || String(e.id ?? '').includes(q)
      );
    }
    if (minScore > 0) list = list.filter(e => (e.overall_score || 0) >= minScore);
    if (sortBy === 'score') list.sort((a, b) => (b.overall_score || 0) - (a.overall_score || 0));
    else list.sort((a, b) => new Date(b.created_at || '').getTime() - new Date(a.created_at || '').getTime());
    return list;
  }, [evaluations, search, minScore, sortBy]);

  const avgScore = evaluations.length
    ? Math.round(evaluations.reduce((s, e) => s + (e.overall_score || 0), 0) / evaluations.length)
    : 0;
  const bestScore = evaluations.length
    ? Math.round(Math.max(...evaluations.map(e => e.overall_score || 0)))
    : 0;

  const exportCSV = () => {
    const rows = [
      ['ID', 'Project ID', 'Score', 'Code Quality', 'Functionality', 'Documentation', 'Innovation', 'Date'],
      ...filtered.map(e => [
        e.id, e.project_id,
        e.overall_score, e.code_quality_score, e.functionality_score,
        e.documentation_score, e.innovation_score, e.created_at,
      ]),
    ];
    const csv  = rows.map(r => r.join(',')).join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url  = URL.createObjectURL(blob);
    const a    = document.createElement('a');
    a.href = url; a.download = `aurora-evaluations-${Date.now()}.csv`; a.click();
  };

  /* ── select style ── */
  const selectStyle: React.CSSProperties = {
    background: 'rgba(10,8,32,.7)', border: `1px solid ${S.border}`,
    borderRadius: S.radiusSm, color: S.text, padding: '8px 12px',
    fontSize: 13, outline: 'none', cursor: 'pointer', fontFamily: 'inherit',
  };

  return (
    <>
      <style>{KF}</style>

      <div style={{ maxWidth: 1100, margin: '0 auto', animation: 'floatUp .45s ease both' }}>

        {/* ── Hero header ── */}
        <div style={{
          position: 'relative', borderRadius: S.radius, overflow: 'hidden',
          marginBottom: 28, padding: '32px 28px',
          background: 'linear-gradient(135deg,rgba(124,58,237,.22) 0%,rgba(79,70,229,.14) 50%,rgba(0,212,255,.08) 100%)',
          border: `1px solid rgba(124,58,237,.32)`,
          backdropFilter: 'blur(16px)',
        }}>
          <div style={{ position: 'absolute', top: -50, right: -30, width: 200, height: 200, borderRadius: '50%', background: 'radial-gradient(circle,rgba(124,58,237,.28) 0%,transparent 70%)', pointerEvents: 'none' }} />
          <div style={{ position: 'absolute', bottom: -30, left: -20, width: 130, height: 130, borderRadius: '50%', background: 'radial-gradient(circle,rgba(0,212,255,.15) 0%,transparent 70%)', pointerEvents: 'none' }} />

          <div style={{ position: 'relative', zIndex: 1, display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', flexWrap: 'wrap', gap: 16 }}>
            <div>
              <div style={{
                display: 'inline-flex', alignItems: 'center', gap: 7, marginBottom: 12,
                background: 'rgba(124,58,237,.2)', border: '1px solid rgba(124,58,237,.38)',
                borderRadius: 999, padding: '4px 13px',
                fontSize: 11, fontWeight: 700, letterSpacing: .8, color: S.accent2,
              }}>
                <BarChart3 size={11} /> EVALUATION HISTORY
              </div>
              <h1 style={{ fontSize: 26, fontWeight: 800, color: '#fff', letterSpacing: -.3, marginBottom: 6 }}>
                All Evaluations
              </h1>
              <p style={{ fontSize: 13.5, color: S.muted, maxWidth: 440 }}>
                Browse, filter, and export all project evaluation records.
              </p>
            </div>

            <div style={{ display: 'flex', gap: 10, alignItems: 'center', flexWrap: 'wrap' }}>
              <button onClick={load} disabled={loading} style={{
                display: 'flex', alignItems: 'center', gap: 7,
                padding: '9px 16px', borderRadius: S.radiusSm,
                background: S.bgSurface, border: `1px solid ${S.border}`,
                color: S.text, fontSize: 13, fontWeight: 600, cursor: loading ? 'not-allowed' : 'pointer',
                transition: 'all .2s', opacity: loading ? .5 : 1,
              }}
                onMouseEnter={e => { if (!loading) e.currentTarget.style.borderColor = S.borderHov; }}
                onMouseLeave={e => { e.currentTarget.style.borderColor = S.border; }}
              >
                <RefreshCw size={14} style={{ animation: loading ? 'spin .8s linear infinite' : 'none' }} /> Refresh
              </button>
              <button onClick={exportCSV} style={{
                display: 'flex', alignItems: 'center', gap: 7,
                padding: '9px 16px', borderRadius: S.radiusSm,
                background: `linear-gradient(135deg,${S.accent},#4f46e5)`,
                border: 'none', color: '#fff', fontSize: 13, fontWeight: 700, cursor: 'pointer',
                boxShadow: `0 0 16px ${S.glow}`, transition: 'all .2s',
              }}
                onMouseEnter={e => (e.currentTarget.style.boxShadow = `0 0 28px ${S.glow}`)}
                onMouseLeave={e => (e.currentTarget.style.boxShadow = `0 0 16px ${S.glow}`)}
              >
                <Download size={14} /> Export CSV
              </button>
            </div>
          </div>
        </div>

        {/* ── Stat cards ── */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit,minmax(170px,1fr))', gap: 14, marginBottom: 24 }}>
          <StatCard icon={<BarChart3 size={18} />} label="Total Evaluations" value={evaluations.length}      accent={S.accent2} />
          <StatCard icon={<TrendingUp size={18} />} label="Average Score"     value={avgScore || '—'}         accent="#2563eb" />
          <StatCard icon={<TrendingUp size={18} />} label="Best Score"        value={bestScore || '—'}        accent={S.green} />
          <StatCard icon={<Filter     size={18} />} label="Filtered Results"  value={filtered.length}         accent={S.cyan} />
        </div>

        {/* ── Error ── */}
        {error && (
          <div style={{
            background: 'rgba(239,68,68,.1)', border: '1px solid rgba(239,68,68,.3)',
            borderRadius: S.radiusSm, padding: '12px 16px', marginBottom: 18,
            display: 'flex', alignItems: 'center', gap: 10, color: '#f87171', fontSize: 13,
          }}>
            <AlertCircle size={15} style={{ flexShrink: 0 }} /> {error}
          </div>
        )}

        {/* ── Filter bar ── */}
        <div style={{
          display: 'flex', gap: 10, alignItems: 'center', flexWrap: 'wrap',
          background: S.bgCard, border: `1px solid ${S.border}`,
          borderRadius: S.radius, padding: '14px 18px', marginBottom: 18,
          backdropFilter: 'blur(10px)',
        }}>
          {/* search */}
          <div style={{ flex: 1, minWidth: 200, position: 'relative' }}>
            <Search size={14} style={{ position: 'absolute', left: 12, top: '50%', transform: 'translateY(-50%)', color: S.muted, pointerEvents: 'none' }} />
            <input
              value={search} onChange={e => setSearch(e.target.value)}
              placeholder="Search by project ID or evaluation ID…"
              style={{
                width: '100%', background: 'rgba(10,8,32,.7)',
                border: `1px solid ${S.border}`, borderRadius: S.radiusSm,
                color: S.text, padding: '8px 12px 8px 34px',
                fontSize: 13, outline: 'none', fontFamily: 'inherit',
                transition: 'all .2s',
              }}
              onFocus={e => { e.target.style.borderColor = S.accent; e.target.style.boxShadow = `0 0 0 3px ${S.glow}`; }}
              onBlur={e  => { e.target.style.borderColor = S.border;  e.target.style.boxShadow = 'none'; }}
            />
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: 7 }}>
            <Filter size={13} color={S.muted} />
            <label style={{ fontSize: 12, color: S.muted, fontWeight: 600 }}>Min Score</label>
            <select value={minScore} onChange={e => setMinScore(Number(e.target.value))} style={selectStyle}>
              <option value={0}>All</option>
              <option value={60}>≥ 60</option>
              <option value={70}>≥ 70</option>
              <option value={80}>≥ 80</option>
              <option value={90}>≥ 90</option>
            </select>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: 7 }}>
            <label style={{ fontSize: 12, color: S.muted, fontWeight: 600 }}>Sort by</label>
            <select value={sortBy} onChange={e => setSortBy(e.target.value as any)} style={selectStyle}>
              <option value="date">Date</option>
              <option value="score">Score</option>
            </select>
          </div>

          <span style={{
            fontSize: 12, color: S.muted, marginLeft: 'auto',
            background: S.bgSurface, border: `1px solid ${S.border}`,
            borderRadius: 999, padding: '4px 12px',
          }}>
            {filtered.length} result{filtered.length !== 1 ? 's' : ''}
          </span>
        </div>

        {/* ── Table / Loading / Empty ── */}
        {loading ? (
          <div style={{
            background: S.bgCard, border: `1px solid ${S.border}`, borderRadius: S.radius,
            padding: '64px 24px', backdropFilter: 'blur(10px)',
            display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 16,
          }}>
            <div style={{
              width: 48, height: 48, borderRadius: '50%',
              border: `3px solid ${S.border}`,
              borderTopColor: S.accent, borderRightColor: S.accent2,
              animation: 'spin .9s linear infinite',
            }} />
            <p style={{ color: S.muted, fontSize: 14 }}>Loading evaluations…</p>
          </div>
        ) : filtered.length === 0 ? (
          <div style={{
            background: S.bgCard, border: `1px solid ${S.border}`, borderRadius: S.radius,
            padding: '64px 24px', backdropFilter: 'blur(10px)',
            display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 14,
          }}>
            <Inbox size={40} color={S.muted} />
            <p style={{ color: S.muted, fontSize: 14 }}>
              {evaluations.length === 0 ? 'No evaluations yet. Submit a project to get started.' : 'No evaluations match your filters.'}
            </p>
          </div>
        ) : (
          <div style={{
            background: S.bgCard, border: `1px solid ${S.border}`,
            borderRadius: S.radius, overflow: 'hidden',
            backdropFilter: 'blur(10px)',
          }}>
            {/* Table header */}
            <div style={{
              display: 'grid',
              gridTemplateColumns: '80px 140px 1fr 90px 90px 90px 1fr 40px',
              padding: '10px 18px', borderBottom: `1px solid ${S.border}`,
              background: 'rgba(22,18,62,.5)',
            }}>
              {['ID', 'Project', 'Overall Score', 'Code', 'Func.', 'Innov.', 'Date', ''].map((h, i) => (
                <div key={i} style={{ fontSize: 10.5, fontWeight: 700, letterSpacing: .7, textTransform: 'uppercase', color: S.muted }}>
                  {h}
                </div>
              ))}
            </div>

            {/* Rows */}
            {filtered.map((ev, idx) => (
              <div
                key={ev.id != null ? String(ev.id) : `${ev.project_id}-${idx}`}
                onClick={() => ev.id && navigate(`/evaluations/${ev.id}`)}
                style={{
                  display: 'grid',
                  gridTemplateColumns: '80px 140px 1fr 90px 90px 90px 1fr 40px',
                  padding: '13px 18px', alignItems: 'center',
                  borderBottom: idx < filtered.length - 1 ? `1px solid ${S.border}` : 'none',
                  cursor: ev.id ? 'pointer' : 'default',
                  transition: 'background .15s',
                }}
                onMouseEnter={e => (e.currentTarget.style.background = 'rgba(124,58,237,.06)')}
                onMouseLeave={e => (e.currentTarget.style.background = 'transparent')}
              >
                <div style={{ fontSize: 12, fontWeight: 700, color: S.accent2 }}>#{ev.id ?? '—'}</div>
                <div style={{ fontSize: 13, color: S.text, fontWeight: 500 }}>Project #{ev.project_id}</div>
                <ScoreBar value={ev.overall_score || 0} />
                <Chip value={ev.code_quality_score} />
                <Chip value={ev.functionality_score} />
                <Chip value={ev.innovation_score} />
                <div style={{ display: 'flex', alignItems: 'center', gap: 5, fontSize: 12, color: S.muted }}>
                  <Clock size={11} />
                  {ev.created_at ? formatDate(ev.created_at) : '—'}
                </div>
                <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
                  <ChevronRight size={15} color={S.muted} />
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </>
  );
};
