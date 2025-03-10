# Open Command Prompt or PowerShell
cd c:\project

# Create project directory
mkdir tts_web_app
cd tts_web_app

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install required packages
pip install flask gtts

# Make sure you're in the tts_web_app directory with the virtual environment activated
python app.py

# In app.py, change the last line to:
app.run(debug=True, port=5001)