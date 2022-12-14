# https://swharden.com/blog/2016-07-19-realtime-audio-visualization-in-python/

import pyaudio
import numpy as np

CHUNK = 2**11
print(CHUNK)
RATE = 44100

p = pyaudio.PyAudio()
stream = p.open(
    format=pyaudio.paInt16, channels=2, rate=RATE, input=True, frames_per_buffer=CHUNK
)

for i in range(int(10 * 44100 / 1024)):  # go for a few seconds
    data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
    peak = np.average(np.abs(data)) * 2
    bars = "#" * int(50 * peak / 2**16)
    print("%04d %05d %s" % (i, peak, bars))

stream.stop_stream()
stream.close()
p.terminate()
