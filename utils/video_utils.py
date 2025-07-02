import cv2 
import os 

def read_video(video_path):
    cap = cv2.VideoCapture(video_path)
    frames = [] 
    while True: 
        ret, frame = cap.read()
        if not ret: 
            break  
        frames.append(frame)
    return frames

def save_video(output_frames, output_path, fps=24.0): 
    if not os.path.exists(os.path.dirname(output_path)): 
        os.makedirs(os.path.dirname(output_path))

    fourcc = cv2.VideoWriter_fourcc(*'XVID') 
    out = cv2.VideoWriter(output_path, fourcc, fps, (output_frames[0].shape[1], output_frames[0].shape[0]))

    for frame in output_frames: 
        out.write(frame)
    out.release()

