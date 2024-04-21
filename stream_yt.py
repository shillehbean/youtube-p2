import subprocess
from picamera import PiCamera
from time import sleep

## Author: Mahmood Mustafa Youssef Shilleh
## DONATE AT: https://buymeacoffee.com/mmshilleh

RESOLUTION = (640, 480)  # Can be adjusted based on your needs
FRAMERATE = 24           # Adjust this based on your camera's capabilities

# YouTube Stream URL and Key
YOUTUBE_URL = "rtmp://a.rtmp.youtube.com/live2"
YOUTUBE_KEY = "your live stream key"  # Replace with your actual YouTube stream key

# Construct the FFmpeg command for streaming
stream_cmd = f'ffmpeg -ar 44100 -ac 2 -acodec pcm_s16le -f s16le -ac 2 -i /dev/zero -f h264 -i - -vcodec copy -acodec aac -ab 128k -g 50 -strict experimental -f flv {YOUTUBE_URL}/{YOUTUBE_KEY}'

# Initialize the camera
camera = PiCamera(resolution=RESOLUTION, framerate=FRAMERATE)
camera.start_preview()
sleep(2)  # Camera warm-up time

# Start the streaming subprocess
stream_pipe = subprocess.Popen(stream_cmd, shell=True, stdin=subprocess.PIPE)

# Start recording and streaming
camera.start_recording(stream_pipe.stdin, format='h264')

try:
    while True:
        sleep(60)
except KeyboardInterrupt:
    # Stop recording upon receiving a keyboard interrupt (Ctrl+C)
    camera.stop_recording()

# Clean up the resources
stream_pipe.stdin.close()
stream_pipe.wait()
camera.close()
