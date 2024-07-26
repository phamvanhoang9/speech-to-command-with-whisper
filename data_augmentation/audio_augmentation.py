import argparse 
import random 
import librosa 
from datetime import datetime 
import os
import sys
# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.config import load_config
from scipy.io.wavfile import read, write 
import numpy as np 
import matplotlib.pyplot as plt 


random.seed(datetime.now().timestamp())

sampling_rate = 16000 
MAX_WAV_VALUE = 32767 

class AudioAugmentation:
    """ 
    Class that performs data augmentation directly on raw audio.
    """
    def __init__(self, sr):
        """
        Initializes an object of the class.

        Args:
            sr (int): sampling rate used.
        """
        self.sr = sr
        
    def read_audio_file(self, filepath):
        """ 
        Loads a clean audio speech file which will be carried out data augmentation.
        
        Args: 
            filepath: path of the file to be loaded.
        
        Returns:
            data: numpy audio data time series.
        """
        data = librosa.core.load(filepath)[0]
        input_length = len(data)
        if len(data) > input_length:
            data = data[:input_length]
        else:
            data = np.pad(data, (0, max(0, input_length - len(data))), "constant")
        
        return data
    
    def write_audio_file(self, filename, data): 
        """ 
        Saves the audio data to a file.
        
        Args: 
            filename: path to save the file
            data: audio data
        """
        
        data = data*MAX_WAV_VALUE
        write(filename, self.sr, data.astype(np.int16))
        
    def add_noise(self, data, rate=0.1):
        """ 
        Inserting white noise at audio data.
        
        Args:
            data: audio data
            rate: noise intensity rate to be inserted.
        
        Returns:
            augmented_data: audio data with white noise inserted.
        """
        noise = np.random.normal(0, 1, len(data))
        augmented_data = data + rate * noise
        
        return augmented_data
    
    def add_external_noise(self, data, noise, rate):
        """ 
        Inserts noise audio data into the clean audio data.
        
        Args:
            data: clean audio data.
            noise: noise audio data.
            rate: noise intensity rate to be inserted.
            
        Returns:
            augmented_data: clean audio data augmented with noise data.
        """
        if len(noise) < len(data):
            while(len(noise) < len(data)):
                noise = np.concatenate((noise, noise[:len(data) - len(noise)]), axis=None)
        else:
            noise = noise[:len(data)]
        
        augmented_data = data + rate * noise
        
        return augmented_data
    
    def shift(self, data, shift_rate, shift_direction='both'):
        """The idea of shifting time is very simple. It just shift audio to left/right with a random second.
        If shifting audio to left (fast forward) with x seconds, first x seconds will mark as 0 (i.e. silence).
        If shifting audio to right (back forward) with x seconds, last x seconds will mark as 0 (i.e. silence).

        Args:
            data (_type_): clean audio data.
            shift_rate (_type_): intensity rate to be shifted
            shift_direction (str, optional): left (fast forward), right (back forward). Defaults to 'both'.
            
        Returns:
            augemented_data: audio data shifted.
        """
        shift = int(self.sr * shift_rate)
        if shift_direction == 'right':
            shift = - shift
        elif shift_direction == 'both':
            direction = np.random.randint(0, 2)
            if direction == 1:
                shift = -shift
                
        augemented_data = np.roll(data, shift)
        if shift > 0:
            augemented_data[:shift] = 0
        else:
            augemented_data[shift:] = 0
        
        return augemented_data
    
    def stretch(self, data, rate=1):
        """Time stretch an audio series for a fixed rate using Librosa

        Args:
            data (_type_): clean audio data.
            rate (int, optional): time stretch rate. Defaults to 1.
            
        Returns:
            augmented_data: audio data time-stretched.
        """
        input_length = len(data)
        augmented_data = librosa.effects.time_stretch(y=data, rate=rate)
        if len(augmented_data) > input_length:
            augmented_data = augmented_data[:input_length]
        else:
            augmented_data = np.pad(augmented_data, (0, max(0, input_length - len(augmented_data))), "constant")
        
        return augmented_data
    
    def pitch(self, data, pitch_factor):
        """Pitch-shift the audio data by pitch_factor half-steps using Librosa.

        Args:
            data (_type_): _description_
            pitch_factor (_type_): _description_
        
        Returns:
            augmented_data: audio data pitch_shifted.
        """
        augmented_data = librosa.effects.pitch_shift(data, sr=self.sr, n_steps=pitch_factor)
        
        return augmented_data
    
    def split_title_line(title_text, max_words=5):
        """A function that splits any string based on specific character

        Args:
            title_text (_type_): _description_
            max_words (int, optional): _description_. Defaults to 5.
            
        Returns:
            A string with maximum number of words on it
        """
        seq = title_text.split()
        
        return '\n'.join([' '.join(seq[i:i + max_words]) for i in range(0, len(seq), max_words)])
    
    def plot_waveform(self, aug_waveform, path, clean_waveform=None, title=None, split_title=False, max_len=None):
        """ 
        Plot a waveform compared to a clean waveform.
        
        Args:
            aug_waveform: audio data augmented.
            path: path to save figure.
            clean_waveform: clean audio data.
            title: title of the image.
            split_title: True or False.
            max_len: maximum length of the audio data to be plotted.
        """
        if max_len is not None:
            aug_waveform = aug_waveform[:max_len]
            clean_waveform = clean_waveform[:max_len]
            
        if split_title:
            title = self.split_title_line(title)
            
        fig = plt.figure(figsize=(10,8))
        fig.text(0.5, 0.18, title, horizontalalignment='center', fontsize=16)
        
        if clean_waveform is not None:
            ax1 = fig.add_subplot(311)
            ax2 = fig.add_subplot(312)
            im = ax1.plot(np.linspace(0, 1, len(clean_waveform)), clean_waveform)
            plt.ylabel('Amplitude')
            
            ax1.set_title('Clean Waveform')
            ax2.set_title('Augmented Waveform')
            
            ax1.set_ylim([-1, 1])
            ax2.set_ylim([-1, 1])
            
        else:
            ax2 = fig.add_subplot(211)
            ax2.set_ylim([-1, 1])
            
        im = ax2.plot(np.linspace(0, 1, len(aug_waveform)), aug_waveform)
        plt.ylabel('Amplitude')
        
        plt.tight_layout()
        plt.savefig(path, format='png')
        plt.close()
        
