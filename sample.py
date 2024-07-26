import torch
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import librosa
from peft import PeftModel, PeftConfig
import os


# Load the model and processor
peft_model_id = "stevehoang9/whisper-small-vi-300steps"
peft_config = PeftConfig.from_pretrained(peft_model_id)
model = WhisperForConditionalGeneration.from_pretrained(
    peft_config.base_model_name_or_path, load_in_8bit=True, device_map="auto"
)
model = PeftModel.from_pretrained(model, peft_model_id)
model.config.use_cache = True

processor = WhisperProcessor.from_pretrained(peft_config.base_model_name_or_path)

# Function to load and preprocess audio file
def load_audio(file_path):
    audio, sr = librosa.load(file_path, sr=16000)
    return audio, sr

# Load and preprocess the audio file
# audio_file_path = "data/vivos/test/waves/VIVOSDEV01/VIVOSDEV01_R043.wav"
audio_file_path = "data/data_test/gay_nhieu_muc_tieu.mp3"
audio, sr = load_audio(audio_file_path)

# Process audio to get the input features
input_features = processor(audio, sampling_rate=sr, return_tensors="pt").input_features
input_features = input_features.half().to(model.device)
# Generate transcription with language set to Vietnamese
forced_decoder_ids = processor.tokenizer.get_decoder_prompt_ids(language='vi', task="transcribe")
model.config.forced_decoder_ids = forced_decoder_ids

# Generate transcription
with torch.no_grad():
    predicted_ids = model.generate(input_features)

# Decode the predicted ids to text
transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]

output_dir = "data/output"
os.makedirs(output_dir, exist_ok=True)

# Save the transcription to a text file
output_file_path = os.path.join(output_dir, "transcription.txt")
with open(output_file_path, "w") as f:
    f.write(transcription)

print("Transcription saved to:", output_file_path)
