from ttsmms import TTS

tts = TTS("./model/shn")

tts.synthesis(
    "သမ်ႇမႃႇၵျၢမ်းလိၵ်ႈ ထႃႇဝရႃႉၽြႃး ထမ်းမၽြႃးပဵၼ်ၸဝ်ႈ",
    wav_path="output/example_shn2.wav",
)
# output: output/example_shn.wav file
