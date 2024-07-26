import os


def extract_audio_paths(base_directory, output_file):
    with open(output_file, 'w') as file:
        for root, _, files in os.walk(base_directory):
            for name in files:
                if name.lower().endswith('.wav'):
                    file.write(os.path.join(root, name) + '\n')

base_directory = 'data/external_noise_data/audio'  
output_file = 'noises_list.txt'
extract_audio_paths(base_directory, output_file)
