import soundfile as sf
import os


inputfile = "/jimmy/data/train_wavernn/hts/"
outputfile = "/jimmy/data/train_wavernn/hts/"

raw_name = os.listdir(inputfile)

for raw in raw_name:
    signal, osr = sf.read(os.path.join(inputfile, raw), subtype="PCM_16", channels=1, samplerate=48000, endian="LITTLE")
    sf.write(os.path.join(inputfile, raw[:-4] + ".wav"), signal, samplerate=osr)
