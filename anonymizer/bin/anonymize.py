"""
Copyright 2018 understand.ai

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[2].resolve()))
import argparse

from anonymizer.anonymization import Anonymizer
from anonymizer.detection import Detector, download_weights, get_weights_path
from anonymizer.obfuscation import Obfuscator


def parse_args():
    parser = argparse.ArgumentParser(
        description='Anonymize faces and license plates in a series of images.')
    parser.add_argument('--input', required=True,
                        metavar='/path/to/input_folder',
                        help='Path to a folder that contains the images that should be anonymized. '
                             'Images can be arbitrarily nested in subfolders and will still be found.')
    parser.add_argument('--image-output', required=True,
                        metavar='/path/to/output_foler',
                        help='Path to the folder the anonymized images should be written to. '
                             'Will mirror the folder structure of the input folder.')
    parser.add_argument('--weights', required=True,
                        metavar='/path/to/weights_foler',
                        help='Path to the folder where the weights are stored. If no weights with the '
                             'appropriate names are found they will be downloaded automatically.')
    parser.add_argument('--image-extensions', required=False, default='jpg,png',
                        metavar='"jpg,png"',
                        help='Comma-separated list of file types that will be anonymized')
    parser.add_argument('--face-threshold', type=float, required=False, default=0.3,
                        metavar='0.3',
                        help='Detection confidence needed to anonymize a detected face. '
                             'Must be in [0.001, 1.0]')
    parser.add_argument('--plate-threshold', type=float, required=False, default=0.3,
                        metavar='0.3',
                        help='Detection confidence needed to anonymize a detected license plate. '
                             'Must be in [0.001, 1.0]')

    parser.add_argument('--write-detections', dest='write_detections', action='store_true')
    parser.add_argument('--no-write-detections', dest='write_detections', action='store_false')
    parser.set_defaults(write_detections=True)

    parser.add_argument('--debug', dest='debug', action='store_true')
    parser.set_defaults(debug=False)

    parser.add_argument('--obfuscation-kernel', required=False, default='21',
                        metavar='kernel_size',
                        help='This parameter is used to change the way the blurring is done. '
                             'For blurring a gaussian kernel is used. The default size of the kernel is 21 pixels '
                             'Higher values lead to a stronger blurring effect but take more time to compute')
    parser.add_argument('--suffix', required=False, default=None,
                        metavar='',
                        help='Suffix for anonimized image filenames')

    args = parser.parse_args()

    print('input: {}'.format(args.input))
    print('image-output: {}'.format(args.image_output))
    print('weights: {}'.format(args.weights))
    print('image-extensions: {}'.format(args.image_extensions))
    print('face-threshold: {}'.format(args.face_threshold))
    print('plate-threshold: {}'.format(args.plate_threshold))
    print('write-detections: {}'.format(args.write_detections))
    print('obfuscation-kernel: {}'.format(args.obfuscation_kernel))
    print('suffix: {}'.format(args.suffix))
    print('debug: {}'.format(args.debug))
    print()

    return args


def main(input_path, image_output_path, weights_path, image_extensions, face_threshold, plate_threshold,
         write_json, obfuscation_parameters, debug, suffix):
    download_weights(download_directory=weights_path)

    kernel_size = obfuscation_parameters.split(',')[0]
    obfuscator = Obfuscator(kernel_size=int(kernel_size), debug=debug)
    detectors = {
        'face': Detector(kind='face', weights_path=get_weights_path(weights_path, kind='face')),
        'plate': Detector(kind='plate', weights_path=get_weights_path(weights_path, kind='plate'))
    }
    detection_thresholds = {
        'face': face_threshold,
        'plate': plate_threshold
    }
    anonymizer = Anonymizer(obfuscator=obfuscator, detectors=detectors)
    anonymizer.anonymize_images(input_path=input_path, output_path=image_output_path,
                                detection_thresholds=detection_thresholds, file_types=image_extensions.split(','),
                                write_json=write_json, suffix=suffix)


if __name__ == '__main__':
    args = parse_args()
    main(input_path=args.input, image_output_path=args.image_output, weights_path=args.weights,
         image_extensions=args.image_extensions, face_threshold=args.face_threshold,
         plate_threshold=args.plate_threshold, write_json=args.write_detections,
         obfuscation_parameters=args.obfuscation_kernel, debug=args.debug, suffix=args.suffix)
