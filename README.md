Music Extraction and Equalization Program (MEEP)
-----------------
Made by PeterTP

MEEP is a batch music (and video) downloading program that is lossless as it does not utilise any codec conversion
Youtube-dl is abandoned and so the much better yt-dlp fork is used
foobar2000 has an added component foo_runcmd
If audio is checked and video is not, technically yt-dlp still downloads the webm but uses ffmpeg to extract it as opus automatically

What it does:
1. Batch file executes the MEEP.py python script
2. Script reads and iterates through urls.txt to invoke command line commands
3. Download files in the form of webm using yt-dlp
4.(If audio checked) Extract the opus audio with ffmpeg from its webm container
5.(If gain is checked) Use foobar2000's replaygain to equalize the loudness of all songs by manipulating opus headers

What to do:
1. Write all web urls into urls.txt, with each url in its own line
2. Double click run.bat
3. Choose the correct settings and click start
4. Profit
(5. Close foobar2000. Auto close does not work very well (especially in large download batches) and is instead minimized to avoid screen clutter)

Settings:
Defaults = [ ✅Download Audio,  ✅Gain Audio ]

Download Audio: Downloads audio from youtube, disables extract to prevent override

Download Video: Downloads video from youtube, check extract audio to get audio as well

Gain Audio: Performs gain on audio files in audio folder

Extract Audio: Extracts audio from video files from video folder to audio folder
