import os
from pathlib import Path
from collections import defaultdict
from datasets import Dataset, DatasetDict


def read_prompts(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    prompts = {}
    for line in lines:
        parts = line.strip().split(' ', 1)
        prompts[parts[0]] = parts[1]
            
    return prompts 

def read_genders(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    genders = {}
    for line in lines:
        parts = line.strip().split(' ', 1)
        genders[parts[0]] = parts[1]
        
    return genders 

def create_dataset(folder_path):
    dataset = []
    prompts = read_prompts(os.path.join(folder_path, 'prompts.txt'))
    genders = read_genders(os.path.join(folder_path, 'genders.txt'))
    
    for speaker_id, gender in genders.items():
        speaker_folder = os.path.join(folder_path, 'waves', speaker_id)
        audio_files = Path(speaker_folder).rglob('*.wav')
        for audio_file in audio_files:
            file_id = audio_file.stem
            transcription = prompts.get(file_id, "")
            dataset.append({
                'audio': str(audio_file),
                'transcription': transcription,
                'gender': gender
            })
            
    return dataset

def list_of_dicts_to_dict_of_lists(lst):
    dict_of_lists = defaultdict(list)
    for d in lst:
        for key, value in d.items():
            dict_of_lists[key].append(value)
    return dict_of_lists

def load_dataset(train_path, test_path):
    train_dataset = create_dataset(train_path)
    train_dict = list_of_dicts_to_dict_of_lists(train_dataset)
    train = Dataset.from_dict(train_dict)
    
    test_dataset = create_dataset(test_path)
    test_dict = list_of_dicts_to_dict_of_lists(test_dataset)
    test = Dataset.from_dict(test_dict) 
    
    return DatasetDict({'train': train, 'test': test})

if __name__ == '__main__':
    dataset = load_dataset()
    print(dataset)
    print(dataset['train'][0])
    
    

# import os
# import soundfile as sf
# from datasets import Dataset, DatasetDict
# from tqdm import tqdm

# def load_dataset(dataset_root):
#     train_data_dir = os.path.join(dataset_root, 'train')
#     test_data_dir = os.path.join(dataset_root, 'test')

#     train_examples = []
#     test_examples = []

#     # Load train data
#     for root, _, files in tqdm(os.walk(train_data_dir), desc='Loading train data', total=len(list(os.walk(train_data_dir)))):
#         for file in files:
#             if file.endswith('.wav'):
#                 speaker_id = os.path.basename(root)
#                 audio_path = os.path.join(root, file)
#                 _, sampling_rate = sf.read(audio_path)
#                 audio_dict = {
#                     'path': file,
#                     'sampling_rate': sampling_rate
#                 }
#                 prompt = get_prompt(train_data_dir, speaker_id, file)
#                 train_examples.append({
#                     'audio': audio_dict,
#                     'transcription': prompt
#                 })

#     # Load test data
#     for root, _, files in tqdm(os.walk(test_data_dir), desc='Loading test data', total=len(list(os.walk(test_data_dir)))):
#         for file in files:
#             if file.endswith('.wav'):
#                 speaker_id = os.path.basename(root)
#                 audio_path = os.path.join(root, file)
#                 _, sampling_rate = sf.read(audio_path)
#                 audio_dict = {
#                     'path': file,
#                     'sampling_rate': sampling_rate
#                 }
#                 prompt = get_prompt(test_data_dir, speaker_id, file)
#                 test_examples.append({
#                     'audio': audio_dict,
#                     'transcription': prompt
#                 })

#     train_dataset = Dataset.from_dict({'audio': [ex['audio'] for ex in train_examples],
#                                        'transcription': [ex['transcription'] for ex in train_examples]})
#     test_dataset = Dataset.from_dict({'audio': [ex['audio'] for ex in test_examples],
#                                       'transcription': [ex['transcription'] for ex in test_examples]})

#     return DatasetDict({'train': train_dataset, 'test': test_dataset})

# def get_prompt(dataset_path):
#     prompts_file = os.path.join(dataset_path, 'prompts.txt')
#     with open(prompts_file, 'r', encoding='utf-8') as f:
#         for line in f:
#             parts = line.strip().split(maxsplit=1) # Split at first space only (to keep the prompt as one string)
#             if len(parts) == 2:
#                 _, prompt = parts # Split the line into prompt_id and prompt
#                 return prompt
#     return None
