from utils import read_video, save_video
from trackers import PlayerTracker, BallTracker
from drawers import (PlayerTracksDrawer, BallTracksDrawer)
from team_assigner import TeamAssigner
from ball_acqusition import BallAcquisitionDetector

def main(): 
    
    video_frames = read_video("input_videos/video_1.mp4")

    player_tracker = PlayerTracker("models/player_detector.pt")
    player_tracks = player_tracker.get_object_tracks(video_frames,
                                                     read_from_stub = True,
                                                     stub_path = "stubs/player_tracks_stubs.pkl"
                                                     )
    ball_tracker = BallTracker("models/ball_detector.pt")
    ball_tracks = ball_tracker.get_object_tracks(video_frames,
                                                 read_from_stub = True,
                                                 stub_path = "stubs/ball_tracks_stubs.pkl"
                                                 )

    ball_tracks = ball_tracker.remove_wrong_detections(ball_tracks)
    ball_tracks = ball_tracker.interpolate_ball_position(ball_tracks)
    team_assigner = TeamAssigner()
    player_assignment = team_assigner.get_player_teams_across_frames(video_frames, 
                                                                     player_tracks, 
                                                                     read_from_stub = True, 
                                                                     stub_path = "stubs/player_assignment_stub.pkl"
                                                                     )

    ball_acquisition_detector = BallAcquisitionDetector()
    ball_acquisition = ball_acquisition_detector.detect_ball_possession(player_tracks, ball_tracks)

    player_tracks_drawer = PlayerTracksDrawer()
    ball_tracks_drawer = BallTracksDrawer()

    output_video_frames = player_tracks_drawer.draw(video_frames, 
                                                    player_tracks, 
                                                    player_assignment, 
                                                    ball_acquisition
                                                    )
    
    output_video_frames = ball_tracks_drawer.draw(output_video_frames, ball_tracks)
    save_video(output_video_frames, "output_videos/output_video.avi")

if __name__ == "__main__": 
    main()
