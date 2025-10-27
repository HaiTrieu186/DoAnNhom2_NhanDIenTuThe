import cv2
import matplotlib.pyplot as plt
net = cv2.dnn.readNetFromTensorflow("graph_opt.pb")
inWidth = 368
inHeight = 368
thr=0.2
BODY_PARTS={"Nose":0,"Neck":1,
            "RShoulder":2,
            "RElbow":3,
            "RWrist":4,
            "LShoulder":5,
            "LElbow":6,
            "LWrist":7,
            "RHip":8,
            "RKnee":9,
            "RAnkle":10,
            "LHip":11,
            "LKnee":12,
            "LAnkle":13,
            "REye":14,
            "LEye":15,
            "REar":16,
            "LEar":17,
            "Background":18
            }
POSE_PAIRS = [ ["Neck","RShoulder"],
               ["Neck","LShoulder"],
               ["RShoulder","RElbow"],
               ["RElbow","RWrist"],
               ["LShoulder","LElbow"],
               ["LElbow","LWrist"],
               ["Neck","RHip"],
               ["RHip","RKnee"],
               ["RKnee","RAnkle"],
               ["Neck","LHip"],
               ["LHip","LKnee"],
               ["LKnee","LAnkle"],
               ["Neck","Nose"],
               ["Nose","REye"],
               ["REye","REar"],
               ["Nose","LEye"],
               ["LEye","LEar"]
               ]

img=cv2.imread("testPose.jpg")
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

def pose_detect(frame):
    frameWidth, frameHeight = frame.shape[:2]
    net.setInput(cv2.dnn.blobFromImage(frame,1.0,(inWidth,inHeight), (127.5,127.5,127.5), True,False))
    out = net.forward()
    out = out[:,:19,:,:]

    assert (len(BODY_PARTS)==out.shape[1])
    points = []
    for i in range(len(BODY_PARTS)):
        heatMap = out[0,i,:,:]

        _,conf, _, point = cv2.minMaxLoc(heatMap)
        x = (frameWidth*point[0])/out.shape[3]
        y = (frameHeight*point[1])/out.shape[2]

        points.append((int(x),int(y)) if conf > thr else None)

    for pair in POSE_PAIRS:
        partFrom = pair[0]
        partTo = pair[1]
        assert(partFrom in BODY_PARTS)
        assert(partTo in BODY_PARTS)

        idFrom = BODY_PARTS[partFrom]
        idTo = BODY_PARTS[partTo]

        if points[idFrom] and points[idTo]:
            cv2.line(frame, points[idFrom], points[idTo], (0,255,255), 3)
            cv2.ellipse(frame, points[idFrom], (3,3),0,0,360, (255,255,0), cv2.FILLED)
            cv2.ellipse(frame, points[idTo], (3,3),0,0,360, (255,0,0), cv2.FILLED)
    t, _ = net.getPerfProfile()
    freq = cv2.getTickFrequency()/1000
    cv2.putText(frame, '%2fms'%(t/freq),(10,20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0))
    return frame
estimated_img = pose_detect(img)
plt.imshow(img)
#plt.imshow(estimated_img)

plt.show()