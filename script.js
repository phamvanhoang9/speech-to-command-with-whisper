const startButton = document.getElementById('startButton');
const stopButton = document.getElementById('stopButton');
const transcriptionElement = document.getElementById('transcription');

let websocket;
let mediaRecorder;

startButton.addEventListener('click', async () => {
    startButton.disabled = true;
    stopButton.disabled = false;
    transcriptionElement.textContent = '';

    // Get user media
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.start();

    websocket = new WebSocket('ws://localhost:8000');

    mediaRecorder.ondataavailable = (event) => {
        if (websocket.readyState === WebSocket.OPEN) {
            websocket.send(event.data);
        }
    };

    websocket.onmessage = (event) => {
        transcriptionElement.textContent += event.data + '\n';
    };
});

stopButton.addEventListener('click', () => {
    startButton.disabled = false;
    stopButton.disabled = true;

    mediaRecorder.stop();
    websocket.close();
});