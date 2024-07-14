import asyncio
import websockets
import numpy as np
import pyaudio
import torch
from transformers import WhisperProcessor, WhisperForConditionalGeneration

from turtle_helper import move_turtle

# Whisper model setup
processor = WhisperProcessor.from_pretrained("stevehoang9/whisper-small-vi")
model = WhisperForConditionalGeneration.from_pretrained("stevehoang9/whisper-small-vi")

commands = ['quay lên trên', 'quay xuống dưới', 'quay sang trái', 'quay sang phải', 'dừng lại', 'tiến lên']

# Audio parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024

# WebSocket server setup
async def audio_handler(websocket, path):
    print("Client connected")
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    try:
        while True:
            audio_data = stream.read(CHUNK)
            signal = np.frombuffer(audio_data, dtype=np.int16)
            inputs = processor(signal, return_tensors="pt", sampling_rate=RATE)
            input_features = inputs.input_features

            with torch.no_grad():
                predicted_ids = model.generate(input_features)
            command = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]

            # Execute command!
            move_turtle(execute_cmd(command)) # what will it happen if the command is unknown?

            await websocket.send(command)

    except websockets.ConnectionClosed:
        print("Client disconnected")
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()

def find_closest_command(prediction_text):
    prediction_text = prediction_text.lower()
    for command in commands:
        if command in prediction_text:
            return command
        
    return "unknown"

def execute_cmd(command):
    if find_closest_command(command) != "unknown":
        command = find_closest_command(command)
    else:
        print(f"Unknown command: {command}")


# Start the WebSocket server
start_server = websockets.serve(audio_handler, "localhost", 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()