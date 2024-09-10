from flask import Flask, request, jsonify
import speech_recognition as sr
from pydub import AudioSegment
AudioSegment.converter = r"C:\Users\caiot\Documents\Código\TCC\bin\ffmpeg"
import os

app = Flask(__name__)

def convert_audio_to_text(audio_path):
    """Converte o arquivo de áudio para texto."""
    recognizer = sr.Recognizer()

    # Converter para WAV se o arquivo não estiver em formato WAV
    if not audio_path.endswith('.wav'):
        audio = AudioSegment.from_file(audio_path)
        wav_path = audio_path.rsplit('.', 1)[0] + '.wav'
        audio.export(wav_path, format='wav')
    else:
        wav_path = audio_path

    # Carregar o áudio convertido
    with sr.AudioFile(wav_path) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio, language='pt-BR')
        except sr.UnknownValueError:
            text = "Não foi possível reconhecer o áudio."
        except sr.RequestError:
            text = "Erro na requisição ao serviço de reconhecimento de fala."

    # Remover o arquivo WAV temporário
    if wav_path != audio_path:
        os.remove(wav_path)

    return text

@app.route('/convert', methods=['POST'])
def convert_audio():
    if 'file' not in request.files:
        return jsonify({"error": "Arquivo de áudio não encontrado."}), 400

    file = request.files['file']
    audio_path = os.path.join('temp', file.filename)
    file.save(audio_path)

    text = convert_audio_to_text(audio_path)
    
    # Limpa o arquivo temporário original
    os.remove(audio_path)

    return jsonify({"text": text})

if __name__ == '__main__':
    app.run(debug=True)
