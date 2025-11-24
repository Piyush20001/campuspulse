# 🚀 Quick Start - Campus Pulse

## Run the App in 3 Steps

```bash
# 1. Navigate to this directory (streamlit_app/)
cd streamlit_app

# 2. Install dependencies (first time only)
pip3 install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

Then open your browser to **http://localhost:8501**

---

## ⚠️ Getting "illegal hardware instruction" Error?

Your CPU doesn't support the default PyTorch build. Use CPU-only version:

```bash
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
streamlit run app.py
```

---

## 📖 Full Documentation

- **Setup issues?** See `../FIRST_TIME_SETUP.md`
- **Import errors?** See `../FIX_IMPORT_ERRORS.md`
- **Hardware errors?** See `../TROUBLESHOOTING_ILLEGAL_INSTRUCTION.md`

---

## ✅ That's It!

The app should now be running. Create an account to get started.

When you're done:
1. Close the browser tab
2. Wait 2 seconds
3. Press Ctrl+C in terminal

(This order prevents shutdown errors)
