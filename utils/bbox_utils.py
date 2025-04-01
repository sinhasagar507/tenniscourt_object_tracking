import numpy as np
def get_center_of_bbox(bbox):
    """
    Calculate the center of a bounding box.

    Parameters:
        bbox (list): A list containing the coordinates of the bounding box in the format [x1, y1, x2, y2].

    Returns:
        tuple: A tuple containing the x and y coordinates of the center of the bounding box.
    """
    x1, y1, x2, y2 = bbox
    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2
    return (center_x, center_y)

def measure_distance(point1, point2):
    """
    Calculate the Euclidean distance between two points.

    Parameters:
        point1 (tuple): A tuple containing the x and y coordinates of the first point.
        point2 (tuple): A tuple containing the x and y coordinates of the second point.

    Returns:
        float: The Euclidean distance between the two points.
    """
    return np.linalg.norm(np.array(point1) - np.array(point2))