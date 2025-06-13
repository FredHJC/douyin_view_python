#!/bin/bash
# Douyin View Tracker - Quick Start Script

echo "🎵 Douyin View Tracker - Starting Application"
echo "=" * 50

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo "📝 Creating .env file from template..."
    
    if [ -f "env.example" ]; then
        cp env.example .env
        echo "✅ Created .env file from env.example"
        echo "🔧 Please edit .env and add your TikHub API key:"
        echo "   nano .env"
        echo ""
        echo "🔑 Get your API key from: https://api.tikhub.io/"
        exit 1
    else
        echo "❌ env.example not found!"
        exit 1
    fi
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "📚 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "🚀 Starting Flask application..."
echo "📱 Open your browser and go to: http://localhost:5000"
echo "⏹️  Press Ctrl+C to stop the server"
echo ""

# Run the application
python app.py 