from utils import read_video, save_video
from trackers import PlayerTracker

def main(): 
    
    video_frames = read_video("input_videos/video_1.mp4")

    player_tracker = PlayerTracker("models/player_detector.pt")
    player_tracks = player_tracker.get_object_tracks(video_frames)

    print(player_tracks)

    save_video(video_frames, "output_videos/output_video.avi")

if __name__ == "__main__": 
    main()
