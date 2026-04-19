import asyncio
import edge_tts

async def main():
    tts = edge_tts.Communicate(
        text='''Marco ist neu in der Stadt. Er hat gestern einen Brief an seine Eltern geschrieben, heute möchte er ihn zur Post bringen. Aber wo ist die Post? Marco hat die Adresse im Internet nicht gefunden. Er muss jemanden fragen. An der Bushaltestelle steht ein alter Mann.
„Entschuldigung, wo ist bitte die Post?“, fragt Marco höflich.
„In der Goethestraße“, antwortet der alte Mann.
„Muss ich mit dem Bus fahren oder kann ich zu Fuß gehen?“, fragt Marco.
„Dieser Bus hält direkt vor der Post. Sie müssen bei der dritten Station aussteigen“, sagt der alte Mann.
„Ich möchte lieber zu Fuß gehen. Wie komme ich zur Goethestraße?“, fragt Marco.
„Sie gehen diese Straße geradeaus und biegen an der ersten Kreuzung rechts ab. Nach ungefähr 500 Metern kommen Sie an eine Ampel. Dort überqueren Sie die Straße und biegen nach links in die Schillerstraße ein. An der nächsten Kreuzung gehen Sie nach rechts in die Goethestraße. Dort ist die Post.“
„Vielen Dank!“, sagt Marco und geht los.''',
        voice="de-DE-ConradNeural"
    )
    await tts.save("output.mp3")

asyncio.run(main())

from piper.voice import PiperVoice

voice = PiperVoice.load("de_DE-thorsten_emotional-medium.onnx")

text = "Hallo Welt, das ist ein Test."

with open("output.wav", "wb") as f:
    for chunk in voice.synthesize(text):
        f.write(chunk.audio_bytes)


# import asyncio
# import edge_tts
# import re
# import tempfile
# import os
#
# VOICE = "de-DE-ConradNeural"
#
# text = """Marco ist neu in der Stadt. Er hat gestern einen Brief geschrieben. Heute geht er zur Post."""
#
# def split_sentences(text):
#     return re.split(r'(?<=[.!?])\s+', text)
#
# async def speak(sentence):
#     communicate = edge_tts.Communicate(sentence, VOICE)
#
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
#         path = f.name
#
#     await communicate.save(path)
#     playsound(pddath)
#     os.remove(path)
#
# async def main():
#     for sentence in split_sentences(text):
#         await speak(sentence)
#
# asyncio.run(main())
