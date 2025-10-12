===============================
1. About this package
===============================

The 'mycmd' package contains a collection of personal day-to-day bash commands designed to improve productivity,
and make commonly used operations more convenient.  
It is lightweight, easy to set up, and fully customizable.
Its only dependency is python3.

===============================
2. How to use it
===============================

git clone https://github.com/tirupati27/mycmd

There are two ways to set up this package:

Method 1: Manual Setup
step 1. Open your terminal.  
step 2. Append the following two lines to your ~/.bashrc file (replace /path/of/the/package/folder with the actual path of this package):  

   export MYCMD="/path/of/the/package/folder"
   source "$MYCMD/.my_custom_bashrc"

step 3. Reload your ~/.bashrc file (source ~/.bashrc) or just restart the terminal to apply the changes:  

   mycmd --version

(note: What is ~/.bashrc file? refer to 3rd topic => Scroll below to read.)
------------------------------------------------------------

Method 2: Automatic Setup via Python Script
step 1. Navigate to the folder where this package is located.  
step 2. Run the 'setup.py' script using Python:  
   
   python setup.py

This will automatically configure your environment to use the commands.  
Now you can start using the custom bash commands in your terminal!

   mycmd --version

Note: This package contains its own 'bashrc' file named '.my_custom_bashrc'.
You can modify it as per your needs. e.g., adding more aliases or functions, or customizing any variables (like PS1).

===============================
3. What is the "~/.bashrc" file?
===============================

The `~/.bashrc` file is a bash script that runs automatically,
whenever you start a new terminal session in **bash** (the most common Linux shell).  
It is located in your home directory (`~` refers to your home folder).  

### Uses of ~/.bashrc file:
- **Customization:** You can set up environment variables, aliases, and functions to personalize your terminal.  
- **Automation:** Commands added here run automatically every time you open a terminal.  
- **Convenience:** Frequently used paths, exports, and shortcuts can be configured once and used everywhere.  

### Why it’s important for this package:
By adding the setup lines into `~/.bashrc`, your custom commands become available globally in every new terminal session,
you don't need to manually re-run the setup each time.

Note: This package contains its own 'bashrc' file named '.my_custom_bashrc'.
You can modify it as per your needs. e.g., adding more aliases or functions, or customizing any variables (like PS1).

© Tirupati 2025
