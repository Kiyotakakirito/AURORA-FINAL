import React, { useEffect, useRef, CSSProperties } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';

/* ── Floating particle ───────────────────────────────── */
interface Particle {
  id: number;
  x: number;
  y: number;
  size: number;
  dur: number;
  delay: number;
  color: string;
}

const COLORS = [
  'rgba(0,212,255,0.65)',
  'rgba(59,130,246,0.55)',
  'rgba(139,92,246,0.5)',
  'rgba(0,180,220,0.45)',
  'rgba(99,179,237,0.4)',
];

function makeParticles(n: number): Particle[] {
  return Array.from({ length: n }, (_, i) => ({
    id: i,
    x: Math.random() * 100,
    y: Math.random() * 100,
    size: 2 + Math.random() * 4,
    dur: 6 + Math.random() * 10,
    delay: Math.random() * 8,
    color: COLORS[Math.floor(Math.random() * COLORS.length)],
  }));
}

const PARTICLES = makeParticles(55);

/* ── Animation variants ──────────────────────────────── */
const containerV = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.08 } },
};
const letterV = {
  hidden: { y: 120, opacity: 0, rotateX: -90 },
  visible: {
    y: 0,
    opacity: 1,
    rotateX: 0,
    transition: { duration: 0.85, ease: [0.16, 1, 0.3, 1] as [number, number, number, number] },
  },
};
const subV = {
  hidden: { opacity: 0, y: 24 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.9, delay: 1.1, ease: 'easeOut' as const } },
};
const taglineV = {
  hidden: { opacity: 0, y: 16 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.8, delay: 1.5, ease: 'easeOut' as const } },
};
const btnV = {
  hidden: { opacity: 0, scale: 0.85, y: 20 },
  visible: {
    opacity: 1, scale: 1, y: 0,
    transition: { duration: 0.7, delay: 2.0, ease: [0.34, 1.56, 0.64, 1] as [number, number, number, number] },
  },
};
const dividerV = {
  hidden: { scaleX: 0, opacity: 0 },
  visible: { scaleX: 1, opacity: 1, transition: { duration: 0.9, delay: 1.8, ease: 'easeOut' as const } },
};

/* ── Keyframe injection (runs once) ──────────────────── */
const KEYFRAMES = `
@keyframes float-particle {
  0%   { transform: translateY(0px) scale(1);   opacity: 0.7; }
  50%  { transform: translateY(-22px) scale(1.1); opacity: 1; }
  100% { transform: translateY(0px) scale(1);   opacity: 0.7; }
}
@keyframes scroll-wheel {
  0%   { transform: translateY(0);   opacity: 1; }
  100% { transform: translateY(10px); opacity: 0; }
}
@keyframes badge-pulse {
  0%, 100% { box-shadow: 0 0 0 0 rgba(0,212,255,0.4); }
  50%       { box-shadow: 0 0 0 8px rgba(0,212,255,0); }
}
@keyframes grid-fade {
  0%   { opacity: 0.03; }
  50%  { opacity: 0.06; }
  100% { opacity: 0.03; }
}
`;

