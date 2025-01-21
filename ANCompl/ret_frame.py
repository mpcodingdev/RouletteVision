from datasets import load_dataset, Image, Dataset, Video
import requests
from decord import VideoReader
from decord import cpu, gpu
import cv2 as cv
import numpy as np

def ret_fr(video_reader, n_fr):
    try:
        frame1 = video_reader.get_batch([n_fr])
    except:
        return False, None
    frame1 = (frame1.asnumpy())[0]
    frame = cv.cvtColor(frame1, cv.COLOR_RGB2BGR)
    if n_fr % 10 == 0: print("FRAME Nº: ", n_fr)
    return True, frame 