# Vivid Binary Patch

**Educational binary patching tutorial for Vivid v2.9.1**

Learn how to bypass license checks in macOS applications using binary patching, ARM64 assembly, and lldb debugging.

---

## ⚠️ Disclaimer

This project is for **educational purposes only**. It demonstrates:
- Binary patching techniques
- ARM64 assembly language
- Reverse engineering with lldb
- macOS code signing

**You must own a legitimate copy of Vivid to use this patcher.**

---

## 📋 Prerequisites

1. **macOS** with Apple Silicon (M1/M2/M3)
- **Vivid:** Mac App Store ([Link](https://apps.apple.com/gb/app/vivid-double-your-brightness/id6443470555?mt=12))
3. **Python 3** (pre-installed on macOS)

---

## 🚀 Quick Start

### Step 1: Download Vivid
```bash
# Download and install Vivid v2.9.1 from the App Store:
# https://apps.apple.com/gb/app/vivid-double-your-brightness/id6443470555?mt=12
```

### Step 2: Run the Patcher
```bash
cd tools
python3 patch_vivid_binary.py
```

### Step 3: Follow Prompts
- Confirm installation when prompted
- Re-sign the app (command provided)
- Launch Vivid

**Done!** All features unlocked. 🎉

---

## 📚 Documentation

### Getting Started
- **[QUICK_START.md](QUICK_START.md)** - 5-minute guide
- **[README.md](README.md)** - Complete explanation

### Learning Materials
- **[docs/ASSEMBLY_EXPLAINED.md](docs/ASSEMBLY_EXPLAINED.md)** - ARM64 assembly for beginners
- **[docs/DEBUGGING_GUIDE.md](docs/DEBUGGING_GUIDE.md)** - Discovery & Debugging Guide

### Examples
- **[examples/lldb_session.txt](examples/lldb_session.txt)** - Real debugging session

---

## 🎓 What You'll Learn

1. **Binary Patching** - Modifying compiled applications
2. **ARM64 Assembly** - Understanding CPU instructions
3. **Reverse Engineering** - Finding license checks with lldb
4. **Code Signing** - macOS security mechanisms
5. **Debugging** - Using lldb effectively

---

## 🔧 How It Works

The patcher:
1. Locates the license check instruction at offset `0x197664`
2. Replaces conditional branch (`tbnz`) with unconditional branch (`b`)
3. Changes bytes from `68 03 00 37` to `1b 00 00 14`
4. Re-signs the application

**Result:** App always executes licensed code path.

---

## 📖 Technical Details

### The Patch

**Original instruction:**
```asm
0x100043664: tbnz w8, #0x0, 0x1000436d0  ; Jump if licensed
```

**Patched instruction:**
```asm
0x100043664: b 0x1000436d0              ; Always jump
```

**Bytes changed:**
- Before: `68 03 00 37`
- After: `1b 00 00 14`

---

## 🛡️ Safety

- ✅ Original binary is backed up automatically
- ✅ Patch is reversible
- ✅ No system modifications
- ✅ Works only on Vivid v2.9.1

**To restore:**
```bash
mv /Applications/Vivid.app/Contents/MacOS/Vivid_original \
   /Applications/Vivid.app/Contents/MacOS/Vivid
```

---

## 📁 Project Structure

```
vivid-patch-complete/
├── README.md                    ← This file
├── QUICK_START.md              ← Quick guide
├── tools/
│   └── patch_vivid_binary.py   ← Patcher script
├── docs/
│   ├── ASSEMBLY_EXPLAINED.md   ← ARM64 tutorial
│   └── DEBUGGING_GUIDE.md      ← lldb tutorial
└── examples/
    └── lldb_session.txt        ← Real session
```

---

## ⚙️ Requirements

- macOS 11.0+ (Big Sur or later)
- Apple Silicon Mac (ARM64)
- Vivid v2.9.1
- Python 3 (included with macOS)

---

## 🤝 Contributing

This is an educational project. Contributions that improve:
- Documentation clarity
- Assembly explanations
- Debugging techniques

are welcome!

---

## 📜 License

This project is for educational purposes. The techniques demonstrated are applicable to understanding software behavior and learning reverse engineering.

**Vivid** is copyrighted software by its respective owners. This project does not distribute Vivid or any copyrighted materials.

---

## 🎯 Learning Path

1. **Run the patcher** (5 min) - See it work
2. **Read README.md** (30 min) - Understand the process
3. **Study ASSEMBLY_EXPLAINED.md** (1 hour) - Learn ARM64
4. **Read DEBUGGING_GUIDE.md** (1 hour) - Master lldb
5. **Review lldb_session.txt** (15 min) - See real example

**Total time:** ~3 hours to become proficient in binary patching!

---

## 💡 Use Cases

- Learning reverse engineering
- Understanding ARM64 architecture
- Practicing debugging skills
- Teaching binary patching
- Security research

---

## 🔗 Resources

- **Vivid:** [App Store](https://apps.apple.com/app/vivid/id1615609653)
- **ARM64 Reference:** https://developer.arm.com/documentation/
- **lldb Tutorial:** https://lldb.llvm.org/use/tutorial.html

---

**Made with ❤️ for the reverse engineering community**
