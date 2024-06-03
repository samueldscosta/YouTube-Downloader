import tkinter
from tkinter import filedialog
import customtkinter
from pytube import YouTube
from pydub import AudioSegment
import os

# Variable to store the selected folder
download_folder = ""

# Folder Selection Function
def select_folder():
    global download_folder
    download_folder = filedialog.askdirectory()
    if download_folder:
        folderLabel.configure(text="Save to: " + download_folder, text_color="white")
    else:
        folderLabel.configure(text="No folder selected", text_color="white")

# Download Function
def startDownload():
    try:
        ytLink = link.get()
        ytObject = YouTube(ytLink, on_progress_callback=on_progress)

        if download_option.get() == "Audio":
            stream = ytObject.streams.get_audio_only()
        else:
            stream = ytObject.streams.get_highest_resolution()

        title.configure(text=ytObject.title, text_color="white")
        finishLabel.configure(text="")

        if download_folder:
            output_file = stream.download(output_path=download_folder)
            if download_option.get() == "Audio":
                convert_to_mp3(output_file)
            finishLabel.configure(text="Downloaded!", text_color="green")
        else:
            finishLabel.configure(text="Select a folder", text_color="red")
    except:
        finishLabel.configure(text="Download Error", text_color="red")

# Convert to MP3 Function
def convert_to_mp3(file_path):
    mp3_path = os.path.splitext(file_path)[0] + ".mp3"
    audio = AudioSegment.from_file(file_path)
    audio.export(mp3_path, format="mp3")
    os.remove(file_path) # Remove the original file

# Progress Bar Function
def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_compeletion = bytes_downloaded / total_size * 100
    per = str(int(percentage_of_compeletion))
    pPercentage.configure(text=per + '%')
    pPercentage.update()

    # Update progress bar
    progressBar.set(float(percentage_of_compeletion) / 100)

# System Settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# Our App Frame
app = customtkinter.CTk()
app.geometry("720x480")
app.title("YouTube Downloader")

# Adding UI Elements
title = customtkinter.CTkLabel(app, text="Insert a YouTube link:")
title.pack(padx=10, pady=10)

# Link Input
url_var = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=40, textvariable=url_var)
link.pack()

# Download Option
download_option = tkinter.StringVar(value="Audio")
audio_radio = customtkinter.CTkRadioButton(app, text="Audio", variable=download_option, value="Audio")
video_radio = customtkinter.CTkRadioButton(app, text="Video", variable=download_option, value="Video")
audio_radio.pack(padx=10, pady=10)
video_radio.pack(padx=10, pady=10)

# Folder Selection
folderButton = customtkinter.CTkButton(app, text="Select Folder", command=select_folder)
folderButton.pack(padx=10, pady=10)

# Folder Label
folderLabel = customtkinter.CTkLabel(app, text="No folder selected")
folderLabel.pack()

# Finished Downloading
finishLabel = customtkinter.CTkLabel(app, text="")
finishLabel.pack()

# Progress Percentage
pPercentage = customtkinter.CTkLabel(app, text="0%")
pPercentage.pack()

progressBar = customtkinter.CTkProgressBar(app, width=400)
progressBar.set(0)
progressBar.pack(padx=10, pady=10)

# Download Button
download = customtkinter.CTkButton(app, text="Download", command=startDownload)
download.pack(padx=10, pady=10)

# Run App
app.mainloop()
