from __future__ import annotations

import datetime as dt
import html
import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT / "workspace"
MODELS = ROOT / "models"


class PipelineError(RuntimeError):
    pass


def run(cmd: list[str], *, capture: bool = False) -> str:
    print("  $", " ".join(cmd))
    try:
        result = subprocess.run(cmd, check=True, text=True, capture_output=capture)
    except subprocess.CalledProcessError as exc:
        detail = f"\n{exc.stderr.strip()}" if getattr(exc, "stderr", None) else ""
        raise PipelineError(f"Command failed: {' '.join(cmd)}{detail}") from exc
    return (result.stdout or "").strip() if capture else ""


def require(name: str) -> None:
    if shutil.which(name) is None:
        raise PipelineError(
            f"Missing dependency: {name}. Run ./scripts/install-local.sh first."
        )


def slugify(value: str) -> str:
    value = re.sub(r"https?://", "", value)
    value = re.sub(r"[^A-Za-z0-9._-]+", "-", value)
    return value.strip("-")[:72] or "video"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def whisper_segments(raw: dict[str, Any]) -> list[dict[str, Any]]:
    segments: list[dict[str, Any]] = []
    for item in raw.get("transcription", []):
        timestamps = item.get("timestamps") or {}
        offsets = item.get("offsets") or {}
        segments.append(
            {
                "start": timestamps.get("from"),
                "end": timestamps.get("to"),
                "start_ms": offsets.get("from"),
                "end_ms": offsets.get("to"),
                "text": (item.get("text") or "").strip(),
            }
        )
    return segments


def find_download(folder: Path) -> Path:
    candidates = [
        p for p in folder.glob("source.*")
        if p.is_file() and p.suffix not in {".json", ".part", ".ytdl"}
    ]
    if not candidates:
        raise PipelineError("yt-dlp finished but no downloaded video file was found.")
    return max(candidates, key=lambda p: p.stat().st_size)


