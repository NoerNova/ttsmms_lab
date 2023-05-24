# Text-to-speech with The Massively Multilingual Speech (MMS) project ([facebookresearch](https://github.com/facebookresearch/fairseq/tree/main/examples/mms))

This project is a TTS-MMS testing lab for study Facebook's TTSMMS project specific to Shan (lang_code: shn) language.

## Install
clone this project
```bash
git clone https://github.com/haohaaorg/ttsmms_lab.git
```

```bash 
cd ttsmms_lab
```

```bash
pip install -r requirements.txt
```

download tts model from facebookresearch and extract to ```model/```
```bash
mkdir -p model/shn/ && wget -qO- https://dl.fbaipublicfiles.com/mms/tts/shn.tar.gz | tar -xz -C model/shn/ --strip-components 1
```

## Usage
use this [shn_tts.py](https://github.com/haohaaorg/ttsmms_lab/blob/main/shn_tts.py) file or create a new one for using Shan's language model
```python
from ttsmms import TTS

tts=TTS("./model/shn")

tts.synthesis("ၼုမ်ႇသိုၵ်းႁၢၼ် ႁဵတ်းၵၢၼ်ၵွၼ်းၶေႃၸိုင်ႈတႆး", wav_path="output/example_shn.wav")
# output: output/example_shn.wav file
```

use this [eng_tts.py](https://github.com/haohaaorg/ttsmms_lab/blob/main/eng_tts.py) file file or create a new one for using English's language model
```python
from ttsmms import TTS

tts = TTS("./model/eng")

tts.synthesis("speech", wav_path="output/example_eng.wav")
# output: output/example_eng.wav file
```

#### or with combine 2 model, as this is a pre-train model which may not support all text or words the idea is to use both english and shan model for multilang in single line text

* [shn_tts_combined.py](https://github.com/haohaaorg/ttsmms_lab/blob/main/shn_tts_combined.py)
  
**don't forget to download english model from**
```bash
 mkdir -p model/eng/ && wget -qO- https://dl.fbaipublicfiles.com/mms/tts/eng.tar.gz | tar -xz -C model/eng/ --strip-components 1
```

## Run
```python
python shn_tts.py

# python eng_tts.py
# python shn_tts_combined.py
```


## License
MIT
