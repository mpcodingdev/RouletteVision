from __future__ import print_function
from datasets import load_dataset
import cv2 as cv
from ANCompl.C_match import match1util
from ANCompl.C_calcroulette import zero_position, find_near
from ANCompl.ret_frame import ret_fr
from ANCompl.C_parser import parser_fn
blur_v = 9
SHOW = False
name_csv = "ANResource\points-v3.csv"
cuadr = [[None, True, True, True, False, False], [False, None, True, True, True, False], 
[False, False, None, True, True, True], [False, False, False, None, True, True], 
[True, False, False, False, None, True], [True, True, False, False, False, None]]
import  random, argparse, csv
from video import create_capture, presets

backSub = cv.createBackgroundSubtractorMOG2()
backSub2 = cv.createBackgroundSubtractorMOG2()
time_pos = [0.55,0.3, 0.70, 0.55, 0.50, 0.5]
time_pos_rev = time_pos[::-1]
contrary_pos = [3,4,5,0,1,2]
n_loops = 2

points_show = [([495, 990],[690,1040]),   ([300, 500],[430, 580]),    ([510, 20],[730, 70]),
                      ([1180, 20],[1400, 70]),( [1485, 500],  [1615, 580]), ([1250,975], [1435,1035])]


class App(object):

    def __init__(self, args, box_number):
        self.args = args
        self.box_number = box_number
        self.trackerAlgorithm = args.tracker_algo
        self.tracker = self.createTracker()

    def createTracker(self): # depending on the algorithm selected uses one or another- IN THIS CASE, ALWAYS NANOTRACK
        params = cv.TrackerNano_Params()
        params.backbone = self.args.nanotrack_backbone
        params.neckhead = self.args.nanotrack_headneck
        params.backend = self.args.backend
        params.target = self.args.target
        tracker = cv.TrackerNano_create(params)
        
        return tracker

    def initializeTracker(self, image):
        bbox = cv.selectROI('tracking', image) # The function creates a window and allows users to select multiple ROIs using the mouse "region of interest (ROI)""
        self.tracker.init(image, bbox) # Initialize the tracker with a known bounding box that surrounded the target.
        return

    def run(self, number, n_vid, write_dir2, direction=None):
        position = []
        time_set = []

        video_v = self.args.input # GET THE VIDEO SOURCE
        ok, image = ret_fr(video_v, 0)
        print(image.shape)
        print("BOX: ", self.box_number)
        self.tracker.init(image, self.box_number)
        i = 0

        point_set = import_points()

        if SHOW:
            image_show = image.copy() 
            c = 0
            for j in point_set:
                colors = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (0,255,255), (255,0,255)]
                c += 1
                for point4 in j:
                    if c > 6:
                        c = 0
                    cv.rectangle(image_show, (point4[1], point4[0]), (point4[1], point4[0]), (colors[c-1]), thickness=4 )
            cv.imshow("image_show", image_show)
            cv.waitKey(0)
        pos_2, clock_dir = position_fun(video_v, point_set)
        pos_2_double = contrary_pos[pos_2]
        print("RETURNED", clock_dir, pos_2)
        f_info, reg_newbox = [], []
        first_trial = True
        doub_analysis = True
        frame_num = 0
        while True: 
            i += 1
            frame_num += 1
            ok, image = ret_fr(video_v, frame_num)
            second = frame_num / 30 #camera.get(cv.CAP_PROP_POS_MSEC) / 1000
            if not ok:
                print("NO OK")
                break
            ok, newbox = self.tracker.update(image)
            reg_newbox.append(newbox)
            if i % 30 == 2:
                print("second", second)
                time_set.append(f"{second:.2f}")
                ind, pos = zero_position(number, newbox)
                position.append((ind))

            fgMask = backSub.apply(image)
            blur = cv.GaussianBlur(fgMask,(blur_v,blur_v),0)
            ret , treshold = cv.threshold(blur, 253, 255,cv.THRESH_BINARY)
            if clock_dir == None:
                clock_dir = dir_newbox(reg_newbox)
                print("clock_dir", clock_dir)
                if clock_dir == None:
                    continue
                else:
                    frame_num += 1
                    print("RESET")
                    f_info, position, time_set = [], [], []

            if first_trial:
                first_trial = False
                sec_before = float(100000)
                for n_fr in range(1):
                    ok, image = ret_fr(video_v, n_fr) #camera.read()
                    fgMask = backSub.apply(image)
                    blur = cv.GaussianBlur(fgMask,(blur_v,blur_v),0)
                    ret , treshold = cv.threshold(blur, 253, 255,cv.THRESH_BINARY)
                    if SHOW:
                        cv.imshow("thresh", treshold)
                        cv.waitKey(0)

            second = float(f"{(frame_num / 30):.2f}")
                
            if SHOW:
                    image_show = image.copy()
                    for i in range(len(point_set)):
                        for point in point_set[i]:
                            cv.rectangle(image_show, (point[1], point[0]), (point[1], point[0]),  (0,0,255), thickness=2)
                    cv.rectangle(image_show, newbox, (0,255,255), thickness=4)

                    cv.imshow("frame_show", image_show)
                    cv.waitKey(0)
            if time_pos[pos_2] < (second-sec_before) and clock_dir:
                pos_2_double += pos_2 +1
                if pos_2_double > 5:
                    pos_2_double = 0
                doub_analysis = True

            if time_pos_rev[pos_2] < (second-sec_before)  and not clock_dir:
                pos_2_double = pos_2 - 1
                if pos_2_double < 0:
                    pos_2_double = 5
                doub_analysis = True

            for point in point_set[pos_2]:

                if treshold[point] == 255:
                    val = check_f(treshold, point, 7)
                    if val:
                        print(pos_2, second)
                        f_info.append((clock_dir, second, pos_2))
                        if not clock_dir:
                            pos_2 = pos_2 -1
                        else:
                            pos_2 += 1
                        if pos_2 > 5:
                            pos_2 = 0
                        elif pos_2 < 0:
                            pos_2 = 5
                        doub_analysis = False
                        sec_before = second
                        
                        break
            if doub_analysis:
                for point in point_set[pos_2_double]:
                    if treshold[point] == 255:
                        val = check_f(treshold, point, 7)
                        if val:
                            doub_analysis = False
                            pos_2 = pos_2_double
                            f_info.append((clock_dir, second, pos_2))
                            if not clock_dir:
                                pos_2 = pos_2 -1
                            else:
                                pos_2 += 1
                            if pos_2 > 5:
                                pos_2 = 0
                            elif pos_2 < 0:
                                pos_2 = 5
                            sec_before = second
                            
                            break
        print("TRUE", f_info)
        reduced, direcc = reduce_f(f_info, n_loops, NO_REDUCE = True)
        print("REDUCED", reduced)
        print("POSITION"    , position)
        print("TIME", time_set)
        write_csv(position, time_set, reduced, direcc,n_vid, write_dir2, direction)

        print('Done')




