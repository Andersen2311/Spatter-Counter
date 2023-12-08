import cv2
import os
from datetime import datetime

def is_bounding_box_within_exclusion_zone(bounding_box, exclusion_radius, exclusion_x, exclusion_y):
    x, y, w, h = bounding_box

    center_x = x + w // 2
    center_y = y + h // 2

    distance_from_exclusion_center = ((center_x - exclusion_x)**2 + (center_y - exclusion_y)**2)**0.5

    return distance_from_exclusion_center <= exclusion_radius

exclusion_radius = 50
exclusion_x, exclusion_y = (300 // 2, (300 // 2) - 60)

object_detector = cv2.createBackgroundSubtractorKNN()

object_count = 0
frame_spark_count = 0

dato = datetime.today().strftime('%Y-%m-%d_%H:%M:%S')

image_folder = "/Users/heinz/Desktop/Projekt Test/Billeder"

desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
spark_count_file = open(os.path.join(desktop_path, f"{dato}new_spark_counts.csv"), "w")

image_count = 0

sorted_filenames = sorted(os.listdir(image_folder))

for filename in sorted_filenames:
    image_path = os.path.join(image_folder, filename)
    frame = cv2.imread(image_path)

    height, width, _ = frame.shape.index()
    roi = frame[0:300, 100:400]

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

    cv2.putText(frame, f"Objects Tracked: {object_count}", (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    #cv2.imshow("Mask", mask)
    #cv2.imshow("Frame", frame)
    cv2.imshow("roi", roi)

    key = cv2.waitKey(1)

    if key == 27:
        break

    spark_count_file.write(f"{filename}: {frame_spark_count}\n")

    frame_spark_count = 0

total_spark_count = object_count

spark_count_file.seek(0)
spark_count_file.write(f"Total Spark Count: {total_spark_count}\n\n")

print(object_count)
spark_count_file.close()
cv2.destroyAllWindows()



