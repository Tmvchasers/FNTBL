"""
Setup script to build the Fortnite Matchmaking Bot into a standalone executable
Run: pyinstaller build_exe.py
"""

import PyInstaller.__main__
import sys
import os

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Build the executable
PyInstaller.__main__.run([
    'fortnite_matchmaking_bot.py',
    '--name=FortniteMatchmakingBot',
    '--onefile',
    '--windowed',
    '--icon=bot_icon.ico',
    '--add-data=bot_icon.ico:.',
    '--hidden-import=fortnitepy',
    '--hidden-import=customtkinter',
    f'--distpath={script_dir}/dist',
    f'--buildpath={script_dir}/build',
    f'--specpath={script_dir}',
])

print("\n" + "="*50)
print("✅ Executable built successfully!")
print(f"Location: {script_dir}/dist/FortniteMatchmakingBot.exe")
print("="*50)
