import cv2
import sys
sys.path.append("../")
import constants
from utils import convert_pixel_distance_to_meters, convert_meters_distance_to_pixels

class MiniCourt():
    def __init__(self, frame):
        self.drawing_rectangle_width = 250  # Set the width of the rectangle to be drawn on the court
        self.drawing_rectangle_height = 450 # Set the height of the rectangle to be drawn on the court
        self.buffer = 50 # Buffer to be used around the drawing area
        self.padding_count = 20 # Padding for other drawing purposes (possibly for spacing elements)

        self.set_canvas_background_box_position(frame) # Initialize the position of the canvas background box using the given frame
        self.set_mini_court_position() # Set the position of the mini court based on the canvas background box
        self.set_court_drawing_kepypoints() # Set the key points for drawing the court
        self.set_court_lines() # Set the lines for the court
        
    def convert_meters_pixels(self, meters):
        return convert_meters_distance_to_pixels(meters, 
                                                 constants.DOUBLE_LINE_WIDTH, 
                                                 self.court_drawing_width
                                                )
        
    def set_court_drawing_kepypoints(self):
        drawing_key_points = [0]*28

        # point 0 
        drawing_key_points[0] , drawing_key_points[1] = int(self.court_start_x), int(self.court_start_y)
        # point 1
        drawing_key_points[2] , drawing_key_points[3] = int(self.court_end_x), int(self.court_start_y)
        # point 2
        drawing_key_points[4] = int(self.court_start_x)
        drawing_key_points[5] = self.court_start_y + self.convert_meters_to_pixels(constants.HALF_COURT_LINE_HEIGHT*2)
        # point 3
        drawing_key_points[6] = drawing_key_points[0] + self.court_drawing_width
        drawing_key_points[7] = drawing_key_points[5] 
        # #point 4
        drawing_key_points[8] = drawing_key_points[0] +  self.convert_meters_to_pixels(constants.DOUBLE_ALLY_DIFFERENCE)
        drawing_key_points[9] = drawing_key_points[1] 
        # #point 5
        drawing_key_points[10] = drawing_key_points[4] + self.convert_meters_to_pixels(constants.DOUBLE_ALLY_DIFFERENCE)
        drawing_key_points[11] = drawing_key_points[5] 
        # #point 6
        drawing_key_points[12] = drawing_key_points[2] - self.convert_meters_to_pixels(constants.DOUBLE_ALLY_DIFFERENCE)
        drawing_key_points[13] = drawing_key_points[3] 
        # #point 7
        drawing_key_points[14] = drawing_key_points[6] - self.convert_meters_to_pixels(constants.DOUBLE_ALLY_DIFFERENCE)
        drawing_key_points[15] = drawing_key_points[7] 
        # #point 8
        drawing_key_points[16] = drawing_key_points[8] 
        drawing_key_points[17] = drawing_key_points[9] + self.convert_meters_to_pixels(constants.NO_MANS_LAND_HEIGHT)
        # # #point 9
        drawing_key_points[18] = drawing_key_points[16] + self.convert_meters_to_pixels(constants.SINGLE_LINE_WIDTH)
        drawing_key_points[19] = drawing_key_points[17] 
        # #point 10
        drawing_key_points[20] = drawing_key_points[10] 
        drawing_key_points[21] = drawing_key_points[11] - self.convert_meters_to_pixels(constants.NO_MANS_LAND_HEIGHT)
        # # #point 11
        drawing_key_points[22] = drawing_key_points[20] +  self.convert_meters_to_pixels(constants.SINGLE_LINE_WIDTH)
        drawing_key_points[23] = drawing_key_points[21] 
        # # #point 12
        drawing_key_points[24] = int((drawing_key_points[16] + drawing_key_points[18])/2)
        drawing_key_points[25] = drawing_key_points[17] 
        # # #point 13
        drawing_key_points[26] = int((drawing_key_points[20] + drawing_key_points[22])/2)
        drawing_key_points[27] = drawing_key_points[21] 

        self.drawing_key_points=drawing_key_points

       
    def set_court_lines(self):
        self.lines = [
            (0, 2),
            (4, 5),
            (6,7),
            (1,3),
            
            (0,1),
            (8,9),
            (10,11),
            (10,11),
            (2,3)
        ]
        
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

    def draw_background_rectangle(self, frame):
        pass