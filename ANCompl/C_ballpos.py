
import cv2 as cv
import numpy as np
import random

from ANCompl.C_calcroulette import find_nearest_2
from ANCompl.ret_frame import ret_fr

#y,x,wh = 165,555, 800
y,x,h,w = 75,440, 980,1030


def main_ball(video_v, when, direct, how_many):
    #video_v 
    register = []
    n_frame = 0
    while True:
        n_frame += 1
        ok, frame = ret_fr(video_v, n_frame)

        if not ok:
            print("NOT OK")
            break

        if n_frame >= when:
            pos_ball = search_p(frame)
            if pos_ball:
                second = n_frame / 30 
                pos_rul, ind_rul = find_nearest_2(pos_ball) # pos_ball has to be x1,y1,wh,he
                register.append([second, ind_rul])
                if len(register) > 6:
                    ind = landing(register, direct)
                    if ind != None:
                        final = register[ind]
                        start = register[0]
                        print(f"breaks in {register[ind][0]}")
                        for r in range(len(register)-ind):
                            register.remove(register[ind])
                        break
    print(register)
    result_ret = reduce(register, how_many, start)
    result_ret.append(final)
    return result_ret # format: start, 5 values and final






def landing(register1, direcc):
    register = register1.copy()
    total = 0
    if direcc:
        for i in range(len(register)-1,len(register)-4,-1):
            initi = register[i-1][1]
            next = register[i][1]
            differ = next - initi
            print(initi, next)
            if differ < 0:
                differ += 1000
            if differ == 0:
                differ = 1
            dif_time = (float(register[i][0]) - float(register[i-1][0])) * 100
            ratio = differ/dif_time
            if 4.8 > ratio > 1:
                total += 1
            if total == 3:
                return i
    else:
        for i in range(len(register)-1,len(register)-4,-1):
            initi = register[i-1][1]
            next = register[i][1]
            differ = initi- next
            if differ < 0:
                differ += 1000
            if differ == 0:
                differ = 1
            dif_time = (float(register[i][0]) - float(register[i-1][0])) * 100
            ratio = differ/dif_time
            if 4.8 > ratio > 1:
                total += 1
            if total == 3:
                return i
        
    return None


def reduce(register, quant, start):
    result_ret = []
    result_ret.append(start)
    register.remove(start)
    leng = len(register)
    ratio2 = int(leng/quant)
    ind = 0
    f = int((ratio2)*2/4) #larger, more random
    print(ratio2, leng)
    
    for ii in range(quant):
        if f > 1:
            ind += (ratio2 + random.randrange(-f+1, f))
        else:
            ind += (ratio2)
        if ind >= leng-1:
            print(ind)
            ind = ind - (ind-leng+1) -(quant-ii-1)
            print(ind)
            print("ii",ii, quant)
        result_ret.append(register[ind])
    return result_ret

def search_p(frame2):
    template = cv.imread("ANResource\BALL-WHITE.png", cv.IMREAD_UNCHANGED)
    template = np.delete(template, 3,2)
    treshold = 0.92
    result = cv.matchTemplate(frame2, template, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
    if max_val >= treshold:
        matchLoc = max_loc
        yy = 10
        xx = 5
        result_ret = (matchLoc[0]-xx, matchLoc[1]-yy, template.shape[0] +xx,template.shape[1]+yy)
        #returns result_ret as x1 y1 w h
        return result_ret
    else:
        print("NOT FOUND")
        return None


if __name__ == "__main__":
    None