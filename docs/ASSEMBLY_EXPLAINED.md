# ARM64 Assembly Language - Beginner's Guide

## What is Assembly Language?

Assembly is a **low-level programming language** that's one step above raw machine code. Each instruction corresponds directly to what the CPU does.

**Comparison:**

| Level | Example | Who Reads It |
|-------|---------|--------------|
| **High-level** | `if (licensed) { showFeatures(); }` | Humans |
| **Assembly** | `tbnz w8, #0x0, 0x1000436d0` | Humans (barely) |
| **Machine code** | `68 03 00 37` | CPU only |

---

## ARM64 Basics

### What is ARM64?

ARM64 (also called AArch64) is the instruction set used by Apple Silicon Macs (M1, M2, M3, etc.). It's the "language" the CPU speaks.

### Registers

Registers are **super-fast temporary storage** inside the CPU. Think of them as variables that the CPU uses.

**ARM64 has 31 general-purpose registers:**

| Register | Size | Purpose |
|----------|------|---------|
| `x0-x30` | 64-bit | General use |
| `w0-w30` | 32-bit | Lower half of x0-x30 |
| `sp` | 64-bit | Stack pointer |
| `pc` | 64-bit | Program counter (current instruction) |

**Example:**
```
x0 = 64-bit register (holds 8 bytes)
w0 = Lower 32 bits of x0 (holds 4 bytes)
```

### Common Instructions

#### 1. Load/Store

```asm
ldr x0, [x1]        ; Load 64-bit value from memory at address in x1 into x0
ldrb w0, [x1]       ; Load 1 byte from memory into w0
str x0, [x1]        ; Store x0 to memory at address in x1
```

**Analogy:** Like `x0 = *x1` in C

#### 2. Arithmetic

```asm
add x0, x1, x2      ; x0 = x1 + x2
sub x0, x1, x2      ; x0 = x1 - x2
mul x0, x1, x2      ; x0 = x1 * x2
```

#### 3. Branches (Jumps)

```asm
b <address>         ; Unconditional jump (always go there)
bl <address>        ; Branch with link (function call)
ret                 ; Return from function
```

#### 4. Conditional Branches

```asm
cbz x0, <address>   ; Jump if x0 == 0
cbnz x0, <address>  ; Jump if x0 != 0
tbnz w0, #0, <addr> ; Jump if bit 0 of w0 is 1
tbz w0, #0, <addr>  ; Jump if bit 0 of w0 is 0
```

---

## The Instruction I Patched

### Original: `tbnz w8, #0x0, 0x1000436d0`

Let's break this down completely:

```
tbnz w8, #0x0, 0x1000436d0
│    │   │     │
│    │   │     └─ Target address (where to jump)
│    │   └─────── Bit number to test (bit 0)
│    └─────────── Register to test (w8)
└──────────────── Instruction: Test Bit and Branch if Not Zero
```

**What it does:**
1. Look at register `w8`
2. Check if bit 0 is set (1)
3. If yes, jump to address `0x1000436d0`
4. If no, continue to next instruction

**In C-like pseudocode:**
```c
if (w8 & 1) {  // If bit 0 is set
    goto 0x1000436d0;
}
```

### Patched: `b 0x1000436d0`

```
b 0x1000436d0
│ │
│ └─ Target address
└─── Instruction: Branch (unconditional)
```

**What it does:**
1. Jump to address `0x1000436d0`
2. That's it - no conditions!

**In C-like pseudocode:**
```c
goto 0x1000436d0;  // Always jump
```

---

## How Instructions Become Bytes

### Instruction Encoding

Each ARM64 instruction is **exactly 4 bytes** (32 bits). The bits encode:
- What operation to perform
- Which registers to use
- Immediate values (constants)
- Jump offsets

### Example: `tbnz w8, #0x0, 0x1000436d0`

**Binary representation:**
```
Bytes:  68 03 00 37
Hex:    0x37000368
Binary: 00110111 00000000 00000011 01101000
```

**Bit fields:**
```
31-24: 00110111 = Opcode (tbnz instruction)
23-19: 00000    = Bit to test (0)
18-5:  00000000000110 = Branch offset
4-0:   01000    = Register number (8 = w8)
```

