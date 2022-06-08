import termcolor
import cv2, mediapipe, numpy
import pytesseract.pytesseract
from pyzbar.pyzbar import decode as qr_decode_dat
from .parse import Hand, Pose, Face, FaceMesh, ScannedText, qr, Objectron, BoundingBox
from .errors import *
import numpy as np, imutils


# Some Detectors could be broken

class Utils:
    def absa(c1: tuple, c2: tuple, t: int):
        """
        Gets two tuples and looks if the (1) values are
        about the same, by subtracting the smaller one from
        the bigger one and looking if the bigger one is bigger
        than t.
        """
        thresh = t
        C1, C2 = c1[1], c2[1]
        if C1 > C2:
            F1 = C1 - C2
            if F1 < thresh:
                return True
            else:
                return False
        else:
            F1 = C2 - C1
            if F1 < thresh:
                return True
            else:
                return False


class HandDetector:
    def __init__(self, mode=False, maxHands=2, detectionConfidence=0.5, trackConfidence=0.5):
        """
        Sets all the values for mediapipe and the other HandDetector functions.
        """
        self.mode = mode
        self.maxHands = maxHands
        self.detectConf = detectionConfidence
        self.trackConf = trackConfidence
        self.sol = mediapipe.solutions
        self.mpHands = self.sol.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectConf, self.trackConf)
        self.mpDraw = self.sol.drawing_utils
        self.nt_list = [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0),
                        (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]

    def get_Hands(self, img):
        """
        Finds the hands img the given img, needs RGB img
        to find the hands, so it first converts them.
        Returns the Hand object with all the landmarks for each hand.
        """
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        res = self.hands.process(imgRGB)
        HAND = 0
        if res.multi_hand_landmarks:
            for handLms in res.multi_hand_landmarks:
                HAND = HAND + 1
                List = []
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = img.shape
                    global _COMP_y_cord
                    _COMP_y_cord = lm.z
                    print(_COMP_y_cord)
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    List.append((cx, cy))
                yield Hand(HAND, List, handLms)
        else:
            return Hand(1, self.nt_list, [])

    def draw_hand(self, img, hand: Hand):
        """
        Draws the Landmarks and connections on the image.
        """
        self.mpDraw.draw_landmarks(img, hand.hand_lms, self.mpHands.HAND_CONNECTIONS)
        return True


