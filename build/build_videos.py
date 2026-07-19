#!/usr/bin/env python3
import json, os, re, subprocess, math, wave, glob, shutil, textwrap
from pathlib import Path

ROOT=Path('/mnt/data/rcc-curriculum-v2')
VIDEOS=ROOT/'videos'; AUDIO=ROOT/'audio'; CAP=ROOT/'captions'; WORK=ROOT/'video_work'
for d in [VIDEOS,AUDIO,CAP,WORK]: d.mkdir(parents=True,exist_ok=True)

ACCENTS={1:'007C83',2:'2C6EAF',3:'D15B47',4:'7057A3'}

REPL=[
 (r'\bRCC\b','R C C'), (r'\bSSH\b','S S H'), (r'\bVS Code\b','V S Code'),
 (r'\bSlurm\b','slurm'), (r'\bSnakemake\b','snake make'), (r'\btmux\b','tee mux'),
 (r'\bMiniforge\b','mini forge'), (r'\bBioconda\b','bio conda'), (r'\bApptainer\b','app tainer'),
 (r'\bSIF\b','S I F'), (r'\bI/O\b','I O'), (r'\bIOPS\b','I O operations per second'),
 (r'\bCPU\b','C P U'), (r'\bCPUs\b','C P Us'), (r'\bGPU\b','G P U'), (r'\bGPUs\b','G P Us'),
 (r'\bRAM\b','ram'), (r'\bFASTQ\.gz\b','fast Q dot G Z'), (r'\bFASTQ\b','fast Q'),
 (r'\bFASTA\b','fast A'), (r'\bBAM\b','bam'), (r'\bCRAM\b','C ram'), (r'\bVCF\.gz\b','V C F dot G Z'),
 (r'\bVCF\b','V C F'), (r'\bSHA-256\b','S H A two fifty six'), (r'\bMaxRSS\b','max R S S'),
 (r'\bsacct\b','S acct'), (r'\bsstat\b','S stat'), (r'\bsbatch\b','S batch'), (r'\bsqueue\b','S queue'),
 (r'\bnvidia-smi\b','N V I D I A S M I'), (r'\bTMPDIR\b','temp directory'),
 (r'\bDAG\b','D A G'), (r'\bGit\b','git'), (r'\bHPC\b','H P C'),
 (r'--nv','dash dash N V'), (r'--cleanenv','dash dash clean env'), (r'\bconda\b','conda'),
]

def speech_text(text):
    t=text.replace('→',' leads to ').replace('·',', ').replace('–','-').replace('—',' - ')
    t=t.replace('`','').replace('“','').replace('”','').replace('’',"'")
    for p,r in REPL: t=re.sub(p,r,t,flags=re.I if p in [r'\bSlurm\b',r'\bSnakemake\b',r'\btmux\b',r'\bMiniforge\b',r'\bBioconda\b',r'\bApptainer\b'] else 0)
    t=re.sub(r'\s+',' ',t).strip()
    return t

def run(cmd, **kw):
    subprocess.run(cmd,check=True,stdout=kw.pop('stdout',subprocess.DEVNULL),stderr=kw.pop('stderr',subprocess.DEVNULL),**kw)

def duration(path):
    out=subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(path)],text=True)
    return float(out.strip())

def srt_time(sec):
    ms=int(round(sec*1000)); h=ms//3600000; ms%=3600000; m=ms//60000; ms%=60000; s=ms//1000; ms%=1000
    return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'

def caption_chunks(text,max_words=19):
    sentences=re.split(r'(?<=[.!?])\s+',text.strip())
    chunks=[]
    for sent in sentences:
        words=sent.split()
        while len(words)>max_words:
            cut=max_words
            # Prefer a punctuation boundary near the end.
            for j in range(max_words-3,max_words+1):
                if j<len(words) and words[j-1].endswith((',',':',';')): cut=j; break
            chunks.append(' '.join(words[:cut])); words=words[cut:]
        if words: chunks.append(' '.join(words))
    return chunks or [text]

def make_audio(part, slide, text, outdir):
    raw=outdir/f'slide_{slide:02d}_raw.wav'; final=outdir/f'slide_{slide:02d}.wav'; txt=outdir/f'slide_{slide:02d}.txt'
    if final.exists(): return final
    txt.write_text(speech_text(text),encoding='utf-8')
    # Clear British synthetic voice with conservative pacing. Sentence punctuation
    # remains in the source, while SoX adds EQ, compression, normalization, and pauses.
    run(['espeak','-v','en-uk-rp','-s','170','-p','43','-a','170','-f',str(txt),'-w',str(raw)])
    run(['sox',str(raw),'-r','48000','-c','1',str(final),
         'vol','0.58','highpass','75','lowpass','10500',
         'equalizer','180','0.8q','-2','equalizer','2600','1.1q','2.2',
         'compand','0.02,0.20','-60,-60,-20,-13,-8,-6','0','-90','0.1',
         'norm','-2.0','pad','0.32','0.65'])
    raw.unlink(missing_ok=True)
    return final

