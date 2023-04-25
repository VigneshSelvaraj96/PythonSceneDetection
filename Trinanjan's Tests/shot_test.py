import cv2

# Open the video file
cap = cv2.VideoCapture('./output-Scene-036.mp4')

# Read the first frame
ret, prev_frame = cap.read()
prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

# Set the threshold for frame difference
threshold = 20

# Initialize a variable to store the previous shot change timestamp
prev_shot_change_timestamp = 0

# Loop through the frames
while True:
    # Read the next frame
    ret, curr_frame = cap.read()
    if not ret:
        break

    # Convert the current frame to grayscale
    curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)

    # Compute the absolute difference between the current and previous frames
    frame_diff = cv2.absdiff(curr_gray, prev_gray)

    # Apply thresholding to the frame difference
    _, thresh = cv2.threshold(frame_diff, threshold, 255, cv2.THRESH_BINARY)

    # Find contours in the thresholded frame difference
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Loop through the contours and check their areas
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1000:  # Adjust this threshold to control shot change detection sensitivity
            # Log the timestamp of the shot change
            curr_timestamp = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0  # Convert to seconds
            if curr_timestamp - prev_shot_change_timestamp > 1:  # Set a minimum time interval between shot changes
                print("Shot change detected at timestamp: {:.2f} seconds".format(curr_timestamp))
                prev_shot_change_timestamp = curr_timestamp

    # Display the current frame with shot change detections
    cv2.imshow('Shot Detection', curr_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Update the previous frame
    prev_gray = curr_gray

# Release the video file and close all windows
cap.release()
cv2.destroyAllWindows()
