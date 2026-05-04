import streamlit as st
import os
import tempfile
from subtitle_generator import generate_karaoke_ass
from video_engine import process_video

st.set_page_config(page_title="Auto-Captions Pro", page_icon="🎬")

st.title("🎬 Transparent Caption Generator")
st.info("Upload audio to get a professional transparent video with animated subtitles.")

audio_file = st.file_uploader("Upload Audio", type=["mp3", "wav", "m4a"])

if audio_file is not None:
    if st.button("Generate Video"):
        with st.spinner("Step 1: Transcribing & Generating Subtitles..."):
            with tempfile.TemporaryDirectory() as tmpdir:
                
                # FIX 1: Preserve the original file extension (e.g., .mp3)
                file_extension = os.path.splitext(audio_file.name)[1]
                input_path = os.path.join(tmpdir, f"input_audio{file_extension}")
                
                with open(input_path, "wb") as f:
                    f.write(audio_file.getbuffer())
                
                ass_file = os.path.join(tmpdir, "subtitles.ass")
                
                # FIX 2: Change output to WebM
                output_vid = os.path.join(tmpdir, "output.webm") 
                
                generate_karaoke_ass(input_path, ass_file)
                
                st.spinner("Step 2: Rendering Transparent Video (This takes time)...")
                
                # FIX 3: Catch the exact error message from the engine
                success, error_msg = process_video(ass_file, input_path, output_vid)
                
                if success:
                    st.success("Video Rendered Successfully!")
                    with open(output_vid, "rb") as f:
                        st.download_button(
                            label="Download Transparent Video",
                            data=f,
                            file_name="captions.webm",
                            mime="video/webm"
                        )
                else:
                    # Print the exact crash reason to the UI
                    st.error(f"Video rendering failed! FFmpeg Error:\n\n{error_msg}")