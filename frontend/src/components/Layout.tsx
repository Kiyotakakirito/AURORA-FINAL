import React, { useState } from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import {
  LayoutDashboard, Upload, History,
  ChevronLeft, Zap, Activity,
} from 'lucide-react';

const navItems = [
  { to: '/dashboard', label: 'Dashboard', icon: <LayoutDashboard size={18} /> },
  { to: '/submit',    label: 'Submit',    icon: <Upload size={18} /> },
  { to: '/history',   label: 'History',   icon: <History size={18} /> },
];

const pageLabels: Record<string, string> = {
  '/dashboard': 'Dashboard',
  '/submit':    'Submit Project',
  '/history':   'Evaluation History',
};

export const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [collapsed, setCollapsed] = useState(false);
  const location = useLocation();

  const currentLabel =
    Object.entries(pageLabels).find(([path]) =>
      path === '/' ? location.pathname === '/' : location.pathname.startsWith(path)
    )?.[1] ?? 'AURORA';

  return (
    <div className={`app-shell ${collapsed ? 'sidebar-collapsed' : ''}`}>

      {/* ─── Sidebar ─── */}
      <motion.aside
        className="sidebar"
        animate={{ width: collapsed ? 64 : 240 }}
        transition={{ duration: 0.35, ease: [0.4, 0, 0.2, 1] }}
      >
        {/* Logo row – no toggle button here */}
        <div className="sidebar-logo">
          <motion.div
            className="logo-icon"
            whileHover={{ scale: 1.1, rotate: 5 }}
            whileTap={{ scale: 0.95 }}
          >
            <Zap size={20} color="#fff" />
          </motion.div>

          <AnimatePresence>
            {!collapsed && (
              <motion.div
                className="logo-text"
                initial={{ opacity: 0, x: -12 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -12 }}
                transition={{ duration: 0.2 }}
              >
                <span className="logo-main">AURORA</span>
                <span className="logo-sub">AI Evaluator</span>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* Nav */}
        <nav className="sidebar-nav">
          {navItems.map((item, idx) => (
            <motion.div
              key={item.to}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: idx * 0.06, duration: 0.3 }}
            >
              <NavLink
                to={item.to}
                end={item.to === '/'}
                className={({ isActive }) => `nav-item ${isActive ? 'nav-active' : ''}`}
                title={collapsed ? item.label : undefined}
              >
                <span className="nav-icon">{item.icon}</span>
                <AnimatePresence>
                  {!collapsed && (
                    <motion.span
                      className="nav-label"
                      initial={{ opacity: 0, width: 0 }}
                      animate={{ opacity: 1, width: 'auto' }}
                      exit={{ opacity: 0, width: 0 }}
                      transition={{ duration: 0.2 }}
                      style={{ overflow: 'hidden', whiteSpace: 'nowrap' }}
                    >
                      {item.label}
                    </motion.span>
                  )}
                </AnimatePresence>
              </NavLink>
            </motion.div>
          ))}
        </nav>

        {/* Bottom */}
        <div className="sidebar-bottom">
          <AnimatePresence>
            {!collapsed && (
              <motion.div
                className="sidebar-version"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
              >
                v3.0.0 — AURORA AI
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </motion.aside>

      {/*
        ─── Collapse toggle ───────────────────────────────────────────────────
        IMPORTANT: this button lives OUTSIDE <motion.aside> so that the
        sidebar's `overflow: hidden` can never clip or block it.
        We animate its `left` position to follow the sidebar edge.
      */}
      <motion.button
        className="collapse-btn"
        onClick={() => setCollapsed(s => !s)}
        animate={{ left: collapsed ? 51 : 227 }}
        transition={{ duration: 0.35, ease: [0.4, 0, 0.2, 1] }}
        whileHover={{ scale: 1.15 }}
        whileTap={{ scale: 0.9 }}
        title={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
      >
        <motion.div
          animate={{ rotate: collapsed ? 180 : 0 }}
          transition={{ duration: 0.3 }}
        >
          <ChevronLeft size={14} />
        </motion.div>
      </motion.button>

      {/* ─── Main ─── */}
      <main className="main-content">
        {/* Top Bar */}
        <header className="top-bar">
          <motion.div
            key={currentLabel}
            className="breadcrumb"
            initial={{ opacity: 0, y: -6 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.25 }}
          >
            {currentLabel}
          </motion.div>
          <div className="top-bar-actions">
            <Activity size={15} color="var(--text-muted)" />
            <div className="aurora-status-dot" title="System Online" />
          </div>
        </header>

        {/* Animated page transitions */}
        <motion.div
          key={location.pathname}
          className="content-area"
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -8 }}
          transition={{ duration: 0.35, ease: [0.4, 0, 0.2, 1] }}
        >
          {children}
        </motion.div>
      </main>
    </div>
  );
};
