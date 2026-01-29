# macOS Code Signing & Security - Explained

## Why do I need to re-sign the app?

When you modify even a single bit in an application binary, you break its **digital signature**. macOS detects this modification and will refuse to run the app, often crashing immediately or showing a "damaged" error.

To fix this, the application must be **re-signed**.

---

## 🛡️ Key Concepts

### 1. Digital Signatures
A digital signature acts like a tamper-evident seal.
- **Original App:** Signed by the developer (Goodsnooze) with an Apple Developer ID.
- **Verification:** macOS checks: "Does the current binary match what the developer signed?"
- **My Patch:** I changed bytes, so the "seal" is broken. Verification fails.

### 2. Ad-Hoc Signing
Since I don't have the original developer's private key, I cannot recreate their signature.
However, I can use **Ad-Hoc Signing**.

- **What it is:** Signing the app with "no identity" (`-` identity).
- **What it tells macOS:** "I (the user) signed this app on this machine. I trust it."
- **Limitation:** The app usually only runs on *your* machine. It's not suitable for distribution.

### 3. The Quarantine Attribute
When you download a file from the internet, macOS adds a hidden tag called `com.apple.quarantine`.
- **Gatekeeper** checks this tag.
- If an app is quarantined, Gatekeeper performs strict checks (Developer ID, Notarization).
- Since I broke the original signature, Gatekeeper will block the app.

---

## 🛠️ The Commands I Use

### 1. Re-signing (`codesign`)

```bash
codesign --force --deep --sign - /Applications/Vivid.app
```

**Breakdown:**
- `--force`: Overwrite the existing (broken) signature.
- `--deep`: Sign frameworks and internal components inside the app bundle.
- `--sign -`: Sign with "ad-hoc" identity (no specific developer certificate).
- `/Applications/Vivid.app`: The target app.

### 2. Removing Quarantine (`xattr`)

```bash
xattr -cr /Applications/Vivid.app
```

**Breakdown:**
- `xattr`: Extended Attributes tool.
- `-c`: Clear (remove) all attributes.
- `-r`: Recursive (apply to all files inside the app).
- **Why:** Removes the `com.apple.quarantine` flag so Gatekeeper doesn't block the app.

---

## ⚠️ Common Errors

### "App is damaged and can't be opened"
- **Cause:** Signature is broken or quarantine flag is present.
- **Fix:** Run both `codesign` and `xattr` commands again.

### "Code signature invalid" (Crash Log)
- **Cause:** You modified the binary but didn't re-sign it.
- **Fix:** Re-sign immediately after patching.

### "Killed: 9"
- **Cause:** iOS/macOS killed the process because code signature validation failed.
- **Fix:** Re-sign with correct entitlements (usually ad-hoc signing is enough for simple apps).

---

## 🧠 Summary

1. **Patching breaks the seal** (signature invalid).
2. **The app must be re-signed** to apply a new "local trust" seal.
3. **Quarantine must be cleared** to tell Gatekeeper "I trust this file."

Without these steps, a patched app on macOS simply won't launch!
