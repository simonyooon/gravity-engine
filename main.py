from utils import read_video, save_video
from trackers import PlayerTracker, BallTracker
from drawers import (PlayerTracksDrawer, BallTracksDrawer, TeamBallControlDrawer)
from team_assigner import TeamAssigner
from ball_acqusition import BallAcquisitionDetector
from pass_and_interception import PassAndInterceptionDetector

def main(): 
    
    video_frames = read_video("input_videos/video_2.mp4")

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

    pass_and_interception_detector = PassAndInterceptionDetector()
    passes = pass_and_interception_detector.detect_passes(ball_acquisition, player_assignment)
    interceptions = pass_and_interception_detector.detect_interceptions(ball_acquisition, player_assignment)


    player_tracks_drawer = PlayerTracksDrawer()
    ball_tracks_drawer = BallTracksDrawer()
    team_ball_control_drawer = TeamBallControlDrawer()

    output_video_frames = team_ball_control_drawer.draw(video_frames, 
                                                        player_assignment, 
                                                        ball_acquisition)

    output_video_frames = player_tracks_drawer.draw(video_frames, 
                                                    player_tracks, 
                                                    player_assignment, 
                                                    ball_acquisition
                                                    )
    
    output_video_frames = ball_tracks_drawer.draw(output_video_frames, ball_tracks)
    save_video(output_video_frames, "output_videos/output_video.avi")

if __name__ == "__main__": 
    main()
