# Transparency Captions App 🎬
[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Live%20Demo-blue)](https://ziad1ayman1-transparency-captions-app.hf.space/)

This modular Python application automates the creation of professional transparent background videos with synchronized, "karaoke-style" animated subtitles. It is designed to take an English audio file and output a high-quality .mov file with an alpha channel, perfect for dropping directly into video editors like Premiere Pro or DaVinci Resolve.

## 📂 Project Structure
The project is split into three distinct modules to ensure clean code and easy maintenance:  

* **`subtitle_generator.py`**: Uses OpenAI Whisper to transcribe audio and generate a .ass (Advanced Substation Alpha) file with precise word-level timing.  
* **`video_engine.py`**: A robust FFmpeg wrapper that renders the transparent video, handles Windows path escaping, and muxes the audio.  
* **`app.py`**: The Streamlit frontend that provides a user-friendly interface for uploading audio and downloading the final video.
  
## 🛠️ Prerequisites
Before running the app, ensure you have the following installed on your system:

* Python 3.8+
* FFmpeg: Must be installed and added to your system's PATH.

## 🚀 Installation & Setup
Clone the Repository:

```Bash
git clone https://github.com/ziad0ayman/transparency-captions-app.git
cd transparency-captions-app
```
Install Dependencies:
The app requires streamlit, openai-whisper, and torch:  

```Bash
pip install -r requirements.txt
```
💻 How to Use
To launch the application locally, run the following command in your terminal:

```Bash
streamlit run app.py
```
## Workflow:

### Upload: Select an English audio file (.mp3, .wav, or .m4a).  

### Generate: Click the "Generate Video" button. The app will first transcribe the audio using the Whisper 'small' model and then render the video.  

### Download: Once complete, a download button will appear for your captions.webm file.  
