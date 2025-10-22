"""
setup.py
Automates the setup of the personal bash commands package (mycmd).
"""

import subprocess
import re
import os
import sys
from datetime import datetime

package_dir = os.getcwd()

# **************************************************************************
# 1. Ensure script is run directly
# **************************************************************************
if __name__ != "__main__":
    print("❌ Error: This script must be run directly with 'python setup.py' from the mycmd package directory.")
    sys.exit(1)


# **************************************************************************
# 2. Check if 'MYCMD' is the actual git repo (https://github.com/tirupati27/mycmd.git)
# **************************************************************************

# Get the actual URL as github.com/user/repo
try:
    actual_url_bytes = subprocess.check_output(
        ["git", "-C", package_dir, "remote", "get-url", "origin"],
        stderr=subprocess.DEVNULL
    )
    actual_url_raw = actual_url_bytes.decode().strip()  # remove whitespace
except subprocess.CalledProcessError:
    actual_url_raw = ""
actual_url = re.sub(r"(git@|https://)github\.com[:/](.*)\.git", r"github.com/\2", actual_url_raw)
# Get the expected URL as github.com/user/repo
expected_url_raw = "https://github.com/tirupati27/mycmd.git"
expected_url = re.sub(r"(git@|https://)github\.com[:/](.*)\.git", r"github.com/\2", expected_url_raw.strip())
# Compare normalized URLs
if not actual_url or actual_url.lower() != expected_url.lower():
    print(f"❌ Error: '{package_dir}' is not the actual git repository.")
    print("Please ensure that the 'mycmd' package is cloned using git.")
    print(f"'git clone {expected_url_raw}'")
    print("OR try to run this script with 'python setup.py' from the mycmd package directory.")
    sys.exit(1)



# **************************************************************************
# 3. Update ~/.bashrc
# **************************************************************************

# ----------------------------
# Variables
# ----------------------------
bashrc_path = os.path.expanduser("~/.bashrc")
timestamp = datetime.now().strftime("%b-%d, %Y")

# ----------------------------
# 1. Prompt for user-name
# ----------------------------
user_name = input("Enter your user name for the shell prompt: ").strip()

# ----------------------------
# 2. Color selection with validation
# ----------------------------
colors = {
    "1": ("Red", "1;31"),
    "2": ("Green", "1;32"),
    "3": ("Yellow", "1;33"),
    "4": ("Blue", "1;34"),
    "5": ("Magenta", "1;35"),
    "6": ("Cyan", "1;36"),
    "7": ("White", "1;37"),
    "8": ("Custom RGB", None)
}

while True:
    print("\nSelect a color for your username in the prompt:")
    for key, (name, _) in colors.items():
        print(f"{key}. {name}")

    choice = input("Enter choice [1-8]: ").strip()

    if choice in colors:
        if choice == "8":
            # RGB input loop
            while True:
                try:
                    r = int(input("Enter Red (0-255): ").strip())
                    g = int(input("Enter Green (0-255): ").strip())
                    b = int(input("Enter Blue (0-255): ").strip())
                    if all(0 <= x <= 255 for x in (r, g, b)):
                        username_color = f"38;2;{r};{g};{b}"
                        break
                    else:
                        print("⚠ RGB values must be between 0 and 255. Try again.")
                except ValueError:
                    print("⚠ Please enter valid integers for RGB. Try again.")
        else:
            username_color = colors[choice][1]
        break
    else:
        print("⚠ Invalid choice. Please select a number between 1 and 8.")

# ----------------------------
# 3. Determine PS1 based on root/non-root
# ----------------------------
if os.geteuid() == 0:
    # Root user
    ps1 = f"export PS1='\\[\\033[{username_color}m\\]{user_name}:\\[\\033[0m\\] \\[\\033[1;34m\\]\\w\\[\\033[0m\\] \\[\\033[{username_color}m\\]#\\[\\033[0m\\] '"
else:
    # Non-root user
    ps1 = f"export PS1='\\[\\033[{username_color}m\\]{user_name}:\\[\\033[0m\\] \\[\\033[38;2;220;100;100m\\]\\w\\[\\033[0m\\] \\[\\033[{username_color}m\\]\\$\\[\\033[0m\\] '"

# ----------------------------
# 4. Lines to add to ~/.bashrc
# ----------------------------
bashrc_lines_to_add = [
    f"\n# Added by mycmd's setup.py on ({timestamp}) © 2025 Tirupati",
    f'declare -xr MYCMD="{package_dir}"',
    'source "$MYCMD/my_bashrc.sh"',
    ps1
]

# ----------------------------
# 5. Read existing content and remove old entries
# ----------------------------
if os.path.exists(bashrc_path):
    with open(bashrc_path, "r") as f:
        existing_lines = f.readlines()
else:
    existing_lines = []

new_lines = []
skip = False
for line in existing_lines:
    if line.startswith("# Added by mycmd's setup.py"):
        skip = True
        continue
    if skip:
        if line.strip() == "" or line.startswith("declare -xr MYCMD=") or line.startswith('source "$MYCMD/') or line.startswith("export PS1='"):
            continue
        else:
            skip = False
    new_lines.append(line.rstrip("\n"))

# ----------------------------
# 6. Append new lines and write to file
# ----------------------------
new_lines.extend(bashrc_lines_to_add)

with open(bashrc_path, "w") as f:
    f.write("\n".join(new_lines) + "\n")

# ----------------------------
# 7. Feedback to user
# ----------------------------
print("\033[1;35mSetup completed Successfully!\033[0m Your '~/.bashrc' file has been updated.")
print("Reload it with: source ~/.bashrc or just restart the terminal.")
