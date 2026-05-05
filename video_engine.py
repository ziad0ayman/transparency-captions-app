import subprocess
import os
import shutil

def process_video(ass_path, audio_path, output_path):
    ffmpeg_bin = shutil.which("ffmpeg")
    if not ffmpeg_bin:
        ffmpeg_bin = "ffmpeg" 

    ass_dir = os.path.dirname(ass_path)
    ass_input = os.path.basename(ass_path) if ass_dir else ass_path
    cwd = ass_dir if ass_dir else None

    command = [
        ffmpeg_bin,
        "-f", "lavfi",
        # Pure green background instead of transparent black
        "-i", "color=c=#00FF00:s=1920x1080", 
        "-i", audio_path,
        "-vf", f"ass={ass_input}",
        # NVIDIA Hardware Encoder (H.264)
        "-c:v", "h264_nvenc", 
        # Standard pixel format (No Alpha)
        "-pix_fmt", "yuv420p", 
        # AAC is the standard audio codec for MP4
        "-c:a", "aac", 
        "-shortest",
        "-y",
        output_path
    ]

    try:
        subprocess.run(command, check=True, capture_output=True, text=True, cwd=cwd)
        return True, ""
    except subprocess.CalledProcessError as e:
        return False, e.stderr