import cv2
import sys
sys.path.append("../")
import sre_constants

class MiniCourt():
    def __init__(self, frame):
        self.drawing_rectangle_width = 250  # Set the width of the rectangle to be drawn on the court
        self.drawing_rectangle_height = 450 # Set the height of the rectangle to be drawn on the court
        self.buffer = 50 # Buffer to be used around the drawing area
        self.padding_count = 20 # Padding for other drawing purposes (possibly for spacing elements)

        self.set_canvas_background_box_position(frame) # Initialize the position of the canvas background box using the given frame
        self.set_mini_court_position() # Set the position of the mini court based on the canvas background box
        
        
    def set_court_drawing_kepypoints(self):
        drawing_keypoints = [0] * 28
        
        # Point 0 
        drawing_keypoints[0], drawing_keypoints[1] = self.court_start_x, self.court_start_y # Top left corner of the mini court
        # Point 1
        drawing_keypoints[2], drawing_keypoints[3] = self.court_end_x, self.court_start_y # Top right corner of the mini court
        
        
        
    def set_mini_court_position(self):
        self.court_start_x = self.start_x + self.padding_count # Calculate the starting x-coordinate for the mini court
        self.court_start_y = self.start_y + self.padding_count # Calculate the starting y-coordinate for the mini court
        self.court_end_x = self.end_x - self.padding_count # Calculate the ending x-coordinate for the mini court
        self.court_end_y = self.end_y - self.padding_count # Calculate the ending y-coordinate for the mini court
        self.court_drawing_width = self.court_end_x - self.court_start_x # Calculate the width of the mini court

    def set_canvas_background_box_position(self, frame):
        frame = frame.copy()

        self.end_x = frame.shape[1] - self.buffer  # Calculate the ending x-coordinate (right edge) of the drawing box
        self.end_y = self.buffer + self.drawing_rectangle_height # Calculate the ending y-coordinate (bottom edge) of the drawing box
        self.start_x = self.end_x - self.drawing_rectangle_width # Calculate the starting x-coordinate (left edge) based on end_x and width
        self.start_y = self.end_y - self.drawing_rectangle_height # Calculate the starting y-coordinate (top edge) based on end_y and height
