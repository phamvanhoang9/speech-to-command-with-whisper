import gdown
import zipfile
import os

# dataset = "https://drive.google.com/file/d/1yI0ehlcoaVm_xEmqQTJN0MlB4r3FQS9i/view?usp=sharing"

file_id = '1yI0ehlcoaVm_xEmqQTJN0MlB4r3FQS9i'
url = f'https://drive.google.com/uc?id={file_id}'
output = 'vivos.zip'

# Download the dataset
gdown.download(url, output, quiet=False)

# Extract the contents of the zip file
with zipfile.ZipFile(output, 'r') as zip_ref:
    zip_ref.extractall('data')

# Remove the zip file after extraction
os.remove(output)