def write_csv(position, time_set, reduced, direcc, num, write_dir3, direction = None):
    num    
    print(num)
    if direction:
        arch = f"{direction}.{num}.txt"     

    else:
         arch = f"ANResults/RESULTS-{write_dir3}/OF1/result.OF1.{num}.txt"
    with open(arch, 'w', newline='' ) as file:
        file.write(str(direcc) + "\n")
        for i in range(len(position)):
            file.write(f"{position[i]},{time_set[i]}\n")
        file.write("CHANGE"+" \n")
        for line in reduced:
            file.write(f"{line[0]},{line[1]}\n")

def run_an1(video, write_dir1, n_vid,direction=None):
    num, box_number = match1util(video)
    print("num", num)
    parser = argparse.ArgumentParser(description="Run tracker")
    parser_fn(parser)
    parser.add_argument("--input", type=str, default=video, help="Path to video source")
    args = parser.parse_args()
    print("box_number", box_number)
    App(args, box_number).run(num, n_vid, write_dir1, direction)

def check_f(frame,point_ch, thres=5):# ¡
    # x1 y1 format
    x1 = point_ch[1]
    y1 = point_ch[0]
    for col in range(x1-5, x1+5):
        count = 0
        for row in range(y1-5, y1+5):
            if frame[row, col] > 250:
                count += 1
        if count > thres: #(count/(y2-y1)) > 0.6
            print("count: ", count)
            return True
    return False

def dir_newbox(reg_newbox):
    indexes = []
    if len(reg_newbox) == 1: return None
    for square in reg_newbox:
        pos, ind = find_near(square, True)
        if ind not in indexes and ind != None:
            indexes.append(ind)
    l = len(indexes)
    if indexes[l-2] > indexes[l-1] and abs(indexes[l-2]-indexes[l-1]) < 25:
        return True
    elif indexes[l-2] < indexes[l-1] and abs(indexes[l-2]-indexes[l-1]) < 25:
        return False
    elif indexes[l-2] > 970 and indexes[l-1] < 30:
        return False
    elif indexes[l-2] > 970 and indexes[l-1] < 30:
        return True
    else:
        return None


