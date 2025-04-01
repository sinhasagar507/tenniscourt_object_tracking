import cv2

def read_video(input_video_path):
    """
    Reads a video file and returns a list of frames.

    Parameters:
    input_video_path (str): The file path of the video to be read.

    Returns:
    list of numpy arrays: A list of frames (images) read from the video.
    """

    # Initialize the VideoCapture object
    cap = cv2.VideoCapture(input_video_path)

    # Initialize the list to store the frames
    video_frames = []

    # Loop through the video frames
    while cap.isOpened():
        # Read the next frame
        ret, frame = cap.read()

        # If the frame was read successfully, add it to the list
        if ret:
            video_frames.append(frame)
        else:
            break

    # Release the VideoCapture to finalize
    cap.release()

    return video_frames

def save_video(output_video_frames, output_video_path):
    """
    Saves a sequence of frames as a video file.

    Parameters:
    output_video_frames (list of numpy arrays): A list of frames (images) to be written as a video.
    output_video_path (str): The file path where the video will be saved.

    Returns:
    None
    """

    # Define the codec for the output video (MJPG - Motion JPEG)
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')

    # Initialize the VideoWriter object
    # - output_video_path: File path to save the video
    # - fourcc: Video codec
    # - 25.0: Frame rate (FPS)
    # - (width, height): Resolution of the video, derived from the first frame
    out = cv2.VideoWriter(
        output_video_path, 
        fourcc, 
        25.0, 
        (output_video_frames[0].shape[1], output_video_frames[0].shape[0])
    )

    # Loop through each frame in the list and write it to the video file
    for frame in output_video_frames:
        out.write(frame)

    # Release the VideoWriter to finalize and save the video file
    out.release()