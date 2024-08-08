# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 16:57:00 2024

@author: enesm
"""

import os
f = open("videos.txt", "r")
text=f.read()
video_lists=text.split("\n")

from faster_whisper import WhisperModel
from pytubefix import YouTube
from pytubefix.cli import on_progress

model_size = "large-v3"

# Run on GPU with FP16
model = WhisperModel(model_size, device="cuda", compute_type="float16")


import pandas as pd
video_dict={"sentence":[],"start":[],"end":[],"video_id":[]}
for video_id in video_lists:
    

    
    url = f"https://www.youtube.com/watch?v={video_id}"
    print(url)
    yt = YouTube(url, on_progress_callback = on_progress)
    ys = yt.streams[-1]
    print(ys)
    ys.download(filename=f'sign_audios/{video_id}.mp4')
    segments, info = model.transcribe(f"sign_audios/{video_id}.mp4", beam_size=3, language="tr")
    
    for segment in segments:
        video_dict["sentence"].append(segment.text)
        video_dict["start"].append(segment.start)
        video_dict["end"].append(segment.end)
        video_dict["video_id"].append(video_id)
pd.DataFrame.from_dict(video_dict).to_csv(f'out.csv', index=False)  

