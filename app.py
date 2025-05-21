import tkinter as tk
import customtkinter as ctk
import sys
import os
import subprocess
from pathlib import Path
from threading import Thread
from tkinter import filedialog, messagebox, StringVar

# Add src directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from src._LocalTranscribe import transcribe, get_path


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        print(Back.CYAN + "Welcome to Local Transcribe with Whisper!\U0001f600\nCheck back here to see some output from your transcriptions.\nDon't worry, they will also be saved on the computer!\U0001f64f")

        # Configure window
        self.title("Whisper Local Transcribe")
        self.geometry("800x600")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Try to set icon if on Windows
        try:
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "icon.ico")
            if os.path.exists(icon_path) and sys.platform.startswith('win'):
                self.iconbitmap(icon_path)
        except Exception as e:
            print(f"Could not set icon: {e}")
        
        # Create main container
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Create title
        self.title_label = ctk.CTkLabel(self.main_frame, text="Whisper Local Transcribe", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Create model selection
        self.model_frame = ctk.CTkFrame(self.main_frame)
        self.model_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        self.model_label = ctk.CTkLabel(self.model_frame, text="Model:")
        self.model_label.grid(row=0, column=0, padx=10, pady=10)
        
        self.models = ["tiny", "base", "small", "medium", "large"]
        
        self.model_var = StringVar(value="base")
        self.model_select = ctk.CTkOptionMenu(
            self.model_frame,
            values=self.models,
            variable=self.model_var
        )
        self.model_select.grid(row=0, column=1, padx=10, pady=10)
        
        # Create language selection
        self.lang_label = ctk.CTkLabel(self.model_frame, text="Language (optional):")
        self.lang_label.grid(row=0, column=2, padx=10, pady=10)
        
        self.lang_var = StringVar(value="")
        self.lang_entry = ctk.CTkEntry(self.model_frame, textvariable=self.lang_var, width=60)
        self.lang_entry.grid(row=0, column=3, padx=10, pady=10)
        
        # Create output format selection
        self.format_frame = ctk.CTkFrame(self.main_frame)
        self.format_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        self.srt_var = tk.BooleanVar(value=True)
        self.srt_checkbox = ctk.CTkCheckBox(self.format_frame, text="SRT Format", variable=self.srt_var)
        self.srt_checkbox.grid(row=0, column=0, padx=10, pady=10)
        
        self.verbose_var = tk.BooleanVar(value=False)
        self.verbose_checkbox = ctk.CTkCheckBox(self.format_frame, text="Verbose Output", variable=self.verbose_var)
        self.verbose_checkbox.grid(row=0, column=1, padx=10, pady=10)
        
        # Create segment duration options
        self.segment_frame = ctk.CTkFrame(self.main_frame)
        self.segment_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        
        self.max_segment_label = ctk.CTkLabel(self.segment_frame, text="Max Segment Duration (sec):")
        self.max_segment_label.grid(row=0, column=0, padx=10, pady=10)
        
        self.max_segment_var = StringVar(value="0")
        self.max_segment_entry = ctk.CTkEntry(self.segment_frame, textvariable=self.max_segment_var, width=60)
        self.max_segment_entry.grid(row=0, column=1, padx=10, pady=10)
        
        self.min_segment_label = ctk.CTkLabel(self.segment_frame, text="Min Segment Duration (sec):")
        self.min_segment_label.grid(row=0, column=2, padx=10, pady=10)
        
        self.min_segment_var = StringVar(value="0")
        self.min_segment_entry = ctk.CTkEntry(self.segment_frame, textvariable=self.min_segment_var, width=60)
        self.min_segment_entry.grid(row=0, column=3, padx=10, pady=10)
        
        # Create file selection section
        self.file_frame = ctk.CTkFrame(self.main_frame)
        self.file_frame.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        
        self.file_label = ctk.CTkLabel(self.file_frame, text="No file or directory selected")
        self.file_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.select_file_button = ctk.CTkButton(self.file_frame, text="Select File", command=self.select_file)
        self.select_file_button.grid(row=0, column=1, padx=10, pady=10)
        
        self.select_dir_button = ctk.CTkButton(self.file_frame, text="Select Directory", command=self.select_directory)
        self.select_dir_button.grid(row=0, column=2, padx=10, pady=10)
        
        # Create transcription button
        self.transcribe_button = ctk.CTkButton(self.main_frame, text="Transcribe", command=self.start_transcription)
        self.transcribe_button.grid(row=5, column=0, padx=20, pady=(10, 20))
        
        # Create progress section
        self.progress_frame = ctk.CTkFrame(self.main_frame)
        self.progress_frame.grid(row=6, column=0, padx=20, pady=10, sticky="ew")
        self.progress_frame.grid_columnconfigure(0, weight=1)
        
        self.progress_label = ctk.CTkLabel(self.progress_frame, text="")
        self.progress_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame)
        self.progress_bar.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.progress_bar.set(0)
        
        # Initialize variables
        self.selected_path = None
        self.is_file = False
        self.transcription_running = False
        self.transcription_thread = None
    
    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=[("Audio Files", "*.mp3 *.wav *.aac *.flac *.m4a *.ogg")]
        )
        if file_path:
            self.selected_path = file_path
            self.is_file = True
            self.file_label.configure(text=f"Selected File: {os.path.basename(file_path)}")
    
    def select_directory(self):
        dir_path = filedialog.askdirectory(title="Select Directory with Audio Files")
        if dir_path:
            self.selected_path = dir_path
            self.is_file = False
            self.file_label.configure(text=f"Selected Directory: {os.path.basename(dir_path)}")
    
    def update_progress(self, percent, message):
        if percent < 0:
            # Error occurred
            messagebox.showerror("Error", message)
            self.progress_label.configure(text=f"Error: {message}")
            self.progress_bar.set(0)
            self.transcribe_button.configure(state="normal")
            self.transcription_running = False
        else:
            self.progress_label.configure(text=message)
            self.progress_bar.set(percent/100)
            if percent >= 100:
                self.progress_label.configure(text="Transcription complete!")
                self.transcribe_button.configure(state="normal")
                self.transcription_running = False
    
    def start_transcription(self):
        if self.transcription_running:
            return
        
        if not self.selected_path:
            messagebox.showerror("Error", "Please select a file or directory first.")
            return
        
        # Get transcription options
        model = self.model_var.get()
        language = self.lang_var.get() or None
        srt_format = self.srt_var.get()
        verbose = self.verbose_var.get()
        
        try:
            max_segment = float(self.max_segment_var.get()) if self.max_segment_var.get() else 0
            min_segment = float(self.min_segment_var.get()) if self.min_segment_var.get() else 0
        except ValueError:
            messagebox.showerror("Error", "Segment duration must be a number.")
            return
        
        # Disable the button while transcribing
        self.transcribe_button.configure(state="disabled")
        self.transcription_running = True
        self.progress_label.configure(text="Starting transcription...")
        self.progress_bar.set(0)
        
        # Start transcription in a separate thread
        self.transcription_thread = Thread(
            target=self.run_transcription,
            args=(model, language, srt_format, verbose, max_segment, min_segment)
        )
        self.transcription_thread.daemon = True
        self.transcription_thread.start()
    
    def run_transcription(self, model, language, srt_format, verbose, max_segment, min_segment):
        try:
            if self.is_file:
                # Single file transcription
                dir_path = os.path.dirname(self.selected_path)
                file_list = [self.selected_path]
            else:
                # Directory transcription
                dir_path = self.selected_path
                file_list = []
                for ext in [".mp3", ".wav", ".aac", ".flac", ".m4a", ".ogg"]:
                    file_list.extend([str(f) for f in Path(dir_path).glob(f"*{ext}")])
                
                if not file_list:
                    self.after(0, lambda: self.update_progress(-1, "No audio files found in the selected directory."))
                    return
            
            result = transcribe(
                path=dir_path,
                glob_file=file_list,
                model=model,
                language=language,
                verbose=verbose,
                max_segment_duration=max_segment if max_segment > 0 else None,
                srt_format=srt_format,
                min_segment_duration=min_segment if min_segment > 0 else 0,
                callback=self.update_progress
            )
            
            # Show the result when completed
            self.after(0, lambda: self.update_progress(100, result))
            
        except Exception as e:
            # Show any errors
            self.after(0, lambda: self.update_progress(-1, str(e)))


if __name__ == "__main__":
    app = App()
    app.mainloop()
