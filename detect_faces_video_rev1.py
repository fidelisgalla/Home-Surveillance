#modified by Fidelis

from pyimagesearch.tempimage import TempImage
from imutils.video import VideoStream
from pyimagesearch.notifications import TwillioDropbox
import numpy as np
import argparse
import warnings
import datetime
import imutils
import json
import time
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", required=True,
	help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True,
	help="path to Caffe pre-trained model")
ap.add_argument("-co", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections")
ap.add_argument("-c", "--conf", required=True,
	help="path to the JSON configuration file")
args = vars(ap.parse_args())

# filter warnings, load the configuration and initialize the Dropbox
# client
warnings.filterwarnings("ignore")
conf = json.load(open(args["conf"]))


# load our serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

# initialize the camera and grab a reference to the raw camera capture
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)

# allow the camera to warmup, then initialize the average frame, last
# uploaded timestamp, and frame motion counter
print("[INFO] warming up...")
time.sleep(conf["camera_warmup_time"])
lastUploaded = datetime.datetime.now()
motionCounter = 0

# capture frames from the camera
while True:
	# grab the raw NumPy array representing the image and initialize
	# the timestamp and occupied/unoccupied text
    frame = vs.read()
    frame = imutils.resize(frame,width=400)
    (h,w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,(300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()
    
    timestamp = datetime.datetime.now()
    text = "Tidak Ada Orang"
    notifSent = False

    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        
        
        if confidence < args["confidence"]:
            continue

		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        (startX, startY, endX, endY) = box.astype("int")
 
		# draw the bounding box of the face along with the associated
		# probability
        
        y = startY - 10 if startY - 10 > 10 else startY + 10
        cv2.rectangle(frame, (startX, startY), (endX, endY),
			(0, 0, 255), 2)
        text = "Ada Orang"
    
    #text = "{:.2f}%".format(confidence * 100)
    
    ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
    # draw the text and timestamp on the frame
    cv2.putText(frame, "Status: {}".format(text), (10, 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
		0.35, (0, 0, 255), 1)

	
	# check to see if the room is occupied
    if text == "Ada Orang":
		# check to see if enough time has passed between uploads
        if (timestamp - lastUploaded).seconds >= conf["min_upload_seconds"]:
			# increment the motion counter
            motionCounter += 1

			# check to see if the number of frames with consistent motion is
			# high enough
            if motionCounter >= conf["min_motion_frames"]:
				# check to see if dropbox sohuld be used
                if conf["use_dropbox"]:
					# write the image to temporary file
                    t = TempImage()
                    cv2.imwrite(t.path, frame)
                    
				# upload the image to Dropbox and cleanup the tempory image
                    tn = TwillioDropbox.TwilioNotifier(conf)
                    
                    #print("[UPLOAD] file {}.jpg".format(ts))
                    #path = "/{base_path}/{timestamp}.jpg".format(
					  # base_path=conf["dropbox_base_path"], timestamp=ts)
                    
                    #client.files_upload(open(t.path, "rb").read(), path)
                    #url = client.files_get_temporary_link(path)
                    if not notifSent:    
                        msg = "Ada Orang Di Luar Rumah"
                        tn.send(t,msg,ts)
                        #time.sleep(3.0)
                        #remove the file after some delays or looking for 
                        t.cleanup()
                        notifSent = True
                        
                    else :
                        notiSent = False
                        
                    #remove the file
                    
                    #t.cleanup()
                 
                    #msg= "Ada Orang Di Luar Rumah"
                
                #send the image
                      
                    #tn.send_message(msg,url.link)
                    #print("[SEND] file {}.jpg".format(ts))
                    #client.files_delete(path)
                    #print("[DELETE] file {}.jpg".format(ts))

				# update the last uploaded timestamp and reset the motion
				# counter
                lastUploaded = timestamp
                motionCounter = 0

	# otherwise, the room is not occupied
    else:
        motionCounter = 0

	# check to see if the frames should be displayed to screen
    if conf["show_video"]:
		# display the security feed
        cv2.imshow("Security Feed", frame)
        key = cv2.waitKey(1) & 0xFF

		# if the `q` key is pressed, break from the lop
        if key == ord("q"):
            break

	# clear the stream in preparation for the next frame
cv2.destroyAllWindows()
vs.stop()