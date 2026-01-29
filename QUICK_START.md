# Quick Start Guide

**Vivid v2.9.1** - Download from Mac App Store:  
<https://apps.apple.com/gb/app/vivid-double-your-brightness/id6443470555?mt=12>

## For the Impatient

**Want to patch Vivid right now?**

```bash
cd vivid-patch-complete/tools
python3 patch_vivid_binary.py
```

Follow the prompts, and you're done!

---

## What You Need

- macOS with Apple Silicon (M1/M2/M3)
- Python 3
- Vivid.app installed in `/Applications/`
- Basic command line knowledge

---

## Step-by-Step

### 1. Run the Patcher

```bash
python3 tools/patch_vivid_binary.py
```

### 2. Install the Patch

When prompted, type `y` to install.

### 3. Re-sign the App

```bash
codesign --force --deep --sign - /Applications/Vivid.app
xattr -cr /Applications/Vivid.app
```

### 4. Launch Vivid

```bash
open /Applications/Vivid.app
```

**Done!** All features are now unlocked.

---

## Understanding What Happened

Read these in order:

1. **README.md** - Overview of the entire process
2. **docs/ASSEMBLY_EXPLAINED.md** - Learn ARM64 basics
3. **docs/DEBUGGING_GUIDE.md** - How I found the license check
4. **examples/lldb_session.txt** - Real debugging session

---

## Files

```
vivid-patch-complete/
├── README.md                    ← Start here
├── QUICK_START.md              ← This file
├── tools/
│   └── patch_vivid_binary.py   ← The patcher
├── docs/
│   ├── ASSEMBLY_EXPLAINED.md   ← ARM64 tutorial
│   └── DEBUGGING_GUIDE.md      ← lldb tutorial
└── examples/
    └── lldb_session.txt        ← Real session transcript
```

---

## Troubleshooting

**Error: "Unexpected bytes at offset"**
- The binary has been updated
- You need to re-find the license check

**Error: "App won't launch"**
- Re-sign the app: `codesign --force --deep --sign - /Applications/Vivid.app`
- Clear quarantine: `xattr -cr /Applications/Vivid.app`

**Features still locked?**
- Delete UserDefaults: `defaults delete com.goodsnooze.vivid`
- Restart Vivid

---

## Learn More

- **ARM64 Architecture:** docs/ASSEMBLY_EXPLAINED.md
- **Debugging Techniques:** docs/DEBUGGING_GUIDE.md
- **Real Example:** examples/lldb_session.txt

---

**Happy Patching!** 🎉
