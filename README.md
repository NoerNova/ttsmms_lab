# Text-to-speech with The Massively Multilingual Speech (MMS) project ([facebookresearch](https://github.com/facebookresearch/fairseq/tree/main/examples/mms))

This project is a TTS-MMS testing lab for study Facebook's TTSMMS project specific to Shan (lang_code: shn) language.

## Install
clone this project
```bash
git clone https://github.com/NoerNova/ttsmms_lab.git
```

```bash 
cd ttsmms_lab
```

```bash
pip install -r requirements.txt
```

download tts model from facebookresearch and extract to ```model/```
```bash
mkdir -p model/ && wget -qO- https://dl.fbaipublicfiles.com/mms/tts/shn.tar.gz | tar -xz -C model/ --strip-components 1
```

## Usage
use this ```shn_tts.py``` file or create a new one
```python
from ttsmms import TTS

tts=TTS("./model/shn")

tts.synthesis("ၼုမ်ႇသိုၵ်းႁၢၼ် ႁဵတ်းၵၢၼ်ၵွၼ်းၶေႃၸိုင်ႈတႆး", wav_path="example2.wav")
# output: example.wav file
```

## Run
```python
python shn_tts.py
```


## License
MIT
