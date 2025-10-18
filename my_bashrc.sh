#!/bin/bash

# ================================================================
# Aim          : To check if the MYCMD environment variable is set.
#                If not set, print an error message and exit the script.
#                And also checks for python, git.
# ================================================================

# Step 1: Check if 'MYCMD' variable is not just set in the environment but also available for the child processes
if ! printenv MYCMD >/dev/null 2>&1; then   # 'printenv' command prints the exported variables only
    echo "❌ Error: 'MYCMD' variable not set in the '~/.bashrc' file."
    echo "Please read the instructions in the README.md file of the mycmd package."
    exit 1  # Exit is most important because subsequent scripts depend on this variable
fi

# Step 2: Check if 'MYCMD' is the actual git repo (https://github.com/tirupati27/mycmd.git)
# Get the actual url as github.com/user/repo
actual_url=$(git -C "$MYCMD" remote get-url origin 2>/dev/null | tr -d '[:space:]' | sed -E 's#(git@|https://)github.com[:/](.*)\.git#github.com/\2#')
# Get the expected url as github.com/user/repo
expected_url=$(echo "https://github.com/tirupati27/mycmd.git" | tr -d '[:space:]' | sed -E 's#(git@|https://)github.com[:/](.*)\.git#github.com/\2#')
# Compare normalized URLs
if [[ -z "$actual_url" || "${actual_url,,}" != "${expected_url,,}" ]]; then
    echo "❌ Error: '$MYCMD' is not the actual git repository."
    echo "Please ensure that the 'mycmd' package is cloned using git."
    echo "'git clone https://github.com/tirupati27/mycmd.git'"
    exit 1
fi

# step 3: check if python is installed
# some commands of this package depend on python
if ! command -v python &> /dev/null; then
    echo "❌ python is not installed. Some command of 'mycmd' package will not work properly."
fi

# step 4: restore the mycmd package as it was in the last git commit
restore_main_branch() {
    cd "$MYCMD"
    git checkout main         # switch to the main branch
    git reset --hard @{u}     # local branch now identical to upstream
    cd
}
restore_main_branch > /dev/null 2>&1           # Silence both stdout and stderr

# ================================================================
# Aim          : Automatically assign frequently used directories
#                to variables (d1, d2, d3, ...) for easy 'cd' access.
#                Variables are read-only, safely handle spaces, 
#                and are exported so child processes can access them.
#                Also defines a function 'p' to print all shortcuts.
# ================================================================

# Define a function to create and print all directory shortcuts. The function will act as a command.
p() {
    local db_file="$MYCMD/my_bashrc-dirs.txt"
    # Create the database file if it doesn't exist
    if [[ ! -f "$db_file" ]]; then
        cat > "$db_file" <<dirEOF
Note:
# ---------------------------------------------
# Add here your frequently used directories one per line.
# your directories will automatically assign to variables (d1, d2, d3, ...) for easy 'cd' access.
# Variables are read-only, safely handle spaces, and are exported so child processes can access them.
# You can use command 'p' to print all shortcuts.
# Example directories:
$HOME/tirupati/Music
/sdcard/Music/songs
# ---------------------------------------------
dirEOF
    fi
    local count=1
    local line var
    while IFS= read -r line; do         # iterating on each line of the database file
        [[ -d "$line" ]] || continue    # skip non-directories line
        var="d$count"
        unset "$var"                    # unset old shortcuts (d1, d2, ...)
        declare -r "$var"="$line"       # Create read-only variable names: d1, d2, ...means cannot be modified
        export "$var"                   # Export, so child processes can access
        echo -e "\033[38;2;200;200;100m\"\$$var\"\033[0m == '$line'"
        ((count++))
    done < "$db_file"
}
export -f p  # Export the function so it can be used in child processes
p > /dev/null 2>&1           # Silence both stdout and stderr

# ================================================================
# Aim          : The below script checks all files in this ($MYCMD) directory
#                and ensures they have executable
#                permission. If a file is missing the execute-permission,
#                the script grants it.
# ================================================================

# Loop through all files in MYCMD directory with no extension
find "$MYCMD" -maxdepth 1 -type f ! -name "*.*" | while read -r file; do
    # Step 2: Check if the file is NOT executable
    if [ ! -x "$file" ]; then
      chmod +x "$file"   # Grant execute permission
    fi
done


# Customize the LS_COLORS variable to change the appearance of 'ls' listings
export LS_COLORS='di=01;34:tw=01;34:ow=01;34:ln=01;96'
export PATH="$MYCMD:$PATH"  # add my custom command directory to PATH

# ================================================================
# Aim          : Aliasing some frequently used commands to shorter versions.
# ================================================================

alias ll='ls -lha --color=auto'          # Long listing with hidden files and human-readable sizes