### Example: `b 0x1000436d0`

**Binary representation:**
```
Bytes:  1b 00 00 14
Hex:    0x1400001b
Binary: 00010100 00000000 00000000 00011011
```

**Bit fields:**
```
31-26: 000101 = Opcode (b instruction)
25-0:  00 00000000 00000000 00011011 = Branch offset
```

---

## Calling Convention

When functions are called, parameters are passed in registers:

| Parameter | Register |
|-----------|----------|
| 1st | `x0` / `w0` |
| 2nd | `x1` / `w1` |
| 3rd | `x2` / `w2` |
| 4th | `x3` / `w3` |
| ... | ... |
| Return value | `x0` / `w0` |

**Example: Objective-C method**
```objc
-[NSUserDefaults boolForKey:(NSString *)key]
```

Maps to:
```
x0 = self (the NSUserDefaults object)
x1 = _cmd (the selector)
x2 = key (the NSString parameter)
Return in x0 (the boolean result)
```

---

## Memory Addressing

### Direct Addressing
```asm
ldr x0, [x1]        ; Load from address in x1
```

### Offset Addressing
```asm
ldr x0, [x1, #8]    ; Load from (x1 + 8)
```

### Pre/Post Indexing
```asm
ldr x0, [x1, #8]!   ; Load from (x1 + 8), then x1 = x1 + 8
ldr x0, [x1], #8    ; Load from x1, then x1 = x1 + 8
```

---

## Stack Operations

The stack is a region of memory used for:
- Local variables
- Function call information
- Temporary storage

```asm
stp x29, x30, [sp, #-16]!   ; Push x29 and x30 onto stack
ldp x29, x30, [sp], #16     ; Pop x29 and x30 from stack
```

**What `stp` does:**
1. Decrease `sp` by 16
2. Store `x29` at `[sp]`
3. Store `x30` at `[sp + 8]`

---

## Common Patterns

### Function Prologue
```asm
stp x29, x30, [sp, #-16]!   ; Save frame pointer and return address
mov x29, sp                  ; Set up frame pointer
sub sp, sp, #32              ; Allocate stack space
```

### Function Epilogue
```asm
add sp, sp, #32              ; Deallocate stack space
ldp x29, x30, [sp], #16     ; Restore frame pointer and return address
ret                          ; Return
```

### If Statement
```asm
cmp x0, #0                   ; Compare x0 with 0
b.eq else_label              ; Branch if equal (x0 == 0)
; if body
b end_if
else_label:
; else body
end_if:
```

---

## Practical Example: My License Check

### The Code Flow

```asm
; Call UserDefaults getter
bl SwiftUI.AppStorage.wrappedValue.getter

; Load the boolean result from stack
ldrb w8, [sp, #0x8]

; Test if licensed (bit 0 of w8)
tbnz w8, #0x0, licensed_code

; Unlicensed - show restrictions
; ... restriction code ...

licensed_code:
; Show all features
; ... premium features ...
```

### After My Patch

```asm
; Call UserDefaults getter
bl SwiftUI.AppStorage.wrappedValue.getter

; Load the boolean result from stack
ldrb w8, [sp, #0x8]

; ALWAYS jump to licensed code (patched!)
b licensed_code

; This code is now unreachable (dead code)
; ... restriction code ...

licensed_code:
; Show all features
; ... premium features ...
```

---

## Tools for Learning

1. **Online ARM64 Assembler:** https://armconverter.com/
2. **Compiler Explorer:** https://godbolt.org/ (see assembly from C code)
3. **ARM Documentation:** https://developer.arm.com/documentation/

---

## Key Takeaways

1. Assembly is **one instruction = one CPU operation**
2. **Registers** are fast temporary storage
3. **Branches** are like goto statements
4. **Conditional branches** check a condition first
5. **Each instruction is 4 bytes** in ARM64
6. **Calling convention** defines how functions receive parameters

---

**Remember:** You don't need to be an assembly expert to do binary patching. You just need to:
1. Find the instruction you want to change
2. Understand what it does
3. Know what you want it to do instead
4. Replace the bytes!
