from ttsmms import TTS
from ftlangdetect import detect
from pydub import AudioSegment
import numpy as np

shn_model = TTS("./model/shn")
eng_model = TTS("./model/eng")

text = "ၸၢမ်းတူၺ်း this is english word လိၵ်ႈတႆး"
text2 = "english letter containe english word english word"
text3 = "ၵူၼ်းဢမ်ႇမီးႁိူၼ်းတၢႆထပ်းၵၼ်ဝၼ်းလဵဝ်ဢမ်ႇယွမ်း သၢမ်ၵေႃႉတီႈဝဵင်းလႃႈသဵဝ်ႈ"
text4 = "ငဝ်ႈငုၼ်းၶွင်ႇသီႇဢဝ်ၶိုၼ်းၸိုင်ႈတႆး RCSS-SSA လႄႈ ပႃႇတီႇမႂ်ႇသုင်ၸိုင်ႈတႆး တပ်ႉသိုၵ်းၸိုင်ႈတႆး SSPP/SSA"

sentences = text4.split()

audio_segments = []
synthesis_vector = []

for sentence in sentences:
    language = detect(sentence)

    if language["lang"] == "en":
        tts = eng_model
    else:
        tts = shn_model

    tts_output = tts.synthesis(sentence)

    audio_data = tts_output["x"]
    sampling_rate = tts_output["sampling_rate"]

    audio_array = np.array(audio_data * 32767, dtype=np.int16)
    audio_segment = AudioSegment(
        audio_array.tobytes(), frame_rate=sampling_rate, sample_width=2, channels=1
    )
    audio_segments.append(audio_segment)

# combined the audio
combined_audio = sum(audio_segments)

# export
combined_audio.export("output/output4.wav", format="wav")
