#!/usr/bin/env python3
"""The Robot Vacuum's Best Excuse — one line, written to entry.txt.

The vacuum speaks for itself: its map flagged one corner as dragon
country, and with the battery nearly dead it declines the fight. The
program is deliberately boring — one fixed line, no network, no clock,
no randomness — so the grader's two runs write byte-identical output.
"""

import argparse
import os
import sys

MAX_CHARS = 140

EXCUSE = (
    "I didn't miss that spot — my map marked it 'here be dragons,' "
    "and at 2% battery I'm not fighting dragons today."
)


class ExcuseWriter:
    """Holds the line, checks it against the gate, and writes it out."""

    def __init__(self, line, limit=MAX_CHARS):
        self.line = line
        self.limit = limit

    def checked(self):
        text = self.line.strip()
        if not text:
            raise ValueError("excuse is empty")
        if len(text) > self.limit:
            raise ValueError(
                f"excuse is {len(text)} chars, over the {self.limit} limit"
            )
        if "\n" in text or "\r" in text:
            raise ValueError("excuse must be a single line")
        return text

    def write_to(self, directory):
        target = os.path.join(directory, "entry.txt")
        os.makedirs(directory, exist_ok=True)
        with open(target, "w", encoding="utf-8") as handle:
            handle.write(self.checked())
        return target


def output_directory(cli_dir):
    if cli_dir:
        return cli_dir
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        return env_dir
    return "/output"


def main(argv=None):
    parser = argparse.ArgumentParser(description="Write the vacuum's excuse.")
    parser.add_argument("--out-dir", default=None, help="output directory")
    args = parser.parse_args(argv)
    writer = ExcuseWriter(EXCUSE)
    try:
        target = writer.write_to(output_directory(args.out_dir))
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"wrote {len(writer.checked())} chars to {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
