import whisper

def format_ass_time(seconds):
    """Converts seconds into the exact timecode format required by ASS files (H:MM:SS.cs)."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    cs = int(round((seconds - int(seconds)) * 100))
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

def generate_karaoke_ass(audio_path, output_ass="karaoke.ass", model_size="small"):
    print(f"Loading Whisper '{model_size}' model...")
    model = whisper.load_model(model_size)
    
    print("Listening to audio and mapping precise word timestamps...")
    result = model.transcribe(audio_path, word_timestamps=True)

    ass_header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Impact,80,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,4,3,2,10,10,80,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    with open(output_ass, "w", encoding="utf-8") as f:
        f.write(ass_header)
        for segment in result["segments"]:
            words = segment["words"]
            for i, active_word in enumerate(words):
                start = format_ass_time(active_word["start"])
                if i < len(words) - 1:
                    end = format_ass_time(words[i+1]["start"])
                else:
                    end = format_ass_time(active_word["end"])
                
                line_text = ""
                for j, w in enumerate(words):
                    word_text = w["word"].strip()
                    if not word_text: continue
                    if j == i:
                        line_text += f"{{\\c&H00FFFF&}}{word_text}{{\\c&HFFFFFF&}} "
                    else:
                        line_text += f"{word_text} "

                f.write(f"Dialogue: 0,{start},{end},Default,,0,0,0,,{line_text.strip()}\n")
    
    print(f"Success! Subtitles saved to {output_ass}")
    return output_ass