class PoseDetector:
    def __init__(self, static_image_mode=False, model_complexity=1, smooth_landmarks=True, min_detection_confidence=0.5,
                 min_tracking_confidence=0.5):
        """
        Sets all the values for mediapipe and the other PoseDetector functions.
        !!! ONLY INITIALIZE THIS ONCE!!!
        """
        self.static_image_mode = static_image_mode
        self.model_complexity = model_complexity
        self.smooth_landmarks = smooth_landmarks
        self.min_detection_conf = min_detection_confidence
        self.min_tracking_conf = min_tracking_confidence
        self.sol = mediapipe.solutions
        self.mpPose = self.sol.pose
        self.pose = self.mpPose.Pose(self.static_image_mode, model_complexity, smooth_landmarks,
                                     min_detection_confidence, min_tracking_confidence)
        self.nt_list = [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0),
                        (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0),
                        (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), ]
        self.mpDraw = self.sol.drawing_utils

    def get_Pose(self, img, wd=True):
        """
        Transforms the img to RGB and then builds the Pose object
        based off all the landmarks on the frame.
        Returns the Pose object with the complete list of landmarks.
        """
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        res = self.pose.process(imgRGB).pose_landmarks
        if res:
            List = []
            if wd:
                for id, lm in enumerate(res.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    List.append((cx, cy))
                try:
                    yield Pose(List, res)
                except IndexError:
                    return Pose(self.nt_list, [])
            else:
                yield Pose(self.nt_list, res)
        else:
            return Pose(self.nt_list, [])

    def draw_pose(self, img, pose: Pose):
        """
        Draws the Landmarks and connections on the image.
        """
        self.mpDraw.draw_landmarks(img, pose.results, self.mpPose.POSE_CONNECTIONS)
        return True


class FaceMeshDetector:
    def __init__(self, static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5,
                 min_tracking_confidence=0.5):
        """
        Sets all the values for mediapipe and the other PoseDetector functions.
        !!! ONLY INITIALIZE THIS ONCE!!!
        """
        self._static_image_mode = static_image_mode
        self._max_num_faces = max_num_faces
        self._min_detection_conf = min_detection_confidence
        self._min_tracking_conf = min_tracking_confidence
        self._sol = mediapipe.solutions
        self._mpDraw = self._sol.drawing_utils
        self._mpFaceMesh = self._sol.face_mesh
        self._face_mesh = self._mpFaceMesh.FaceMesh()
        self._drawSpec = self._mpDraw.DrawingSpec(thickness=1, circle_radius=2)

    def get_faces(self, img):
        """
        Transforms the img to RGB and then builds the FaceMesh object
        based off all the landmarks on the frame.
        Returns the FaceMesh object with the complete list of landmarks.
        """
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        res = self._face_mesh.process(imgRGB)
        if res.multi_face_landmarks:
            for faceLms in res.multi_face_landmarks:
                List = []
                c = -1
                for lm in faceLms.landmark:
                    c = c + 1
                    ih, iw, ic = img.shape
                    cx, cy = int(lm.x * iw), int(lm.y * ih)
                    List.append(((cx, cy), c))
                yield FaceMesh(List, faceLms)

    def draw_mesh(self, img, face_mesh: FaceMesh):
        """
        Draws the Landmarks and connections on the image.
        """
        self._mpDraw.draw_landmarks(img, face_mesh.fLms, self._mpFaceMesh.FACE_CONNECTIONS, self._drawSpec,
                                    self._drawSpec)
        return True


class FaceDetection:
    def __init__(self, min_detection_confidence=0.5, model_selection=1):
        self.sol = mediapipe.solutions
        self.mpFaceDetection = self.sol.face_detection
        self.mpDraw = self.sol.drawing_utils
        self.min_detection_conf = min_detection_confidence
        self.model_selection = model_selection
        self.FaceDetection = self.mpFaceDetection.FaceDetection(self.min_detection_conf, self.model_selection)

    def get_faces(self, img):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        res = self.FaceDetection.process(imgRGB)
        if res.detections:
            for id, detections in enumerate(res.detections):
                iw, ih, ic = img.shape
                score = int(float(detections.score[0]) * 100)
                ld = detections.location_data
                rbb = ld.relative_bounding_box
                bbox = int(rbb.xmin * iw) + 55, int(rbb.ymin * ih) - 70, int(rbb.width * iw) + 50, int(
                    rbb.height * ih) - 20
                List = []
                c = 0
                for kp in ld.relative_keypoints:
                    c = c + 1
                    cx, cy = int(kp.x * iw) + 85, int(kp.y * ih) - 50
                    cent = (cx, cy)
                    List.append((cent, c))
                yield Face(List, res, score, bbox)

    def draw_face(self, img, face: Face):
        cv2.rectangle(img, face.bbox, color=(0, 0, 255), thickness=3)
        for lm in face.lms:
            cv2.circle(img, (lm[0], lm[1]), 1, (0, 0, 255), 1)
        cv2.putText(img, f'{face.conf_score}%', (face.bbox[0], face.bbox[1]), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)


class Gestures:
    """
    Looks at the bottom of the finger and on the tip, if
    the tip is higher, it returns true. On the thumb it looks
    at the bottom and the point above, if both are about the same
    (22px margin) it returns true.

    The locked gestures (ROCK,SCISSOR,PAPER) look at the fingers up and
    returns true if the right fingers are up/down.
    """

    def __init__(self, hand: Hand):
        self.hand = hand

    def INDEX_finger_up(self):
        L1 = self.hand.INDEX
        if L1[0][1] > L1[3][1]:
            return True
        else:
            return False

    def THUMB_finger_up(self):
        L1 = self.hand.THUMB
        if L1[0][1] > L1[3][1] and not Utils.absa(L1[0], L1[1], 22):
            return True
        else:
            return False

    def PINKY_finger_up(self):
        L1 = self.hand.PINKY
        if L1[0][1] > L1[3][1]:
            return True
        else:
            return False

    def RING_finger_up(self):
        L1 = self.hand.RING
        if L1[0][1] > L1[3][1]:
            return True
        else:
            return False

    def MIDDLE_finger_up(self):
        L1 = self.hand.MIDDLE
        if L1[0][1] > L1[3][1]:
            return True
        else:
            return False

    def paper(self):
        if self.INDEX_finger_up() and self.RING_finger_up() and self.PINKY_finger_up() and self.MIDDLE_finger_up():
            return True
        else:
            return False

    def rock(self):
        if self.INDEX_finger_up() or self.RING_finger_up() or self.PINKY_finger_up() or self.MIDDLE_finger_up():
            return False
        else:
            return True

    def scissor(self):
        if self.INDEX_finger_up() and self.MIDDLE_finger_up() and not self.RING_finger_up() and not self.PINKY_finger_up():
            return True
        else:
            return False


class MixDetection:
    def __init__(self, img):
        self.img = img

    def detect_License_Placte(self):
        img = cv2.resize(self.img, (600, 400))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.bilateralFilter(gray, 13, 15, 15)
        edged = cv2.Canny(gray, 30, 200)
        contours = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
        screenCnt = None
        for c in contours:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.018 * peri, True)
            if len(approx) == 4:
                screenCnt = approx
                break
        if screenCnt is None:
            return [None, None]
        else:
            detected = 1
        if detected == 1:
            cv2.drawContours(img, [screenCnt], -1, (0, 0, 255), 3)
        try:
            mask = np.zeros(gray.shape, np.uint8)
            self.new_image = cv2.bitwise_and(img, img, mask=mask)
            (x, y) = np.where(mask == 255)
            (topx, topy) = (np.min(x), np.min(y))
            (bottomx, bottomy) = (np.max(x), np.max(y))
            Cropped = gray[topx:bottomx + 1, topy:bottomy + 1]
            self.Cropped = cv2.resize(Cropped, (400, 200))
        except:
            return [None, None]
        return [self.Cropped, self.new_image]


