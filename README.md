# Home Surveillance Using OpenCV, Deep Learning, Twilio and Dropbox

In this tutorial, we will build the home surveillance with OpenCV, Twilio anc Dropbox. 

## 1. Feature of Our Home Surveillance

The feature of our home surveillance are :
- Ability to detect and capture face of a person then send the detection result to certain user using Twilio. This can be considered as __Notification__. Most of the home surveillance camera doesn't have ability to recognize the face of intruder.
- Detection result image can be kept for long time in __free cloud storage__. In this tutorial, we use __Dropbox__. The other cloud storage are : Google Drive, AWS S3, etc.
- Ability to real time streaming over different network using VNC. With this feature from our home surveillance system, we can see the real time condition of our home although we are far away from our home. 

## 2. Scheme

##3. Prerequisite
To begin building our home surveillnace system, we need :

- Twilio API (install using `pip install twilio`)
- Dropbox API (install using `pip install dropbox`)
- OpenCV
- Numpy
