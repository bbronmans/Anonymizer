import math

import numpy as np
from PIL import Image, ImageFilter


class Obfuscator:
    """ This class is used to blur box regions within an image with gaussian blurring. """
    def __init__(self, kernel_size=21, debug=False, blur_scale=1):
        """
        :param kernel_size: Size of the blurring kernel.
        :param debug: Obfuscation done by red rectangles instead of default blurring when set to true.
        """
        # Kernel must be uneven because of a simplified padding scheme
        assert kernel_size % 2 == 1

        self.kernel_size = kernel_size
        self.debug = debug
        self.blur_scale = blur_scale

    def obfuscate(self, image, boxes):
        """
        Anonymize all bounding boxes in a given image.
        :param image: The image as np.ndarray with shape==(height, width, channels).
        :param boxes: A list of boxes.
        :param blur_scale: Scales the box size.
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

            if self.blur_scale != 1:
                print(image.shape)
                height, width, _ = image.shape
                center_y = y_min + (y_max - y_min) / 2
                new_len_y = (y_max - y_min) * self.blur_scale
                y_min = max(0, int(center_y - new_len_y / 2))
                y_max = min(height - 1, int(center_y + new_len_y / 2))

                center_x = x_min + (x_max - x_min) / 2
                new_len_x = (x_max - x_min) * self.blur_scale
                x_min = max(0, int(center_x - new_len_x / 2))
                x_max = min(width - 1, int(center_x + new_len_x / 2))

                print("x")
                print(x_min, x_max)
                print("y")
                print(y_min, y_max)

            if self.debug:
                anonymized_image[y_min:y_max, x_min:x_max, :] = [255, 0, 0]
            else:
                crop = anonymized_image[y_min:y_max, x_min:x_max, :]
                crop = np.array(Image.fromarray(crop).filter(ImageFilter.GaussianBlur(radius=self.kernel_size)))
                anonymized_image[y_min:y_max, x_min:x_max, :] = crop

        return anonymized_image
