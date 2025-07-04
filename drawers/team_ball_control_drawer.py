class TeamBallControlDrawer:
    def __init__(self):
        pass
    
    def draw(self, video_frames, player_assignment, ball_acquisition):
        team_ball_control = [] 

        for player_assignment_frame, ball_acquisition_frame in zip(player_assignment, ball_acquisition):
            if ball_acquisition_frame == -1:
                team_ball_control.append(-1)
                continue

            if ball_acquisition_frame not in player_assignment_frame:
                team_ball_control.append(-1)
                continue

            if player_assignment_frame[ball_acquisition_frame] == 1:
                team_ball_control.append(1)
            else:
                team_ball_control.append(2)

        return team_ball_control
    
    