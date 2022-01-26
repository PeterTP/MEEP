# Imports
import os
import time
from tkinter import *

# Directories
FFMPEG = "programs\\ffmpeg\\bin\\ffmpeg.exe"
YT_DLP = "programs\\ffmpeg\\bin\\yt-dlp.exe"
FOOBAR = "programs\\foobar2000\\foobar2000.exe"
VIDEO = "videos"
AUDIO = "audios"
ALARM = "programs\\alarm.opus"

# Check if directories exist
if not os.path.exists(VIDEO):
    os.mkdir(VIDEO)
if not os.path.exists(AUDIO):
    os.mkdir(AUDIO)

# Settings Dict
settings = {}

# Functions
def apply():  # If none of the options are checked, the default is used
    if audio_option.get() or video_option.get() or gain_option.get() or extract_option.get():
        settings.update({
            "audio": audio_option.get(),
            "video": video_option.get(),
            "gain": gain_option.get(),
            "extract": extract_option.get()
        })
    else:
        settings.update({
            "audio": 1,
            "video": 0,
            "gain": 1,
            "extract": 0
        })
    gui.destroy()


def download_check():
    if video_option.get():
        audio_checkbox.config(state="disabled")
        if audio_option.get():
            extract_checkbox.config(state="normal")
            extract_option.set(1)
        audio_option.set(0)
    else:
        audio_checkbox.config(state="normal")


def audio_check():
    if audio_option.get():
        extract_checkbox.config(state="disabled")
        extract_option.set(0)
    else:
        extract_checkbox.config(state="normal")


# Initializing program
print("\nMEEP is commencing its operations")

# Creating GUI
gui = Tk()
gui.title("MEEP")
# gui.geometry("505x215")
gui.rowconfigure(0, weight=1)
gui.columnconfigure(0, weight=1)

top_frame = Frame(gui, padx=16, pady=8, bg="#CCCCCC",
                  highlightbackground="#DDDDDD", highlightthickness=3)
top_frame.grid(row=0, column=0, sticky="NSEW")

label_title = Label(top_frame, justify=LEFT, bg="#CCCCCC", text="Settings:")
label_title.config(font=("Tahoma", 16))
label_title.grid(row=0, column=0, sticky="W")
label = Label(top_frame, justify=LEFT, bg="#CCCCCC", text=(
    "Defaults = [ ✅Download Audio,  ✅Gain Audio ]\n"
   	"Download Audio:	Downloads audios from youtube. 'Extract Audio' disabled to avoid override\n"
   	"Download Video:	Downloads videos from youtube. If you want audio, check 'Extract Audio'\n"
   	"Gain Audio:	Performs gain on audios in 'audios' folder, no downloads needed\n"
    "Extract Audio:	Extracts audio from videos in 'videos' folder to 'audios' folder, no downloads needed"
))
label.config(font=("Arial", 12))
label.grid(row=1, column=0)

bottom_frame = Frame(gui, padx=16, pady=8)
bottom_frame.grid(row=1, column=0, sticky="NSEW")
bottom_frame.rowconfigure(0, weight=1)
bottom_frame.columnconfigure(0, weight=1)
bottom_frame.columnconfigure(1, weight=1)
bottom_frame.columnconfigure(2, weight=1)
bottom_frame.columnconfigure(3, weight=1)

audio_option = IntVar(value=1)
extract_option = IntVar(value=0)
video_option = IntVar(value=0)
gain_option = IntVar(value=1)

audio_checkbox = Checkbutton(bottom_frame, justify=LEFT, onvalue=1, offvalue=0,
                             text="Download Audio", variable=audio_option, command=audio_check)
audio_checkbox.config(font=("Arial", 11))
audio_checkbox.grid(row=0, column=0, sticky="W")
video_checkbox = Checkbutton(bottom_frame, justify=LEFT, onvalue=1, offvalue=0,
                             text="Download Video", variable=video_option, command=download_check)
