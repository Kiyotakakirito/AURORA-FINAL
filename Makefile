.PHONY: help install test run-backend run-frontend build clean docker-build docker-up docker-down

# Default target
help:
	@echo "Available commands:"
	@echo "  install      - Install dependencies for backend and frontend"
	@echo "  test         - Run all tests"
	@echo "  run-backend  - Start backend development server"
	@echo "  run-frontend - Start frontend development server"
	@echo "  build        - Build frontend for production"
	@echo "  clean        - Clean build artifacts"
	@echo "  docker-build  - Build Docker images"
	@echo "  docker-up    - Start services with Docker Compose"
	@echo "  docker-down  - Stop Docker Compose services"

# Install dependencies
install:
	@echo "Installing backend dependencies..."
	cd backend && pip install -r requirements.txt
	@echo "Installing frontend dependencies..."
	cd frontend && npm install

# Run tests
test:
	@echo "Running tests..."
	pytest tests/ -v

# Run backend development server
run-backend:
	@echo "Starting backend server..."
	cd backend && python main.py

# Run frontend development server
run-frontend:
	@echo "Starting frontend server..."
	cd frontend && npm start

# Build frontend for production
build:
	@echo "Building frontend..."
	cd frontend && npm run build

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	rm -rf frontend/build
	rm -rf frontend/node_modules
	rm -rf backend/__pycache__
	rm -rf backend/app/__pycache__
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Docker commands
docker-build:
	@echo "Building Docker images..."
	docker-compose build

docker-up:
	@echo "Starting Docker services..."
	docker-compose up -d

docker-down:
	@echo "Stopping Docker services..."
	docker-compose down

# Development setup
dev-setup: install
	@echo "Setting up development environment..."
	cp backend/.env.example backend/.env
	@echo "Please edit backend/.env with your configuration"
	@echo "Development setup complete!"

# Production deployment
deploy: build docker-build
	@echo "Ready for deployment!"
	@echo "Run 'docker-compose up -d' to start production services"
