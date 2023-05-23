# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import os
import glob
import json
import math
import torch
from torch import nn
from torch.nn import functional as F
from torch.utils.data import DataLoader
import numpy as np
import ttsmms.commons
import ttsmms.utils
import argparse
from ttsmms.data_utils import TextAudioLoader, TextAudioCollate, TextAudioSpeakerLoader, TextAudioSpeakerCollate
from ttsmms.models import SynthesizerTrn
from scipy.io.wavfile import write

class TextMapper(object):
    def __init__(self, vocab_file):
        self.symbols = [x.replace("\n", "") for x in open(vocab_file).readlines()]
        self.SPACE_ID = self.symbols.index(" ")
        self._symbol_to_id = {s: i for i, s in enumerate(self.symbols)}
        self._id_to_symbol = {i: s for i, s in enumerate(self.symbols)}

    def text_to_sequence(self, text, cleaner_names):
        '''Converts a string of text to a sequence of IDs corresponding to the symbols in the text.
        Args:
        text: string to convert to a sequence
        cleaner_names: names of the cleaner functions to run the text through
        Returns:
        List of integers corresponding to the symbols in the text
        '''
        sequence = []
        clean_text = text.strip()
        for symbol in clean_text:
            symbol_id = self._symbol_to_id[symbol]
            sequence += [symbol_id]
        return sequence

    def get_text(self, text, hps):
        text_norm = self.text_to_sequence(text, hps.data.text_cleaners)
        if hps.data.add_blank:
            text_norm = commons.intersperse(text_norm, 0)
        text_norm = torch.LongTensor(text_norm)
        return text_norm

    def filter_oov(self, text):
        val_chars = self._symbol_to_id
        txt_filt = "".join(list(filter(lambda x: x in val_chars, text)))
        # print(f"text after filtering OOV: {txt_filt}")
        return txt_filt

class TTS:
    def __init__(self, model_dir_path: str) -> None:
        self.model_path = model_dir_path
        self.vocab_file = f"{self.model_path}/vocab.txt"
        self.config_file = f"{self.model_path}/config.json"
        assert os.path.isfile(self.config_file), f"{self.config_file} doesn't exist"
        self.hps = ttsmms.utils.get_hparams_from_file(self.config_file)
        self.text_mapper = TextMapper(self.vocab_file)
        self.net_g = SynthesizerTrn(
            len(self.text_mapper.symbols),
            self.hps.data.filter_length // 2 + 1,
            self.hps.train.segment_size // self.hps.data.hop_length,
            **self.hps.model
        )
        _ = self.net_g.eval()

        self.g_pth = f"{self.model_path}/G_100000.pth"
        _ = ttsmms.utils.load_checkpoint(self.g_pth, self.net_g, None)
        self.sampling_rate=self.hps.data.sampling_rate
    def synthesis(self, txt, wav_path=None):
        txt = self.text_mapper.filter_oov(txt)
        stn_tst = self.text_mapper.get_text(txt, self.hps)
        with torch.no_grad():
            x_tst = stn_tst.unsqueeze(0)#.cuda()
            x_tst_lengths = torch.LongTensor([stn_tst.size(0)])#.cuda()
            hyp = self.net_g.infer(
                x_tst, x_tst_lengths, noise_scale=.667,
                noise_scale_w=0.8, length_scale=1.0
            )[0][0,0].cpu().float().numpy()
        if wav_path != None:
            write(wav_path, self.hps.data.sampling_rate, hyp)
            return wav_path
        return {"x":hyp,"sampling_rate":self.sampling_rate}

def generate():
    parser = argparse.ArgumentParser(description='TTS inference')
    parser.add_argument('--model-dir', type=str, help='model checkpoint dir')
    parser.add_argument('--wav', type=str, help='output wav path')
    parser.add_argument('--txt', type=str, help='input text')
    args = parser.parse_args()
    ckpt_dir, wav_path, txt = args.model_dir, args.wav, args.txt

    vocab_file = f"{ckpt_dir}/vocab.txt"
    config_file = f"{ckpt_dir}/config.json"
    assert os.path.isfile(config_file), f"{config_file} doesn't exist"
    hps = ttsmms.utils.get_hparams_from_file(config_file)
    text_mapper = TextMapper(vocab_file)
    net_g = SynthesizerTrn(
        len(text_mapper.symbols),
        hps.data.filter_length // 2 + 1,
        hps.train.segment_size // hps.data.hop_length,
        **hps.model)
    net_g#.cuda()
    _ = net_g.eval()

    g_pth = f"{ckpt_dir}/G_100000.pth"
    # print(f"load {g_pth}")

    _ = utils.load_checkpoint(g_pth, net_g, None)

    # print(f"text: {txt}")
    txt = txt.lower()
    txt = text_mapper.filter_oov(txt)
    stn_tst = text_mapper.get_text(txt, hps)
    with torch.no_grad():
        x_tst = stn_tst.unsqueeze(0)#.cuda()
        x_tst_lengths = torch.LongTensor([stn_tst.size(0)])#.cuda()
        hyp = net_g.infer(
            x_tst, x_tst_lengths, noise_scale=.667,
            noise_scale_w=0.8, length_scale=1.0
        )[0][0,0].cpu().float().numpy()

    os.makedirs(os.path.dirname(wav_path), exist_ok=True)
    # print(f"wav: {wav_path}")
    write(wav_path, hps.data.sampling_rate, hyp)
    return


if __name__ == '__main__':
    generate()
