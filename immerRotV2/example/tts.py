from TTS.api import TTS
import sounddevice as sd
import lmstudio as lms
import re

tts = TTS(model_name="tts_models/de/thorsten/tacotron2-DDC")

model = lms.llm("google/gemma-4-e4b")
result = model.respond("Wer bist du?")


def clean_text(text):
    text = re.sub(r'<\|channel>.*?<channel\|>', '', text, flags=re.DOTALL)
    
    text = re.sub(r'[\*\#\_\`\~\>]+', '', text)
    
    text = re.sub(r'\n+', ' ', text)
    
    return text.strip()

res = clean_text(result.content)

print(res)


while True:
    text = res

    if not text:
        continue

    wav = tts.tts(text)
    sd.play(wav, samplerate=22050)
    sd.wait()
