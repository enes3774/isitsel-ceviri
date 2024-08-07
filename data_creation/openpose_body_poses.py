# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 15:42:43 2024

@author: enesm
"""
#yaklaşık 4gb VRAM ile çalışıyor, sadece iskelet pozları için

import subprocess
import os

video_ids=os.listdir("sign_videos_processed")


# Define the command and its arguments
for video_id in video_ids:
    command = [
    'bin\\OpenPoseDemo.exe',
    '--video', f'sign_videos_processed/{video_id}.mp4',
    '--scale_number', '4',
    '--scale_gap', '0.25',
    '--write_json', f'pose_results/{video_id}/',
    '--number_people_max', '1',
    '--display', '0',
    '--render_pose', '0'
]


    result = subprocess.run(command, capture_output=True, text=True)
    print(f"{video_id} bitti")
    print(result)