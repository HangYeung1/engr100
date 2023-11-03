import cv2
import numpy as np

########## INITAL SETUP ##########

# Load names of classes and assign random colors
classes = open('coco.names').read().strip().split('\n')
np.random.seed(42)
colors = np.random.randint(0, 255, size=(len(classes), 3), dtype='uint8')

# Load network and model using yolo files
net = cv2.dnn.readNetFromDarknet('yolov3.cfg', 'yolov3.weights')
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

# Get output layers
net.getUnconnectedOutLayers()

# Get layer names
ln = net.getLayerNames()
try:
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]
except IndexError:
    ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]

# Create video capture object
vid = cv2.VideoCapture(0)


########## CV FUNCTIONS ##########

def detect_people(img):
	# Construct a blob from the image
	blob = cv2.dnn.blobFromImage(img, 1/255.0, (416, 416), swapRB=True, crop=False)
	r = blob[0, 0, :, :]
	net.setInput(blob)

	# Forward pass
	outputs = net.forward(ln)
	img_copy = img.copy()

	boxes = []
	confidences = []
	classIDs = []
	h, w = img_copy.shape[:2]

	# List of found people
	# x, y, w, h
	peopleFound = []

	# Loop over the outputs
	confidence_level = 0.2

	for output in outputs:
		for detection in output:
			scores = detection[5:]
			classID = np.argmax(scores)
			confidence = scores[classID]
			if confidence > confidence_level:
				box = detection[:4] * np.array([w, h, w, h])
				(centerX, centerY, width, height) = box.astype("int")
				x = int(centerX - (width / 2))
				y = int(centerY - (height / 2))
				box = [x, y, int(width), int(height)]
				if classID == 0:
					boxes.append(box)
					confidences.append(float(confidence))
					classIDs.append(classID)

	indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
	if len(indices) > 0:
		for i in indices.flatten():
			(x, y) = (boxes[i][0], boxes[i][1])
			(w, h) = (boxes[i][2], boxes[i][3])
			color = [int(c) for c in colors[classIDs[i]]]

			#  -- Arguments for CV2 rectangle:
			cv2.rectangle(img_copy, (x, y), (x + w, y + h), color, 4)

			# Labels and confidences for the image
			text = "{}: {:.4f}".format(classes[classIDs[i]], confidences[i])
			cv2.putText(img_copy, text, (x,y -5), cv2.FONT_HERSHEY_SIMPLEX,
					.7, color, 2, cv2.LINE_AA)
			
			# Add to list of people found
			peopleFound.append((x,y, width, height))
	
	cv2.imshow('camera', img_copy)
	return peopleFound

def find_biggest(peopleFound):
	biggest = 0
	current = 0
	for person in peopleFound:
		if person[2] * person[3] > biggest:
			biggest = current
			current += 1
	if len(peopleFound) > 0:
		biggestPerson = peopleFound[biggest]
		return (biggestPerson[0] + biggestPerson[2]/2, biggestPerson[1] + biggestPerson[3]/2)
	return None

########## MAIN LOOP ##########
while(True):
	# Grab latest frame
	ret, img = vid.read()
	img = cv2.resize(img, (0,0), fx = 0.5, fy = 0.5)
	imgX = img.shape[1]
	imgY = img.shape[0]

	# Detect people in the frame
	peopleFound = detect_people(img)
	target = find_biggest(peopleFound)
	if target is not None:
		print(target[0] / imgX, target[1] / imgY)
	else:
		print("No target found")

	# Quit if 'q' is pressed
	if cv2.waitKey(1) & 0xFF == ord('q'): 
		print("Quitting...")
		break

########## CLEANUP ##########

# Relase the VideoCapture object
vid.release() 

# Destroy all the windows
cv2.destroyAllWindows() 