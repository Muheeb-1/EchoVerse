# test_audio.py
from services.rewrite import rewrite_text
from services.tts import text_to_speech
from io import BytesIO

if __name__ == "__main__":
    sample = "Hello students! Today we will learn about AI and audiobooks. This is a short test."
    tone = "Inspiring"

    print("Requesting rewrite...")
    rewritten = rewrite_text(sample, tone)
    print("Rewritten text:", rewritten)

    if rewritten and not rewritten.lower().startswith("error:"):
        print("Generating audio...")
        try:
            audio_buffer = text_to_speech(rewritten)
            if isinstance(audio_buffer, BytesIO):
                with open("test_echoverse.mp3", "wb") as f:
                    f.write(audio_buffer.getvalue())
                print("Audio file created at: test_echoverse.mp3")
            else:
                print("Unexpected return type from text_to_speech:", type(audio_buffer))
        except Exception as e:
            print("Error generating audio:", e)
    else:
        print("Skipping TTS because rewrite returned an error.")
