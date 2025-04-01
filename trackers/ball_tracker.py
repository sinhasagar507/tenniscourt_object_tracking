from ultralytics import YOLO  # Import YOLO model from Ultralytics
import cv2  # Import OpenCV
import pickle as pkl  # Import pickle for saving/loading data
import pandas as pd 

class BallTracker:
    """
    A class to track players in a video using the YOLO object detection model.
    """

    def __init__(self, model_path):
        """
        Initializes the PlayerTracker with a given YOLO model.

        Parameters:
        model_path (str): Path to the YOLO model file.
        """
        self.model = YOLO(model_path)  # Load the YOLO model
        
    def interpolate_ball_positions(self, ball_positions):
        """
        Interpolates missing ball positions in a sequence of bounding boxes.

        This function expects `ball_positions` to be a list of dictionaries, where each dictionary
        contains a key `1` that maps to a list of four numbers representing the ball’s bounding box 
        coordinates in the format [x1, y1, x2, y2].

        For example:
            ball_positions = [
                {1: [100, 150, 200, 250]},
                {1: [102, 152, 202, 252]},
                {1: [105, 155, 205, 255]},
                # ... more frames
            ]

        The function performs the following steps:
            1. Extracts the bounding box list for each frame using key `1`.
            2. Converts the list of bounding boxes into a Pandas DataFrame with columns ["x1", "y1", "x2", "y2"].
            3. Interpolates any missing values in the DataFrame.
            4. Uses backfill to replace any remaining missing values.
            5. Converts the DataFrame back into a list of dictionaries in the original format.

        Parameters:
            ball_positions (list of dict): A list where each element is a dictionary with key `1` 
                                        mapping to a list of four bounding box coordinates.

        Returns:
            list of dict: A list of dictionaries containing the interpolated bounding box coordinates.
        """
        # Extract bounding box lists using key 1
        ball_positions = [x.get(1, []) for x in ball_positions]
        
        # Convert the list into a Pandas DataFrame with specified column names
        df_ball_positions = pd.DataFrame(ball_positions, columns=["x1", "y1", "x2", "y2"])
        
        # Interpolate missing values and backfill any remaining missing data
        df_ball_positions = df_ball_positions.interpolate()
        df_ball_positions = df_ball_positions.bfill()
        
        # Convert the DataFrame back into the original list of dictionaries format
        ball_positions = [{1: x} for x in df_ball_positions.to_numpy().tolist()]
        
        return ball_positions

        
    def detect_frames(self, frames, read_from_stub=False, stub_path=None):
        """Detects and tracks players across an entire video
        """
        ball_detections = []
        
        if read_from_stub:
            # Load player detections from a pickle file
            with open(stub_path, 'rb') as f:
                ball_detections = pkl.load(f)
            return ball_detections
        
        for frame in frames:
            player_dict = self.detect_frame(frame)
            ball_detections.append(player_dict)
            
        if stub_path is not None:
            # Save the player detections to a pickle file
            with open(stub_path, 'wb') as f:
                pkl.dump(ball_detections, f)
            
        return ball_detections
            

    def detect_frame(self, frame):
        """
        Detects and tracks players in a given video frame.

        Parameters:
        frame (numpy array): A single video frame.

        Returns:
        dict: A dictionary mapping track IDs to bounding box coordinates for detected players.
        """

        # Perform object detection and tracking on the frame
        # `persist=True` ensures the tracking information is maintained across frames
        results = self.model.predict(frame, conf=0.15)[0]  

        # Dictionary to store detected players (track ID as key, bounding box as value)
        ball_dict = {}

        # Iterate over all detected bounding boxes in the frame
        for box in results.boxes:
            result = box.xyxy[0].tolist()  # Get bounding box coordinates in [x_min, y_min, x_max, y_max] format  
            ball_dict[1] = result  # Store the player’s bounding box with its tracking ID

        return ball_dict  # Return dictionary containing detected players
    
    def draw_bounding_boxes(self, video_frames, ball_detections):
        """Draw bounding boxes around detected players in each frame of the video"""
        output_video_frames = []
        
        for frame, ball_dict in zip(video_frames, ball_detections):
            # Draw bounding boxes around detected players
            for track_id, bbox in ball_dict.items():
                x_min, y_min, x_max, y_max = bbox
                cv2.putText(frame, f"Ball {track_id}", (int(bbox[0]), int(bbox[1] - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2) # Draw the player ID
                cv2.rectangle(frame, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (0, 255, 0), 2) # Draw a blue rectangle around the player AND 2 
            output_video_frames.append(frame)
            
        return output_video_frames