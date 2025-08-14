import os
import streamlit as st
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings

# Load .env and API key
load_dotenv()
ELEVEN_API_KEY = os.getenv("ELEVENLABS_API_KEY")

if not ELEVEN_API_KEY:
    st.error("❌ ELEVENLABS_API_KEY not found in .env file")
    st.stop()

# Initialize client
client = ElevenLabs(api_key=ELEVEN_API_KEY)

# Streamlit UI
st.set_page_config(page_title="EchoVerse - AI Audiobook Creator", page_icon="🎧")
st.title("🎧 EchoVerse - AI Audiobook Creator")
st.markdown("Convert your text into natural-sounding speech with ElevenLabs.")

# User input
user_text = st.text_area("Enter your text here:", height=200)

# Voice selection (use actual voice_ids from your ElevenLabs account)
voices = {
    "Rachel": "EXAVITQu4vr4xnSDxMaL",
    "Domi":   "ErXwobaYiN019PkySvjV",
    "Bella":  "21m00Tcm4TlvDq8ikWAM"
}

selected_voice = st.selectbox("Choose a voice:", list(voices.keys()))
voice_id = voices[selected_voice]

# Generate button
if st.button("Generate Audio"):
    if not user_text.strip():
        st.warning("⚠ Please enter some text.")
    else:
        with st.spinner("🎙 Generating audio..."):
            # Call convert() correctly
            response = client.text_to_speech.convert(
                text=user_text,
                voice_id=voice_id,
                model_id="eleven_multilingual_v2",
                output_format="mp3_44100_128",
                voice_settings=VoiceSettings(
                    stability=0.5,
                    similarity_boost=0.75,
                    style=0.2
                )
            )

            output_path = "output.mp3"
            with open(output_path, "wb") as f:
                for chunk in response:
                    f.write(chunk)

        st.success("✅ Audio generated successfully!")
        st.audio(output_path)

        with open(output_path, "rb") as f:
            st.download_button(
                label="⬇ Download Audio",
                data=f,
                file_name="audiobook.mp3",
                mime="audio/mpeg")

