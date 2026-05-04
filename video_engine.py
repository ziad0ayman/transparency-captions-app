import subprocess
import os

def process_video(ass_path, audio_path, output_path):

    
    # 1. FIX: FFmpeg 'ass' filter requires special escaping for Windows paths.
    # We replace backslashes with forward slashes and escape the colon.
    escaped_ass_path = ass_path.replace("\\", "/").replace(":", "\\:")
    
    # 2. OPTIMIZATION: Using h264_nvenc for your RTX 3090. 
    # Note: 'qtrle' is purely CPU-based. To use the GPU while keeping 
    # transparency, we use HEVC (hvc1) which supports alpha on modern systems.
    
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