
from __future__ import print_function
from datasets import load_dataset
import cv2 as cv
import numpy as np
from AN1_vid_1 import loop_an1
from ANCompl.C_match import match1util
from ANCompl.C_calcroulette import zero_position
from ANCompl.C_ballpos import main_ball
from ANCompl.ret_frame import ret_fr
from ANCompl.C_parser import parser_fn
import math
import argparse
from video import create_capture, presets
SHOW = False
pi = math.pi
backSub = cv.createBackgroundSubtractorMOG2()
num_res = 5 

class App(object):

    def __init__(self, args, box_number):
        self.args = args
        self.box_number = box_number
        self.trackerAlgorithm = args.tracker_algo
        self.tracker2 = self.createTracker()
        self.tracker = self.createTracker()

    def createTracker(self): # depending on the algorithm selected uses one or another- IN THIS CASE, ALWAYS NANOTRACK
        params = cv.TrackerNano_Params()
        params.backbone = self.args.nanotrack_backbone
        params.neckhead = self.args.nanotrack_headneck
        params.backend = self.args.backend
        params.target = self.args.target
        tracker = cv.TrackerNano_create(params)
        
        return tracker

    def run(self, number, n_vid, act_vers, direction=None):
        position_reg = []
        time_reg = []
        video_v = self.args.input # GET THE VIDEO SOURCE
        ok, frame = ret_fr(video_v, 0)

        print("BOX: ", self.box_number)
        self.tracker.init(frame, self.box_number)

        #BG-SUB2
        point_list = get_points() # 
        point, when = where(point_list , video_v) # 
        
        if SHOW:
            frame_copy = frame.copy()
            cv.rectangle(frame_copy, point, point, (0,255,0), thickness=13)
            cv.imshow("SHOW1", frame_copy)
            cv.waitKey(0)
        i = 0
        clock_sense = None
        ind_dir = []
        FINAL = False
        frame_num = 0
        while True:
            i += 1
            frame_num += 1
            ok, frame = ret_fr(video_v, frame_num)
            if not ok:
                break
            frame1 = frame.copy()
            ok, newbox = self.tracker.update(frame1) # Update the tracker, find the new most likely bounding box for the target.
            if SHOW:
                frame_copy2 = frame.copy()
                cv.rectangle(frame_copy2, newbox, (0,255,0), thickness=7)
                cv.imshow("FRAME2", frame_copy2)
                cv.waitKey(0)
            
            if clock_sense == None and newbox:
                ind, pos = zero_position(number, newbox) 
                ind_dir.append(ind)
                if i > 3:
                    clock_sense = direct_f(ind_dir, i-2)
                    print("RETURNED CLOCKSENSE", clock_sense)
            if i % 30 == 2: # WRTIE INFO
                ind, pos = zero_position(number, newbox) 
                second = frame_num / 30 
                time_reg.append(f"{second:.2f}")
                position_reg.append((ind))
            if i+1 >= when and FINAL == False and clock_sense != None:
                print("INFO",  when, clock_sense, num_res)
                reg_res = main_ball(video_v, when, clock_sense, num_res) # function that returns the movements of the ball from the moment it enters
                FINAL = True
        write_csv(position_reg, time_reg, reg_res, n_vid, act_vers, direction)
        print('Done')




def write_csv(position_reg, time_reg, reg_res, num, version_ac3, direction=None):
    if direction:
        dir_txt = f"{direction}.{num}.txt"     
    else:
        dir_txt = f"ANResults/RESULTS-{version_ac3}/OF2/result.OF2.{num}.txt"
    print(dir_txt)
    with open(dir_txt, 'w', newline='' ) as file:
        for i in range(len(position_reg)):
            file.write(f"{position_reg[i]},{time_reg[i]}\n")
        file.write("CHANGE"+" \n")
        for line in reg_res:
            file.write(f"{line[0]},{line[1]}\n")


def run_an2(video_inp, version_ac2, n_vid, direction=None):
    num, box_number = match1util(video_inp)
    print("NUM: ", num, "BOX: ", box_number)
    parser = argparse.ArgumentParser(description="Run tracker")
    parser_fn(parser)
    parser.add_argument("--input", type=str, default=video_inp, help="Path to video source")
    args = parser.parse_args()
    App(args, box_number).run(num, n_vid, version_ac2, direction)

def direct_f(register, total):
    print(register)
    if register[total] > register[total+1]:
        if register[total] > 900 and register[total+1] < 100:
            return False
        else:
            return False
    elif register[total+1] > register[total]:
        if register[total+1] > 900 and register[total] < 100: 
            return False
        else:   
            return True
    else:
        return None


def get_points():
    center = [int(732+450/2), int(354+450/2)]
    points = PointsInCircum(465, 500)# 
    points2 = PointsInCircum(475, 500)   #510,  360
    point_list = []
    for ind in range(len(points)):
        point = points[ind]
        point2 = points2[ind]
        point[0] = int(point[0] + center[0])
        point[1] = int(((point[1]*0.98) + center[1]))
        point2[0] = int(point2[0] + center[0])
        point2[1] = int(((point2[1]*0.98) + center[1]))
        point_list.append(point) 
        point_list.append(point2) 
    return point_list
            
def PointsInCircum(r,n=100):
    return [[int(math.cos(2*pi/n*x)*r),int(math.sin(2*pi/n*x)*r)] for x in range(0,n+1)]




def where(points, vr_w):
    point_start = None
    n_fra = 1
    while True:
        n_fra += 1
        ret, frame = ret_fr(vr_w, n_fra)
        fgMask1 = backSub.apply(frame)
        ret , treshold1 = cv.threshold(fgMask1.copy(), 200, 255,cv.THRESH_BINARY)
        if SHOW:
            cv.imshow("threshold", treshold1.copy())
            cv.waitKey(0)
        for point in points:
            if treshold1[point[1], point[0]] == 255:
                point_start = points.index(point)
                total = 0
                for i in range(-3,3):
                    index = point_start + i
                    if treshold1[(points[index])[1],(points[index])[0]] > 225:
                        total += 1
                    if total > 5: # 
                        return point, n_fra

def loop_an2(set, version_ac, ini):
    errors = []
    dataset_loop = (load_dataset("mp-coder/RouletteVision-Dataset",  f"S{set}"))["output"]

    for i in range(ini, 22):          
        print("ACTUAL", i)
        try:
            video_input = dataset_loop[i]["video"]
            run_an2(video_input, version_ac, i, f"RESULT/OUTPUT-RES/OF2-OUTPUT.{set}")
        except:
            print(f"ERROR: {i}")
            errors.append(i)
    return errors



if __name__ == "__main__":
    A = 0
    version_ac = 2
    errors = []
    set = 1
    errors2 = []
    if A == 1:
        errors.append(loop_an2(4, 0, 0))
    else:
        n_vid = 172
        dataset_s1 = load_dataset("mp-coder/RouletteVision-Dataset", 'S2') #
        s1_output = dataset_s1["output"]
        video = s1_output[n_vid]["video"]

        run_an2(video,version_ac, n_vid, f"RESULT/OUTPUT-RES/OF2-OUTPUT.2")
    print(f"ERRORS X: {errors2}")
    print(f"ERRORS 2: {errors}")

