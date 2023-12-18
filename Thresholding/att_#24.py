import cv2
import os
import datetime as dt

### Input path to folder containing images, for the program to count spatter.
# Image folder path
IMAGE_FOLDER = "/Volumes/T7/Uddannelse/3. sem/Projekt/2. omgang eksperimenter/Ny filter/Billeder til gruppen/3/4,5kw"
if IMAGE_FOLDER == None:
    print("Cannot find folder.")
    while IMAGE_FOLDER == None:
        break







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
frame_spatter_count = 0

# Save print/output file to the desktop
DESKTOP_PATH = os.path.join(os.path.expanduser('~'), 'Desktop/Tests')
#assert DESKTOP_PATH is not None, "Failed to find folder named 'Tests'. Check whether the folder was created as per the instructions or if it was spelled correctly."
if DESKTOP_PATH == None:
    print("Failed to find folder named 'Tests'. Check whether the folder was created as per the instructions or if it was spelled correctly.")
    while DESKTOP_PATH == None:
        break

SPATTER_COUNT_FILE_PATH = os.path.join(DESKTOP_PATH, f"{dato}-spatterCounts.csv")
#assert SPATTER_COUNT_FILE_PATH is not None, "Failed to write .csv file. Did DESKTOP_PATH fail?"
if SPATTER_COUNT_FILE_PATH == None:
    print("Failed to write .csv file. Did DESKTOP_PATH fail?")
    while SPATTER_COUNT_FILE_PATH == None:
        break


# Sort filenames in ascending order
sorted_filenames = sorted([os.path.join(IMAGE_FOLDER, filename) for filename in os.listdir(IMAGE_FOLDER)])
assert sorted_filenames is not None, "Failed sorting, check correct import"

# Looping for each file in folder
with open(SPATTER_COUNT_FILE_PATH, "w") as spatter_count_file:
    for filename in sorted_filenames:
        image_path = os.path.join(IMAGE_FOLDER, filename)
        frame = cv2.imread(image_path)
        frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        ret, thresh = cv2.threshold(frameGray, 50, 255, cv2.THRESH_BINARY)

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
                frame_spatter_count += 1

                if not eventExclusionZone(bounding_box, EXCLUSION_RADIUS, *EXCLUSION_CENTER):
                    filtered_detections.append(bounding_box)
        
        key = cv2.waitKey(10)

        if key == 27:
            break

        # Write frame spatter count to file, with new format
        spatter_count_file.write(f"{filename}+{hour}, on this frame, counted amount is = {frame_spatter_count}\n")

        # Reset spatter count for next frame
        frame_spatter_count = 0

    # Total spatter count
    total_spatter_count = object_count

    # Write total spatter count to the beginning of the sheet
    spatter_count_file.seek(0)
    spatter_count_file.write(f"Total Spatter Count: {total_spatter_count}\n")


print(object_count)
if object_count <= 0:
    print(IMAGE_FOLDER)
else:
    print("File path not found")

cv2.destroyAllWindows()

