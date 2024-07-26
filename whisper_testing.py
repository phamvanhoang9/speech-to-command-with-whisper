import whisper
import os


model = whisper.load_model("small")

# load audio and pad/trim it to fit 30 seconds
audio = whisper.load_audio("data/data_test/gay_nhieu_muc_tieu.mp3")
audio = whisper.pad_or_trim(audio)

# make log-Mel spectrogram and move to the same device as the model
mel = whisper.log_mel_spectrogram(audio).to(model.device)

# detect the spoken language
_, probs = model.detect_language(mel)
print(f"Detected language: {max(probs, key=probs.get)}")

# decode the audio
options = whisper.DecodingOptions()
result = whisper.decode(model, mel, options)


output_dir = "data/output"
os.makedirs(output_dir, exist_ok=True)

# Save the transcription to a text file
output_file_path = os.path.join(output_dir, "whisper_small_trans.txt")
with open(output_file_path, "w") as f:
    f.write(result.text)

print("Transcription saved to:", output_file_path)