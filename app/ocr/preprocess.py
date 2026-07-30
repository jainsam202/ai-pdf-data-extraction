import cv2
import numpy as np


class ImagePreprocessor:

    @staticmethod
    def preprocess(image):

        image = np.array(image)

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_RGB2GRAY,
        )

        _, threshold = cv2.threshold(
            gray,
            150,
            255,
            cv2.THRESH_BINARY,
        )

        return threshold