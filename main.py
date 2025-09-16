import cv2
from tkinter import Tk
from tkinter.filedialog import askopenfilename

root = Tk()
root.title("Select Puzzle Files")   # set the title
# root.withdraw()   # don't hide the window if you want to see it

grid_filename = askopenfilename(title="Pick the grid file")
picture_filename = askopenfilename(title="Pick the picture file")

# Load image in grayscale
img = cv2.imread(grid_filename, cv2.IMREAD_GRAYSCALE)
 
# Apply Gaussian Blur to reduce noise
blur = cv2.GaussianBlur(img, (5, 5), 1.4)
 
# Apply Canny Edge Detector
edges = cv2.Canny(blur, threshold1=100, threshold2=20)
 
edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

# Replace white pixels with green
edges_bgr[edges == 255] = (0, 0, 0)
import cv2

# --- Load puzzle edges (from Canny) and the original puzzle photo ---

puzzle = cv2.imread(grid_filename)



# --- Fit another image to the puzzle’s size ---
overlay_img = cv2.imread(picture_filename)
overlay_resized = cv2.resize(overlay_img, (puzzle.shape[1], puzzle.shape[0]))

# --- Create a mask of the puzzle region ---
# (invert edges so puzzle area = white, outside = black)
mask = cv2.bitwise_not(edges)
mask = cv2.threshold(mask, 10, 255, cv2.THRESH_BINARY)[1]

# --- Apply the mask to overlay image ---
puzzle_filled = cv2.bitwise_and(overlay_resized, overlay_resized, mask=mask)

# --- Add green puzzle lines on top ---
final = cv2.addWeighted(puzzle_filled, 1, edges_bgr, 1, 0)

# --- Save & show result ---
cv2.imwrite("puzzle_with_image.png", final)
cv2.imshow("Puzzle with Image", final)
cv2.waitKey(30000) # wait for 30 seconds
cv2.destroyAllWindows()