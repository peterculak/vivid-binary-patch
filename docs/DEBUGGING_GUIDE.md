# LLDB Debugging Guide - Finding License Checks

## What is lldb?

**lldb** (Low-Level Debugger) is a tool that lets you:
- Pause a running program
- Inspect memory and registers
- Step through code line-by-line
- Find where specific functions are called

Think of it like putting a program "under a microscope" to see exactly what it's doing.

---

## Basic lldb Commands

### Starting lldb

```bash
# Launch an app in lldb
lldb /path/to/app

# Attach to a running process
lldb -p <process_id>
```

### Essential Commands

| Command | What It Does |
|---------|--------------|
| `run` or `r` | Start the program |
| `continue` or `c` | Resume execution |
| `quit` or `q` | Exit lldb |
| `help <command>` | Get help on a command |

---

## Breakpoints

### What is a Breakpoint?

A breakpoint **pauses execution** when a specific point in the code is reached. It's like saying "stop here so I can look around."

### Setting Breakpoints

```lldb
# Break on a function name
br set -n "functionName"

# Break on an Objective-C method
br set -n "-[ClassName methodName:]"

# Break at a specific address
br set -a 0x100043664

# Break on a file and line (if you have source code)
br set -f file.c -l 42
```

### Managing Breakpoints

```lldb
# List all breakpoints
br list

# Delete a breakpoint
br delete 1

# Disable a breakpoint
br disable 1

# Enable a breakpoint
br enable 1
```

### Conditional Breakpoints

Only stop when a condition is true:

```lldb
# Set a breakpoint
br set -n "-[NSUserDefaults boolForKey:]"

# Add a condition
br modify 1 -c '(BOOL)[(NSString *)$arg3 isEqualToString:@"userHasValidLicense"]'
```

**What this does:** Only stops when the key parameter equals "userHasValidLicense"

---

## Inspecting State

### Viewing Registers

```lldb
# Show all registers
register read

# Show specific register
register read x0

# Show register in different format
register read x0 --format hex
```

### Printing Values

```lldb
# Print a variable/expression
p variableName

# Print as object (Objective-C/Swift)
po $x0

# Print with format
p/x $x0    # Hexadecimal
p/d $x0    # Decimal
p/t $x0    # Binary
```

### Examining Memory

```lldb
# Read memory at address
x/4xb 0x100043664
│ │││ │
│ │││ └─ Address
│ ││└─── Format: b = byte
│ │└──── Format: x = hex
│ └───── Count: 4 bytes
└─────── Command: examine

# Other formats
x/4xw 0x100043664  # 4 words (32-bit)
x/s 0x100043664    # String
```

---

## Stepping Through Code

### Step Commands

```lldb
# Step into (follow function calls)
step
s

# Step over (execute function without entering)
next
n

# Step out (finish current function)
finish

# Step one instruction
stepi
si

# Step over one instruction
nexti
ni
```

### Frame Navigation

```lldb
# Show call stack
bt

# Move up the call stack
up

# Move down the call stack
down

# Show current frame
frame info

# Select a specific frame
frame select 2
```

---

## Disassembly

### Viewing Assembly Code

```lldb
# Disassemble current function
disassemble

# Disassemble with context (30 instructions)
disassemble -c 30

# Disassemble around current PC
disassemble -p

# Disassemble specific address
disassemble -s 0x100043664 -c 10

# Disassemble a function by name
disassemble -n functionName
```

---

## Finding Functions

### Image Commands

```lldb
# List loaded images (libraries/executables)
image list

# Find symbols matching a pattern
image lookup -r -n "license"

# Find address of a symbol
image lookup -n "main"

# Find what's at an address
image lookup -a 0x100043664
```

---

## Phase 0: Discovery - How to find a key check

Before I could set a breakpoint on `userHasValidLicense`, I had to **find** that key first. Here's how you discover such things:

### Method 1: Strings Analysis

The simplest way is to look for interesting text strings inside the binary.

```bash
strings /Applications/Vivid.app/Contents/MacOS/Vivid | grep -i "license"
```

This outputs:
```
LicenseWindowController
userHasValidLicense
isLicenseValid
...
```

`userHasValidLicense` looks like a boolean flag stored in preferences!

### Method 2: Monitoring UserDefaults

I can spy on what keys the app is checking at runtime.

1. Set a breakpoint on `boolForKey:` without conditions:
   ```lldb
   br set -n "-[NSUserDefaults boolForKey:]"
   ```

2. Add a command to print the key name automatically:
   ```lldb
   br command add 1
   po (NSString *)$x2
   continue
   DONE
   ```

3. Run the app and watch the log:
   ```
   isFirstLaunch
   darkModeEnabled
   userHasValidLicense  <-- Bingo!
   ```

### Method 3: Inspecting Preferences File

macOS apps store settings in `~/Library/Preferences`.

```bash
defaults read com.goodsnooze.vivid
```

If the app has ever saved its license status, you might see:
```
"userHasValidLicense" = 0;
```

**Conclusion:** `userHasValidLicense` is the critical key determining the app's state.

