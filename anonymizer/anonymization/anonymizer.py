import json
from pathlib import Path

import numpy as np
from PIL import Image
from tqdm import tqdm


def load_np_image(image_path):
    image = Image.open(image_path).convert('RGB')
    # width, height = image.size
    # image = image.resize((width//4, height//4))
    np_image = np.array(image)

    exif_data = image.info['exif']
    return np_image, exif_data


def save_np_image(image, image_path, exif_data):
    pil_image = Image.fromarray((image).astype(np.uint8), mode='RGB')
    pil_image.save(image_path, exif=exif_data)


def save_detections(detections, detections_path):
    json_output = []
    for box in detections:
        json_output.append({
            'y_min': box.y_min,
            'x_min': box.x_min,
            'y_max': box.y_max,
            'x_max': box.x_max,
            'score': box.score,
            'kind': box.kind
        })
    with open(detections_path, 'w') as output_file:
        json.dump(json_output, output_file, indent=2)


class Anonymizer:
    def __init__(self, detectors, obfuscator):
        self.detectors = detectors
        self.obfuscator = obfuscator

    def anonymize_image(self, image, detection_thresholds):
        assert set(self.detectors.keys()) == set(detection_thresholds.keys()),\
            'Detector names must match detection threshold names'
        detected_boxes = []
        for kind, detector in self.detectors.items():
            new_boxes = detector.detect(image, detection_threshold=detection_thresholds[kind])
            detected_boxes.extend(new_boxes)
        return self.obfuscator.obfuscate(image, detected_boxes), detected_boxes

    def anonymize_images(self, input_path, output_path, detection_thresholds, file_types, write_json, suffix=None):
        print('Anonymizing images in {} and saving the anonymized images to {}...'.format(input_path, output_path))

        Path(output_path).mkdir(exist_ok=True)
        assert Path(output_path).is_dir(), 'Output path must be a directory'

        files = []
        for file_type in file_types:
            files.extend(list(Path(input_path).glob('**/*.{}'.format(file_type))))

        for input_image_path in tqdm(files):
            # Create output - output directory
            relative_path = input_image_path.relative_to(input_path)

            if suffix:
                relative_path = relative_path.with_name("{name}_{suffix}{ext}".format(name=relative_path.stem,
                                                                                      suffix=suffix,
                                                                                      ext=relative_path.suffix))

            (Path(output_path) / relative_path.parent).mkdir(exist_ok=True, parents=True)
            output_image_path = (Path(output_path) / relative_path)
            output_detections_path = (Path(output_path) / relative_path).with_suffix('.json')

            # Anonymize image
            image, exif_data = load_np_image(str(input_image_path))
            anonymized_image, detections = self.anonymize_image(image=image, detection_thresholds=detection_thresholds)
            save_np_image(image=anonymized_image, image_path=str(output_image_path), exif_data=exif_data)
            if write_json:
                save_detections(detections=detections, detections_path=str(output_detections_path))
