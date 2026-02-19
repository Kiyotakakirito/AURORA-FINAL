#!/usr/bin/env python3
"""
Setup script for Ollama AI models
This script helps install and configure Ollama for the AI Project Evaluation System
"""

import subprocess
import sys
import asyncio
import httpx
import json

async def check_ollama_installation():
    """Check if Ollama is installed and running"""
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get("http://localhost:11434/api/tags")
            return response.status_code == 200
    except Exception:
        return False

async def list_available_models():
    """List available Ollama models"""
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get("http://localhost:11434/api/tags")
            if response.status_code == 200:
                data = response.json()
                return [model["name"] for model in data.get("models", [])]
    except Exception:
        pass
    return []

async def pull_model(model_name):
    """Pull a model from Ollama"""
    print(f"Pulling {model_name} model... This may take a few minutes.")
    
    try:
        async with httpx.AsyncClient(timeout=600) as client:  # 10 minutes timeout
            response = await client.post(
                "http://localhost:11434/api/pull",
                json={"name": model_name}
            )
            
            if response.status_code == 200:
                print(f"✅ Successfully pulled {model_name}")
                return True
            else:
                print(f"❌ Failed to pull {model_name}")
                return False
    except Exception as e:
        print(f"❌ Error pulling {model_name}: {e}")
        return False

def print_installation_instructions():
    """Print Ollama installation instructions"""
    print("=" * 60)
    print("OLLAMA SETUP INSTRUCTIONS")
    print("=" * 60)
    print("\n1. Install Ollama:")
    print("   Visit: https://ollama.ai/")
    print("   Download and install Ollama for your operating system")
    print("\n2. Start Ollama:")
    print("   - Windows: Run Ollama from Start Menu")
    print("   - macOS: Run 'ollama serve' in terminal")
    print("   - Linux: Run 'ollama serve' in terminal")
    print("\n3. Verify installation:")
    print("   Run this script again after installation")
    print("\n4. Recommended models for evaluation:")
    print("   - llama3.1 (8B): Good balance of speed and quality")
    print("   - llama3.1 (70B): Higher quality, slower")
    print("   - codellama: Specialized for code analysis")
    print("\n5. Pull a model:")
    print("   ollama pull llama3.1")
    print("=" * 60)

async def main():
    """Main setup function"""
    print("🔍 Checking Ollama installation...")
    
    # Check if Ollama is running
    if not await check_ollama_installation():
        print("❌ Ollama is not installed or not running")
        print_installation_instructions()
        return
    
    print("✅ Ollama is running!")
    
    # List available models
    models = await list_available_models()
    if models:
        print(f"\n📦 Available models: {', '.join(models)}")
    else:
        print("\n📦 No models found")
    
    # Recommended models
    recommended_models = ["llama3.1", "codellama"]
    
    print(f"\n🎯 Recommended models: {', '.join(recommended_models)}")
    
    # Ask user if they want to pull a model
    if not models:
        print("\nNo models found. You need at least one model for evaluation.")
        choice = input("Would you like to pull llama3.1? (y/n): ").lower().strip()
        
        if choice in ['y', 'yes']:
            success = await pull_model("llama3.1")
            if success:
                print("\n🎉 Setup complete! Your AI evaluation system is ready.")
            else:
                print("\n❌ Setup failed. Please check your internet connection and try again.")
        else:
            print("\nTo pull a model manually, run:")
            print("ollama pull llama3.1")
    else:
        print("\n🎉 Your AI evaluation system is ready!")
    
    # Test the backend connection
    print("\n🔗 Testing backend connection...")
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get("http://localhost:8000/api/v1/ai/status")
            if response.status_code == 200:
                data = response.json()
                print("✅ Backend AI service is configured!")
                print(f"   Using Ollama: {data.get('use_ollama', False)}")
                print(f"   Current model: {data.get('ollama', {}).get('current_model', 'N/A')}")
            else:
                print("⚠️  Backend may not be running. Start it with:")
                print("   cd backend && python main.py")
    except Exception:
        print("⚠️  Backend may not be running. Start it with:")
        print("   cd backend && python main.py")

if __name__ == "__main__":
    print("🚀 Ollama Setup for AI Project Evaluation System")
    print("=" * 50)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Setup cancelled by user")
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        sys.exit(1)