def main():
    """ 
    Example of using this class.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--base_dir', default='./')
    parser.add_argument('-i', '--input_file', type=str, required=True, help="input wav file")
    parser.add_argument('-o', '--output_dir', type=str, required=True, help="output dir of data augmented files")
    parser.add_argument('-c', '--config_path', type=str, required=True, help="json file with configurations")
    args = parser.parse_args()
    
    config = load_config(args.config_path)
    
    with open(config.data_aug['noises_filepath'], "r") as f:
        noises_file_content = f.readlines()
    
    aa = AudioAugmentation(sampling_rate)
    data = aa.read_audio_file(args.input_file)
    
    from os.path import basename, dirname, join 
    from os import makedirs 
    
    output_file = basename(args.input_file).split('.')[0]
    
    # Adding white noise to sound
    filename = join(args.output_dir, output_file + '_noise.wav')
    makedirs(dirname(filename), exist_ok=True)
    noise_rate = random.uniform(config.data_aug['noise_range_min'], config.data_aug['noise_range_max'])
    data_aug = aa.add_noise(data, noise_rate)
    aa.write_audio_file(filename, data_aug)
    aa.plot_waveform(data_aug, filename.replace('.wav', '.png'), data)
    
    # Shifting the sound 
    filename = join(args.output_dir, output_file + '_shift.wav')
    shift_rate = random.uniform(config.data_aug['shift_roll_range_min'], config.data_aug['shift_roll_range_max'])
    data_aug = aa.shift(data, shift_rate)
    aa.write_audio_file(filename, data_aug)
    aa.plot_waveform(data_aug, filename.replace('.wav', '.png'), data)
    
    # Stretching the sound 
    filename = join(args.output_dir, output_file + '_stretch.wav')
    stretch_rate = random.uniform(config.data_aug['stretch_range_min'], config.data_aug['stretch_range_max'])
    data_aug = aa.shift(data, stretch_rate)
    aa.write_audio_file(filename, data_aug)
    aa.plot_waveform(data_aug, filename.replace('.wav', '.png'), data)
    
    # Changing pitch
    filename = join(args.output_dir, output_file + '_pitch.wav')
    pitch_rate = random.uniform(config.data_aug['stretch_range_min'], config.data_aug['stretch_range_max'])
    data_aug = aa.shift(data, pitch_rate)
    aa.write_audio_file(filename, data_aug)
    aa.plot_waveform(data_aug, filename.replace('.wav', '.png'), data)
    
    # Inserting external noises
    filename = join(args.output_dir, output_file + '_exnoise.wav')
    noise_filepath = random.choice(noises_file_content).strip()
    noise = aa.read_audio_file(noise_filepath)
    ex_noise_rate = random.uniform(config.data_aug['external_noise_range_min'], config.data_aug['external_noise_range_max'])
    aa.plot_waveform(noise*ex_noise_rate, filename.replace('.wav', '_noise.png'), data)
    data_aug = aa.add_external_noise(data, noise, ex_noise_rate)
    aa.write_audio_file(filename, data_aug)
    aa.plot_waveform(data_aug, filename.replace('.wav', '.png'), data)
    
if __name__ == "__main__":
    main()