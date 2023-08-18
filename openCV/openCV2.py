import cv2, time
video = cv2.VideoCapture(0)
video.release()
cv2.destroyAllWindows()

check,frame = video.read()

check
frame

print(frame)

video = cv2.VideoCapture(0)
a = 1
while True:
    a = a+1
    check,frame = video.read()
    print(frame)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow("mnp", gray_img)
    
    key = cv2.waitKey(1)
    
    if key == ord('q'):
        break
print(a)
video.release()
cv2.destroyAllWindows()