def make_segment(img,audio,out,accent,dur):
    # Slide-based training video. A low frame rate is sufficient for static instructional material.
    vf=(
      "scale=1280:720,"
      f"drawbox=x=0:y=714:w='min(1280,1280*t/{dur:.3f})':h=6:color=0x{accent}@0.88:t=fill,"
      "format=yuv420p"
    )
    run(['ffmpeg','-y','-loop','1','-framerate','2','-i',str(img),'-i',str(audio),
         '-vf',vf,'-t',f'{dur:.3f}','-r','2','-c:v','libx264','-preset','ultrafast','-tune','stillimage','-crf','23',
         '-c:a','aac','-aac_coder','fast','-b:a','144k','-ar','48000','-shortest',str(out)])

def build_part(part):
    narr=json.load(open(ROOT/'narration'/f'RCC_Onboarding_Part_{part}_Narration.json'))
    slide_dir=ROOT/'qa_slides'/f'part{part}'
    work=WORK/f'part{part}'; shutil.rmtree(work,ignore_errors=True); work.mkdir(parents=True)
    audiodir=AUDIO/f'part{part}'; audiodir.mkdir(parents=True,exist_ok=True)
    entries=[]; timeline=0.0; audio_files=[]; slide_specs=[]
    for item in narr:
        idx=item['slide']; audio=make_audio(part,idx,item['text'],audiodir); dur=duration(audio)
        audio_files.append(audio)
        slide_specs.append((slide_dir/f'slide-{idx}.png',dur))
        chunks=caption_chunks(item['text']); counts=[max(1,len(c.split())) for c in chunks]; total=sum(counts)
        local=0.0
        for c,n in zip(chunks,counts):
            cdur=dur*n/total
            entries.append((timeline+local,timeline+local+cdur,c))
            local+=cdur
        timeline+=dur
    # Concatenate identical PCM WAV files without re-encoding.
    alist=work/'audio_concat.txt'
    alist.write_text('\n'.join(f"file '{a}'" for a in audio_files)+'\n')
    full_audio=work/f'part{part}_narration.wav'
    run(['ffmpeg','-y','-f','concat','-safe','0','-i',str(alist),'-c','copy',str(full_audio)])
    # Build a variable-frame-rate slideshow. Each PNG is one video frame held for
    # the exact duration of its corresponding narration segment.
    ilist=work/'images_concat.txt'
    lines=[]
    for img,dur in slide_specs:
        lines.append(f"file '{img}'")
        lines.append(f'duration {dur:.6f}')
    lines.append(f"file '{slide_specs[-1][0]}'")
    ilist.write_text('\n'.join(lines)+'\n')
    out=VIDEOS/f'RCC_Onboarding_Part_{part}_Video.mp4'
    lastdur=slide_specs[-1][1]
    vf=f'fps=1,scale=1280:720:flags=lanczos,tpad=stop_mode=clone:stop_duration={lastdur:.6f},format=yuv420p'
    run(['ffmpeg','-y','-f','concat','-safe','0','-i',str(ilist),'-i',str(full_audio),
         '-vf',vf,'-fps_mode','vfr','-c:v','libx264','-preset','veryfast','-tune','stillimage','-crf','20',
         '-c:a','aac','-aac_coder','fast','-b:a','144k','-ar','48000','-t',f'{timeline:.3f}','-movflags','+faststart',str(out)])
    srt=CAP/f'RCC_Onboarding_Part_{part}_Captions.srt'
    with open(srt,'w',encoding='utf-8') as f:
        for i,(st,en,tx) in enumerate(entries,1):
            f.write(f'{i}\n{srt_time(st)} --> {srt_time(en)}\n{tx}\n\n')
    return out,timeline,srt

import sys
parts=[int(x) for x in sys.argv[1:]] if len(sys.argv)>1 else [1,2,3,4]
summary=[]
for p in parts:
    out,dur,srt=build_part(p); summary.append((p,out,dur,srt)); print(f'Part {p}: {dur/60:.2f} min -> {out}', flush=True)
# Merge current summaries with any existing entries.
sp=ROOT/'meta'/'video_summary.json'
existing=[]
if sp.exists():
    try: existing=json.loads(sp.read_text())
    except Exception: existing=[]
by={int(x['part']):x for x in existing}
for p,o,d,srt in summary: by[p]={'part':p,'video':str(o),'duration_seconds':d,'captions':str(srt)}
sp.write_text(json.dumps([by[k] for k in sorted(by)],indent=2))
