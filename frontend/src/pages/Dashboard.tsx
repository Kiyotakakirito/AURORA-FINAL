import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  BarChart2, Star, Activity, TrendingUp,
  ArrowUpRight, Clock, ChevronRight, Upload
} from 'lucide-react';
import {
  AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, Legend,
} from 'recharts';
import { getOverviewStats, listEvaluations } from '../lib/api';
import { useAuroraStore } from '../lib/store';

const PIE_COLORS = ['#7c3aed', '#2563eb', '#0891b2', '#059669'];

const scoreColor = (s: number) =>
  s >= 80 ? '#22c55e' : s >= 60 ? '#eab308' : '#ef4444';

const formatDate = (iso: string) => {
  try { return new Date(iso).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }); }
  catch { return iso; }
};

/* ── Stat Card ─────────────────────────────────────── */
const StatCard: React.FC<{
  icon: React.ReactNode; label: string; value: string | number;
  sub?: string; color?: string; delay?: number;
}> = ({ icon, label, value, sub, color = '#7c3aed', delay = 0 }) => (
  <motion.div
    className="stat-card"
    style={{ '--accent': color } as React.CSSProperties}
    initial={{ opacity: 0, y: 24 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ delay, duration: 0.45, ease: [0.4, 0, 0.2, 1] }}
    whileHover={{ y: -6, scale: 1.02 }}
  >
    <div className="stat-icon" style={{ background: `${color}22`, color }}>
      {icon}
    </div>
    <div className="stat-body">
      <p className="stat-label">{label}</p>
      <p className="stat-value">{value}</p>
      {sub && <p className="stat-sub">{sub}</p>}
    </div>
  </motion.div>
);

/* ── Custom Tooltip ────────────────────────────────── */
const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload?.length) {
    return (
      <div style={{
        background: '#0f0f22', border: '1px solid rgba(124,58,237,0.3)',
        borderRadius: 10, padding: '10px 14px',
      }}>
        <p style={{ color: '#a5a3c8', fontSize: 12, marginBottom: 4 }}>{label}</p>
        <p style={{ color: '#a78bfa', fontWeight: 700, fontSize: 16 }}>
          {payload[0].value}<span style={{ fontSize: 11, color: '#5e5c7a' }}>/100</span>
        </p>
        <p style={{ color: '#5e5c7a', fontSize: 11 }}>{payload[0].payload.count} submissions</p>
      </div>
    );
  }
  return null;
};