def reduce_f(reg_red, loops_red, NO_REDUCE):
    result = []
    if not NO_REDUCE:
        if len(reg_red) < loops_red*6:
            loops_red = 1
        for i in range(loops_red*6):
            try:
                result.append((reg_red[i][1], reg_red[i][2]))
            except:
                print("shit")
                None
    else:
        for i in range(len(reg_red)):
            try:
                result.append((reg_red[i][1], reg_red[i][2]))
            except:
                print("shit")
                None            
    return result, reg_red[0][0]

def position_fun(video_p, points):
    for n in range(5):
        ret, frame = ret_fr(video_p, n)
        fgMask = backSub2.apply(frame) 
        blur = cv.GaussianBlur(fgMask, (blur_v,blur_v),0)
        ret , treshold = cv.threshold(blur, 253, 255,cv.THRESH_BINARY)
    sec = []
    forward = False
    n_frame = 5
    while True:
        n_frame += 1
        ret, frame = ret_fr(video_p, n_frame)
        if not ret and len(sec) > 1: 
            where2, clock_dir2 = func_2(sec)
            if where2 != None:
                return where2, clock_dir2
        else:
            return 1, None

        fgMask = backSub2.apply(frame)
        blur = cv.GaussianBlur(fgMask,(blur_v,blur_v),0)
        ret , treshold = cv.threshold(blur, 253, 255,cv.THRESH_BINARY)
        if forward:
            forward = False
            for _ in range(7):
                n_frame += 1
                ret, frame = ret_fr(video_p, n_frame)
                if not ret and len(sec) > 1: 
                    where2, clock_dir2 = func_2(sec)
                    if where2 != None:
                        return where2, clock_dir2
                fgMask = backSub2.apply(frame)
                blur = cv.GaussianBlur(fgMask,(blur_v,blur_v),0)
                ret , treshold = cv.threshold(blur, 253, 255,cv.THRESH_BINARY)
        for i, set in enumerate(points):
            for puntto in set:
                if treshold[puntto] > 250:
                    res = check_f(treshold, puntto, thres=8) # 
                    if res:
                        forward = True
                        sec.append(i)
                        print("sec", sec)
                        if len(sec) > 2:
                            where, clock_dir4 = check_seg(sec)
                            if where != None:
                                return where, clock_dir4
                        break
def func_2(sec2):
    values = []
    for num in sec2:
        if num not in values:
            values.append(num)
        if len(values) == 2:
            return values[0], cuadr[values[0]][values[1]]
    return None, None

def import_points():
    
    ret_points = []
    with open(name_csv, mode='r') as file:
        reader = csv.reader(file)
        sublist = []
        for row in reader:

            if row[0] == "0":
                ret_points.append(sublist)
                sublist = []
                
            else:
                sublist.append((int(row[0]), int(row[1])))
            
    return ret_points

def check_seg(sec_c):
    first = True
    for i in range(len(sec_c)-1):
        anterior = sec_c[i]
        actual = sec_c[i+1]
        if first and anterior != actual:
            first = False
            clock_dir3 = cuadr[anterior][actual]
        elif anterior != actual:
            if cuadr[anterior][actual] == clock_dir3:
                return sec_c[0], clock_dir3
    return None, None
                
def loop_an1(set, start, end):
    errors = []
    dataset_loop = (load_dataset("mp-coder/RouletteVision-Dataset", f"S{set}"))["input"]
    video_input = dataset_loop[3]["video"]
    run_an1(video_input, version_ac, 3, f"RESULT/INPUT-RES/OF1-INPUT.{set}")
    for i in range(start, len(dataset_loop)):
        if True:
            print("ACTUAL", i)
            try:
                video_input = dataset_loop[i]["video"]
                run_an1(video_input, version_ac, i, f"RESULT/INPUT-RES/OF1-INPUT.{set}")
            except:
                print(f"ERROR: {i}")
                errors.append(i)
    return errors

version_ac = 13


if __name__ == '__main__':
    A = 0
    version_ac = 13
    write_dir = version_ac
    set = 1
    errors = []
    if A == 1:
        errors.append(loop_an1(set, 0, 113))
        print(f"ERRORS: {errors}")
    else:
        n_vid = 49
        dataset_s1 = load_dataset("mp-coder/RouletteVision-Dataset", 'S2') # split="input"
        s1_input = dataset_s1["input"]
        video = s1_input[n_vid]["video"]

        run_an1(video,version_ac, n_vid, "TEMP")

