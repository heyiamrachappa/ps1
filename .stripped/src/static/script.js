let mediaRecorder;
let audioChunks = [];
let isRecording = false;

const recordBtn = document.getElementById('recordBtn');
const statusLabel = document.getElementById('statusLabel');
const resultCard = document.getElementById('resultCard');
const loadingIndicator = document.getElementById('loadingIndicator');
const songTitle = document.getElementById('songTitle');
const songArtist = document.getElementById('songArtist');
const confidenceBadge = document.getElementById('confidenceBadge');
const latencyBadge = document.getElementById('latencyBadge');

recordBtn.addEventListener('click', async () => {
    if (!isRecording) {
        startRecording();
    } else {
        stopRecording();
    }
});

async function startRecording() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        
        
        const mimeType = MediaRecorder.isTypeSupported('audio/webm') ? 'audio/webm' : 'audio/ogg';
        mediaRecorder = new MediaRecorder(stream, { mimeType });
        audioChunks = [];

        mediaRecorder.ondataavailable = (event) => {
            audioChunks.push(event.data);
        };

        mediaRecorder.onstop = sendAudioToServer;

        mediaRecorder.start();
        isRecording = true;
        recordBtn.classList.add('recording');
        statusLabel.innerText = "Listening... (5s)";
        resultCard.classList.add('hidden');

        setTimeout(() => {
            if (isRecording) stopRecording();
        }, 5000);

    } catch (err) {
        console.error("Error accessing microphone:", err);
        statusLabel.innerText = "Mic Error. Check Permissions.";
    }
}

function stopRecording() {
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        mediaRecorder.stop();
    }
    isRecording = false;
    recordBtn.classList.remove('recording');
    statusLabel.innerText = "Analyzing...";
    loadingIndicator.classList.remove('hidden');
}

async function sendAudioToServer() {
    const audioBlob = new Blob(audioChunks, { type: mediaRecorder.mimeType });
    const formData = new FormData();
    formData.append('file', audioBlob, 'query.webm');

    try {
        const response = await fetch('/identify', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        loadingIndicator.classList.add('hidden');
        displayResult(data);

    } catch (err) {
        console.error("Error identifying audio:", err);
        statusLabel.innerText = "Error Identifying. Try again.";
        loadingIndicator.classList.add('hidden');
    }
}

function displayResult(data) {
    if (data.result && data.result.best_match) {
        const fullPath = data.result.best_match;
        
        const parts = fullPath.split('/');
        const fileName = parts[parts.length - 1].replace('.wav', '');
        
        songTitle.innerText = fileName;
        songArtist.innerText = parts[1] ? parts[1].toUpperCase() : "Unknown Artist";
        confidenceBadge.innerText = `${data.result.confidence}% Confidence`;
        latencyBadge.innerText = `${data.latency_ms}ms`;
        
        resultCard.classList.remove('hidden');
        statusLabel.innerText = "Found a Match!";
    } else {
        statusLabel.innerText = "No Match Found. Try a longer clip.";
    }
}
