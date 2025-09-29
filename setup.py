"""
setup.py
Automates the setup of the personal bash commands package (mycmd).
"""

import os
import sys
from datetime import datetime

# ----------------------------
# 1. Ensure script is run directly
# ----------------------------
if __name__ != "__main__":
    print("❌ Error: This script must be run directly with 'python setup.py' from the package directory.")
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
# 3. Update ~/.bashrc
# ----------------------------
bashrc_path = os.path.expanduser("~/.bashrc")
package_dir = os.getcwd()
timestamp = datetime.now().strftime("%b-%d, %Y")

bashrc_lines_to_add = [
    f"\n# Added by mycmd's setup.py on ({timestamp}) © Tirupati 2025",
    f'export MYCMD="{package_dir}"',
    'source "$MYCMD/.my_custom_bashrc"'
]

# Check if lines already exist to prevent duplicates
with open(bashrc_path, "r") as f:
    existing_content = f.read()

if (bashrc_lines_to_add[1] in existing_content) and (bashrc_lines_to_add[2] in existing_content):
    print("\033[1;35mSetup already done previously.\033[0m\nNo changes made to ~/.bashrc.")
    sys.exit(0)

with open(bashrc_path, "a") as f:
    f.write("\n".join(bashrc_lines_to_add))

print("\033[1;35mSetup completed Successfully!\033[0m Your '~/.bashrc' file has been updated.")
print("Reload it with: source ~/.bashrc or just restart the terminal.")
