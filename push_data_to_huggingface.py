import os
from pathlib import Path
import soundfile as sf
from datasets import Dataset, DatasetDict, Audio
from tqdm import tqdm

# Paths to the dataset
train_path = 'data/vietnamese_ASR/vivos/train'
test_path = 'data/vietnamese_ASR/vivos/test'

def read_prompts(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    prompts = {}
    for line in lines:
        parts = line.strip().split(' ', 1)
        prompts[parts[0]] = parts[1]
    return prompts

def read_genders(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    genders = {}
    for line in lines:
        parts = line.strip().split(' ')
        genders[parts[0]] = parts[1]
    return genders

def create_dataset(folder_path, batch_size=100):
    dataset = []
    prompts = read_prompts(os.path.join(folder_path, 'prompts.txt'))
    genders = read_genders(os.path.join(folder_path, 'genders.txt'))

    for speaker_id, gender in genders.items():
        speaker_folder = os.path.join(folder_path, 'waves', speaker_id)
        audio_files = list(Path(speaker_folder).rglob('*.wav'))  # Convert generator to list
        
        for i in range(0, len(audio_files), batch_size):
            batch_files = audio_files[i:i + batch_size]
            batch_data = []
            for audio_file in tqdm(batch_files, desc=f"Processing {speaker_id} Batch {i//batch_size + 1}"):
                file_id = audio_file.stem
                transcription = prompts.get(file_id, "")
                audio_data, sampling_rate = sf.read(audio_file)
                batch_data.append({
                    'path': str(audio_file),
                    'array': audio_data,
                    'sampling_rate': sampling_rate,
                    'sentence': transcription,
                    'gender': gender
                })
            dataset.extend(batch_data)
            
    return dataset

# Create train and test datasets
train_dataset = create_dataset(train_path)
test_dataset = create_dataset(test_path)

# Convert to dictionary with lists for each column
def restructure_dataset(dataset):
    return {
        'path': [item['path'] for item in dataset],
        'audio': [{'path': item['path'], 'array': item['array'], 'sampling_rate': item['sampling_rate']} for item in dataset],
        'sentence': [item['sentence'] for item in dataset],
        'gender': [item['gender'] for item in dataset]
    }

train_dict = restructure_dataset(train_dataset)
test_dict = restructure_dataset(test_dataset)

from huggingface_hub import notebook_login

notebook_login()

# Convert to Hugging Face Dataset
def convert_to_hf_dataset(data_dict):
    return Dataset.from_dict(data_dict).cast_column("audio", Audio(sampling_rate=16000))

train_hf_dataset = convert_to_hf_dataset(train_dict)
test_hf_dataset = convert_to_hf_dataset(test_dict)

# Create DatasetDict
hf_datasets = DatasetDict({
    'train': train_hf_dataset,
    'test': test_hf_dataset
})

# Check the structure
print(hf_datasets)

# Push to Hugging Face Hub
hf_datasets.push_to_hub('stevehoang9/vietnamese_ASR')