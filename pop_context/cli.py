from __future__ import annotations

import argparse
import sys
import webbrowser

from . import __version__
from .pipeline import PipelineError, analyze


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="pop-context", description="POP//CONTEXT local-first audiovisual evidence pipeline.")
    p.add_argument("--version", action="store_true")
    sub = p.add_subparsers(dest="command")
    a = sub.add_parser("analyze", help="Analyze a short window from a video URL.")
    a.add_argument("url")
    a.add_argument("--start", type=int, default=0, help="Start time in seconds.")
    a.add_argument("--duration", type=int, default=60, help="Seconds to analyze. Default: 60.")
    a.add_argument("--model", default="tiny.en", choices=["tiny.en", "base.en"], help="Local whisper.cpp model.")
    a.add_argument("--no-open", action="store_true", help="Do not open the generated report.")
    return p


def main() -> None:
    p = parser()
    args = p.parse_args()
    if args.version:
        print(f"POP//CONTEXT {__version__}")
        return
    if args.command != "analyze":
        p.print_help()
        return
    if args.start < 0 or args.duration < 5 or args.duration > 600:
        p.error("--start must be >= 0; --duration must be between 5 and 600 seconds.")
    try:
        report = analyze(args.url, start=args.start, duration=args.duration, model_name=args.model)
    except PipelineError as exc:
        print(f"\nERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
    print(f"\nDone: {report}")
    if not args.no_open:
        webbrowser.open(report.resolve().as_uri())


if __name__ == "__main__":
    main()
