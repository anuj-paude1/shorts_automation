from moviepy.editor import *
from moviepy.video.fx.all import crop
import moviepy.audio.fx.all as afx

from stt import get_audio_timestamp
from get_content import bard_text
import random

def format_text(video,word):
    text=TextClip(txt=word,method='label',color="white",font="./fonts/CARIBOLD.ttf",fontsize=130*1.5,align='center',stroke_color="black",stroke_width=7)
    return text.set_position((video.size[0]*0.5-text.size[0]/2,video.size[1]*0.55))
    

def add_caption(video,data):
    clips=[]
    clips.append(video)
    for _ in data :
        text=format_text(video,_["word"])
        duration=float(_["end"])-float(_["start"])
        clips.append(text.set_duration(duration).set_start(float(_["start"])))
        print(_["word"],float(_["start"]),float(_["end"]))
    video=CompositeVideoClip(clips)
    return video


def get_random(path):
    if os.path.exists(path) and os.path.isdir(path):
        files = [os.path.join(path, file) for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]
        if files:
            return random.choice(files)
        else:
            return "No files found in the directory."
    else:
        return "Invalid directory path or directory does not exist."

def clip_for_duration(vid_aud,duration):
    start=random.uniform(15,vid_aud.duration-duration)
    end=start+duration
    vid_aud=vid_aud.subclip(start,end)
    return vid_aud

def crop_video(clip : VideoFileClip):
    (w, h) = clip.size
    set_height=h
    set_width=set_height*9/16
    cropped_clip : VideoFileClip = crop(clip, width=set_width, height=set_height, x_center=w/2, y_center=h/2)
    cropped_clip= cropped_clip.volumex(0)
    return cropped_clip

def set_watermark(video,text="Quotino"):
    watermark_text = TextClip(text, fontsize=80, color="white", bg_color="transparent")
    video=CompositeVideoClip([video,watermark_text.set_position((video.size[0]*0.3,video.size[1]*0.8)).set_opacity(0.5)])
    return video



def main():
    
    voice_over_name="test_audio_1.wav"
    backgound_video_path=get_random("../contents_bg/background_video/")
    backgound_audio_path=get_random("../contents_bg/background_audio/")
    
    main_voice=AudioFileClip(f"../temp/audios/{voice_over_name}")
    duration=main_voice.duration+3
    bg_audio=AudioFileClip(backgound_audio_path).fx(afx.volumex, 0.1).set_duration(duration)
    bg_video=crop_video(VideoFileClip(backgound_video_path).set_duration(duration))

    
    bg_audio=clip_for_duration(bg_audio,duration)
    bg_video=clip_for_duration(bg_video.resize((1080,1920)),duration)

    
    final_audio=CompositeAudioClip([bg_audio,main_voice])
    final_video=bg_video.set_audio(final_audio)

    # change watermark according to channel name
    final_video=set_watermark(final_video,text="@quotino")
    
    raw_data=get_audio_timestamp(audio_name=voice_over_name)
    words=raw_data['result']
    print(raw_data)
    sentence=raw_data
    final_video=add_caption(final_video,words).set_duration(duration)

    final_video.write_videofile("../temp/outputs/test.mp4", codec="libx264")
    

if __name__=="__main__":
    main()