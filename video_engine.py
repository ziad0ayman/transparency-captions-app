import subprocess
import os
import shutil

def process_video(ass_path, audio_path, output_path):
    ffmpeg_bin = shutil.which("ffmpeg")
    if not ffmpeg_bin:
        ffmpeg_bin = "ffmpeg" 

    if os.name == 'nt':
        escaped_ass_path = ass_path.replace("\\", "/").replace(":", "\\:")
    else:
        escaped_ass_path = ass_path.replace("\\", "/")

    command = [
        ffmpeg_bin,
        "-f", "lavfi",
        "-i", "color=c=black@0:s=1920x1080", 
        "-i", audio_path,
        "-vf", f"ass='{escaped_ass_path}'",
        # --- THE FIX: Highly compressed transparency ---
        "-c:v", "libvpx-vp9",    # VP9 Codec
        "-pix_fmt", "yuva420p",  # Explicitly tell it to use the Alpha channel
        "-auto-alt-ref", "0",    # Required for WebM transparency
        "-c:a", "libopus",       # Standard lightweight audio codec for WebM
        "-shortest", 
        "-y",
        output_path
    ]

    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        # Return True and an empty error message
        return True, ""
    except subprocess.CalledProcessError as e:
        # Return False and the exact reason it crashed
        return False, e.stderr