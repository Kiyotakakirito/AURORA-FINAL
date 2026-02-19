# AI-Based Automated Project Evaluation System

An intelligent system that analyzes student source code (ZIP/GitHub) and project reports (PDF) to generate automated scoring and feedback.

## Features

- **Multi-format Support**: Process ZIP files, GitHub repositories, and PDF reports
- **AI-Powered Analysis**: Uses advanced AI models for code quality assessment
- **Automated Scoring**: Configurable evaluation criteria and rubrics
- **Detailed Feedback**: Comprehensive feedback on code quality, structure, and documentation
- **Web Interface**: Modern React-based UI for submissions and results
- **Database Storage**: Persistent storage of evaluations and feedback history

## Architecture

```
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Configuration
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic
│   │   └── utils/          # Utilities
│   ├── requirements.txt
│   └── main.py
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│   ├── package.json
│   └── public/
├── evaluation_engine/      # Core evaluation logic
│   ├── code_analyzer.py
│   ├── pdf_processor.py
│   ├── scoring_engine.py
│   └── feedback_generator.py
├── tests/                  # Test suite
└── docs/                   # Documentation
```

## Technology Stack

- **Backend**: Python 3.9+, FastAPI, SQLAlchemy
- **Frontend**: React 18, TypeScript, Tailwind CSS, shadcn/ui
- **AI Integration**: OpenAI GPT-4, Anthropic Claude
- **Database**: SQLite (development), PostgreSQL (production)
- **File Processing**: PyPDF2, GitPython, zipfile
- **Deployment**: Docker, Docker Compose

## Getting Started

### Prerequisites
- Python 3.9+
- Node.js 16+
- Git

### Installation

1. Clone the repository
2. Set up backend:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
3. Set up frontend:
   ```bash
   cd frontend
   npm install
   ```
4. Run the application:
   ```bash
   # Backend
   cd backend && python main.py
   
   # Frontend
   cd frontend && npm start
   ```

## Usage

1. Submit project files (ZIP, GitHub URL, or PDF report)
2. Configure evaluation criteria
3. Receive automated scoring and detailed feedback
4. View evaluation history and analytics

## Configuration

Edit `backend/app/core/config.py` to configure:
- AI API keys
- Database settings
- Scoring rubrics
- File upload limits

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License
