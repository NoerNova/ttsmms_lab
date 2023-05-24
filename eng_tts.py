from ttsmms import TTS

tts = TTS("./model/eng")

tts.synthesis("speech", wav_path="output/example_eng.wav")
# output: output/example_eng.wav file