class Segmentation:
    def __init__(self, rep_img, rem_perc: float, model_sel=0, body=False):
        """
        rep_img is the replacement for the background.
        rem_perc is the percentage of the background that gets deleted (0.85 is good)
        bod is if the foreground or the background should be replaced
        :param rep_img:
        The replacement for the background.
        :param rem_perc:
        The percentage of the background that gets deleted (0.85 is good)
        :param model_sel:
        :param body:
        The foreground or the background should be replaced
        """
        self.rem = rem_perc
        self.replace_img = rep_img
        self.mode_sel = model_sel
        self.bod = body
        self.model = mediapipe.solutions.selfie_segmentation.SelfieSegmentation(self.mode_sel)

    def segment(self, img):
        """
        The given background Image must be the same size as the normal Image
        :param img:
        Input Image to cut
        :return:
        Segmented Image
        """
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.model.process(imgRGB)  # Create a black-white image
        if self.bod:
            condition = numpy.stack((results.segmentation_mask,) * 3, axis=-1) < self.rem
        else:  # Apply rem_perc
            condition = numpy.stack((results.segmentation_mask,) * 3, axis=-1) > self.rem
        if isinstance(self.replace_img, tuple):
            _imgBg = numpy.zeros(img.shape, dtype=numpy.uint8)
            _imgBg[:] = self.replace_img  # Make the background
            imgOut = numpy.where(condition, img, _imgBg)
        else:
            imgOut = numpy.where(condition, img, self.replace_img)  # Combine both
        return imgOut


class TextRecognition:
    def __init__(self, img, tesseract_dir: str = None):
        """
        :param img:
        :param tesseract_dir:
        """
        if not tesseract_dir:
            try:
                import tesseract_pack
                self.dat_here = tesseract_pack.data_here
            except ModuleNotFoundError:
                print(termcolor.colored(
                    'tesseract-ocr is needed for TextRecognition, install "tesseract-ocr-data" or specify "tesseract_dir"'))
                return
        else:
            self.dat_here = tesseract_dir
        self.def_img = img
        self.IMG = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.shape = self.IMG.shape
        tmp_hIMG, tmp_wImg, ust = self.shape
        self.hIMG = tmp_hIMG
        self.wIMG = tmp_wImg
        tox = '\\'
        self.install = (f'{self.dat_here.replace(tox, "/")}\\tesseract.exe')

    def get_data(self):
        pytesseract.pytesseract.tesseract_cmd = self.install
        result1 = pytesseract.pytesseract.image_to_boxes(self.IMG)
        result2 = pytesseract.pytesseract.image_to_string(self.IMG)
        obj = ScannedText(result1, result2, self.hIMG, self.wIMG)
        return obj

    def draw_all(self, obj: ScannedText):
        img = self.def_img
        for b in obj.boxes:
            cv2.rectangle(img, (b[0], obj.height - b[1]), (b[2], obj.height - b[3]), (0, 0, 255), 3)
        return img


