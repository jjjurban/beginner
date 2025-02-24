# FaceBox
Detects faces in real-time with green boxes using MTCNN.

## Setup
1. Use Python 3.12 (e.g., `brew install python@3.12` on macOS).
2. Create a virtual env: `/opt/homebrew/opt/python@3.12/bin/python3.12 -m venv facebox_env`.
3. Activate it: `source facebox_env/bin/activate`.
4. Install dependencies: `pip install -r requirements.txt`.
5. Run: `python facebox.py`.

## Notes
- Requires a webcam. On macOS, disable Continuity Camera if issues arise.
- Press 'q' to quit.