---

## Debugging Session

### Step 1: Launch Vivid in lldb

```bash
lldb /Applications/Vivid.app/Contents/MacOS/Vivid
```

### Step 2: Set Breakpoint on UserDefaults

```lldb
(lldb) br set -n "-[NSUserDefaults boolForKey:]"
Breakpoint 1: where = Foundation`-[NSUserDefaults(NSUserDefaults) boolForKey:], address = 0x...
```

### Step 3: Add Condition to Filter for License Key

```lldb
(lldb) breakpoint modify 1 -c '(BOOL)[(NSString *)$arg3 isEqualToString:@"userHasValidLicense"]'
```

**Why `$arg3`?**
- `$arg1` = `self` (the NSUserDefaults object)
- `$arg2` = `_cmd` (the selector)
- `$arg3` = first parameter (the key string)

### Step 4: Run the App

```lldb
(lldb) run
Process 1234 launched: '/Applications/Vivid.app/Contents/MacOS/Vivid' (arm64)
Process 1234 stopped
* thread #1, queue = 'com.apple.main-thread', stop reason = breakpoint 1.1
```

### Step 5: Inspect the Key

```lldb
(lldb) po (NSString *)$x2
userHasValidLicense
```

**Success!** I caught the license check.

### Step 6: Find the Calling Code

```lldb
# Let the function complete
(lldb) finish

# Go up to the caller
(lldb) up

# Show the assembly code
(lldb) disassemble -c 30
```

### Step 7: Find the Branch Instruction

Look for something like:
```asm
0x100043664: tbnz w8, #0x0, 0x1000436d0
```

### Step 8: Note the Address

```lldb
(lldb) frame info
frame #0: 0x100043664 Vivid`___lldb_unnamed_symbol2980
```

**This is the address I need to patch!**

### Step 9: Get the Bytes

```lldb
(lldb) x/4xb 0x100043664
0x100043664: 0x68 0x03 0x00 0x37
```

**These are the bytes I'll replace!**

---

## Advanced Techniques

### Breakpoint Commands

Execute commands automatically when a breakpoint hits:

```lldb
br set -n "-[NSUserDefaults boolForKey:]"
br command add 1
po (NSString *)$x2
continue
DONE
```

This will:
1. Print the key
2. Automatically continue
3. Let you see all keys being checked

### Scripting

```lldb
# Python script
script print("Hello from Python!")

# Load a Python script
command script import /path/to/script.py
```

### Watchpoints

Stop when a memory location changes:

```lldb
# Watch a variable
watchpoint set variable myVar

# Watch a memory address
watchpoint set expression -- 0x100043664
```

---

## Common Issues

### Issue: Breakpoint Never Hits

**Possible causes:**
1. Function name is wrong
2. Function is inlined (optimized away)
3. Code path isn't executed

**Solution:** Try broader breakpoints or use watchpoints

### Issue: Can't Read Registers

**Possible cause:** Wrong architecture (x86_64 vs ARM64)

**Solution:** Check with `image list` and ensure you're debugging the right slice

### Issue: Symbols Not Found

**Possible cause:** Stripped binary (no debug symbols)

**Solution:** Use addresses instead of function names

---

## Practical Tips

1. **Use tab completion** - lldb supports tab completion for commands
2. **Save sessions** - Use `settings set target.save-jit-objects true`
3. **Aliases** - Create shortcuts: `command alias bd breakpoint disable`
4. **History** - Use arrow keys to recall previous commands
5. **Multiple breakpoints** - Set several and see which one hits first

---

## Example Session

```lldb
$ lldb /Applications/Vivid.app/Contents/MacOS/Vivid
(lldb) br set -n "-[NSUserDefaults boolForKey:]"
Breakpoint 1: where = Foundation`...
(lldb) br modify 1 -c '(BOOL)[(NSString *)$arg3 isEqualToString:@"userHasValidLicense"]'
(lldb) run
Process 1234 stopped
* thread #1, stop reason = breakpoint 1.1
(lldb) po (NSString *)$x2
userHasValidLicense
(lldb) finish
(lldb) up
(lldb) disassemble -c 30
...
0x100043664: tbnz w8, #0x0, 0x1000436d0
...
(lldb) x/4xb 0x100043664
0x100043664: 0x68 0x03 0x00 0x37
(lldb) quit
```

---

## Resources

- **Official lldb Tutorial:** https://lldb.llvm.org/use/tutorial.html
- **lldb Cheat Sheet:** https://www.nesono.com/sites/default/files/lldb%20cheat%20sheet.pdf
- **GDB to lldb Command Map:** https://lldb.llvm.org/use/map.html

---

## Key Takeaways

1. **Breakpoints** pause execution at specific points
2. **Conditional breakpoints** only stop when conditions are met
3. **Registers** hold function parameters and return values
4. **Disassembly** shows the actual machine code
5. **Frame navigation** lets you see the call stack
6. **lldb is powerful** but takes practice!

---

**Remember:** Debugging is detective work. You're looking for clues about what the program is doing. lldb gives you the tools to investigate!
