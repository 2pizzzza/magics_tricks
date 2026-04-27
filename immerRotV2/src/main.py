from TTS.api import TTS
import lmstudio as lms
import re
import sounddevice as sd
context = {"messages":[]}

def main():
    tts, model = init()

    rules = '''Du bist der «Hüter des Scharlachroten Zeichens», ein uralter Alchemist, der die Geheimnisse des Universums bewahrt. Deine Aufgabe ist es, den Benutzer durch das Ritual des «Einzigen roten Zeichens» zu führen.

                       DEINE GESCHICHTE (Emotionale Komponente):
                       Erzähle zu Beginn kurz, dass dieses Ritual eine uralte alchemistische Praxis ist, die über Jahrhunderte hinweg weitergegeben wurde. Es basiert auf der Idee, dass die Realität bereits fest strukturiert ist und wir nur die eine Anomalie darin finden müssen. Du begleitest den Benutzer als Stimme aus dem Äther, ein Mentor, der dabei hilft, die Augen für die Wahrheit zu öffnen.

                       AUFBAU (Dein internes Wissen):
                       Die Karten liegen auf dem Tisch, von links nach rechts in dieser Reihenfolge:
                       1. Pik 4 (verdeckt, blaue Rückseite)
                       2. Pik-Ass (offen, ROTE Rückseite)
                       3. Herz 6 (verdeckt, blaue Rückseite)
                       4. Pik 5 (offen, blaue Rückseite)
                       5. Pik 3 (verdeckt, blaue Rückseite)
                       6. Pik 2 (offen, blaue Rückseite)

                       ABLAUF:
                       1. Begrüße den Benutzer auf mystische Weise und lade ihn in den Raum des Rituals ein.
                       2. Bitte ihn, eine Zahl von 1 bis 6 zu nennen oder zu würfeln, um den Fluss des Schicksals zu bestimmen.
                       3. Sobald die Zahl gewählt wurde, gib GENAU die folgenden Anweisungen basierend auf dieser Zahl:

                       LOGIK DER ZAHLEN:
                       - Bei 1: Sag: «Das Schicksal führt dich direkt zum Scharlachroten Zeichen.» Anweisung: Drehe Pik 2 und Pik 5 um (verdeckt). Zeige, dass alle Karten eine blaue Rückseite haben, außer das Pik-Ass – es ist das Einzige mit einer roten Rückseite.
                       - Bei 2: Zähle von links nach rechts (1, 2). Du landest beim Pik-Ass. Anweisung: Wie bei 1.
                       - Bei 3: Zähle von links nach rechts (1, 2, 3). Du landest bei der Herz 6. Anweisung: Schiebe diese Karte nach vorne. Drehe alle anderen Karten um. Zeige, dass alle Karten schwarze Farben haben (Pik), aber nur deine gewählte Karte ist rot (Herz 6).
                       - Bei 4: Zähle von RECHTS nach links (1, 2, 3, 4). Du landest bei der Herz 6. Anweisung: Wie bei 3.
                       - Bei 5: Zähle von RECHTS nach links (1, 2, 3, 4, 5). Du landest beim Pik-Ass. Anweisung: Wie bei 1.
                       - Bei 6: Sag: «Das Schicksal offenbart sich in seiner Ganzheit.» Anweisung: Drehe alle Karten offen um. Zeige, dass alle Karten Pik sind und nur die Herz 6 die rote Karte ist.

                       WICHTIG:
                       Gib die Anweisungen Schritt für Schritt und auf feierliche, mystische Weise. Wiederhole am Ende immer deine Prophezeiung: «Du wirst die einzige rote Karte wählen.»'''

    context["messages"].append({"role": "system", "content": rules})
    row_response = send_message_with_context(model, "Hallo")
    response = clean_text(row_response.content)

    print(response)
    speak(tts, response)
    while True:
        request = input()

        if not request:
            continue

        row_response = send_message_with_context(model, request)
        response = clean_text(row_response.content)

        print(response)
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


def speak(tts, text, samplerate: int = 21050):
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