# gimp-rpc-linux
GIMP Rich Presence support on Linux!

[![pypresence](https://img.shields.io/badge/using-pypresence-00bb88.svg?style=for-the-badge&logo=discord&logoWidth=20)](https://github.com/qwertyquerty/pypresence)

### Information and Instructions
- To use this, either autorun the Python file at startup, or run it before running GIMP
- The script listens for GIMP and activates RPC when GIMP is opened (0% CPU usage on my shitCPUtm)
- Requirements: `wmctrl`
- Installing `wmctrl`: 
  - Arch: `sudo pacman -S wmctrl`
  - Ubuntu/Debian: `sudo apt install wmctrl`
