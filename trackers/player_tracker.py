from ultralytics import YOLO  # Import YOLO model from Ultralytics
import cv2  # Import OpenCV
import pickle as pkl # Import pickle for saving/loading data

import sys
sys.path.append("../")  # Add parent directory to the system path

from utils import measure_distance, get_center_of_bbox


class PlayerTracker:
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
        
    def choose_players(self, court_keypoints, player_dict):
        distances = []
        
        for track_id, bbox in player_dict.items():
            player_center = get_center_of_bbox(bbox)
            
            min_distance = float('inf')
            for i in range(0, len(court_keypoints), 2):
                court_keypoint = (court_keypoints[i], court_keypoints[i+1])
                distance = measure_distance(player_center, court_keypoint)
                
                if distance < min_distance:
                    min_distance = distance
            # Append the track ID and the minimum distance to the list
            distances.append((track_id, min_distance))
            
        # Sort the distances in ascending order
        distances.sort(key=lambda x: x[1])
        
        # Choose the first two players based on the minimum distance
        chosen_players = [distances[0][0], distances[1][0]]
        return chosen_players
            
        
    def choose_and_filter_players(self, court_keypoints, player_detections):
        """Chooses and filters nearest players based on their positions relative to the court keypoints.
        """
        player_detections_first_frame = player_detections[0]
        chosen_player = self.choose_players(court_keypoints, player_detections_first_frame)
        filtered_player_detections = []
        for player_dict in player_detections:
            filtered_player_dict = {track_id: bbox for track_id, bbox in player_dict.items() if track_id in chosen_player}
            filtered_player_detections.append(filtered_player_dict)
        return filtered_player_detections
        
    def detect_frames(self, frames, read_from_stub=False, stub_path=None):
        """Detects and tracks players across an entire video
        """
        player_detections = []
        
        if read_from_stub:
            # Load player detections from a pickle file
            with open(stub_path, 'rb') as f:
                player_detections = pkl.load(f)
            return player_detections
        
        for frame in frames:
            player_dict = self.detect_frame(frame)
            player_detections.append(player_dict)
            
        if stub_path is not None:
            # Save the player detections to a pickle file
            with open(stub_path, 'wb') as f:
                pkl.dump(player_detections, f)
            
        return player_detections
            

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
        results = self.model.track(frame, persist=True)[0]  

        # Retrieve object class names from the model results
        id_name_dict = results.names  

        # Dictionary to store detected players (track ID as key, bounding box as value)
        player_dict = {}

        # Iterate over all detected bounding boxes in the frame
        for box in results.boxes:
            track_id = int(box.id.tolist()[0])  # Extract the tracking ID of the detected object
            result = box.xyxy[0].tolist()  # Get bounding box coordinates in [x_min, y_min, x_max, y_max] format

            # Extract class ID and convert to class name
            object_cls_id = box.cls.tolist()[0]  
            object_cls_name = id_name_dict[object_cls_id]  

            # Check if the detected object is a "person"
            if object_cls_name == "person":
                player_dict[track_id] = result  # Store the player’s bounding box with its tracking ID

        return player_dict  # Return dictionary containing detected players
    
    def draw_bounding_boxes(self, video_frames, player_detections):
        """Draw bounding boxes around detected players in each frame of the video"""
        output_video_frames = []
        
        for frame, player_dict in zip(video_frames, player_detections):
            # Draw bounding boxes around detected players
            for track_id, bbox in player_dict.items():
                x_min, y_min, x_max, y_max = bbox
                cv2.putText(frame, f"Player {track_id}", (int(bbox[0]), int(bbox[1] - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2) # Draw the player ID
                
                cv2.rectangle(frame, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (0, 0, 255), 2) # Draw a blue rectangle around the player AND 2 
            output_video_frames.append(frame)
            
        return output_video_frames