/* ── Dashboard Page ───────────────────────────────── */
export const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const { stats, setStats, evaluations, setEvaluations, setIsLoadingStats } = useAuroraStore();
  const [loading, setLoading] = useState(!stats);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const load = async () => {
      setLoading(true); setError(null);
      try {
        const [sRes, eRes] = await Promise.all([getOverviewStats(), listEvaluations(0, 30)]);
        setStats(sRes.data);
        setEvaluations(eRes.data || []);
      } catch (err: any) {
        setError(err.message || 'Failed to load dashboard data');
      } finally { setLoading(false); setIsLoadingStats(false); }
    };
    load();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const chartData = React.useMemo(() => {
    const map: Record<string, { date: string; avg: number; count: number; total: number }> = {};
    evaluations.forEach((ev) => {
      if (!ev.created_at) return;
      const d = formatDate(ev.created_at);
      if (!map[d]) map[d] = { date: d, avg: 0, count: 0, total: 0 };
      map[d].count += 1;
      map[d].total += ev.overall_score || 0;
    });
    return Object.values(map).map((v) => ({ ...v, avg: Math.round(v.total / v.count) })).slice(-14);
  }, [evaluations]);

  const submissionTypeCounts = React.useMemo(() => {
    const raw = stats?.submission_type_counts ?? {};
    return [
      { name: 'GitHub', value: raw['github'] ?? 0 },
      { name: 'ZIP',    value: raw['zip']    ?? 0 },
      { name: 'PDF',    value: raw['pdf']    ?? 0 },
    ];
  }, [stats]);

  const recentList = stats?.recent_evaluations?.length
    ? stats.recent_evaluations
    : evaluations.slice(0, 6);

  if (loading) {
    return (
      <div className="page-loading">
        <div className="aurora-spinner" />
        <p>Loading dashboard…</p>
      </div>
    );
  }

  return (
    <div className="dashboard-page">
      {/* Header */}
      <div className="page-header">
        <motion.div
          initial={{ opacity: 0, x: -16 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.4 }}
        >
          <h1>Dashboard</h1>
          <p>Real-time overview of all student project evaluations</p>
        </motion.div>
        <motion.div
          className="header-actions"
          initial={{ opacity: 0, x: 16 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.4, delay: 0.1 }}
        >
          <motion.button
            className="btn-primary"
            onClick={() => navigate('/submit')}
            whileHover={{ scale: 1.05, y: -2 }}
            whileTap={{ scale: 0.97 }}
          >
            <Upload size={15} /> Submit Project
          </motion.button>
        </motion.div>
      </div>

      {error && <div className="error-banner">{error}</div>}

      {/* Stat Cards */}
      <div className="stats-grid">
        <StatCard
          icon={<BarChart2 size={22} />} label="Total Submissions"
          value={stats?.total_projects ?? evaluations.length} sub="All time"
          color="#7c3aed" delay={0}
        />
        <StatCard
          icon={<Star size={22} />} label="Average Score"
          value={stats?.average_score ? `${stats.average_score.toFixed(1)}/100` : '—'}
          sub="Across all evaluations" color="#2563eb" delay={0.07}
        />
        <StatCard
          icon={<Activity size={22} />} label="Evaluations Run"
          value={stats?.total_evaluations ?? 0} sub="AI evaluations completed"
          color="#0891b2" delay={0.14}
        />
        <StatCard
          icon={<TrendingUp size={22} />} label="High Performers"
          value={evaluations.filter(e => (e.overall_score || 0) >= 80).length}
          sub="Scored ≥ 80" color="#059669" delay={0.21}
        />
      </div>

      {/* Charts */}
      <motion.div
        className="charts-row"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.35, duration: 0.45 }}
      >
        {/* Score Trend */}
        <div className="chart-card" style={{ flex: 2 }}>
          <h3 className="chart-title">Score Trend — Last 14 Days</h3>
          {chartData.length > 0 ? (
            <ResponsiveContainer width="100%" height={220}>
              <AreaChart data={chartData} margin={{ top: 5, right: 10, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="auroraGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%"  stopColor="#7c3aed" stopOpacity={0.5} />
                    <stop offset="95%" stopColor="#2563eb" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <XAxis dataKey="date" stroke="#3d3b5a" tick={{ fill: '#6b6a8a', fontSize: 11 }} />
                <YAxis domain={[0, 100]} stroke="#3d3b5a" tick={{ fill: '#6b6a8a', fontSize: 11 }} />
                <Tooltip content={<CustomTooltip />} />
                <Area
                  type="monotone" dataKey="avg" stroke="#7c3aed"
                  strokeWidth={2.5} fill="url(#auroraGrad)" name="Avg Score"
                  dot={{ r: 4, fill: '#7c3aed', strokeWidth: 0 }}
                  activeDot={{ r: 6, fill: '#a78bfa', strokeWidth: 0 }}
                />
              </AreaChart>
            </ResponsiveContainer>
          ) : (
            <div className="chart-empty">No evaluation data yet. Submit a project to see trends.</div>
          )}
        </div>

        {/* Submission Types Pie */}
        <div className="chart-card" style={{ flex: 1 }}>
          <h3 className="chart-title">Submission Types</h3>
          <ResponsiveContainer width="100%" height={220}>
            <PieChart>
              <Pie
                data={submissionTypeCounts} cx="50%" cy="48%"
                innerRadius={55} outerRadius={78} paddingAngle={4}
                dataKey="value" startAngle={90} endAngle={-270}
              >
                {submissionTypeCounts.map((_, i) => (
                  <Cell key={i} fill={PIE_COLORS[i % PIE_COLORS.length]} />
                ))}
              </Pie>
              <Legend
                iconType="circle" iconSize={8}
                formatter={(v) => <span style={{ color: '#a5a3c8', fontSize: 12 }}>{v}</span>}
              />
              <Tooltip
                contentStyle={{ background: '#0f0f22', border: '1px solid rgba(124,58,237,0.3)', borderRadius: 8 }}
                labelStyle={{ color: '#e5e7eb' }}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </motion.div>

      {/* Recent Evaluations */}
      <motion.div
        className="recent-card"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5, duration: 0.45 }}
      >
        <div className="card-header">
          <h3>Recent Evaluations</h3>
          <button className="link-btn" onClick={() => navigate('/history')}>
            View All <ChevronRight size={14} />
          </button>
        </div>
        <div className="recent-list">
          {recentList.map((ev, i) => (
            <motion.div
              key={ev.id || i}
              className="recent-item"
              onClick={() => ev.id && navigate(`/evaluations/${ev.id}`)}
              initial={{ opacity: 0, x: -12 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.55 + i * 0.06 }}
              whileHover={{ x: 4 }}
            >
              <div className="recent-left">
                <div className="recent-avatar">
                  {String(ev.project_id || i + 1).slice(0, 2).toUpperCase()}
                </div>
                <div>
                  <p className="recent-title">Project #{ev.project_id}</p>
                  {ev.created_at && (
                    <p className="recent-time">
                      <Clock size={11} /> {formatDate(ev.created_at)}
                    </p>
                  )}
                </div>
              </div>
              <div className="recent-score" style={{ color: scoreColor(ev.overall_score || 0) }}>
                {ev.overall_score ? `${Math.round(ev.overall_score)}/100` : '—'}
                <ArrowUpRight size={14} />
              </div>
            </motion.div>
          ))}

          {recentList.length === 0 && (
            <div className="empty-state">
              <BarChart2 size={36} />
              <p>No evaluations yet.<br /><span onClick={() => navigate('/submit')}>Submit your first project →</span></p>
            </div>
          )}
        </div>
      </motion.div>
    </div>
  );
};
