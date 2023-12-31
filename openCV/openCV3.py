import cv2, time
first_frame = None
video = cv2.VideoCapture(0)
while True:
    check,frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21,21), 0)
    if first_frame is None:
        first_frame = gray
        continue
        
    delta_frame = cv2.absdiff(first_frame,gray)
    thresh_delta = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_delta = cv2.dilate(thresh_delta, None, iterations = 0)
    (cnts,_) = cv2.findContours(thresh_delta, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for contour in cnts:
        if cv2.contourArea(contour)< 10000:
            (x,y,w,h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 4)
    
    cv2.imshow('Frame', frame)
    cv2.imshow('threshold', thresh_delta)
    cv2.imshow('CapturingGray', gray)
    cv2.imshow('DeltaFrame', delta_frame)
    
    
    key = cv2.waitKey(1)
    
    if key == ord('q'):
        break
        
video.release()
cv2.destroyAllWindows()