class qrbar_code:
    def __init__(self, img):
        self.raw_ = qr_decode_dat(img)
        if not self.raw_ == []:
            self.object = qr(img, self.raw_)
        else:
            self.object = None

    def qr_shown(self):
        if self.object == None:
            return False
        else:
            return True

    def get_text(self):
        if self.object == None: return
        obj: qr = self.object
        return obj.decoded_txt

    def get_all_data(self):
        if self.object == None: return
        obj: qr = self.object
        return obj


class ObjectTracking:
    def __init__(self, img, bbox: tuple, tracker: int = 0):
        """
        Tracks an object (the bounding box) on an image,
        initialize after the camera, and then use track()
        in a loop. We recommend using the default KCF tracker
        because it is general purpose and very accurate and fast.
        MIL is also a valid option but it does not report failure.
        :param img:
        The image including the object
        :param bbox:
        The box that the object is in
        :param tracker:
        The tracker:
        0 = KCF
        1 = CSRT
        2 = MIL
        :return
        Returns [Objectron] object, which includes
        the bounding box, and the center.
        """
        if tracker < 0 or tracker > 2:
            raise InvalidArgument("Argument 'tracker' has to be within 0-2")
        self._tracker_type = tracker
        self._img = img
        self._bbox = bbox
        self._create_tracker()
        self.LOST = False

    def _create_tracker(self):
        if self._tracker_type == 0:
            self._tracker = cv2.TrackerKCF_create()
        elif self._tracker_type == 1:
            self._tracker = cv2.TrackerCSRT_create()
        else:
            self._tracker = cv2.TrackerMIL_create()
        self._tracker.init(self._img, self._bbox)

    def track(self, img):
        self._img = img
        suc, bbox = self._tracker.update(self._img)
        if suc:
            self.LOST = False
            return Objectron(bbox)
        else:
            self.LOST = True
            return Objectron(None)


class Coco:
    def __init__(self, image, configPath='ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt',
                 weightsPath="frozen_inference_graph.pb"):
        """
        The files (configPath and weightsPath) are required. (I got them from here : https://usercontent.one/wp/www.computervision.zone/wp-content/uploads/2021/07/Drone-Object-Detection.zip?media=1632743877)
        :param image:
        :param configPath:
        :param weightsPath:
        """
        self.img = image
        self.thres = 0.55
        self.nmsThres = 0.2
        self.classNames = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat',
                           'traffic light', 'fire hydrant', 'street sign', 'stop sign', 'parking meter', 'bench',
                           'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'hat',
                           'backpack', 'umbrella', 'shoe', 'eye glasses', 'handbag', 'tie', 'suitcase', 'frisbee',
                           'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard',
                           'surfboard', 'tennis racket', 'bottle', 'plate', 'wine glass', 'cup', 'fork', 'knife',
                           'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog',
                           'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'mirror', 'dining table',
                           'window', 'desk', 'toilet', 'door', 'tv', 'laptop', 'mouse', 'remote', 'keyboard',
                           'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'blender', 'book',
                           'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush', 'hair brush']
        self.configPath = configPath
        self.weightsPath = weightsPath
        self.net = cv2.dnn_DetectionModel(weightsPath, configPath)
        self.net.setInputSize(320, 320)
        self.net.setInputScale(1.0 / 127.5)
        self.net.setInputMean((127.5, 127.5, 127.5))
        self.net.setInputSwapRB(True)

    def look(self):
        classIds, confs, bbox = self.net.detect(self.img, confThreshold=self.thres, nmsThreshold=self.nmsThres);
        ret = []
        try:
            for classId, conf, box in zip(classIds.flatten(), confs.flatten(), bbox): ret += [
                {self.classNames[classId - 1].upper()}, {round(conf * 100, 2)}, classId, conf, box]
        except:
            return [None, None, None, None, None]
        return ret
