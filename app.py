import streamlit as st
import os
import tempfile
from subtitle_generator import generate_karaoke_ass
from video_engine import process_video

st.set_page_config(page_title="Auto-Captions Pro", page_icon="🎬")

st.title("🎬 Green Screen Caption Generator")
st.info("Upload audio to get a professional green screen video with animated subtitles.")

audio_file = st.file_uploader("Upload Audio", type=["mp3", "wav", "m4a"])

if audio_file is not None:
    if st.button("Generate Video"):
        # 1. Open the temp directory first
        with tempfile.TemporaryDirectory() as tmpdir:
            file_extension = os.path.splitext(audio_file.name)[1]
            input_path = os.path.join(tmpdir, f"input_audio{file_extension}")
            
            with open(input_path, "wb") as f:
                f.write(audio_file.getbuffer())
            
            ass_file = os.path.join(tmpdir, "subtitles.ass")
            
            # FIXED: Changed from output.webm to output.mp4
            output_vid = os.path.join(tmpdir, "output.mp4") 
            
            # 2. Start the first spinner
            with st.spinner("Step 1: Transcribing & Generating Subtitles..."):
                generate_karaoke_ass(input_path, ass_file)
            
            # 3. The first spinner ends here. Now start the second one!
            with st.spinner("Step 2: Rendering Green Screen MP4 Video (Using Hardware Acceleration)..."):
                success, error_msg = process_video(ass_file, input_path, output_vid)
            
            # 4. Handle the results
            if success:
                st.success("Video Rendered Successfully!")
                with open(output_vid, "rb") as f:
                    st.download_button(
                        label="Download Green Screen .mp4",
                        data=f,
                        file_name="captions.mp4",
                        mime="video/mp4"
                    )
            else:
                st.error(f"Video rendering failed! FFmpeg Error:\n\n{error_msg}")