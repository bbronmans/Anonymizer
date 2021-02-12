import math

import numpy as np
from PIL import Image, ImageFilter


class Obfuscator:
    """ This class is used to blur box regions within an image with gaussian blurring. """
    def __init__(self, kernel_size=21, debug=False):
        """
        :param kernel_size: Size of the blurring kernel.
        :param debug: Obfuscation done by red rectangles instead of default blurring when set to true.
        """
        # Kernel must be uneven because of a simplified padding scheme
        assert kernel_size % 2 == 1

        self.kernel_size = kernel_size
        self.debug = debug

    def obfuscate(self, image, boxes):
        """
        Anonymize all bounding boxes in a given image.
        :param image: The image as np.ndarray with shape==(height, width, channels).
        :param boxes: A list of boxes.
        :return: The anonymized image.
        """
        if len(boxes) == 0:
            return np.copy(image)

        anonymized_image = np.copy(image)

        for box in boxes:
            x_min = int(math.floor(box.x_min))
            y_min = int(math.floor(box.y_min))
            x_max = int(math.ceil(box.x_max))
            y_max = int(math.ceil(box.y_max))

            if self.debug:
                anonymized_image[y_min:y_max, x_min:x_max, :] = [255, 0, 0]
            else:
                crop = anonymized_image[y_min:y_max, x_min:x_max, :]
                crop = np.array(Image.fromarray(crop).filter(ImageFilter.GaussianBlur(radius=self.kernel_size)))
                anonymized_image[y_min:y_max, x_min:x_max, :] = crop

        return anonymized_image
