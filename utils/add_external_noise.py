import soundata

# Specify the file path where you want to download the dataset
dataset_path = 'data/external_noise_data'

# Initialize the dataset and set the download path
dataset = soundata.initialize('urbansound8k', data_home=dataset_path)

dataset.download()  # download the dataset
dataset.validate()  # validate that all the expected files are there

example_clip = dataset.choice_clip()  # choose a random example clip
print(example_clip)  # see the available data
