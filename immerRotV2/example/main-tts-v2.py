# from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq
#
# processor = AutoProcessor.from_pretrained("primeline/whisper-large-v3-turbo-german")
# model = AutoModelForSpeechSeq2Seq.from_pretrained("primeline/whisper-large-v3-turbo-german")

# import torch
# from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
#
# model_id = "primeline/whisper-large-v3-turbo-german"
#
# device = "cuda:0" if torch.cuda.is_available() else "cpu"
# torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
#
# model = AutoModelForSpeechSeq2Seq.from_pretrained(
#     model_id,
#     torch_dtype=torch_dtype,
#     low_cpu_mem_usage=True,
#     use_safetensors=True
# ).to(device)
#
# processor = AutoProcessor.from_pretrained(model_id)
#
# pipe = pipeline(
#     "automatic-speech-recognition",
#     model=model,
#     tokenizer=processor.tokenizer,
#     feature_extractor=processor.feature_extractor,
#     chunk_length_s=30,
#     batch_size=16,
#     return_timestamps=True,
#     torch_dtype=torch_dtype,
#     device=0 if torch.cuda.is_available() else -1
# )
#
# result = pipe("audio.wav")
# print(result["text"])

import torch
import soundfile as sf
from chatterbox.tts import ChatterboxTTS
from huggingface_hub import hf_hub_download
from safetensors.torch import load_file

MODEL_REPO = "SebastianBodza/Kartoffelbox-v0.1"
T3_CHECKPOINT_FILE = "t3_cfg.safetensors"
device = "cuda" if torch.cuda.is_available() else "cpu"

model = ChatterboxTTS.from_pretrained(device=device)

print("Downloading and applying German patch...")
checkpoint_path = hf_hub_download(repo_id=MODEL_REPO, filename=T3_CHECKPOINT_FILE)

t3_state = load_file(checkpoint_path, device="cpu")

model.t3.load_state_dict(t3_state)
print("Patch applied successfully.")


text = "Tief im verwunschenen Wald, wo die Bäume uralte Geheimnisse flüsterten, lebte ein kleiner Gnom namens Fips, der die Sprache der Tiere verstand."

reference_audio_path = "/tts_model/uitoll.mp3"
output_path = "output_cloned_voice.wav"

print("Generating speech...")
with torch.inference_mode():
    wav = model.generate(
        text,
        audio_prompt_path=reference_audio_path,
        exaggeration=0.5,
        temperature=0.6,
        cfg_weight=0.3,
    )

sf.write(output_path, wav.squeeze().cpu().numpy(), model.sr)
print(f"Audio saved to {output_path}")


