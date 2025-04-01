from utils import save_video, read_video
from trackers import PlayerTracker, BallTracker
from court_line_detector import CourtLineDetector
import cv2

def main():
    
    # Read in the input-video frame
    input_video_path = "data/input_video.mp4"
    video_frames = read_video(input_video_path)
    
    # Detect players
    player_tracker = PlayerTracker(model_path="yolov8x.pt")
    ball_tracker = BallTracker(model_path="models/yolov5_last.pt")
    
    player_detections = player_tracker.detect_frames(video_frames, 
                                                     read_from_stub=True, 
                                                     stub_path="tracker_stubs/player_detections.pkl")
    ball_detections = ball_tracker.detect_frames(video_frames,
                                                 read_from_stub=False, 
                                                 stub_path="tracker_stubs/ball_detections.pkl")
    
    ball_detections = ball_tracker.interpolate_ball_positions(ball_detections)
    
    court_model_path = "models/keypoints_model_1.pth"
    courtLine_detector = CourtLineDetector(model_path=court_model_path)
    court_keypoints = courtLine_detector.predict(video_frames[0])
    
    
    # Choose players 
    player_detections = player_tracker.choose_and_filter_players(court_keypoints, player_detections)
    
    # Draw bounding boxes around players, ball and court lines
    output_video_frames = player_tracker.draw_bounding_boxes(video_frames, player_detections)
    output_video_frames = ball_tracker.draw_bounding_boxes(output_video_frames, ball_detections)
    output_video_frames = courtLine_detector.draw_keypoints_on_video(output_video_frames, court_keypoints)
    
    
    # Draw frame number on top left corner 
    for i, frame in enumerate(output_video_frames):
        cv2.putText(frame, f"Frame: {i}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    # output_video_path = "data/output_videos/output_video.avi"
    # output_video_path_ball = "data/output_videos/output_video_ball.avi"
    output_video_path = "data/output_videos/output_video.avi"
    
    # Save the output video with player bounding boxes
    # save_video(output_video_frames, output_video_path)
    # save_video(output_video_path_ball, output_video_path_ball)
    save_video(output_video_frames, output_video_path)
    
if __name__ == '__main__':
    main()