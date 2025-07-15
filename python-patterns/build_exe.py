#!/usr/bin/env python3
"""
Build script for creating standalone CRT Test Suite executable
"""

import os
import sys
import subprocess

def build_executable():
    """Build the executable using PyInstaller"""
    
    # PyInstaller command
    cmd = [
        'pyinstaller',
        '--onefile',  # Single file executable
        '--windowed',  # No console window
        '--name', 'NEONpulse_CRT_Test_Suite',
        '--icon', 'NONE',  # We'll add an icon later if needed
        '--add-data', 'requirements.txt:.',  # Include requirements
        'crt_test_suite.py'
    ]
    
    # Add Windows-specific options
    if sys.platform == 'win32':
        cmd.extend([
            '--version-file', 'version_info.txt',
            '--uac-admin'  # Request admin privileges for fullscreen
        ])
    
    print("Building executable...")
    print(" ".join(cmd))
    
    try:
        subprocess.run(cmd, check=True)
        print("\nBuild complete! Executable is in the 'dist' folder.")
        
        # Create a batch file for easy launching on Windows
        if sys.platform == 'win32':
            with open('dist/Run_CRT_Test_Suite.bat', 'w') as f:
                f.write('@echo off\n')
                f.write('NEONpulse_CRT_Test_Suite.exe\n')
            print("Created Run_CRT_Test_Suite.bat for easy launching.")
            
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        return False
        
    return True

def create_version_info():
    """Create version info file for Windows executable"""
    version_info = """# Version info for Windows executable
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'NEONpulseTechshop'),
        StringStruct(u'FileDescription', u'Professional CRT Monitor Test Patterns'),
        StringStruct(u'FileVersion', u'1.0.0.0'),
        StringStruct(u'InternalName', u'CRT_Test_Suite'),
        StringStruct(u'LegalCopyright', u'© 2024 NEONpulseTechshop'),
        StringStruct(u'OriginalFilename', u'NEONpulse_CRT_Test_Suite.exe'),
        StringStruct(u'ProductName', u'NEONpulse CRT Test Suite'),
        StringStruct(u'ProductVersion', u'1.0.0.0')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)"""
    
    with open('version_info.txt', 'w') as f:
        f.write(version_info)
    
if __name__ == "__main__":
    # Create version info for Windows
    if sys.platform == 'win32':
        create_version_info()
        
    # Build the executable
    success = build_executable()
    
    if success:
        print("\n" + "="*50)
        print("Build successful!")
        print("The executable can be found in the 'dist' folder")
        print("It can be run on Windows XP/98 and newer systems")
        print("="*50)