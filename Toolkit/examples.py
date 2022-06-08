import cv2,keyboard,time
from .tracking import Segmentation,FaceDetection,Hand,Gestures,HandDetector,Utils

class Exmp_Tracking:
    """
    Use 1 for an external camera and 0 for an internal one.
    """
    @staticmethod
    def bg_removal(rep_img:str,rep_perc:float,input=1,quit_key='esc'):
        cap = cv2.VideoCapture(input)
        rep_img_ = cv2.imread(rep_img)
        seg = Segmentation(rep_img_,rep_perc)
        while True:
            _, img = cap.read()
            ref_img = seg.segment(img)
            cv2.imshow("Image", ref_img)
            if keyboard.is_pressed(quit_key):
                return
            cv2.waitKey(1)

    @staticmethod
    def face_detection(input=1, quit_key='esc'):
        cap = cv2.VideoCapture(input)
        pTime = time.time()
        detector = FaceDetection()
        while True:
            _, img = cap.read()
            faces = detector.get_faces(img)
            for face in faces:
                for lm in face.lms:
                    cv2.putText(img, f'{str(face.ext_lms[1][1])}', lm, cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
                detector.draw_face(img, face)
            cTime = time.time()
            fps = 1 / (cTime - pTime)
            cv2.putText(img, f'FPS : {str(int(fps))}', (10, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            pTime = cTime
            cv2.imshow("Image", img)
            if keyboard.is_pressed(quit_key):
                return
            cv2.waitKey(1)

    @staticmethod
    def SPS(input=1, quit_key='esc'):
        """
        Simple scissor paper rock game. Input is for 'cv2.VideoCapture(input)'
        """
        global a_time, erg
        erg = 0
        class hand_init:
            @staticmethod
            def zei(hand: Hand):
                g1, g2, g3 = Gestures.paper(hand), Gestures.rock(hand), Gestures.scissor(hand)
                if g1:
                    cv2.putText(img, f'PAPER', (10, 50), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)
                    return 1
                elif g2:
                    cv2.putText(img, f'ROCK', (10, 50), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)
                    return 2
                elif g3:
                    cv2.putText(img, f'SCISSOR', (10, 50), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)
                    return 3
                else:
                    return 4

            @staticmethod
            def pst(a1: int, a2: int):
                global erg
                if a1 == 4 or a2 == 4:
                    erg = 3
                    return
                if a1 == 1:
                    if a2 == 1:
                        erg = 4
                        return
                    elif a2 == 2:
                        erg = 1
                        return
                    elif a2 == 3:
                        erg = 2
                        return
                elif a1 == 2:
                    if a2 == 2:
                        erg = 4
                        return
                    elif a2 == 3:
                        erg = 1
                        return
                    elif a2 == 1:
                        erg = 2
                        return
                elif a1 == 3:
                    if a2 == 1:
                        erg = 1
                        return
                    elif a2 == 2:
                        erg = 2
                        return
                    elif a2 == 3:
                        erg = 4
                        return

        vid = cv2.VideoCapture(input)
        detector = HandDetector(detectionConfidence=0.75, trackConfidence=0.75)
        a_time = time.time() + 5
        while True:
            _, img = vid.read()
            hands = detector.get_Hands(img)
            c_time = time.time()
            for hand in hands:
                if not erg == 0:
                    if erg == 1:
                        cv2.putText(img, 'PLAYER1 WON SHOW ONLY INDEX FINGER TO RESTART', (20, 50),
                                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
                    elif erg == 2:
                        cv2.putText(img, 'PLAYER2 WON SHOW ONLY INDEX FINGER TO RESTART', (20, 50),
                                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
                    elif erg == 3:
                        cv2.putText(img, 'WRONG GESTURE SHOW ONLY INDEX FINGER TO RESTART', (20, 50),
                                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
                    elif erg == 4:
                        cv2.putText(img, 'NOT SURE SHOW ONLY INDEX FINGER TO RESTART', (20, 50), cv2.FONT_HERSHEY_PLAIN,
                                    2, (255, 255, 255), 2)
                    if Gestures.INDEX_finger_up(hand) and not Gestures.RING_finger_up(
                            hand) and not Gestures.PINKY_finger_up(hand) and not Gestures.MIDDLE_finger_up(
                            hand) and not Gestures.THUMB_finger_up(hand):
                        cv2.putText(img, 'RESTARTING', (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
                        a_time = time.time() + 5
                        erg = 0
                        continue
                elif Utils.absa((0, c_time), (0, a_time), 0.1):
                    if hand.hand_n == 1:
                        global a1
                        a1 = hand_init.zei(hand)
                    elif hand.hand_n == 2:
                        a2 = hand_init.zei(hand)
                elif erg == 0:
                    cv2.putText(img, f'STARTING IN : {str(a_time - c_time)}', (20, 50), cv2.FONT_HERSHEY_PLAIN, 2,
                                (255, 255, 255), 2)
                cv2.putText(img, str(hand.hand_n), hand.WRIST, cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 2)
            hand_init = hand_init()
            if Utils.absa((0, c_time), (0, a_time), 0.1):
                try:
                    hand_init.pst(a1, a2)
                except NameError:
                    erg = 0
            cv2.imshow("Image", img)
            if keyboard.is_pressed(quit_key): return
            cv2.waitKey(1)