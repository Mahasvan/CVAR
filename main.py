import cv2
import numpy as np

# Define the ArUco dictionary and parameters
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)  # Use the desired dictionary type
parameters =  cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

running = cv2.imread('running.png')
interrupted = cv2.imread('interrupted.png')
done = cv2.imread('done.png')

# Initialize the webcam
cap = cv2.VideoCapture(0)

import timer

duration_string = input("Enter time for the timer (ex: 10m30s): ")
seconds = timer.get_seconds_from_input(duration_string)

timer.timer(seconds)

print("Timer started for " + timer.pretty_time_from_seconds(seconds))

while True:
    # Read a frame from the webcamz
    ret, frame = cap.read()
    from timer import timer_done
    
    # Detect ArUco markers in the frame
    corners, ids, rejectedImgPoints = detector.detectMarkers(frame)
    if ids is not None:
        for marker_id, marker_corners in zip(ids, corners):

            if timer_done == 0:
                image_to_overlay = running
            elif timer_done == 1:
                image_to_overlay = done
            elif timer_done == 2:
                image_to_overlay = interrupted
            
            # print(marker_id)
            # print(list(marker_corners[0]))

            marker_size = int(marker_corners[0][1][0] - marker_corners[0][0][0])

            # print(marker_size)

            mask = np.zeros(frame.shape, dtype=np.uint8)
            cv2.fillPoly(mask, np.int32([marker_corners]), (255, 255, 255))
            try:
                overlay_resized = cv2.resize(image_to_overlay, (marker_size, marker_size))
            except cv2.error:
                continue

            marker_width = 100  # real world units

            overlay_width = image_to_overlay.shape[1]
            overlay_height = image_to_overlay.shape[0]
            dst_points = np.array([[0, 0], [overlay_width, 0], [overlay_width, overlay_height], [0, overlay_height]], dtype=np.float32)
            perspective_transform = cv2.getPerspectiveTransform(dst_points, marker_corners)

            overlay_warped = cv2.warpPerspective(image_to_overlay, perspective_transform, (frame.shape[1], frame.shape[0]))

            # print(overlay_resized.shape, overlay_warped.shape)

            alpha = 0.4
            frame = cv2.addWeighted(frame, alpha, overlay_warped, 1-alpha, 1)


    cv2.imshow('ArUco Marker with Overlay', frame)

    # Exit the loop when the 'q' key is pressed
    waitkey = cv2.waitKey(1) & 0xFF
    if waitkey == ord('q'):
        timer.stop_timer()
        print("Timer stopped.")
        break
    elif waitkey == ord('r'):
        print("Timer reset.")
        timer.set_timer_interrupted()
    

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
