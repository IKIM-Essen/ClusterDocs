#!/usr/bin/env python3
"""Generate and build video lessons for RCC Classes 5–15.

The Markdown course pages remain authoritative. This script selects the key
sections for each class, creates a concise visual storyboard and narration,
then uses the same speech mastering and video encoding profile as Classes 1–4.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import shutil
import subprocess
import tempfile
import textwrap
from pathlib import Path

import build_videos as media


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs/course"
FRAMES = ROOT / "slides/frames"
NARRATION = ROOT / "narration"
CAPTIONS = ROOT / "captions"
OUTPUT = ROOT / "videos-enhanced"
REPORT = ROOT / "meta/course-video-build-report.json"

CLASS_FILES = {
    5: "class-05-slurm.md",
    6: "class-06-vhosts.md",
    7: "class-07-python-notebooks.md",
    8: "class-08-r-analysis.md",
    9: "class-09-shiny.md",
    10: "class-10-notebook-to-service.md",
    11: "class-11-biomedical-data-privacy.md",
    12: "class-12-efficient-io.md",
    13: "class-13-storage-architecture.md",
    14: "class-14-wet-lab-data-workflows.md",
    15: "class-15-data-lifecycle.md",
}

ACCENTS = {
    5: "D15B47", 6: "0A8FB2", 7: "2C6EAF", 8: "7057A3", 9: "B4233D",
    10: "2B8A65", 11: "A56500", 12: "D15B47", 13: "0B456E",
    14: "0A8FB2", 15: "2B8A65",
}

SECTIONS = {
    5: ["Three execution modes", "Everyday Slurm commands", "Pattern 1", "Pattern 2", "Pattern 3", "Built-in availability protection", "What the examples prove"],
    6: ["Learning outcomes", "What is in scope", "Standard architecture", "Division of responsibility", "Safe data-access patterns", "Request and approval workflow", "Local copyable example", "Completion gate"],
    7: ["Learning goals", "The RCC notebook rule", "Large-data pattern", "Copyable example", "Python tool choices", "Good security", "Completion gate"],
    8: ["Learning goals", "Recommended R workflow", "Handling larger tables", "Reproducibility", "Copyable example", "Good cluster patterns", "Completion gate"],
    9: ["Learning goals", "Development mode", "What makes Shiny production-ready", "Safe data pattern", "Common mistakes", "Completion gate"],
    10: ["Learning goals", "Decision guide", "Service boundary", "Preparing for review", "Completion gate"],
    11: ["Learning outcome", "The RCC rule in one sentence", "Why biomedical data receive special protection", "A practical RCC decision model", "Genomic research", "X-ray", "Data minimisation", "Legal and institutional resources", "Completion gate"],
    12: ["Learning objectives", "1. Storage is part", "2. Streaming", "4. Why runtime", "5. The RCC staging pattern", "8. Snakemake integration", "10. Cache containers", "12. Diagnose", "14. Decision checklist"],
    13: ["Learning objectives", "1. Redis", "2. MinIO", "3. RCC network", "4. Large files", "6. JuiceFS", "8. Slurm placement", "10. Diagnosing", "Completion gate"],
    14: ["Learning objectives", "1. Four different roles", "2. The instrument-data lifecycle", "3. Before starting", "4. Choosing a transfer", "5. File count", "10. When RCC", "11. A safe handoff", "12. Verification", "Practical exercise"],
    15: ["Learning objectives", "1. The lifecycle", "2. Classify", "3. Match storage", "4. Build the minimum archive", "5. Coscine", "6. Archive acceptance", "7. Review", "Completion gate"],
}


def plain(value: str) -> str:
    value = re.sub(r"```.*?```", " ", value, flags=re.DOTALL)
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"!\[[^]]*\]\([^)]*\)", " ", value)
    value = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", value)
    value = re.sub(r"^\s*[|].*[|]\s*$", " ", value, flags=re.MULTILINE)
    value = re.sub(r"^\s*(?:[-*+] |\d+[.)] )", "", value, flags=re.MULTILINE)
    value = value.replace("**", "").replace("__", "").replace("`", "")
    value = re.sub(r"(?:^|\n)\s*>\s*", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def words(value: str, limit: int) -> str:
    tokens = value.split()
    result = " ".join(tokens[:limit])
    if len(tokens) > limit:
        result = result.rstrip(" ,;:") + "."
    return result


def slide_points(body: str) -> list[str]:
    """Extract distinct, reader-friendly points without flattening Markdown structure."""
    candidates: list[str] = []

    # Tables usually contain the clearest comparison. Keep the label and its
    # recommended use, while ignoring delimiter rows and secondary caveats.
    for line in body.splitlines():
        if not re.match(r"^\s*\|.*\|\s*$", line):
            continue
        cells = [plain(cell) for cell in line.strip().strip("|").split("|")]
        if len(cells) < 2 or all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            continue
        if cells[0].lower() in {"mode", "task", "option", "layer", "component", "risk"}:
            continue
        if cells[0] and cells[1]:
            candidates.append(f"{cells[0]}: {cells[1]}")

    # Preserve list-item boundaries; flattening a semicolon list produces
    # unhelpful fragments such as "The gate" and "submits one job".
    for match in re.finditer(r"^\s*(?:[-*+] |\d+[.)] )(.+)$", body, re.MULTILINE):
        point = plain(match.group(1))
        if point:
            candidates.append(point)

    # Finally take complete prose sentences from non-table, non-code blocks.
    prose = re.sub(r"```.*?```", " ", body, flags=re.DOTALL)
    prose = re.sub(r"^\s*\|.*\|\s*$", " ", prose, flags=re.MULTILINE)
    prose = re.sub(r"^\s*(?:[-*+] |\d+[.)] ).*$", " ", prose, flags=re.MULTILINE)
    for sentence in re.split(r"(?<=[.!?])\s+", plain(prose)):
        if sentence.strip():
            candidates.append(sentence.strip())

    distinct: list[str] = []
    seen: set[str] = set()
    for candidate in candidates:
        point = words(candidate, 17)
        key = re.sub(r"[^a-z0-9]+", " ", point.lower()).strip()
        if not key or key in seen:
            continue
        seen.add(key)
        distinct.append(point)
        if len(distinct) == 3:
            break
    return distinct


def parse_document(class_number: int) -> tuple[str, list[dict[str, str]]]:
    text = (DOCS / CLASS_FILES[class_number]).read_text(encoding="utf-8")
    title_match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    title = title_match.group(1) if title_match else f"Class {class_number}"
    matches = list(re.finditer(r"^##\s+(.+)$", text, re.MULTILINE))
    available: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        available.append((match.group(1).strip(), text[match.end():end].strip()))

    selected: list[dict[str, str]] = []
    for wanted in SECTIONS[class_number]:
        found = next(((heading, body) for heading, body in available if heading.lower().startswith(wanted.lower())), None)
        if not found:
            continue
        heading, body = found
        clean = plain(body)
        if not clean:
            continue
        narration = words(clean, 105)
        bullets = slide_points(body)
        selected.append({"title": re.sub(r"^\d+\.\s*", "", heading), "narration": narration, "bullets": bullets})
    if not selected:
        raise ValueError(f"No selected sections found for Class {class_number}")
    return title, selected


def wrap(value: str, width: int) -> list[str]:
    return textwrap.wrap(value, width=width, break_long_words=False, break_on_hyphens=False)


def text_svg(lines: list[str], x: int, y: int, size: int, color: str, weight: int = 400, step: int | None = None) -> str:
    step = step or int(size * 1.28)
    tspans = "".join(f'<tspan x="{x}" y="{y + i * step}">{html.escape(line)}</tspan>' for i, line in enumerate(lines))
    return f'<text font-family="Arial, Helvetica, sans-serif" font-size="{size}" font-weight="{weight}" fill="#{color}">{tspans}</text>'


def cover_svg(class_number: int, title: str, total: int) -> str:
    accent = ACCENTS[class_number]
    short = re.sub(rf"^Class {class_number}:\s*", "", title, flags=re.IGNORECASE)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720">
<rect width="1280" height="720" fill="#{accent}"/>
<circle cx="1110" cy="100" r="250" fill="#ffffff" opacity=".07"/><circle cx="1180" cy="650" r="320" fill="#062A46" opacity=".10"/>
{text_svg([f'CLASS {class_number}'], 92, 105, 22, 'FFFFFF', 700)}
{text_svg(wrap(short, 34), 92, 190, 52, 'FFFFFF', 700, 62)}
{text_svg(['Video-first RCC learning path', 'Watch first · use the page for commands and exercises'], 96, 450, 24, 'FFFFFF', 400, 38)}
<rect x="92" y="575" width="360" height="58" rx="18" fill="#ffffff" opacity=".16"/>
{text_svg([f'{total} focused chapters · captions included'], 119, 612, 18, 'FFFFFF', 700)}
</svg>'''


def lesson_svg(class_number: int, slide: int, total: int, item: dict[str, object]) -> str:
    accent = ACCENTS[class_number]
    title_lines = wrap(str(item["title"]), 46)[:2]
    bullets = list(item["bullets"])[:3]
    cards = []
    base_y = 235
    for index, bullet in enumerate(bullets, 1):
        y = base_y + (index - 1) * 125
        lines = wrap(str(bullet), 55)[:2]
        cards.append(f'<rect x="84" y="{y-42}" width="850" height="98" rx="16" fill="#F5F8FA" stroke="#DCE3E8"/>')
        cards.append(f'<circle cx="121" cy="{y+7}" r="22" fill="#{accent}"/>')
        cards.append(text_svg([str(index)], 114, y + 14, 18, "FFFFFF", 700))
        cards.append(text_svg(lines, 165, y, 22, "15202B", 500, 29))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720">
<rect width="1280" height="720" fill="#FFFFFF"/><rect width="18" height="720" fill="#{accent}"/><rect x="18" width="1262" height="10" fill="#{accent}" opacity=".2"/>
{text_svg([f'CLASS {class_number} · CHAPTER {slide-1}'], 84, 75, 17, accent, 700)}
{text_svg(title_lines, 84, 130, 38, '062A46', 700, 45)}
{''.join(cards)}
<rect x="995" y="205" width="200" height="350" rx="32" fill="#{accent}" opacity=".09"/>
<circle cx="1095" cy="305" r="60" fill="#{accent}"/>{text_svg([str(slide-1)], 1078, 322, 48, 'FFFFFF', 700)}
<path d="M1095 375 V475" stroke="#{accent}" stroke-width="8" stroke-linecap="round" opacity=".45"/><path d="M1070 450 L1095 480 L1120 450" fill="none" stroke="#{accent}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" opacity=".65"/>
{text_svg(['WATCH', 'UNDERSTAND', 'APPLY'], 1038, 525, 15, accent, 700, 24)}
<line x1="84" y1="670" x2="1195" y2="670" stroke="#DCE3E8"/>{text_svg(['RCC video lesson'], 84, 699, 13, '607084')}{text_svg([f'{slide} / {total}'], 1150, 699, 13, '607084')}
</svg>'''


def render_assets(class_number: int) -> tuple[str, list[dict[str, object]]]:
    title, sections = parse_document(class_number)
    cover_narration = (
        f"Welcome to {title}. This video introduces the core decisions and working patterns. "
        "Watch the complete lesson first, then use the written class page for copyable commands, exercises, and detailed reference material."
    )
    slides: list[dict[str, object]] = [{"slide": 1, "title": title, "narration": cover_narration, "bullets": []}]
    for index, section in enumerate(sections, 2):
        slides.append({"slide": index, **section})
    total = len(slides)
    frame_dir = FRAMES / f"class{class_number}"
    shutil.rmtree(frame_dir, ignore_errors=True)
    frame_dir.mkdir(parents=True)
    for item in slides:
        number = int(item["slide"])
        svg = cover_svg(class_number, title, total - 1) if number == 1 else lesson_svg(class_number, number, total, item)
        with tempfile.NamedTemporaryFile("w", suffix=".svg", encoding="utf-8", delete=False) as handle:
            handle.write(svg)
            svg_path = Path(handle.name)
        subprocess.run(["rsvg-convert", "-w", "1280", "-h", "720", "-o", str(frame_dir / f"slide-{number:02d}.png"), str(svg_path)], check=True)
        svg_path.unlink()

    narration_path = NARRATION / f"RCC_Onboarding_Class_{class_number}_Video_Narration.md"
    lines = [f"# {title} — video narration", ""]
    for item in slides:
        lines.extend((f"## Slide {item['slide']}: {item['title']}", "", str(item["narration"]), ""))
    narration_path.write_text("\n".join(lines), encoding="utf-8")
    return title, slides


def build_class(class_number: int, voice: str, rate: int) -> dict[str, object]:
    title, slides = render_assets(class_number)
    frame_dir = FRAMES / f"class{class_number}"
    with tempfile.TemporaryDirectory(prefix=f"rcc-class{class_number}-") as temp:
        work = Path(temp)
        audio_files: list[Path] = []
        durations: list[float] = []
        captions: list[tuple[float, float, str]] = []
        timeline = 0.0
        for item in slides:
            number = int(item["slide"])
            audio = work / f"slide-{number:02d}.wav"
            media.synthesize(str(item["narration"]), audio, voice, rate)
            seconds = media.duration(audio)
            audio_files.append(audio); durations.append(seconds)
            chunks = media.caption_chunks(str(item["narration"]))
            weights = [max(1, len(chunk.split())) for chunk in chunks]
            local = 0.0
            for chunk, weight in zip(chunks, weights):
                span = seconds * weight / sum(weights)
                captions.append((timeline + local, timeline + local + span, chunk)); local += span
            timeline += seconds

        audio_list = work / "audio.txt"
        audio_list.write_text("\n".join(f"file '{path}'" for path in audio_files) + "\n")
        full_audio = work / "narration.wav"
        media.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(audio_list), "-c", "copy", str(full_audio)])
        frame_list = work / "frames.txt"
        frame_lines: list[str] = []
        for item, seconds in zip(slides, durations):
            frame = frame_dir / f"slide-{int(item['slide']):02d}.png"
            frame_lines.extend((f"file '{frame}'", f"duration {seconds:.6f}"))
        frame_lines.append(f"file '{frame_dir / f'slide-{len(slides):02d}.png'}'")
        frame_list.write_text("\n".join(frame_lines) + "\n")

        OUTPUT.mkdir(exist_ok=True)
        video = OUTPUT / f"RCC_Onboarding_Class_{class_number}_Video_Enhanced.mp4"
        media.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(frame_list), "-i", str(full_audio),
                   "-vf", "fps=2,scale=1280:720:flags=lanczos,format=yuv420p", "-c:v", "libx264", "-preset", "medium", "-tune", "stillimage", "-crf", "20",
                   "-c:a", "aac", "-af", "pan=stereo|c0=c0|c1=c0", "-ac", "2", "-b:a", "160k", "-ar", "48000",
                   "-disposition:a:0", "default", "-metadata:s:a:0", "language=eng", "-metadata:s:a:0", "title=English narration",
                   "-t", f"{timeline:.3f}", "-movflags", "+faststart", str(video)])

        caption_path = CAPTIONS / f"RCC_Onboarding_Class_{class_number}_Captions.srt"
        with caption_path.open("w", encoding="utf-8") as handle:
            for index, (start, end, caption) in enumerate(captions, 1):
                handle.write(f"{index}\n{media.srt_time(start)} --> {media.srt_time(end)}\n{caption}\n\n")

    return {"class": class_number, "title": title, "voice": voice, "locale": "en_GB", "rate_words_per_minute": rate,
            "slide_count": len(slides), "duration_seconds": round(timeline, 3), "video": str(video.relative_to(ROOT)),
            "video_sha256": media.sha256(video), "captions": str(caption_path.relative_to(ROOT)), "caption_entries": len(captions),
            "audio_channels": 2, "audio_target_lufs": -16, "audio_true_peak_limit_db": -1.5}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("classes", nargs="*", type=int, default=list(range(5, 16)))
    parser.add_argument("--voice", default=media.VOICE)
    parser.add_argument("--rate", type=int, default=media.RATE)
    args = parser.parse_args()
    for command in ("say", "ffmpeg", "ffprobe", "rsvg-convert"):
        media.require(command)
    existing: dict[int, dict[str, object]] = {}
    if REPORT.exists():
        existing = {int(item["class"]): item for item in json.loads(REPORT.read_text())}
    for class_number in args.classes:
        if class_number not in CLASS_FILES:
            raise SystemExit("Classes must be selected from 5 through 15")
        result = build_class(class_number, args.voice, args.rate)
        existing[class_number] = result
        print(f"Class {class_number}: {result['duration_seconds'] / 60:.1f} min -> {result['video']}", flush=True)
    REPORT.write_text(json.dumps([existing[key] for key in sorted(existing)], indent=2) + "\n")


if __name__ == "__main__":
    main()