video_checkbox.config(font=("Arial", 11))
video_checkbox.grid(row=0, column=1, sticky="W")
gain_checkbox = Checkbutton(bottom_frame, justify=LEFT, onvalue=1,
                            offvalue=0, text="Gain Audio", variable=gain_option)
gain_checkbox.config(font=("Arial", 11))
gain_checkbox.grid(row=1, column=0, sticky="W")
extract_checkbox = Checkbutton(bottom_frame, justify=LEFT, onvalue=1,
                               offvalue=0, text="Extract Audio", variable=extract_option)
extract_checkbox.config(font=("Arial", 11), state="disabled")
extract_checkbox.grid(row=1, column=1, sticky="W")

button = Button(bottom_frame, text="Start", width=25, height=1, command=apply)
button.grid(row=0, column=3, rowspan=2, pady=3, sticky="NSEW")
gui.mainloop()

initial_time = time.time()
print("\n" + time.ctime(initial_time) + "\n")

# Opening and processing urls
file = open("urls.txt", "r").readlines()
urls = []
for e in file:
    urls.append(e.strip())  # \n stripped for each line
    print(e.strip())

if settings:
    # Downloading url files
    if settings["video"]:  # If Video option checked
        print("\nMEEP is downloading video files")
        i = 1
        for e in urls:  # Tell yt-dlp to output to VIDEO and download the file with the best audio from available formats
            print("\nDownload no.: " + str(i))
            print("\nTotal time passed in seconds "
                  + str(time.time()-initial_time))  # Print time passed
            command_v = YT_DLP + " -o " + VIDEO + \
                "\\%(title)s.%(ext)s -f bestvideo+bestaudio " + e
            print("\nMEEP executed the command:\n" + command_v + "\n")
            os.system(command_v)
            print("\nMEEP completed a download")
            i += 1
    if settings["audio"]:  # If Audio option checked
        print("\nMEEP is downloading audio files")
        i = 1
        for e in urls:  # Tell yt-dlp to output to AUDIO and download the file with the best audio from available formats
            print("\nDownload no." + str(i))
            print("\nTotal time passed in seconds "
                  + str(time.time()-initial_time))  # Print time passed
            command_a = YT_DLP + " -o " + AUDIO + \
                "\\%(title)s.%(ext)s -x -f bestaudio " + e
            print("\nMEEP executed the command:\n" + command_a + "\n")
            os.system(command_a)
            print("\nMEEP completed a download")
            i += 1
    if settings["extract"]:  # Extract audio from video
        print("\nMEEP is extracting audio from videos")
        videos = os.listdir(VIDEO)
        for e in videos:  # Tell ffmpeg to say yes to overwrite, input VIDEO, no video stream and copy audio without compression
            # This was the fastest out of 12 different methods for ext removal (worst was regex)
            filename = e[:-len(e.split('.')[-1])-1]
            command_e = FFMPEG + " -y -i \"" + VIDEO + "\\" + e + \
                "\" -vn -acodec copy \"" + AUDIO + "\\" + filename + ".opus\""
            print("\nMEEP executed the command:\n" + command_e + "\n")
            os.system(command_e)
    if settings["gain"]:  # Tells foobar2000 to use the runcmd component to execute manipulate opus header gain. Thank god runcmd exists
        command_g = "start /min " + FOOBAR + \
            " /runcmd-files=\"ReplayGain/Manipulate Opus header gain (no prompt, use last settings)\" " + AUDIO
        print("\nMEEP executed the command:\n" + command_g)
        os.system(command_g)
        print("\nMEEP is applying gain to audio files")
else:
    print("\nMEEP will exit without doing anything")

# End
print("\nMEEP has completed its downloads and played a sound to alert you! Note: This does not mean gain is completed")
os.system("start /min " + ALARM)  # Oi its done
print("\nTotal time passed in seconds "
      + str(time.time()-initial_time))  # Print time passed