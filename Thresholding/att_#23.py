import cv2
import os
import datetime as dt

### Input path to folder containing images, for the program to count sparks.
# Image folder path
IMAGE_FOLDER = "INSERT FOLDER PATH HERE"
assert IMAGE_FOLDER is not None








def eventExclusionZone(bounding_box, exclusion_radius, exclusion_x, exclusion_y):
    # Extract bounding box coordinates
    x, y, w, h = bounding_box

    # Calculate center of the bounding box
    center_x = x + w // 2
    center_y = y + h // 2

    # Determine if the bounding box center lies within the exclusion zone
    distance_from_exclusion_center = ((center_x - exclusion_x)**2 + (center_y - exclusion_y)**2)**0.5

    return distance_from_exclusion_center <= exclusion_radius

#String time from datetime package
now = dt.datetime.now()
dato = now.strftime("%d-%m-%Y_%H-%M-%S")
hour = now.strftime("%H-%M")

# Define exclusion zone parameters
EXCLUSION_RADIUS = 80  # Radius of the exclusion circle
EXCLUSION_CENTER = (268, 175 )  # Coordinates of the exclusion zone center

# Initialize counts
object_count = 0
frame_spark_count = 0

# Save print/output file to the desktop
DESKTOP_PATH = os.path.join(os.path.expanduser('~'), 'Desktop/Tests')
assert DESKTOP_PATH is not None, "Failed to find folder named 'Tests'. Check whether the folder was created as per the instructions or if it was spelled correctly."
SPARK_COUNT_FILE_PATH = os.path.join(DESKTOP_PATH, f"{dato}-sparkCounts.csv")
assert SPARK_COUNT_FILE_PATH is not None, "Failed to write .csv file. Did DESKTOP_PATH fail?"

# Sort filenames in ascending order
sorted_filenames = sorted([os.path.join(IMAGE_FOLDER, filename) for filename in os.listdir(IMAGE_FOLDER)])
assert sorted_filenames is not None, "Failed sorting, check correct import"

# Looping for each file in folder
with open(SPARK_COUNT_FILE_PATH, "w") as spark_count_file:
    for filename in sorted_filenames:
        image_path = os.path.join(IMAGE_FOLDER, filename)
        frame = cv2.imread(image_path)
        frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        ret, thresh = cv2.threshold(frameGray, 60, 255, cv2.THRESH_BINARY)

        # Check if the image is loaded successfully
        if frame is None:
            print(f"Error loading image: {image_path}")
            continue

        roi = thresh        
        mask = roi
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        filtered_detections = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if 2 < area < 400:
                bounding_box = cv2.boundingRect(cnt)

                object_count += 1
                frame_spark_count += 1

                if not eventExclusionZone(bounding_box, EXCLUSION_RADIUS, *EXCLUSION_CENTER):
                    filtered_detections.append(bounding_box)
        
        key = cv2.waitKey(10)

        if key == 27:
            break

        # Write frame spark count to file, with new format
        spark_count_file.write(f"{filename}+{hour}, on this frame, counted amount is = {frame_spark_count}\n")

        # Reset spark count for next frame
        frame_spark_count = 0

    # Total spark count
    total_spark_count = object_count

    # Write total spark count to the beginning of the sheet
    spark_count_file.seek(0)
    spark_count_file.write(f"Total Spark Count: {total_spark_count}\n")


print(object_count)
if object_count <= 0:
    print(IMAGE_FOLDER)
else:
    print("File path not found")

cv2.destroyAllWindows()

