<div align="center">

# ✦ A U R O R A ✦

### AI-Based Automated Project Evaluation System

*Using Code Understanding & Report Analysis*

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.x-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-F7DF1E?style=for-the-badge)](LICENSE)

<br/>

> **AURORA** is an intelligent, end-to-end evaluation platform that analyses student source code *(ZIP / GitHub)* and project reports *(PDF)* — delivering rich, automated scoring and actionable feedback powered by state-of-the-art AI.

<br/>

---

</div>

## 🌟 Why AURORA?

Grading student projects manually is slow, inconsistent, and resource-intensive. AURORA solves this by combining **static code analysis**, **AI-driven understanding**, and **natural language report comprehension** into a single, seamless pipeline — giving educators instant, objective, and detailed evaluations.

---

## ✨ Feature Highlights

| Capability | Details |
|---|---|
| 📦 **Multi-format Ingestion** | ZIP archives, GitHub repository URLs, PDF reports |
| 🤖 **AI-Powered Analysis** | GPT-4 & Claude for deep code & report understanding |
| 📊 **Automated Scoring** | Configurable rubrics with per-criterion breakdown |
| 💬 **Rich Feedback** | Inline comments, quality metrics & improvement tips |
| 🖥️ **Modern Web UI** | React 18 + TypeScript + Tailwind CSS + shadcn/ui |
| 🗃️ **Persistent History** | Full evaluation logs stored in SQLite / PostgreSQL |
| 🐳 **Docker Ready** | One-command deployment with Docker Compose |
| 🔒 **Supabase Auth & RLS** | Row-level security for multi-tenant environments |

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                        AURORA                           │
│                                                         │
│   ┌──────────────┐       ┌──────────────────────────┐   │
│   │   React UI   │──────▶│   FastAPI  Backend       │   │
│   │  (TypeScript)│◀──────│   REST  /  WebSocket     │   │
│   └──────────────┘       └────────────┬─────────────┘   │
│                                       │                 │
│              ┌────────────────────────┼──────────────┐  │
│              │      Evaluation Engine               │  │
│              │  ┌──────────────┐  ┌───────────────┐ │  │
│              │  │ Code Analyzer│  │ PDF Processor │ │  │
│              │  └──────┬───────┘  └──────┬────────┘ │  │
│              │         │                 │          │  │
│              │  ┌──────▼─────────────────▼──────┐  │  │
│              │  │      Scoring  Engine (AI)      │  │  │
│              │  └───────────────┬────────────────┘  │  │
│              │                  │                   │  │
│              │  ┌───────────────▼────────────────┐  │  │
│              │  │     Feedback  Generator         │  │  │
│              │  └────────────────────────────────┘  │  │
│              └──────────────────────────────────────┘  │
│                                                         │
│   ┌──────────────────────────────────────────────────┐  │
│   │               Database  (SQLite / PostgreSQL)    │  │
│   └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## 🗂️ Project Structure

```
AURORA/
│
├── 📂 backend/                   # FastAPI backend service
│   ├── app/
│   │   ├── api/                  # REST endpoints
│   │   ├── core/                 # Config & Supabase client
│   │   ├── models/               # SQLAlchemy ORM models
│   │   ├── services/             # Business logic layer
│   │   └── utils/                # Helper utilities
│   ├── migrations/               # Alembic database migrations
│   ├── requirements.txt
│   ├── Dockerfile
│   └── main.py
│
├── 📂 frontend/                  # React + TypeScript UI
│   ├── src/
│   │   ├── components/           # Reusable UI components
│   │   ├── pages/                # Route-level pages
│   │   │   ├── LandingPage.tsx
│   │   │   ├── Dashboard.tsx
│   │   │   ├── EvaluationDetail.tsx
│   │   │   └── EvaluationHistory.tsx
│   │   ├── lib/                  # API client & state store
│   │   └── index.css
│   ├── package.json
│   └── Dockerfile
│
├── 📂 evaluation_engine/         # Core AI evaluation logic
│   ├── code_analyzer.py          # Static + AI code analysis
│   ├── pdf_processor.py          # PDF extraction & parsing
│   ├── scoring_engine.py         # Rubric-based scoring
│   └── feedback_generator.py    # Natural language feedback
│
├── 📂 tests/                     # Test suite
├── 📄 docker-compose.yml
├── 📄 Makefile
└── 📄 README.md
```