export const LandingPage: React.FC = () => {
  const navigate = useNavigate();
  const canvasRef = useRef<HTMLCanvasElement>(null);

  /* Inject keyframes once */
  useEffect(() => {
    const id = 'lp-keyframes';
    if (!document.getElementById(id)) {
      const s = document.createElement('style');
      s.id = id;
      s.textContent = KEYFRAMES;
      document.head.appendChild(s);
    }
  }, []);

  /* Subtle aurora gradient canvas animation */
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d')!;
    let frame = 0;
    let raf: number;

    const resize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    resize();
    window.addEventListener('resize', resize);

    const draw = () => {
      frame += 0.003;
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      const cx = canvas.width / 2;
      const cy = canvas.height / 2;

      const orbs = [
        { x: cx + Math.sin(frame) * 180,        y: cy + Math.cos(frame * 0.7) * 140,  r: 420, c: 'rgba(0,212,255,0.12)' },
        { x: cx + Math.cos(frame * 0.9) * 220,  y: cy + Math.sin(frame * 1.1) * 100,  r: 360, c: 'rgba(59,130,246,0.10)' },
        { x: cx + Math.sin(frame * 1.3) * 140,  y: cy + Math.cos(frame * 0.5) * 200,  r: 310, c: 'rgba(139,92,246,0.08)' },
        { x: cx + Math.cos(frame * 0.6) * 260,  y: cy + Math.sin(frame * 0.8) * 80,   r: 280, c: 'rgba(0,180,220,0.08)' },
      ];

      orbs.forEach(o => {
        const g = ctx.createRadialGradient(o.x, o.y, 0, o.x, o.y, o.r);
        g.addColorStop(0, o.c);
        g.addColorStop(1, 'transparent');
        ctx.fillStyle = g;
        ctx.beginPath();
        ctx.arc(o.x, o.y, o.r, 0, Math.PI * 2);
        ctx.fill();
      });

      raf = requestAnimationFrame(draw);
    };
    draw();
    return () => { cancelAnimationFrame(raf); window.removeEventListener('resize', resize); };
  }, []);

  /* ── Styles ──────────────────────────────────────────── */
  const s: Record<string, CSSProperties> = {
    root: {
      position: 'relative',
      width: '100vw',
      height: '100vh',
      overflow: 'hidden',
      background: 'radial-gradient(ellipse at 50% 30%, #050d1a 0%, #020810 100%)',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      fontFamily: "'Inter', 'Segoe UI', sans-serif",
    },
    canvas: {
      position: 'absolute',
      inset: 0,
      zIndex: 0,
      pointerEvents: 'none',
    },
    grid: {
      position: 'absolute',
      inset: 0,
      zIndex: 1,
      pointerEvents: 'none',
      backgroundImage: `
        linear-gradient(rgba(0,212,255,0.035) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,212,255,0.035) 1px, transparent 1px)
      `,
      backgroundSize: '60px 60px',
      animation: 'grid-fade 6s ease-in-out infinite',
    },
    particles: {
      position: 'absolute',
      inset: 0,
      zIndex: 2,
      pointerEvents: 'none',
    },
    content: {
      position: 'relative',
      zIndex: 10,
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      textAlign: 'center',
      gap: '0px',
      padding: '0 24px',
      maxWidth: '900px',
      width: '100%',
    },
    badge: {
      display: 'inline-flex',
      alignItems: 'center',
      gap: '8px',
      background: 'rgba(0,212,255,0.08)',
      border: '1px solid rgba(0,212,255,0.25)',
      borderRadius: '999px',
      padding: '6px 18px',
      fontSize: '12px',
      fontWeight: 600,
      letterSpacing: '0.08em',
      color: 'rgba(0,212,255,0.9)',
      textTransform: 'uppercase' as const,
      marginBottom: '32px',
      animation: 'badge-pulse 3s ease-in-out infinite',
    },
    badgeDot: {
      width: '7px',
      height: '7px',
      borderRadius: '50%',
      background: '#00d4ff',
      boxShadow: '0 0 8px rgba(0,212,255,0.8)',
    },
    auroraWord: {
      display: 'flex',
      gap: '4px',
      perspective: '600px',
      marginBottom: '16px',
    },
    auroraLetter: {
      fontSize: 'clamp(72px, 14vw, 140px)',
      fontWeight: 900,
      lineHeight: 1,
      background: 'linear-gradient(135deg, #00d4ff 0%, #3b82f6 40%, #8b5cf6 80%, #00b4dc 100%)',
      WebkitBackgroundClip: 'text',
      WebkitTextFillColor: 'transparent',
      display: 'inline-block',
      textShadow: 'none',
      filter: 'drop-shadow(0 0 20px rgba(0,212,255,0.3))',
      letterSpacing: '-0.02em',
    },
    fullform: {
      fontSize: 'clamp(13px, 1.8vw, 17px)',
      letterSpacing: '0.22em',
      textTransform: 'uppercase' as const,
      color: 'rgba(148,201,232,0.7)',
      fontWeight: 500,
      marginBottom: '28px',
      marginTop: '4px',
    },
    divider: {
      width: '120px',
      height: '1px',
      background: 'linear-gradient(90deg, transparent, rgba(0,212,255,0.5), transparent)',
      transformOrigin: 'left',
      marginBottom: '28px',
    },
    tagline: {
      fontSize: 'clamp(14px, 2vw, 18px)',
      color: 'rgba(180,210,230,0.75)',
      lineHeight: 1.65,
      fontWeight: 400,
      marginBottom: '44px',
      maxWidth: '560px',
    },
    cta: {
      position: 'relative',
      background: 'linear-gradient(135deg, rgba(0,212,255,0.15), rgba(59,130,246,0.15), rgba(139,92,246,0.1))',
      border: '1px solid rgba(0,212,255,0.4)',
      borderRadius: '14px',
      padding: '16px 40px',
      color: '#ffffff',
      fontSize: '16px',
      fontWeight: 700,
      cursor: 'pointer',
      letterSpacing: '0.04em',
      display: 'inline-flex',
      alignItems: 'center',
      gap: '10px',
      backdropFilter: 'blur(12px)',
      marginBottom: '48px',
      transition: 'all 0.3s ease',
      outline: 'none',
      minWidth: '200px',
      justifyContent: 'center',
    },
    pills: {
      display: 'flex',
      flexWrap: 'wrap' as const,
      gap: '10px',
      justifyContent: 'center',
    },
    pill: {
      background: 'rgba(255,255,255,0.04)',
      border: '1px solid rgba(255,255,255,0.1)',
      borderRadius: '999px',
      padding: '6px 16px',
      fontSize: '12px',
      color: 'rgba(180,210,230,0.7)',
      fontWeight: 500,
      letterSpacing: '0.04em',
      backdropFilter: 'blur(8px)',
    },
    scrollHint: {
      position: 'absolute',
      bottom: '32px',
      left: '50%',
      transform: 'translateX(-50%)',
      zIndex: 10,
      display: 'flex',
      flexDirection: 'column' as const,
      alignItems: 'center',
    },
    scrollMouse: {
      width: '26px',
      height: '40px',
      border: '2px solid rgba(0,212,255,0.3)',
      borderRadius: '13px',
      display: 'flex',
      justifyContent: 'center',
      paddingTop: '6px',
    },
    scrollWheel: {
      width: '4px',
      height: '10px',
      borderRadius: '2px',
      background: 'rgba(0,212,255,0.6)',
      animation: 'scroll-wheel 1.6s ease-in-out infinite',
    },
  };

  const features = ['Code Analysis', 'Report Understanding', 'AI Scoring', 'Detailed Feedback'];

  return (
    <div style={s.root}>
      {/* Canvas aurora bg */}
      <canvas ref={canvasRef} style={s.canvas} />

      {/* Grid overlay */}
      <div style={s.grid} aria-hidden />

      {/* Floating particles */}
      <div style={s.particles} aria-hidden>
        {PARTICLES.map(p => (
          <span
            key={p.id}
            style={{
              position: 'absolute',
              left: `${p.x}%`,
              top: `${p.y}%`,
              width: p.size,
              height: p.size,
              borderRadius: '50%',
              background: p.color,
              boxShadow: `0 0 ${p.size * 2}px ${p.color}`,
              animation: `float-particle ${p.dur}s ease-in-out infinite`,
              animationDelay: `${p.delay}s`,
            }}
          />
        ))}
      </div>

      {/* ── Content ── */}
      <div style={s.content}>

        {/* Badge */}
        <motion.div
          style={s.badge}
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.3 }}
        >
          <span style={s.badgeDot} />
          AI-Powered Project Evaluation System
        </motion.div>

        {/* AURORA letters */}
        <motion.div
          style={s.auroraWord}
          variants={containerV}
          initial="hidden"
          animate="visible"
          aria-label="AURORA"
        >
          {'AURORA'.split('').map((ch, i) => (
            <motion.span key={i} style={s.auroraLetter} variants={letterV}>
              {ch}
            </motion.span>
          ))}
        </motion.div>

        {/* Full form */}
        <motion.p style={s.fullform} variants={subV} initial="hidden" animate="visible">
          Automated Universal Review And Objective Rating Analyzer
        </motion.p>

        {/* Divider */}
        <motion.div style={s.divider} variants={dividerV} initial="hidden" animate="visible" />

        {/* Tagline */}
        <motion.p style={s.tagline} variants={taglineV} initial="hidden" animate="visible">
          Evaluate student projects with intelligent code analysis,<br />
          report comprehension, and multi-dimensional scoring.
        </motion.p>

        {/* CTA button */}
        <motion.button
          style={s.cta}
          variants={btnV}
          initial="hidden"
          animate="visible"
          whileHover={{ scale: 1.05, y: -4, boxShadow: '0 0 40px rgba(0,212,255,0.35), 0 20px 40px rgba(0,0,0,0.4)' }}
          whileTap={{ scale: 0.97 }}
          onClick={() => navigate('/dashboard')}
        >
          Launch Dashboard
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            <path d="M5 12h14M12 5l7 7-7 7" />
          </svg>
        </motion.button>

        {/* Feature pills */}
        <motion.div
          style={s.pills}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 2.5, duration: 0.8 }}
        >
          {features.map(t => (
            <span key={t} style={s.pill}>{t}</span>
          ))}
        </motion.div>
      </div>

      {/* Scroll hint */}
      <motion.div
        style={s.scrollHint}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 3, duration: 1 }}
      >
        <span style={s.scrollMouse}>
          <span style={s.scrollWheel} />
        </span>
      </motion.div>
    </div>
  );
};
