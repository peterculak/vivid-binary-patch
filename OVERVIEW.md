# Vivid Binary Patch - Complete Package

**Target:** Vivid v2.9.1  
**Download:** [Mac App Store](https://apps.apple.com/gb/app/vivid-double-your-brightness/id6443470555?mt=12)

## 📦 What's Included

This folder contains **everything** you need to understand and apply the Vivid binary patch:

```
vivid-patch-complete/

├── README.md                   ← Complete guide (start here!)
├── INDEX.md                    ← Documentation navigation
├── QUICK_START.md              ← 5-minute quick start
├── tools/
│   └── patch_vivid_binary.py  ← Patcher script
├── docs/
│   ├── ASSEMBLY_EXPLAINED.md  ← ARM64 assembly tutorial
│   └── DEBUGGING_GUIDE.md     ← lldb debugging guide
└── examples/
    └── lldb_session.txt       ← Real debugging session
```

---

## 🚀 Quick Start

### Step 1: Run the Patcher

```bash
cd vivid-patch-complete/tools
python3 patch_vivid_binary.py
```

### Step 2: Install (when prompted)

Type `y` to install to `/Applications/`

### Step 3: Re-sign

```bash
codesign --force --deep --sign - /Applications/Vivid.app
xattr -cr /Applications/Vivid.app
```

### Step 4: Launch

```bash
open /Applications/Vivid.app
```

**Done!** All features unlocked! 🎉

---

## 📚 Learning Path

1. **QUICK_START.md** - Get it working (5 min)
2. **README.md** - Understand the process (30 min)
3. **docs/ASSEMBLY_EXPLAINED.md** - Learn ARM64 (1 hour)
4. **docs/DEBUGGING_GUIDE.md** - Learn lldb (1 hour)
5. **examples/lldb_session.txt** - See it in action (15 min)

---

## 🎯 What This Package Does

- ✅ Includes **original Vivid app** (no need to download)
- ✅ **Patcher script** creates patched version in this folder
- ✅ **Complete documentation** with beginner-friendly explanations
- ✅ **Real examples** from my actual debugging session
- ✅ **Self-contained** - everything you need in one place

---

## 🔧 How It Works

The patcher:
1. Reads `Vivid_original.app`
2. Finds the license check instruction
3. Creates `Vivid_patched.app` with the patch applied
4. Optionally installs to `/Applications/`

**Safe:** Original app is never modified!

---

## 📖 Documentation

- **INDEX.md** - Navigation guide
- **README.md** - Complete explanation
- **QUICK_START.md** - Fast track
- **docs/ASSEMBLY_EXPLAINED.md** - ARM64 tutorial
- **docs/DEBUGGING_GUIDE.md** - lldb tutorial
- **examples/lldb_session.txt** - Real session

---

## ⚠️ Important Notes

- This is for **educational purposes** only
- Original app included for **convenience**
- All patches happen in **this folder** first
- You choose when to install to `/Applications/`

---

## 🎓 Perfect For

- Learning binary patching
- Understanding ARM64 assembly
- Practicing reverse engineering
- Teaching others

---

**Share this entire folder with colleagues!** Everything they need is here. 🚀
