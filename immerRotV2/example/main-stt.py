from vosk import Model, KaldiRecognizer
import queue
import sounddevice as sd
import json
import webrtcvad

model = "vosk-model-de-0.21"
SAMPLE_RATE = 16000
FRAME_DURATION = 30
FRAME_SIZE = int(SAMPLE_RATE * FRAME_DURATION / 1000) * 2

MAX_SILENCE_FRAMES = 10

q = queue.Queue()

def callback(indata, frames, time, status):
    q.put(bytes(indata))


vad = webrtcvad.Vad(2)
vad.set_mode(3)
model = Model(model)
rec = KaldiRecognizer(model, SAMPLE_RATE)

print("SAY.....")

speech_buffer = []
silence_counter = 0
recording = False

with sd.RawInputStream(
    samplerate=SAMPLE_RATE,
    blocksize=FRAME_SIZE // 2,
    dtype='int16',
    channels=1,
    callback=callback
):
    while True:
        data = q.get()

        for i in range(0, len(data), FRAME_SIZE):
            frame = data[i:i+FRAME_SIZE]
            if len(frame) < FRAME_SIZE:
                continue
            
            is_speech = vad.is_speech(frame, SAMPLE_RATE)

            if is_speech:
                recording = True
                silence_counter = 0
                speech_buffer.append(frame)

            elif recording:
                speech_buffer.append(frame)
                silence_counter += 1

                if silence_counter > MAX_SILENCE_FRAMES:
                    print("end")

                    full_text = ""
                    rec.Reset()

                    for chunk in speech_buffer:
                        if rec.AcceptWaveform(chunk):
                            res = json.loads(rec.Result())
                            if res["text"]:
                                full_text += " " + res["text"]

                    final_res = json.loads(rec.FinalResult())
                    full_text += " " + final_res.get("text", "")

                    print("result ", full_text.strip())
                    speech_buffer = []
                    silence_counter = 0
                    recording = False

                    print("\nsay again")
