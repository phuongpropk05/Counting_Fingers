import cv2
import time
import os
import hand as htm

cap = cv2.VideoCapture(0)
pTime = 0

FolderPath = "Fingers"
lst = os.listdir(FolderPath)
lst_2 = []

for i in lst:
    image = cv2.imread(f"{FolderPath}/{i}")
    lst_2.append(image)

detector = htm.handDetector(detectionCon=1)
fingerId = [4, 8, 12, 16, 20]

while True:
    ret, frame = cap.read()
    frame = detector.findHands(frame)
    lmList = detector.findPosition(frame, draw=False)
    print(lmList)

    if len(lmList) != 0:
        fingers = []
        # Viet cho ngon cai (Diem 4 nam ben trai hay ben phai diem 3)
        if lmList[fingerId[0]][1] < lmList[fingerId[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        #Viet cho ngon dai
        for id in range(1,5):
            if lmList[fingerId[id]][2] < lmList[fingerId[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        songontay = fingers.count(1)

        h, w, c = lst_2[songontay-1].shape
        frame[0:h, 0:w] = lst_2[songontay-1]

    
        cv2.rectangle(frame,(0,200),(150,400),(0,255,0), -1)
        cv2.putText(frame, str(songontay), (30,390), cv2.FONT_HERSHEY_TRIPLEX, 5, (255,255,255), 5)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    font = cv2.FONT_HERSHEY_SCRIPT_COMPLEX
    img = cv2.putText(frame, f"fps: {int(fps)}", (150,70), font, 3, (0,0,0), 7)



    cv2.imshow("Dem Ngon Tay", frame)
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()