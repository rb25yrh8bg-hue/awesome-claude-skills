#!/usr/bin/env python3
"""Minimal WhisperX-compatible CLI backed by faster-whisper (CPU, no torch)."""
import argparse, json, os, sys
p = argparse.ArgumentParser()
p.add_argument('audio'); p.add_argument('--model', default='small'); p.add_argument('--device', default='cpu')
p.add_argument('--compute_type', default='int8'); p.add_argument('--batch_size', default='8'); p.add_argument('--output_dir', default='.')
p.add_argument('--output_format', default='json'); p.add_argument('--task', default='transcribe'); p.add_argument('--language', default=None)
p.add_argument('--no_align', action='store_true'); p.add_argument('--vad_method', default=None); p.add_argument('--verbose', default='False')
a = p.parse_args()
from faster_whisper import WhisperModel
ct = 'int8' if a.compute_type == 'default' else a.compute_type
m = WhisperModel(a.model, device=a.device, compute_type=ct)
segs, info = m.transcribe(a.audio, language=a.language, vad_filter=True)
out = [{'start': round(s.start, 2), 'end': round(s.end, 2), 'text': s.text.strip()} for s in segs]
stem = os.path.splitext(os.path.basename(a.audio))[0]
with open(os.path.join(a.output_dir, stem + '.json'), 'w', encoding='utf-8') as f:
    json.dump({'segments': out, 'language': info.language}, f, ensure_ascii=False)
