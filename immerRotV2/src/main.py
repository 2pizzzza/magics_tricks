from TTS.api import TTS
import sounddevice as sd
import lmstudio as lms
import re

context = {"messages":[]}

def main():
    tts, model = init()
    context["messages"].append({"role": "system", "content": "Du bist ein klunge Assistent"})

    while True:
        request = input()

        if not request:
            continue

        row_response = send_message_with_context(model, request)
        response = clean_text(row_response.content)

        speak(tts,response)


def init():
    tts = TTS(model_name="tts_models/de/thorsten/tacotron2-DDC")
    model = lms.llm("google/gemma-4-e4b")

    return tts, model

def send_message(model, text):
    row_response = model.respond(text)
    return row_response

def send_message_with_context(model, text):
    context["messages"].append({"role": "user", "content": text})
    row_response = model.respond(context)
    context["messages"].append({"role":"assistant", "content":row_response})

    return row_response

def speak(tts, text, samplerate: int = 22050):
    wav = tts.tts(text)
    sd.play(wav, samplerate=samplerate)
    sd.wait()

def clean_text(text):
    text = re.sub(r'<\|channel>.*?<channel\|>', '', text, flags=re.DOTALL)
    text = re.sub(r'[\*\#\_\`\~\>]+', '', text)
    text = re.sub(r'\n+', ' ', text)

    return text.strip()

if __name__ == '__main__':
    main()