---

## 🛠️ Technology Stack

<div align="center">

| Layer | Technology |
|---|---|
| **Backend** | Python 3.9+, FastAPI, SQLAlchemy, Alembic |
| **Frontend** | React 18, TypeScript, Tailwind CSS, shadcn/ui, Zustand |
| **AI Models** | OpenAI GPT-4, Anthropic Claude |
| **Database** | SQLite *(dev)* · PostgreSQL / Supabase *(prod)* |
| **File Parsing** | PyPDF2, GitPython, zipfile |
| **Auth & Security** | Supabase Auth, Row-Level Security |
| **Containerisation** | Docker, Docker Compose |
| **Testing** | Pytest |

</div>

---

## 🚀 Getting Started

### Prerequisites

- **Python** 3.9+
- **Node.js** 16+
- **Git**
- **Docker** *(optional, for containerised setup)*

---

### ⚡ Quick Start (Docker — Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/Kiyotakakirito/AURORA-FINAL.git
cd AURORA-FINAL

# 2. Copy environment variables
cp backend/.env.example backend/.env
#    → Fill in your API keys and database URL

# 3. Launch everything
docker-compose up --build
```

🌐 Open **http://localhost:3000** in your browser.

---

### 🔧 Manual Setup

**Backend**

```bash
cd backend
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Initialise the database
python setup_db.py

# Start the API server
uvicorn app.main:app --reload --port 8000
```

**Frontend**

```bash
cd frontend
npm install
npm start
```

🌐 Frontend → **http://localhost:3000** · API Docs → **http://localhost:8000/docs**

---

## ⚙️ Configuration

Edit `backend/.env` (copy from `.env.example`):

```env
# AI API Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Database
DATABASE_URL=sqlite:///./aurora.db       # or postgresql://...

# Supabase (optional)
SUPABASE_URL=https://xxxx.supabase.co
SUPABASE_KEY=your-anon-key

# Uploads
MAX_UPLOAD_SIZE_MB=50
```

Edit `backend/app/core/config.py` to customise:
- 🎯 Scoring rubrics & weightings
- 📁 Allowed file types
- 🔑 Auth settings

---

## 📋 How It Works

```
 Student Submits                 AURORA Processes              Results Delivered
 ─────────────                  ─────────────────             ─────────────────
 📁 ZIP File   ─┐               ┌─ Code Analysis ─┐           ┌─ Score Report
 🔗 GitHub URL ──▶  Ingestion  ──▶─ PDF Parsing   ──▶  AI  ──▶─ Criterion Breakdown
 📄 PDF Report ─┘               └─ Rubric Scoring ─┘           └─ Detailed Feedback
```

1. **Submit** your project (ZIP, GitHub URL, or PDF)
2. **Configure** evaluation criteria and scoring weights
3. **AURORA analyses** code structure, quality, documentation & report
4. **Receive** an instant, detailed score report with actionable feedback
5. **Track** all evaluations in the history dashboard

---

## 🧪 Running Tests

```bash
# From project root
pytest

# With coverage
pytest --cov=backend/app tests/
```

---

## 🤝 Contributing

Contributions are what make open source amazing. Here's how to get involved:

1. **Fork** the repository
2. **Create** a feature branch → `git checkout -b feature/amazing-feature`
3. **Commit** your changes → `git commit -m 'feat: add amazing feature'`
4. **Push** → `git push origin feature/amazing-feature`
5. Open a **Pull Request** 🎉

Please make sure your code passes `pytest` and follows existing conventions.

---

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for more information.

---

<div align="center">

Made with ❤️ for smarter, fairer education

⭐ **Star this repo if AURORA helps you!** ⭐

[![GitHub stars](https://img.shields.io/github/stars/Kiyotakakirito/AURORA-FINAL?style=social)](https://github.com/Kiyotakakirito/AURORA-FINAL/stargazers)

</div>
