import cv2
import numpy as np 
import time

def generate_grabcut(mask, image):
    gc_mask = np.array(mask)
    gc_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    gc_mask[gc_mask>0] = cv2.GC_PR_FGD
    gc_mask[gc_mask==0] = cv2.GC_BGD

    fgModel = np.zeros((1, 65), dtype='float')
    bgModel = np.zeros((1, 65), dtype='float')

    start = time.time()
    (gc_mask, bgModel, fgModel) = cv2.grabCut(gc_image, gc_mask, None, bgModel, fgModel, 5, mode = cv2.GC_INIT_WITH_MASK)
    end = time.time()
    running_time = end-start
    output_mask = (gc_mask == cv2.GC_PR_FGD).astype('uint8') * 255
    return output_mask, running_time
