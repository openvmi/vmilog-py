import subprocess

def startMpegStream(width, height, frameRate, url):
    _ffmpegStream = [
        'ffmpeg',
        '-f', 'rawvideo',
        '-pixel_format', 'bgr24',
        '-video_size', '{}x{}'.format(width, height),
        '-framerate',str(frameRate),
        '-i', '-',
        '-f', 'mpegts',
        '-codec:v', 'mpeg1video',
        '-bf', '0',
        url
    ]
    p = subprocess.Popen(_ffmpegStream, stdin=subprocess.PIPE)
    return p
    