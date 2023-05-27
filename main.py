import pandas as pd
from ultralytics import YOLO
from yolo_pretrain.tracker import*
from imgToText import*
from dbOperations import*
import datetime

"""My Notes
#CCTV Camera Resolution has to be reduced to desired frame size i.e 1280*720
"""

#Assign pre-trained weights
model=YOLO('support/yolov8n_best.pt')

def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE :
        colorsBGR = [x, y]
        print(colorsBGR)


#cv2.namedWindow('BR Vehicle Tracking')
#cv2.setMouseCallback('BR Vehicle Tracking', RGB)

cap=cv2.VideoCapture('images/Myveh.mp4')
#cap=cv2.VideoCapture(0)

my_file = open("support/object_classes.txt", "r")
data = my_file.read()
class_list = data.split("\n")

# Tracker Class & Image Reading Class initialization.
tracker=Tracker()
readImage=imgToText()
vehLogEntry=vehManagement()

count=0
car_count=1
vh_detected={}
detected_cars={}

video_res_width=1020
video_res_height=600
offset=6
offset2=video_res_height//2    #eg 200


#To draw Lines Eg: Spot1,Spot2
cy1=video_res_height-offset2  #eg 400
cx1=offset*8  #eg 100
cx2=video_res_width-cx1 #920
cy2=cy1+100
numberPlates={}


while True:
    ret,frame = cap.read()
    if not ret:
        break
    count += 1
    if count % 3 != 0:
        continue
    frame=cv2.resize(frame,(video_res_width,video_res_height))
    results=model.predict(frame, False,verbose=False)
    a=results[0].boxes.data
    px=pd.DataFrame(a).astype("float")

    list=[]
    for index,row in px.iterrows():
        x1=int(row[0])
        y1=int(row[1])
        x2=int(row[2])
        y2=int(row[3])
        d=int(row[5])
        c=class_list[d]
        if 'car' in c:
            list.append([x1,y1,x2,y2])

    bbox_id=tracker.update(list)

    for bbox in bbox_id:
        x3,y3,x4,y4,id=bbox
        cx=int(x3+x4)//2
        cy=int(y3+y4)//2

        if cy1 < (cy+offset) and cy1 > (cy-offset) and id not in vh_detected:
               vh_detected[id]=cy
               cv2.circle(frame, (cx, cy), 4, (255, 0, 0), -1)
               cv2.putText(frame, str(car_count), (cx, cy), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)
               #saving image
               image_name='images/detected_car'+str(car_count)+'.jpg'
               if not cv2.imwrite(image_name,frame):
                      raise Exception("Could not write image")
               else:
                      print(image_name)
                      #Converting cropped numberplate image to text
                      Num_plate_text=readImage.cropImage(image_name)
                      print(Num_plate_text)
                      veh_entrytime=datetime.datetime.now()
                      print(veh_entrytime)
                      #Storing to the database table.
                      vehLogEntry.addEntry(Num_plate_text,str(veh_entrytime),'1')
                      vehLogEntry.select_all_tasks('vehicle_logging')
               car_count += 1

    cv2.line(frame, (cx1, cy1), (cx2, cy1), (255, 255, 255), 1)
    cv2.putText(frame, "Detecting Point", (cx1-offset, cy1), cv2.FONT_HERSHEY_COMPLEX, 0.8, (243, 250, 18), 1)

    cv2.imshow("BR Vehicle Tracking", frame)
    if cv2.waitKey(0)&0xFF==26:
        break

cap.release()
cv2.destroyAllWindows()
