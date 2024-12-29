# YouTube_Shorts_Generator
The YouTube Shorts Generator is a Streamlit web app that downloads YouTube videos, trims them into short clips, and adds captions. It uses **Pytube** for downloading and **FFmpeg** for video processing, creating 9:16 aspect ratio shorts for easy sharing.


How to run file ->
1. **Install Dependencies**:  
   ```bash
   pip install streamlit pytube ffmpeg-python
   sudo apt install ffmpeg   # or brew install ffmpeg (for macOS)
   ```

2. Save Script: Save your code in a Python file (e.g., `youtube_shorts_generator.py`).

3. Run Streamlit App:  
   ```bash
   streamlit run youtube_shorts_generator.py
   ```

4. Access App: Open `http://localhost:8501` in your browser.

5. Use App: Enter a YouTube URL, set options, and click "Generate Shorts".
