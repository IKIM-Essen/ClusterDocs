#!/usr/bin/env python3
"""Build narrated RCC class videos from committed slide frames and Markdown.

The default speech backend is the macOS ``say`` synthesizer with the British
English Daniel voice.  Audio is mastered with ffmpeg and captions are generated
from the unmodified narration text.  No production RCC service is contacted.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FRAMES = ROOT / "slides" / "frames"
NARRATION = ROOT / "narration"
CAPTIONS = ROOT / "captions"
OUTPUT = ROOT / "videos-enhanced"
REPORT = ROOT / "meta" / "video-build-report.json"

VOICE = "Daniel"
RATE = 172

PRONUNCIATION = [
    (r"\bRCC\b", "R C C"),
    (r"\bSSH\b", "S S H"),
    (r"\bVS Code\b", "Visual Studio Code"),
    (r"\bSlurm\b", "slurm"),
    (r"\bSnakemake\b", "snake make"),
    (r"\btmux\b", "tee mux"),
    (r"\bMiniforge\b", "mini forge"),
    (r"\bBioconda\b", "bio conda"),
    (r"\bApptainer\b", "app tainer"),
    (r"\bSIF\b", "S I F"),
    (r"\bI/O\b", "I O"),
    (r"\bIOPS\b", "I O operations per second"),
    (r"\bCPU\b", "C P U"),
    (r"\bCPUs\b", "C P Us"),
    (r"\bGPU\b", "G P U"),
    (r"\bGPUs\b", "G P Us"),
    (r"\bRAM\b", "ram"),
    (r"\bFASTQ\.gz\b", "fast Q dot G Z"),
    (r"\bFASTQ\b", "fast Q"),
    (r"\bFASTA\b", "fast A"),
    (r"\bBAM\b", "bam"),
    (r"\bCRAM\b", "C ram"),
    (r"\bVCF\.gz\b", "V C F dot G Z"),
    (r"\bVCF\b", "V C F"),
    (r"\bSHA-256\b", "S H A two fifty six"),
    (r"\bMaxRSS\b", "max R S S"),
    (r"\bsacct\b", "S acct"),
    (r"\bsstat\b", "S stat"),
    (r"\bsbatch\b", "S batch"),
    (r"\bsqueue\b", "S queue"),
    (r"\bnvidia-smi\b", "N V I D I A S M I"),
    (r"\bTMPDIR\b", "temp directory"),
    (r"\bDAG\b", "D A G"),
    (r"--nv", "dash dash N V"),
    (r"--cleanenv", "dash dash clean env"),
]


def run(command: list[str], *, capture: bool = False) -> str:
    result = subprocess.run(
        command,
        check=True,
        text=True,
        stdout=subprocess.PIPE if capture else subprocess.DEVNULL,
        stderr=subprocess.PIPE if capture else subprocess.DEVNULL,
    )
    return result.stdout


def require(command: str) -> None:
    if not shutil.which(command):
        raise SystemExit(f"Required command not found: {command}")


def parse_narration(path: Path) -> list[dict[str, object]]:
    text = path.read_text(encoding="utf-8")
    matches = list(re.finditer(r"^## Slide (\d+):\s*(.+)$", text, re.MULTILINE))
    slides: list[dict[str, object]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        body = text[match.end() : end].strip()
        body = re.sub(r"\s+", " ", body)
        slides.append({"slide": int(match.group(1)), "title": match.group(2), "text": body})
    if not slides:
        raise ValueError(f"No slide narration found in {path}")
    return slides


def speech_text(text: str) -> str:
    value = (
        text.replace("→", " leads to ")
        .replace("·", ", ")
        .replace("–", "-")
        .replace("—", " - ")
        .replace("`", "")
        .replace("“", "")
        .replace("”", "")
        .replace("’", "'")
    )
    for pattern, replacement in PRONUNCIATION:
        value = re.sub(pattern, replacement, value, flags=re.IGNORECASE)
    # A short, explicit pause between sentences avoids the rushed cadence common
    # to unedited text-to-speech while retaining natural within-sentence rhythm.
    value = re.sub(r"(?<=[.!?])\s+", " [[slnc 190]] ", value)
    return re.sub(r"\s+", " ", value).strip()


def duration(path: Path) -> float:
    value = run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=nw=1:nk=1",
            str(path),
        ],
        capture=True,
    )
    return float(value.strip())


def srt_time(seconds: float) -> str:
    milliseconds = int(round(seconds * 1000))
    hours, milliseconds = divmod(milliseconds, 3_600_000)
    minutes, milliseconds = divmod(milliseconds, 60_000)
    secs, milliseconds = divmod(milliseconds, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"


def caption_chunks(text: str, max_words: int = 16) -> list[str]:
    chunks: list[str] = []
    for sentence in re.split(r"(?<=[.!?])\s+", text.strip()):
        words = sentence.split()
        while len(words) > max_words:
            cut = max_words
            for candidate in range(max_words - 4, max_words + 1):
                if words[candidate - 1].endswith((",", ":", ";")):
                    cut = candidate
                    break
            chunks.append(" ".join(words[:cut]))
            words = words[cut:]
        if words:
            chunks.append(" ".join(words))
    return chunks


def synthesize(text: str, output: Path, voice: str, rate: int) -> None:
    raw = output.with_suffix(".aiff")
    run(["say", "-v", voice, "-r", str(rate), "-o", str(raw), speech_text(text)])
    if raw.stat().st_size < 8192:
        raw.unlink(missing_ok=True)
        raise RuntimeError(
            "macOS speech synthesis returned no audio. Run this build in a "
            "normal Terminal session (not a restricted sandbox) and try again."
        )
    # Speech-focused cleanup followed by broadcast-style loudness normalization.
    filters = (
        "highpass=f=75,lowpass=f=10500,"
        "deesser=i=0.22:m=0.45:f=0.5,"
        "acompressor=threshold=0.10:ratio=2.2:attack=18:release=180:makeup=1.5,"
        "loudnorm=I=-16:LRA=7:TP=-1.5,"
        "apad=pad_dur=0.55"
    )
    run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(raw),
            "-af",
            filters,
            "-ar",
            "48000",
            "-ac",
            "1",
            "-c:a",
            "pcm_s24le",
            str(output),
        ]
    )
    raw.unlink()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def build_part(part: int, voice: str, rate: int, keep_work: bool) -> dict[str, object]:
    slides = parse_narration(NARRATION / f"RCC_Onboarding_Part_{part}_Narration.md")
    frame_dir = FRAMES / f"part{part}"
    expected = [frame_dir / f"slide-{int(item['slide']):02d}.png" for item in slides]
    missing = [str(path) for path in expected if not path.exists()]
    if missing:
        raise SystemExit("Missing committed video frame(s): " + ", ".join(missing))

    work_parent = ROOT / "video-work" if keep_work else None
    if work_parent:
        work_parent.mkdir(exist_ok=True)
        work = work_parent / f"part{part}"
        shutil.rmtree(work, ignore_errors=True)
        work.mkdir()
        cleanup = None
    else:
        cleanup = tempfile.TemporaryDirectory(prefix=f"rcc-video-part{part}-")
        work = Path(cleanup.name)

    audio_files: list[Path] = []
    slide_durations: list[float] = []
    caption_entries: list[tuple[float, float, str]] = []
    timeline = 0.0
    for item in slides:
        number = int(item["slide"])
        audio = work / f"slide-{number:02d}.wav"
        synthesize(str(item["text"]), audio, voice, rate)
        seconds = duration(audio)
        audio_files.append(audio)
        slide_durations.append(seconds)
        chunks = caption_chunks(str(item["text"]))
        weights = [max(1, len(chunk.split())) for chunk in chunks]
        local = 0.0
        for chunk, weight in zip(chunks, weights):
            chunk_duration = seconds * weight / sum(weights)
            caption_entries.append((timeline + local, timeline + local + chunk_duration, chunk))
            local += chunk_duration
        timeline += seconds

    audio_list = work / "audio.txt"
    audio_list.write_text("\n".join(f"file '{path}'" for path in audio_files) + "\n")
    full_audio = work / "narration.wav"
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(audio_list), "-c", "copy", str(full_audio)])

    image_list = work / "frames.txt"
    lines: list[str] = []
    for frame, seconds in zip(expected, slide_durations):
        lines.extend((f"file '{frame}'", f"duration {seconds:.6f}"))
    lines.append(f"file '{expected[-1]}'")
    image_list.write_text("\n".join(lines) + "\n")

    OUTPUT.mkdir(exist_ok=True)
    video = OUTPUT / f"RCC_Onboarding_Part_{part}_Video_Enhanced.mp4"
    run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(image_list),
            "-i",
            str(full_audio),
            "-vf",
            "fps=2,scale=1280:720:flags=lanczos,format=yuv420p",
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-tune",
            "stillimage",
            "-crf",
            "20",
            "-c:a",
            "aac",
            "-b:a",
            "160k",
            "-ar",
            "48000",
            "-t",
            f"{timeline:.3f}",
            "-movflags",
            "+faststart",
            str(video),
        ]
    )

    CAPTIONS.mkdir(exist_ok=True)
    captions = CAPTIONS / f"RCC_Onboarding_Part_{part}_Captions.srt"
    with captions.open("w", encoding="utf-8") as handle:
        for index, (start, end, text) in enumerate(caption_entries, 1):
            handle.write(f"{index}\n{srt_time(start)} --> {srt_time(end)}\n{text}\n\n")

    result = {
        "part": part,
        "voice": voice,
        "locale": "en_GB",
        "rate_words_per_minute": rate,
        "slide_count": len(slides),
        "duration_seconds": round(timeline, 3),
        "video": str(video.relative_to(ROOT)),
        "video_sha256": sha256(video),
        "captions": str(captions.relative_to(ROOT)),
        "caption_entries": len(caption_entries),
        "audio_target_lufs": -16,
        "audio_true_peak_limit_db": -1.5,
    }
    if cleanup:
        cleanup.cleanup()
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("parts", nargs="*", type=int, default=[1, 2, 3, 4])
    parser.add_argument("--voice", default=VOICE)
    parser.add_argument("--rate", type=int, default=RATE)
    parser.add_argument("--keep-work", action="store_true")
    args = parser.parse_args()
    require("say")
    require("ffmpeg")
    require("ffprobe")
    if not all(part in {1, 2, 3, 4} for part in args.parts):
        raise SystemExit("Parts must be selected from 1, 2, 3, and 4")

    existing: dict[int, dict[str, object]] = {}
    if REPORT.exists():
        existing = {int(item["part"]): item for item in json.loads(REPORT.read_text())}
    for part in args.parts:
        report = build_part(part, args.voice, args.rate, args.keep_work)
        existing[part] = report
        print(f"Part {part}: {report['duration_seconds'] / 60:.1f} min -> {report['video']}")
    REPORT.write_text(json.dumps([existing[key] for key in sorted(existing)], indent=2) + "\n")


if __name__ == "__main__":
    main()
