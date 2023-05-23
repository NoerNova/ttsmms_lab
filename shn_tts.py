from ttsmms import TTS

tts=TTS("./model/shn")

tts.synthesis("ၼုမ်ႇသိုၵ်းႁၢၼ် ႁဵတ်းၵၢၼ်ၵွၼ်းၶေႃၸိုင်ႈတႆး", wav_path="example2.wav")
# output: example.wav file
