import streamlit as st
import subprocess
import os
import whisper
from googletrans import Translator
from gtts import gTTS
from IPython.display import Audio

# Configuration de l'interface
st.set_page_config(page_title="Transcription & Traduction YouTube", layout="centered")

st.title("🎥 Transcription et Traduction de Vidéo YouTube")
st.markdown("🚀 Entrez une URL de vidéo YouTube, et obtenez la transcription en français et la traduction en anglais.")

# Entrée de l'URL YouTube
url = st.text_input("Entrez l'URL de la vidéo YouTube :", "")

if url:
    # Affichage de la vidéo YouTube dans l'interface
    video_id = url.split("v=")[-1]
    st.video(url)

    # Téléchargement de l'audio avec yt-dlp
    st.subheader("🔄 Téléchargement et extraction audio...")
    audio_file = "audio.mp3"
    command = f'yt-dlp -x --audio-format mp3 -o "{audio_file}" "{url}"'
    subprocess.run(command, shell=True)

    if os.path.exists(audio_file):
        st.success("✅ Audio extrait avec succès !")

        # Chargement du modèle Whisper
        model = whisper.load_model("base")  # Peut être "small", "medium", "large"

        # Transcription en français
        st.subheader("📝 Transcription en Français")
        result = model.transcribe(audio_file, language="fr")
        french_text = result["text"]
        st.text_area("Texte en français :", french_text, height=150)

        # Traduction en anglais avec Whisper
        st.subheader("🌍 Traduction en Anglais")
        translated_result = model.transcribe(audio_file, task="translate")
        english_text = translated_result["text"]
        st.text_area("Texte en anglais :", english_text, height=150)

        # Lecture de la traduction avec gTTS
        st.subheader("🔊 Lecture audio de la traduction")
        tts = gTTS(english_text, lang="en")
        tts.save("translation.mp3")
        st.audio("translation.mp3", format="audio/mp3")
    else:
        st.error("❌ Impossible de télécharger l'audio. Vérifiez l'URL.")

