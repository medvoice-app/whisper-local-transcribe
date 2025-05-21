# Whisper Local Transcribe

A simple application for transcribing audio files using OpenAI's Whisper model, with both GUI and API interfaces.

## Features

- Desktop GUI application (tkinter-based)
- FastAPI server for API-based transcription
- Single file and batch directory transcription
- SRT and TXT output formats
- Multiple language support
- Segment duration control for better readability
- Support for all Whisper models (tiny, base, small, medium, large)

## Quick Start Guide

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the GUI application:
   ```bash
   python client/app.py
   ```

3. Use the interface to:
   - Select a Whisper model
   - Choose output format and options
   - Select a file or directory of audio files
   - Start transcription

2. Access the API at http://localhost:8000 (docs at /docs)

## File Structure

- `/client` - Desktop GUI application
- `/server` - FastAPI server
- `/src` - Core transcription logic
- `/uploads` - Uploaded audio files
- `/uploads/transcriptions` - Transcription output files

## API Usage

### Method 1: One-Step Upload and Transcribe

```python
import requests

# Upload file and start transcription in one step
files = {"file": open("audio.mp3", "rb")}
params = {
    "model": "base",
    "language": "en",
    "srt_format": True,
    "verbose": True
}
response = requests.post("http://localhost:8000/upload_and_transcribe", files=files, params=params)
task_id = response.json()["task_id"]

# Check status periodically
response = requests.get(f"http://localhost:8000/status/{task_id}")
status = response.json()["status"]

# Get result when completed
if status == "completed":
    response = requests.get(f"http://localhost:8000/result/{task_id}")
    transcription = response.json()["transcription"]
    print(transcription)
```

### Method 2: Separate Upload and Transcribe Steps

```python
import requests

# Upload file
files = {"file": open("audio.mp3", "rb")}
response = requests.post("http://localhost:8000/upload", files=files)
task_id = response.json()["task_id"]

# Start transcription
options = {
    "model": "base",
    "language": "en",
    "srt_format": True
}
response = requests.post(f"http://localhost:8000/transcribe/{task_id}", json=options)

# Check status
response = requests.get(f"http://localhost:8000/status/{task_id}")
status = response.json()["status"]

# Get result when completed
if status == "completed":
    response = requests.get(f"http://localhost:8000/result/{task_id}")
    transcription = response.json()["transcription"]
    print(transcription)
```

## Server Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DEFAULT_MODEL` | Default model name | `base` |
| `MAX_CONCURRENT_TASKS` | Maximum concurrent transcriptions | `1` |
| `TASK_CLEANUP_HOURS` | Hours to keep tasks before cleanup | `24` |
| `PYTORCH_CUDA_ALLOC_CONF` | PyTorch CUDA memory settings | `max_split_size_mb:512` |

### Command Line Options for Debug Server

```
usage: run_debug_server.py [-h] [--host HOST] [--port PORT] [--reload] [--model MODEL]
                          [--max-tasks MAX_TASKS] [--log-level LOG_LEVEL]

Run the Whisper Local Transcribe API in debug mode

options:
  -h, --help            show this help message and exit
  --host HOST           Host to bind the server to
  --port PORT           Port to bind the server to
  --reload              Enable auto-reload for development
  --model MODEL         Default model to use for transcription
  --max-tasks MAX_TASKS
                        Maximum number of concurrent transcription tasks
  --log-level LOG_LEVEL
                        Logging level (debug, info, warning, error, critical)
```

## Memory Usage Guidelines

To minimize memory usage:

1. Use smaller models (tiny, base) for faster processing and lower memory footprint
2. Process one file at a time (MAX_CONCURRENT_TASKS=1)
3. Set memory limits in docker-compose.yaml if using Docker
4. Use the PyTorch CUDA memory allocation settings to prevent GPU memory issues
