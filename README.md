# Drowsiness_Detection_Deployment

things to do:
- may need to add "runs" folder
- run "python app.py" to run the code

folder structure:  
runs  
static  
  &nbsp;&nbsp;&nbsp;&nbsp; - detect  
  &nbsp;&nbsp;&nbsp;&nbsp; - initial  
  &nbsp;&nbsp;&nbsp;&nbsp; - uploads  
  &nbsp;&nbsp;&nbsp;&nbsp; - style.css    
templates  
  &nbsp;&nbsp;&nbsp;&nbsp; - cam.html  
  &nbsp;&nbsp;&nbsp;&nbsp; - image.html  
  &nbsp;&nbsp;&nbsp;&nbsp; - index.html  
app.py  
best-yolo8.tiny.pt  
requirements.txt  

Command to run-

docker run -it -v $PWD:/app/ --device=/dev/video1:/dev/video0 -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY app-image