def extract_frames(video: Path, frames_dir: Path, duration: int) -> list[str]:
    frames_dir.mkdir(parents=True, exist_ok=True)
    for old in frames_dir.glob("frame-*.jpg"):
        old.unlink()

    times = sorted(set([0, max(0, duration // 2), max(0, duration - 1)]))
    files: list[str] = []
    for index, seconds in enumerate(times, start=1):
        output = frames_dir / f"frame-{index:02d}-{seconds:04d}s.jpg"
        run([
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
            "-ss", str(seconds), "-i", str(video),
            "-frames:v", "1", "-q:v", "3", str(output),
        ])
        if output.exists():
            files.append(str(output.relative_to(frames_dir.parent)))
    return files


def make_report(folder: Path, analysis: dict[str, Any]) -> Path:
    report = folder / "report.html"
    metadata = analysis["source"]
    title = html.escape(metadata.get("title") or "Untitled video")
    source_url = html.escape(metadata.get("webpage_url") or metadata.get("original_url") or "")
    transcript = analysis["transcript"]["segments"]
    frames = analysis["visual"]["frames"]

    transcript_html = "\n".join(
        f"""
        <article class="segment">
          <time>{html.escape(str(seg.get('start') or ''))} → {html.escape(str(seg.get('end') or ''))}</time>
          <p>{html.escape(seg.get('text') or '')}</p>
        </article>
        """
        for seg in transcript
    ) or "<p class='muted'>No speech segments returned.</p>"

    frames_html = "\n".join(
        f"""
        <figure>
          <img src="{html.escape(frame)}" alt="Representative video frame">
          <figcaption>{html.escape(frame)}</figcaption>
        </figure>
        """
        for frame in frames
    ) or "<p class='muted'>No frames extracted.</p>"

    payload = html.escape(json.dumps(analysis, indent=2, ensure_ascii=False))

    report.write_text(f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>POP//CONTEXT — {title}</title>
<style>
:root {{ color-scheme:dark; --bg:#08090b; --panel:#111318; --ink:#f4f0e8; --muted:#90949d; --line:#292d35; --acid:#b8ff39; --violet:#aa8cff; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--bg); color:var(--ink); font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace; }}
main {{ width:min(1100px,calc(100% - 32px)); margin:0 auto; padding:54px 0 100px; }}
header {{ border-bottom:1px solid var(--line); padding-bottom:30px; }}
.eyebrow {{ color:var(--acid); font-size:11px; letter-spacing:.14em; }}
h1 {{ font-family:Arial Black,Helvetica,sans-serif; font-size:clamp(40px,8vw,88px); margin:.15em 0; letter-spacing:-.06em; }}
h2 {{ margin-top:60px; font-size:13px; letter-spacing:.14em; color:var(--violet); }}
a {{ color:var(--acid); }}
.meta {{ color:var(--muted); line-height:1.6; }}
.grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:12px; }}
figure {{ margin:0; border:1px solid var(--line); background:var(--panel); }}
img {{ width:100%; display:block; }}
figcaption {{ color:var(--muted); font-size:10px; padding:8px; }}
.segment {{ display:grid; grid-template-columns:170px 1fr; gap:20px; padding:16px 0; border-top:1px solid var(--line); }}
time {{ color:var(--muted); font-size:11px; }}
.segment p {{ margin:0; line-height:1.55; }}
details {{ margin-top:60px; }}
pre {{ overflow:auto; padding:20px; border:1px solid var(--line); background:var(--panel); white-space:pre-wrap; }}
.muted {{ color:var(--muted); }}
@media(max-width:700px) {{ .grid {{ grid-template-columns:1fr; }} .segment {{ grid-template-columns:1fr; gap:5px; }} }}
</style>
</head>
<body>
<main>
<header>
  <div class="eyebrow">POP//CONTEXT // LOCAL EVIDENCE REPORT</div>
  <h1>{title}</h1>
  <div class="meta">
    analyzed locally · {html.escape(analysis['created_at'])}<br>
    window: {analysis['window']['start_seconds']}s → {analysis['window']['end_seconds']}s<br>
    <a href="{source_url}" target="_blank" rel="noopener">source ↗</a>
  </div>
</header>
<h2>REPRESENTATIVE FRAMES</h2>
<div class="grid">{frames_html}</div>
<h2>TRANSCRIPT</h2>
<section>{transcript_html}</section>
<details><summary>RAW analysis.json</summary><pre>{payload}</pre></details>
</main>
</body>
</html>
""")
    return report


def analyze(url: str, *, start: int = 0, duration: int = 60, model_name: str = "tiny.en") -> Path:
    for dependency in ("yt-dlp", "ffmpeg", "whisper-cli"):
        require(dependency)

    model = MODELS / f"ggml-{model_name}.bin"
    if not model.exists():
        raise PipelineError(f"Whisper model not found: {model}\nRun ./scripts/install-local.sh first.")

    WORKSPACE.mkdir(exist_ok=True)
    metadata_raw = run(["yt-dlp", "--skip-download", "--dump-single-json", url], capture=True)
    metadata = json.loads(metadata_raw)
    identity = metadata.get("id") or slugify(url)
    folder = WORKSPACE / slugify(str(identity))
    folder.mkdir(parents=True, exist_ok=True)
    write_json(folder / "metadata.json", metadata)

    end = start + duration
    print("\n[1/4] downloading analysis window")
    run([
        "yt-dlp", "--no-playlist",
        "--download-sections", f"*{start}-{end}",
        "--force-keyframes-at-cuts",
        "-f", "bv*[height<=720]+ba/b[height<=720]/b",
        "--merge-output-format", "mp4",
        "-o", str(folder / "source.%(ext)s"),
        url,
    ])
    video = find_download(folder)

    audio = folder / "audio.wav"
    print("\n[2/4] normalizing audio")
    run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-i", str(video), "-vn", "-ac", "1", "-ar", "16000",
        "-c:a", "pcm_s16le", str(audio),
    ])

    print("\n[3/4] transcribing locally with whisper.cpp")
    transcript_prefix = folder / "transcript"
    run([
        "whisper-cli", "-m", str(model), "-f", str(audio),
        "-ojf", "-of", str(transcript_prefix), "-l", "en", "-np",
    ])

    whisper_json = folder / "transcript.json"
    if not whisper_json.exists():
        raise PipelineError("whisper-cli did not produce transcript.json. Check its terminal output.")
    whisper_raw = load_json(whisper_json)

    print("\n[4/4] extracting representative frames + report")
    frames = extract_frames(video, folder / "frames", duration)

    analysis = {
        "schema_version": "0.1",
        "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "project": "POP//CONTEXT",
        "mode": "local-first",
        "source": {
            "id": metadata.get("id"),
            "title": metadata.get("title"),
            "channel": metadata.get("channel") or metadata.get("uploader"),
            "duration": metadata.get("duration"),
            "webpage_url": metadata.get("webpage_url"),
            "original_url": url,
            "local_video": video.name,
            "local_audio": audio.name,
        },
        "window": {"start_seconds": start, "duration_seconds": duration, "end_seconds": end},
        "transcript": {
            "engine": "whisper.cpp",
            "model": model_name,
            "language": (whisper_raw.get("result") or {}).get("language"),
            "segments": whisper_segments(whisper_raw),
        },
        "visual": {"method": "fixed representative frame sampling", "frames": frames},
        "audio": {"semantic_events": [], "note": "Semantic non-speech audio analysis is a later milestone."},
        "culture": {"references": [], "note": "Cultural memory/reasoning is intentionally not implemented yet."},
        "interpretation": {
            "literal": None, "emotional": None, "cultural": None,
            "note": "Evidence first. Interpretation comes after the local evidence pipeline is stable.",
        },
    }

    write_json(folder / "analysis.json", analysis)
    report = make_report(folder, analysis)
    print(f"\nPOP//CONTEXT report: {report}")
    return report
