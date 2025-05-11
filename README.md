# Local Transcribe with Whisper 
A simple desktop application to transcribe audio and video files using OpenAI's Whisper speech recognition system. No programming experience required!

![GUI Interface](images/gui-windows.png)

## What's New in Version 1.2
- **Automatic file detection** - No need to specify file types anymore
- **Language options** - Specify language or leave blank for auto-detection
- **Easy model selection** - Simple dropdown with all available models
- **Improved interface** - More user-friendly GUI

## Features

- **Folder Processing**: Select a folder and transcribe all compatible audio/video files at once
- **Language Options**: Auto-detect or specify for better accuracy 
- **Model Selection**: Choose from various sizes ("base" to "large") with English-specialized options (".en" models)
- **Progress Tracking**: Monitor transcription with progress bar and terminal output
- **Export Options**: Save as regular text or SRT subtitle format
- **Segment Control**: Adjust maximum and minimum segment durations

## Installation Options

### Option 1: Windows Installation
1. **Download the files**:
   - Download the [ZIP file](https://github.com/soderstromkr/transcribe/archive/refs/heads/main.zip) and extract it
   - Or clone with git: `git clone https://github.com/soderstromkr/transcribe.git`

2. **Install Python dependencies**:
   - Install [Miniconda](https://docs.anaconda.com/free/miniconda/miniconda-install/) (recommended for beginners)
   - Install FFmpeg through conda:
     ```
     conda install -c conda-forge ffmpeg-python
     ```
   - Install other dependencies:
     ```
     pip install -r requirements.txt
     ```

3. **Run the application**:
   - From Anaconda Prompt: `python app.py`
   - Or use the included `run_Windows.bat` file

### Option 2: WSL2 (Windows Subsystem for Linux) Setup
Setting up the GUI application in WSL2 requires a few extra steps:

1. **Install X Server** (to display the GUI):
   - Download and install [VcXsrv](https://sourceforge.net/projects/vcxsrv/) (free)
   - Launch XLaunch and configure:
     - Select "Multiple windows"
     - Set display number to "0"
     - Select "Start no client"
     - **Important**: Check "Disable access control"
     - Save configuration for future use

2. **Configure WSL2**: 
   - Add to your `~/.bashrc` file:
     ```bash
     # Add these two lines:
     export DISPLAY=$(grep -m 1 nameserver /etc/resolv.conf | awk '{print $2}'):0
     export LIBGL_ALWAYS_INDIRECT=1
     ```
   - Apply changes: `source ~/.bashrc`

3. **Install dependencies**:
   ```bash
   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate
   
   # Install required packages
   sudo apt-get update
   sudo apt-get install -y python3-tk ffmpeg
   pip install -r requirements.txt
   ```

4. **Fix icon compatibility**:
   - Edit `app.py` to handle Linux/WSL2:
     ```python
     # Change this line:
     # root.iconbitmap('images/icon.ico')
     
     # To this:
     import sys
     if sys.platform.startswith('win'):
         root.iconbitmap('images/icon.ico')
     # Skip icon for Linux
     ```

5. **Run the app**:
   ```bash
   # Make sure X Server is running on Windows
   source venv/bin/activate
   python app.py
   ```

### Building an Executable (Windows)
The application includes `build_setup.py` for creating a standalone Windows executable using cx_Freeze:

1. Install cx_Freeze: `pip install cx_freeze`
2. Run the build script: `python build_setup.py build`
3. Find the executable in the `build` directory

## How to Use

1. **Start the application**
   - The app will open with a GUI window and a terminal for additional info

2. **Select folder**
   - Click "Browse" to select a folder containing your audio/video files
   - Note: The app processes entire folders, not individual files

3. **Choose settings**
   - **Model**: Select from dropdown (smaller models are faster, larger are more accurate)
   - **Language**: Leave blank for auto-detection or specify a language
   - **Segment Duration**: Optionally set min/max segment length in seconds
   - **Format**: Check "Export as SRT" for subtitle format (optional)
   - **Verbose mode**: Enable for detailed transcription progress in terminal

4. **Run transcription**
   - Click "Transcribe" to begin
   - A progress bar will display the status
   - Transcribed files will be saved in a "transcriptions" folder within your selected directory

5. **View results**
   - When complete, a message will show the transcription output
   - Find all transcribed files in the "transcriptions" subfolder

**Tip**: To run offline later, first use the app online with the sample folder to download and cache the model files locally.
## For Developers

- **Jupyter Notebook**: See [example.ipynb](example.ipynb) for using the transcription function directly
- **Code Structure**: Core transcription logic is in `src/_LocalTranscribe.py`, GUI in `app.py`
- **Dependencies**: Listed in `requirements.txt` (openai-whisper, customtkinter, colorama)
- **Performance Notes**: Processing speed depends on model size and your hardware

## Troubleshooting

- **Display issues in WSL2**: Verify X Server is running and DISPLAY is set correctly
- **Missing GUI components**: Install additional libraries: `sudo apt-get install -y libxcb-xinerama0 libxcb-icccm4`
- **FFmpeg errors**: Ensure ffmpeg is installed and in your PATH
- **Slow performance**: Try using a smaller model like "base" or "small"

---

[^1]: If not using Conda, see [these instructions](https://stackoverflow.com/questions/65836756/python-ffmpeg-wont-accept-path-why) for handling PATH issues with ffmpeg-python.

[![DOI](https://zenodo.org/badge/617404576.svg)](https://zenodo.org/badge/latestdoi/617404576)
