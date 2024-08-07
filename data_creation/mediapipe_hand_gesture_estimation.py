"""
şimdi bizim 3d contruscion için uğraşmamız çok sıkınıtlı, her kişinin bone featurelri ile model eğitmek görselleştirmek çoook uzun
onun yerine pose featurlar openpose ile çıakcak ve hand ise mediapipe dan, hand için kendi scriptim var, tüm framlerde mesela
sol el bir framde gözükmediyse gözüken ve gözükmeyen arasına koyucam, basit bir yöntem ama işe yarar reconstrution için,
diğer özellikler çok kötü çalışıyor, ve küçük el hareketeriden eksiklikler çok sıkınıt yapmaz
pose lardan gerekenler o skelatl modeli kullanıp gerekneleri alıcaz ve kafayı 0,0 norması sayabiliriz

"""


#subprocess ile openpose çalıştıran ve jsona kaydeden bir script
# bin\OpenPoseDemo.exe --video examples/media/out.mp4 --scale_number 4 --scale_gap 0.25 --save_json 


#mediapipe ile hand pose estimation
"""
burada kendi tracking rule based check yapalım pose data wrist verisi varsa
mediapipe model 0. veri ile openpose 4 veya 7. veri arasındaki fark 60 pikselden küçük mü na bakıcaz eğer değilse durdursun ve tespit edilmiş mi bakalım


confidence score ile bu poz verilerini de kaydet
"""


import cv2
import mediapipe as mp
import json
import os
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
mp_holistic = mp.solutions.holistic
rwrist=0
import math
lwrist=0
import time
def save_results_to_json(results, filename, image_width, image_height,image):
    
    if os.path.exists(filename):
       try:
        with open(filename, 'r') as f:
          output = json.load(f)
       except:
           print(filename)
       try:
         person = output["people"][0]
       except:
           return image
    else:
        print(filename+"bu dosya buraya kadar açık")
        image="hata"
        return image
        
       
       

    
    if results.multi_hand_landmarks:
        #print(len(results.multi_hand_landmarks))
        for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
            hand_keypoints_2d = []
            out=0
            for landmark in hand_landmarks.landmark:
                hand_keypoints_2d.extend([
                    landmark.x * image_width, 
                    landmark.y * image_height, 
                    results.multi_handedness[i].classification[0].score
                ])
                if len(hand_keypoints_2d)<4:
                    #print(hand_keypoints_2d)
                    #print(person["pose_keypoints_2d"][15:18])
                    #print(person["pose_keypoints_2d"][24:27])
                    rwrist_index = 4 * 3  # RWrist index (4th keypoint)
                    lwrist_index = 7 * 3  # LWrist index (7th keypoint)

    
                    rwrist = (int(person["pose_keypoints_2d"][rwrist_index]), int(person["pose_keypoints_2d"][rwrist_index + 1]))
                    lwrist = (int(person["pose_keypoints_2d"][lwrist_index]), int(person["pose_keypoints_2d"][lwrist_index + 1]))
                    distance=min(math.sqrt((rwrist[0]-hand_keypoints_2d[0])**2+(rwrist[1]-hand_keypoints_2d[1])**2),math.sqrt((lwrist[0]-hand_keypoints_2d[0])**2+(lwrist[1]-hand_keypoints_2d[1])**2))
                    #print(distance)
                    if distance>60:
                        cv2.circle(image, (rwrist), 10, (255,255,0), -1)
                        cv2.circle(image, (lwrist), 10, (255,255,0), -1)
                        out=1
                        break
                    cv2.circle(image, (rwrist), 10, (255,0,0), -1)
                    cv2.circle(image, (lwrist), 10, (255,0,0), -1)
            score=results.multi_handedness[i].classification[0].score
            #(score)
            if results.multi_handedness[i].classification[0].label == 'Left':
                if out:
                    person["hand_left_keypoints_2d"]=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                else:
                    person["hand_left_keypoints_2d"] = hand_keypoints_2d
            else:
                if out:
                    person["hand_right_keypoints_2d"]=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                else:
                    person["hand_right_keypoints_2d"] = hand_keypoints_2d
    if len( person["hand_left_keypoints_2d"])<1:
        
         person["hand_left_keypoints_2d"]=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    if len( person["hand_right_keypoints_2d"])<1:
         person["hand_right_keypoints_2d"]=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    output["people"][0]=person
    with open(filename, 'w') as f:
        json.dump(output, f, indent=4)
    return image
# For webcam input:
"""    
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output2.avi', fourcc, 20.0, (720, 1080))
"""


data_lists=os.listdir("pose_results")
# Process and save hand data
for vid_id in data_lists:
 frame_idx = 0
 cap = cv2.VideoCapture(f"sign_videos_processed/{vid_id}.mp4")
 with mp_hands.Hands(
    model_complexity=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.8) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            break

        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)
        image.flags.writeable = True
        image_height, image_width, _ = image.shape
        image=save_results_to_json(results, f'pose_results/{vid_id}/{vid_id}_{str(frame_idx).zfill(12)}_keypoints.json', image_width, image_height,image)
        frame_idx += 1
        if image=="hata":
            print(str(vid_id)+"hataa")
            print(frame_idx)
            break
        
        
        """
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

        cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
        out.write(image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
        
        if frame_idx%10==0:
            print("frame: "+str(frame_idx))
        """
cap.release()
"""
out.release()
"""