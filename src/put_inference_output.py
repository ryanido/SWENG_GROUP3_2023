import cv2
import numpy

import labels.coco91 as coco
import colour_palette as palette

numpy.set_printoptions(suppress=True, precision=3)

colours = palette.get_colour_palette(len(coco.labels))


def get_most_probable_bounds(box, size):
  box[0] = box[0] * size[1]
  box[1] = box[1] * size[0]
  box[2] = box[2] * size[1]
  box[3] = box[3] * size[0]
  box[0] = max(int(box[0]), 0)
  box[1] = max(int(box[1]), 0)
  box[2] = min(int(box[2]), size[1])
  box[3] = min(int(box[3]), size[0])

  return numpy.int32(box)


def put_inference_output(image, inference_output):
  confidence_threshold = 0.3
  label_height = 18

  for detection in inference_output:
    score = numpy.float32(detection[2])

    if (score < confidence_threshold):
      break

    box = detection[3:]
    label_index = numpy.int32(detection[1])

    if (score >= confidence_threshold):
      box = get_most_probable_bounds(box, [image.shape[0], image.shape[1]])
      xmin = box[0]
      ymin = box[1]
      xmax = box[2]
      ymax = box[3]

      det_label = f'{score*100:2.1f}% {coco.labels[label_index]}'

      colour = colours[label_index]
      text_colour = (28, 28, 28)

      cv2.rectangle(
          image,
          (xmin, ymin), (xmax, ymax),
          colour, 2)
      cv2.rectangle(
          image,
          (xmin, ymin - label_height), (xmax, ymin),
          colour, -1)
      cv2.rectangle(
          image,
          (xmin, ymin - label_height), (xmax, ymin),
          colour, 2)
      cv2.putText(
          image,
          det_label,
          (xmin, ymin - 7),
          cv2.FONT_HERSHEY_SIMPLEX, 0.4, text_colour, 1)
