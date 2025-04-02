def convert_pixel_distance_meters(pixel_distance, reference_height_in_meters, reference_height_in_pixels):
    """
    Converts a distance in pixels to meters based on a reference height.

    Parameters:
    pixel_distance (float): The distance in pixels to be converted.
    reference_height_in_meters (float): The reference height in meters.
    reference_height_in_pixels (float): The reference height in pixels.

    Returns:
    float: The converted distance in meters.
    """
    # Calculate the conversion factor
    conversion_factor = reference_height_in_meters / reference_height_in_pixels
    
    # Convert the pixel distance to meters
    return pixel_distance * conversion_factor