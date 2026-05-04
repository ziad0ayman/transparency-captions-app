import streamlit as st
import os
import tempfile
from subtitle_generator import generate_karaoke_ass
from video_engine import process_video

st.set_page_config(page_title="Auto-Captions Pro", page_icon="🎬")

st.title("🎬 Transparent Caption Generator")
st.info("Upload audio to get a professional .mov with vanilla karaoke subtitles.")

audio_file = st.file_uploader("Upload Audio", type=["mp3", "wav", "m4a"])

if audio_file is not None:
    if st.button("Generate Video"):
        with st.spinner("Step 1: Transcribing & Generating Subtitles..."):
            # Create a persistent temp directory for this session
            with tempfile.TemporaryDirectory() as tmpdir:
                # Save uploaded audio
                input_path = os.path.join(tmpdir, "input_audio")
                with open(input_path, "wb") as f:
                    f.write(audio_file.getbuffer())
                
                ass_file = os.path.join(tmpdir, "subtitles.ass")
                output_mov = os.path.join(tmpdir, "output.mov")
                
                # Run Module 1
                generate_karaoke_ass(input_path, ass_file)
                
                st.spinner("Step 2: Rendering Transparent Video...")
                # Run Module 2
                success = process_video(ass_file, input_path, output_mov)
                
                if success:
                    st.success("Video Rendered Successfully!")
                    with open(output_mov, "rb") as f:
                        st.download_button(
                            label="Download Transparent .mov",
                            data=f,
                            file_name="captions.mov",
                            mime="video/quicktime"
                        )
                else:
                    st.error("Video rendering failed. Check FFmpeg installation.")