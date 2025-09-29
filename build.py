#!/usr/bin/env python3
"""
build.py
Automates the build of the personal bash commands package (mycmd) as ./builds/build_version-info.zip.
"""

import zipfile      # BUILT-IN MODULE
import os
import sys
import datetime as dt

# ----------------------------
# 1. Ensure script is run directly
# ----------------------------
if __name__ != "__main__":
    print("❌ Error: This script must be run directly with 'python build.py' from the package directory.")
    sys.exit(1)

# ----------------------------
# 2. Check required files and whether we are in the package directory
# ----------------------------
required_files = [".my_custom_bashrc", "mycmd", "README.txt"]

missing_files = [f for f in required_files if not os.path.isfile(f)]
if missing_files:
    print("❌ Error: Please run this script from the package directory:\nRead the README.txt file for instructions.")
    sys.exit(1)

# ----------------------------
# 3. Update the version info in README.txt
# ----------------------------
file_path = "README.txt"
with open(file_path, "r") as f:
    lines = f.readlines()                # Read all lines
second_line = lines[1].strip()           # i.e. "Version: 1.0 (as on Sep 25, 2025)"
version = float(second_line.split()[1])  # Extract "1.0" as float
version = round(version + 0.1, 1)        # Increment version by 0.1
# Get today’s date in "Mon DD, YYYY" format
today = dt.datetime.today().strftime("%b %d, %Y")
new_line = f"Version: {version} (as on {today})\n"  # Build new second line
lines[1] = new_line     # Update the second line
# Write back to the file
with open(file_path, "w") as f:
    f.writelines(lines)

# ----------------------------
# 4. Create ./builds/build_version-info.zip
# ----------------------------

today = dt.datetime.today().strftime("%b-%d-%Y")
zip_file_path = f"./builds/mycmd_V-{version}_{today}.zip"

with zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED) as zipf:
    for item in os.listdir("."):
        if item == "build.py":      # exclude build.py file
            continue
        if os.path.isfile(item):    # only files in current dir
            zipf.write(item)

print(f"\033[1;35mBuild completed Successfully!\033[0m Created '{zip_file_path}' containing the package files.")
