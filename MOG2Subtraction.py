import cv2
import os

def is_bounding_box_within_exclusion_zone(bounding_box, exclusion_radius, exclusion_x, exclusion_y):
    # Extract bounding box coordinates
    x, y, w, h = bounding_box

    # Calculate center of the bounding box
    center_x = x + w // 2
    center_y = y + h // 2

    # Determine if the bounding box center lies within the exclusion zone
    distance_from_exclusion_center = ((center_x - exclusion_x)**2 + (center_y - exclusion_y)**2)**0.5

    return distance_from_exclusion_center <= exclusion_radius

# Define exclusion zone parameters
exclusion_radius = 50  # Radius of the exclusion circle
exclusion_x, exclusion_y = (300 // 2, (300 // 2)-60)  # Coordinates of the exclusion zone center

# Object detection
object_detector = cv2.createBackgroundSubtractorMOG2(history=5, varThreshold=48)

object_count = 0
frame_spark_count = 0  # Initialize frame spark count

image_folder = PATH

# Save the text file to the desktop
desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
spark_count_file = open(os.path.join(desktop_path, "spark_countsMOG2.csv"), "w")

image_count = 0

# Sort filenames in ascending order
sorted_filenames = sorted(os.listdir(image_folder))

for filename in sorted_filenames:
    image_path = os.path.join(image_folder, filename)
    frame = cv2.imread(image_path)

    height, width, _ = frame.shape
    roi = frame[0:300, 100:400]

    # Initialize mask before using it
    mask = object_detector.apply(roi)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    filtered_detections = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 5 and area < 200:
            bounding_box = cv2.boundingRect(cnt)

            object_count += 1
            frame_spark_count += 1

            if not is_bounding_box_within_exclusion_zone(bounding_box, exclusion_radius, exclusion_x, exclusion_y):
                filtered_detections.append(bounding_box)

    for bounding_box in filtered_detections:
        x, y, w, h = bounding_box
        cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 3)

    # Display the number of objects tracked
    cv2.putText(frame, f"Objects Tracked: {object_count}", (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    #cv2.imshow("Mask", mask)
    #cv2.imshow("Frame", frame)
    cv2.imshow("roi", roi)

    key = cv2.waitKey(1)

    if key == 27:
        break

    # Write frame spark count to text file
    spark_count_file.write(f"{filename}: {frame_spark_count}\n")

    # Reset frame spark count for next frame
    frame_spark_count = 0

# Calculate total spark count
total_spark_count = object_count

# Write total spark count to the beginning of the file
spark_count_file.seek(0)
spark_count_file.write(f"Total Spark Count: {total_spark_count}\n\n")

print(object_count)
spark_count_file.close()
cv2.destroyAllWindows()