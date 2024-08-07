from pytubefix import YouTube
from pytubefix.cli import on_progress
import subprocess


file1 = open('sign_data/videos.txt', 'r')
Lines = file1.readlines()
videos_list=[]
count = 0
# Strips the newline character
for line in Lines:
    count += 1
    videos_list.append(line.strip())



import cv2

def crop_video(input_file, output_file, width, height, x, y, codec='XVID', bitrate=None):
    # Open the input video
    cap = cv2.VideoCapture(input_file)

    # Check if the video was opened successfully
    if not cap.isOpened():
        print(f"Error: Could not open video {input_file}")
        return

    # Get the frames per second (fps) of the input video
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*codec)
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Crop the frame
        cropped_frame = frame[y:y+height, x:x+width]

        # Write the cropped frame to the output video
        out.write(cropped_frame)

    # Release the video capture and writer objects
    cap.release()
    out.release()

    # Close all OpenCV windows
    cv2.destroyAllWindows()

    print(f"Video saved as {output_file}")


codec = 'XVID'  # Change to the codec you prefer


for video_url in videos_list:
    yt = YouTube("https://www.youtube.com/watch?v="+video_url, on_progress_callback = on_progress)
    is_downloaded=0
    for stream in yt.streams:
        if stream.resolution=="1080p":
            stream.download(filename=f'sign_videos/{video_url}.mp4')
            print(yt.title+" is downloading...")
            is_downloaded=1
            break
    if is_downloaded:
        input_file = f'sign_videos/{video_url}.mp4'
        output_file = f'sign_videos_processed/{video_url}.mp4'
        width, height, x, y = 720, 1080, 1200, 0

        crop_video(input_file, output_file, width, height, x, y,codec)
    else:
        print(yt.title+" doesnt have any 1080p stream")
   