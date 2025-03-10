from flask import Flask, request, send_file, render_template
import sqlite3
from gtts import gTTS
import io

app = Flask(__name__)

# Function to initialize the database
def init_db():
    conn = sqlite3.connect('tts_database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS text_to_speech 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  user_input TEXT NOT NULL, 
                  audio_file BLOB NOT NULL, 
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

# Function to fetch all entries from the database
def get_all_entries():
    conn = sqlite3.connect('tts_database.db')
    c = conn.cursor()
    c.execute("SELECT id, user_input, created_at FROM text_to_speech")
    entries = c.fetchall()
    conn.close()
    return entries

# Route for the home page with form and list of entries
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['text']

        # Generate audio file using gTTS
        tts = gTTS(text=user_input, lang='en')
        audio_io = io.BytesIO()
        tts.write_to_fp(audio_io)
        audio_data = audio_io.getvalue()
        audio_io.close()

        # Store in SQLite
        conn = sqlite3.connect('tts_database.db')
        c = conn.cursor()
        c.execute("INSERT INTO text_to_speech (user_input, audio_file) VALUES (?, ?)", 
                  (user_input, audio_data))
        conn.commit()
        conn.close()

        # Serve the audio file back to the user
        return send_file(io.BytesIO(audio_data), mimetype='audio/mp3', as_attachment=True, download_name='output.mp3')

    # For GET request, render the template with entries
    entries = get_all_entries()
    return render_template('index.html', entries=entries)

# Route to retrieve an audio file by ID
@app.route('/audio/<int:id>')
def get_audio(id):
    conn = sqlite3.connect('tts_database.db')
    c = conn.cursor()
    c.execute("SELECT audio_file FROM text_to_speech WHERE id = ?", (id,))
    audio_data = c.fetchone()[0]
    conn.close()
    return send_file(io.BytesIO(audio_data), mimetype='audio/mp3')

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)