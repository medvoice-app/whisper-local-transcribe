# Whisper Local Transcribe

A simple application for transcribing audio files using OpenAI's Whisper model.

## Features

- Modern GUI application (CustomTkinter-based)
- Single file and batch directory transcription
- SRT and TXT output formats
- Multiple language support
- Segment duration control for better readability
- Support for all Whisper models (tiny, base, small, medium, large)
- Real-time progress tracking

## Quick Start Guide

### GUI Application (Recommended)

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the GUI application:
   ```bash
   python app.py
   
   # Or using the Makefile
   make gui
   ```

## File Structure

- `/app.py` - Main GUI application
- `/src` - Core transcription logic
- `/uploads/transcriptions` - Transcription output files
- `/images` - Application icons and images
- `/sample_audio` - Sample audio files for testing

## Memory Usage Guidelines

To minimize memory usage:

1. Use smaller models (tiny, base) for faster processing and lower memory footprint
2. Process one file at a time when using the API server (MAX_CONCURRENT_TASKS=1)
3. Close other memory-intensive applications when processing large audio files
4. For GPU users, adjust PyTorch CUDA memory settings if needed
