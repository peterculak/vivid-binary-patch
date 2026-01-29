# Vivid Binary Patch - Documentation Index

## 📚 Documentation Structure

### Getting Started
1. **[QUICK_START.md](QUICK_START.md)** - Run the patcher in 5 minutes
2. **[README.md](README.md)** - Complete overview and explanation

### Learning Materials
3. **[docs/ASSEMBLY_EXPLAINED.md](docs/ASSEMBLY_EXPLAINED.md)** - ARM64 assembly for beginners
4. **[docs/DEBUGGING_GUIDE.md](docs/DEBUGGING_GUIDE.md)** - Using lldb to find patches
5. **[docs/CODESIGNING_EXPLAINED.md](docs/CODESIGNING_EXPLAINED.md)** - Why I need to re-sign apps

### Examples
5. **[examples/lldb_session.txt](examples/lldb_session.txt)** - Real debugging session

### Tools
6. **[tools/patch_vivid_binary.py](tools/patch_vivid_binary.py)** - The patcher script

---

## 🎯 Reading Order

### For Beginners
1. Start with **QUICK_START.md** to run the patcher
2. Read **README.md** to understand what happened
3. Read **ASSEMBLY_EXPLAINED.md** to learn the basics
4. Read **DEBUGGING_GUIDE.md** to learn the process

### For Experienced Developers
1. **README.md** - Get the overview
2. **examples/lldb_session.txt** - See the actual process
3. **tools/patch_vivid_binary.py** - Study the code

### For Teaching Others
1. **README.md** - Share the complete guide
2. **ASSEMBLY_EXPLAINED.md** - Explain assembly concepts
3. **examples/lldb_session.txt** - Show real examples

---

## 📖 What Each File Covers

### QUICK_START.md
- How to run the patcher
- Basic troubleshooting
- Minimal explanation

### README.md
- Complete process explanation
- Beginner-friendly analogies
- Step-by-step breakdown
- How the patcher works

### docs/ASSEMBLY_EXPLAINED.md
- ARM64 architecture basics
- Register usage
- Common instructions
- Instruction encoding
- The specific instruction we patched

### docs/DEBUGGING_GUIDE.md
- lldb basics
- Breakpoints and conditions
- Inspecting memory and registers
- Disassembly
- Finding functions

### docs/CODESIGNING_EXPLAINED.md
- What is digital signing?
- Why patching breaks signatures
- Ad-hoc signing explained
- The quarantine attribute
- Common errors and fixes

### examples/lldb_session.txt
- Real transcript of finding the license check
- Shows actual commands and output
- Demonstrates the process

### tools/patch_vivid_binary.py
- The actual patcher script
- Well-commented code
- Safe patching process
- Verification steps

---

## 🎓 Learning Path

```
Start Here
    ↓
QUICK_START.md (5 min)
    ↓
Run the patcher
    ↓
README.md (30 min)
    ↓
Understand the process
    ↓
ASSEMBLY_EXPLAINED.md (1 hour)
    ↓
Learn ARM64 basics
    ↓
DEBUGGING_GUIDE.md (1 hour)
    ↓
Learn lldb
    ↓
examples/lldb_session.txt (15 min)
    ↓
See it in action
    ↓
You're now a binary patcher! 🎉
```

---

## 💡 Key Concepts by File

| Concept | Where to Learn |
|---------|----------------|
| What is binary patching? | README.md |
| How do CPUs work? | ASSEMBLY_EXPLAINED.md |
| What is assembly? | ASSEMBLY_EXPLAINED.md |
| How to use lldb? | DEBUGGING_GUIDE.md |
| How to find patches? | DEBUGGING_GUIDE.md |
| Real example? | examples/lldb_session.txt |
| How does the patcher work? | README.md + patch_vivid_binary.py |

---

## 🔧 Practical Use

### To Patch Vivid
→ QUICK_START.md

### To Understand How
→ README.md

### To Learn the Techniques
→ ASSEMBLY_EXPLAINED.md + DEBUGGING_GUIDE.md

### To Teach Someone
→ Share this entire folder!

---

**Total Reading Time:** ~3 hours  
**Total Understanding:** Priceless 🎓
