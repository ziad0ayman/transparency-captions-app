import subprocess
import os
import shutil
    
def process_video(ass_path, audio_path, output_path):

    
# 1. Check if FFmpeg is actually installed in the system path
    ffmpeg_bin = shutil.which("ffmpeg")
    if not ffmpeg_bin:
        print("FFmpeg not found in system path.")
        return False

    # 2. Linux (Streamlit Cloud) does NOT need the colon escaping like Windows
    # Windows needs 'C\:', but Linux just needs a clean path.
    if os.name == 'nt':  # Windows
        escaped_ass_path = ass_path.replace("\\", "/").replace(":", "\\:")
    else:  # Linux (Streamlit Cloud)
        escaped_ass_path = ass_path
    
    # 2. OPTIMIZATION: Using h264_nvenc. 
    
    command = [
        "ffmpeg",
        "-hwaccel", "cuda",             # Use CUDA hardware acceleration
        "-f", "lavfi",
        "-i", "color=c=black@0:s=1920x1080", # Transparent base
        "-i", audio_path,
        "-vf", f"ass='{escaped_ass_path}'",
        "-c:v", "qtrle",                # Keeping qtrle for maximum compatibility
        "-c:a", "aac",
        "-shortest",
        "-y",
        output_path
    ]

    try:
        # We capture stderr to see exactly what goes wrong if it fails again
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg Error Output: {e.stderr}")
        return False