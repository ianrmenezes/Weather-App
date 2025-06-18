#!/usr/bin/env python3
"""
Setup script for Weather App
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
    except subprocess.CalledProcessError:
        print("❌ Error installing packages. Please try manually: pip install -r requirements.txt")
        return False
    return True

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = ".env"
    if not os.path.exists(env_file):
        print("🔧 Creating .env file...")
        with open(env_file, "w") as f:
            f.write("# OpenWeather API Key\n")
            f.write("# Get your free API key from: https://openweathermap.org/api\n")
            f.write("OPENWEATHER_API_KEY=your_api_key_here\n")
        print("✅ .env file created!")
        print("⚠️  Please edit .env file and add your OpenWeather API key")
    else:
        print("✅ .env file already exists")

def main():
    print("🌤️ Weather App Setup")
    print("=" * 30)
    
    # Install requirements
    if not install_requirements():
        return
    
    # Create .env file
    create_env_file()
    
    print("\n🎉 Setup complete!")
    print("\nNext steps:")
    print("1. Get your free API key from: https://openweathermap.org/api")
    print("2. Edit the .env file and replace 'your_api_key_here' with your actual API key")
    print("3. Run the app: streamlit run app.py")
    print("4. Open your browser to http://localhost:8501")

if __name__ == "__main__":
    main() 