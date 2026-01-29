#!/usr/bin/env python3
"""
Vivid Binary Patcher - Permanent License Unlock
Target: Vivid v2.9.1 (https://apps.apple.com/gb/app/vivid-double-your-brightness/id6443470555?mt=12)
Patches the tbnz instruction to always jump to licensed code
"""

import sys
import shutil
from pathlib import Path

# Configuration - patches Vivid in /Applications/
VIVID_APP = Path("/Applications/Vivid.app")
ORIGINAL_BINARY = VIVID_APP / "Contents/MacOS/Vivid"
PATCHED_BINARY = VIVID_APP / "Contents/MacOS/Vivid_patched"
BACKUP_BINARY = VIVID_APP / "Contents/MacOS/Vivid_original"

# Patch details
FILE_OFFSET = 0x197664  # Correct offset in universal binary (ARM64 slice)
ORIGINAL_BYTES = b'\x68\x03\x00\x37'  # tbnz w8, #0x0, 0x1000436d0
PATCHED_BYTES = b'\x1b\x00\x00\x14'   # b 0x1000436d0 (unconditional branch)

def verify_binary():
    """Verify Vivid is installed and has the expected bytes"""
    if not VIVID_APP.exists():
        print(f"❌ Error: Vivid not found at {VIVID_APP}")
        print(f"   Please download and install Vivid v2.9.1 from the App Store:")
        print(f"   https://apps.apple.com/gb/app/vivid-double-your-brightness/id6443470555?mt=12")
        return False
    
    binary = Path(ORIGINAL_BINARY)
    
    with open(binary, 'rb') as f:
        f.seek(FILE_OFFSET)
        actual_bytes = f.read(4)
    
    if actual_bytes == PATCHED_BYTES:
        print("⚠️  Binary is already patched!")
        return False
    
    if actual_bytes != ORIGINAL_BYTES:
        print(f"❌ Error: Unexpected bytes at offset {hex(FILE_OFFSET)}")
        print(f"   Expected: {ORIGINAL_BYTES.hex()}")
        print(f"   Found:    {actual_bytes.hex()}")
        return False
    
    print(f"✅ Binary verified - found expected bytes at {hex(FILE_OFFSET)}")
    return True

def create_patched_copy():
    """Create a patched copy of the Vivid binary"""
    if PATCHED_BINARY.exists():
        print(f"⚠️  Patched binary already exists")
        response = input("   Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("❌ Aborted")
            return False
        PATCHED_BINARY.unlink()
    
    # Copy original to patched
    shutil.copy2(ORIGINAL_BINARY, PATCHED_BINARY)
    print(f"✅ Created patched copy")
    return True

def apply_patch():
    """Apply the binary patch to the copied file"""
    with open(PATCHED_BINARY, 'r+b') as f:
        f.seek(FILE_OFFSET)
        f.write(PATCHED_BYTES)
    
    print(f"✅ Patch applied to {PATCHED_BINARY}!")
    print(f"   Offset:   {hex(FILE_OFFSET)}")
    print(f"   Original: {ORIGINAL_BYTES.hex()} (tbnz w8, #0x0, ...)")
    print(f"   Patched:  {PATCHED_BYTES.hex()} (b ...)")

def verify_patch():
    """Verify the patch was applied correctly"""
    with open(PATCHED_BINARY, 'rb') as f:
        f.seek(FILE_OFFSET)
        actual_bytes = f.read(4)
    
    if actual_bytes != PATCHED_BYTES:
        print(f"❌ Error: Patch verification failed!")
        return False
    
    print(f"✅ Patch verified successfully!")
    return True

def install_patch():
    """Replace original binary with patched version"""
    # Backup original if not already backed up
    if not BACKUP_BINARY.exists():
        print(f"📦 Backing up original binary...")
        shutil.copy2(ORIGINAL_BINARY, BACKUP_BINARY)
        print(f"✅ Original backed up to Vivid_original")
    
    # Replace with patched version
    shutil.copy2(PATCHED_BINARY, ORIGINAL_BINARY)
    print(f"✅ Installed patched binary!")
    
    # Clean up patched copy
    PATCHED_BINARY.unlink()
    return True

def main():
    print("=" * 60)
    print("Vivid Binary Patcher - License Unlock")
    print("=" * 60)
    print()
    
    # Step 1: Verify original binary
    print("Step 1: Verifying original binary...")
    if not verify_binary():
        return 1
    print()
    
    # Step 2: Create patched copy
    print("Step 2: Creating patched copy...")
    if not create_patched_copy():
        return 1
    print()
    
    # Step 3: Apply patch
    print("Step 3: Applying patch...")
    apply_patch()
    print()
    
    # Step 4: Verify patch
    print("Step 4: Verifying patch...")
    if not verify_patch():
        print("⚠️  Removing failed patch...")
        Path(PATCHED_BINARY).unlink()
        return 1
    print()
    
    # Step 5: Install the patch
    print("=" * 60)
    print("🎉 Patch created successfully!")
    print("=" * 60)
    print()
    response = input("Install the patch now? (y/n): ")
    
    if response.lower() == 'y':
        print()
        print("Step 5: Installing patch...")
        install_patch()
        print()
        print("=" * 60)
        print("✅ Patch installed!")
        print("=" * 60)
        print()
        print("Next steps:")
        print("1. Re-sign the app:")
        print("   codesign --force --deep --sign - /Applications/Vivid.app")
        print()
        print("2. Clear quarantine:")
        print("   xattr -cr /Applications/Vivid.app")
        print()
        print("3. Launch Vivid:")
        print("   open /Applications/Vivid.app")
        print()
        print("💡 To restore original:")
        print("   mv /Applications/Vivid.app/Contents/MacOS/Vivid_original \\")
        print("      /Applications/Vivid.app/Contents/MacOS/Vivid")
    else:
        print()
        print("Patch ready but not installed.")
        print("To install manually, run this script again.")
    
    print()
    return 0

if __name__ == "__main__":
    sys.exit(main())
