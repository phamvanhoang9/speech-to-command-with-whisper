import os 
import subprocess # used to run shell commands
import argparse 

def convert_audio(input_path, output_path, sampling_rate):
    try:
        command = [
            'ffmpeg', # ffmpeg is a command line tool to convert multimedia files
            '-i', input_path,
            '-ar', str(sampling_rate),
            '-ac', '1', # mono
            '-y', # overwrite output file if it exists
            '-sample_fmt', 's16', # signed 16-bit PCM
            '-f', 'wav', # output format
            output_path
        ]
        subprocess.run(command, check=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        # print(f"Successfully converted {input_path} to {output_path} with sampling rate {sampling_rate} Hz")
    except subprocess.CalledProcessError as e:
        print(f"Error converting {input_path}: {e.stderr.decode()}")

def main():
    parser = argparse.ArgumentParser(description="Convert all audio files to .wav files with a specific sampling rate.")
    parser.add_argument('input_dir', type=str, help="Directory containing input audio file.")
    parser.add_argument('output_dir', type=str, help="Directory to save output audio files.")
    parser.add_argument('--sampling_rate', type=int, default=16000, help="Target sampling rate (default: 16000 Hz).")   
    args = parser.parse_args()
    
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
        
    for root, _, files in os.walk(args.input_dir): # root is the current directory, _ is the list of subdirectories, files is the list of files
        for file in files:
            if file.endswith(('.mp3', '.wav')):
                input_path = os.path.join(root, file)
                output_file_name = os.path.splitext(file)[0] + '.wav' # ensure output file has .wav extension
                output_path = os.path.join(args.output_dir, output_file_name)
                convert_audio(input_path, output_path, args.sampling_rate)
                
if __name__ == "__main__":
    main()