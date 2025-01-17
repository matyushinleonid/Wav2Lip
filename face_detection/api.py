from __future__ import print_function

import os
from enum import Enum

import cv2
import numpy as np
import torch
from torch.utils.model_zoo import load_url

try:
    import urllib.request as request_file
except BaseException:
    import urllib as request_file

from .models import FAN, ResNetDepth
from .utils import *


class LandmarksType(Enum):
    """Enum class defining the type of landmarks to detect.

    ``_2D`` - the detected points ``(x,y)`` are detected in a 2D space and follow the visible contour of the face
    ``_2halfD`` - this points represent the projection of the 3D points into 3D
    ``_3D`` - detect the points ``(x,y,z)``` in a 3D space

    """

    _2D = 1
    _2halfD = 2
    _3D = 3


class NetworkSize(Enum):
    # TINY = 1
    # SMALL = 2
    # MEDIUM = 3
    LARGE = 4

    def __new__(cls, value):
        member = object.__new__(cls)
        member._value_ = value
        return member

    def __int__(self):
        return self.value


ROOT = os.path.dirname(os.path.abspath(__file__))


class FaceAlignment:
    def __init__(
        self,
        landmarks_type,
        network_size=NetworkSize.LARGE,
        device="cuda",
        flip_input=False,
        face_detector="sfd",
        verbose=False,
    ):
        self.device = device
        self.flip_input = flip_input
        self.landmarks_type = landmarks_type
        self.verbose = verbose

        network_size = int(network_size)

        if "cuda" in device:
            torch.backends.cudnn.benchmark = True

        # Get the face detector
        face_detector_module = __import__(
            "face_detection.detection." + face_detector,
            globals(),
            locals(),
            [face_detector],
            0,
        )
        self.face_detector = face_detector_module.FaceDetector(
            device=device, verbose=verbose
        )

    def get_detections_for_batch(self, images):
        images = images[..., ::-1]
        detected_faces = self.face_detector.detect_from_batch(images.copy())

        return detected_faces
