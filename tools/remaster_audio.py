#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'videos'; OUT=ROOT/'videos-enhanced'; OUT.mkdir(exist_ok=True)
PRE='highpass=f=75,lowpass=f=9800,equalizer=f=2400:t=q:w=1.1:g=1.4,equalizer=f=5200:t=q:w=1.0:g=-1.0,deesser=i=0.08:m=0.35:f=0.55,acompressor=threshold=0.10:ratio=1.8:attack=25:release=220:makeup=1.15'

def run(cmd,capture=False):
    return subprocess.run(cmd,check=True,text=True,stdout=subprocess.PIPE if capture else None,stderr=subprocess.PIPE if capture else None)

def analyse(src):
    p=run(['ffmpeg','-hide_banner','-nostats','-i',str(src),'-map','0:a:0','-af',PRE+',loudnorm=I=-16:LRA=6:TP=-1.5:print_format=json','-f','null','-'],capture=True)
    m=re.search(r'\{\s*"input_i".*?\}',p.stderr,re.S)
    if not m: raise RuntimeError('loudnorm analysis missing')
    return json.loads(m.group(0))

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--part',type=int,action='append'); a=ap.parse_args()
    results=[]
    sources=sorted(SRC.glob('RCC_Onboarding_Part_*_Video.mp4'))
    if a.part:
        sources=[p for p in sources if any(f'Part_{n}_' in p.name for n in a.part)]
    for src in sources:
        data=analyse(src)
        ln=("loudnorm=I=-16:LRA=6:TP=-1.5:linear=true:"+
            f"measured_I={data['input_i']}:measured_LRA={data['input_lra']}:"+
            f"measured_TP={data['input_tp']}:measured_thresh={data['input_thresh']}:offset={data['target_offset']}")
        out=OUT/(src.stem+'_Enhanced.mp4')
        subprocess.run(['ffmpeg','-y','-hide_banner','-i',str(src),'-map','0:v:0','-map','0:a:0','-map','0:s?','-c:v','copy','-c:s','copy','-af',PRE+','+ln,'-c:a','aac','-b:a','160k','-ar','48000','-movflags','+faststart',str(out)],check=True)
        results.append({'source':src.name,'output':out.name,'input_lufs':data['input_i'],'target_lufs':-16,'true_peak_target_dbtp':-1.5})
    (OUT/'audio-remaster-report.json').write_text(json.dumps(results,indent=2)+'\n')
if __name__=='__main__': main()
