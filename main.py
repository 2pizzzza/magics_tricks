import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

# API-Key aus der .env Datei laden
client = genai.Client(api_key=os.getenv("GEMINI_API"))

def read_instruction(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Du bist ein hilfreicher Assistent."

def run_magical_gemini():
    # WICHTIG: Nutze chats.create für eine fortlaufende Konversation
    chat = client.chats.create(
        model="gemini-2.5-flash",  # Nutze 1.5-flash für bessere Stabilität
        config={
            "system_instruction": read_instruction("./system_instruction.txt"),
            "temperature": 0.8
        }
    )

    name = input("Name: ")
    sternzeichen = input("Sternzeichen: ")
    geburtstag = input("Geburtstag: ")

    # Erster Prompt, um die Befragung zu starten
    prompt = f"Ich bin {name}, {sternzeichen}, geboren am {geburtstag}. Starte die Befragung."

    for i in range(6):
        # Hier nutzt du jetzt das korrekte Chat-Objekt
        response = chat.send_message(prompt)
        print(f"\nAI: {response.text}")

        user_answer = input("Deine Antwort: ")
        prompt = user_answer

    # Abschluss der Befragung
    final_response = chat.send_message("Generiere nun das finale Ergebnis basierend auf meinen Antworten.")
    print("\n" + "=" * 50)
    print(final_response.text)
    print("=" * 50)

if __name__ == "__main__":
    run_magical_gemini()

