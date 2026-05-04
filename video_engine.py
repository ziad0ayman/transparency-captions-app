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
        "-i", "color=c=black@0:s=1920x1080",
        "-i", audio_path,
        "-vf", f"ass={ass_input}",
        "-c:v", "libvpx-vp9",
        "-pix_fmt", "yuva420p",
        "-auto-alt-ref", "0",
        "-c:a", "libopus",
        "-shortest",
        "-y",
        output_path
    ]

    try:
        subprocess.run(command, check=True, capture_output=True, text=True, cwd=cwd)
        # Return True and an empty error message
        return True, ""
    except subprocess.CalledProcessError as e:
        # Return False and the exact reason it crashed
        return False, e.stderr