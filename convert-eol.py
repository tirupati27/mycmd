#!/usr/bin/env python3

# A script to convert line endings between CRLF and LF safely.

import os
import sys
import tempfile
import shutil

def detect_line_endings(file_path):
    """Detect if a file uses CRLF or LF endings."""
    with open(file_path, "rb") as f:
        for line in f:
            if b"\r\n" in line:
                return "CRLF"
    return "LF"

def convert_crlf_to_lf(file_path):
    """Convert CRLF to LF safely."""
    with tempfile.NamedTemporaryFile("wb", delete=False) as tmp_file:
        with open(file_path, "rb") as f:
            for line in f:
                tmp_file.write(line.replace(b"\r\n", b"\n"))
    shutil.move(tmp_file.name, file_path)

def convert_lf_to_crlf(file_path):
    """Convert LF to CRLF safely."""
    with tempfile.NamedTemporaryFile("wb", delete=False) as tmp_file:
        with open(file_path, "rb") as f:
            for line in f:
                tmp_file.write(line.replace(b"\n", b"\r\n"))
    shutil.move(tmp_file.name, file_path)

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <file-path>")
        sys.exit(1)

    file_path = sys.argv[1]

    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' not found!")
        sys.exit(1)

    current_ending = detect_line_endings(file_path)
    print(f"Current line endings for '{file_path}': {current_ending}")

    if current_ending == "CRLF":
        answer = input("Convert CRLF → LF? [y/N]: ").strip().lower()
        if answer == "y":
            convert_crlf_to_lf(file_path)
            print(f"Converted '{file_path}' to LF successfully!")
        else:
            print("Conversion skipped.")
    else:
        answer = input("Convert LF → CRLF? [y/N]: ").strip().lower()
        if answer == "y":
            convert_lf_to_crlf(file_path)
            print(f"Converted '{file_path}' to CRLF successfully!")
        else:
            print("Conversion skipped.")

if __name__ == "__main__":
    main()
