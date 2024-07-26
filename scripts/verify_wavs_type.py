import argparse # For argument parsing
import soundfile as sf # For reading .wav files
from glob import glob # For searching files
from tqdm import tqdm # For progress bar
import os


def verify(args):
    search_path = os.path.join(args.base_dir, '**', '*.wav')
    print(f"Searching for files in: {search_path}")
    wav_files = sorted(glob(search_path, recursive=True))
    print(f"Found {len(wav_files)} .wav files.")
    
    for wavfile in tqdm(wav_files):
        ob = sf.SoundFile(wavfile)
        if ob.subtype != 'PCM_16' or ob.channels != 1 or ob.samplerate != 16000:
            print(wavfile)
            print('Sample rate: {}'.format(ob.samplerate))
            print('Channels: {}'.format(ob.channels))
            print('Subtype: {}'.format(ob.subtype))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base_dir', default='./')
    parser.add_argument('--csv_file', default='metadata.csv', help='Name of csv file')
    args = parser.parse_args()
    verify(args)
    
if __name__ == "__main__":
    main()