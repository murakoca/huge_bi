from moviepy.editor import TextClip, concatenate_videoclips, AudioFileClip
import os

def create_video(script, output_path="report.mp4"):
    clips = []
    for item in script:
        txt_clip = TextClip(item['text'], fontsize=24, color='white', bg_color='black', size=(640,480))
        txt_clip = txt_clip.set_duration(item['duration'])
        clips.append(txt_clip)
    final = concatenate_videoclips(clips)
    final.write_videofile(output_path, fps=24)
    return output_path