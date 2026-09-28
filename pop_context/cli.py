from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pop-context",
        description="Multimodal cultural intelligence for video.",
    )
    parser.add_argument(
        "url",
        nargs="?",
        help="Video URL to analyze. Pipeline implementation arrives next.",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Print the current POP//CONTEXT version.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.version:
        print("POP//CONTEXT 0.1.0")
        return

    if not args.url:
        parser.print_help()
        return

    print(f"POP//CONTEXT received: {args.url}")
    print("The multimodal pipeline is scaffolded but not wired yet.")


if __name__ == "__main__":
    main()
