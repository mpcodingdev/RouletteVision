
import cv2 as cv

import math
pi = math.pi



roule = [0,32,15,19,4,21,2,25,17,34,6,27,13,36,11,30,8,23,10,5,24,16,33,1,20,14,31,9,22,18,29,7,28,12,35,3,26]
circunf = 2852
dist = round(circunf/37, 2)
radio = 420 # 454
can = 1000
center = [int(732+450/2), int(349+450/2)]
#width_num = int(circunf/37)

def PointsInCircum(r,n=100):
    return [[int(math.cos(2*pi/n*x)*r),int(math.sin(2*pi/n*x)*r)] for x in range(0,n+1)]

points = PointsInCircum(radio, can) #
for i, point in enumerate(points):
    points[i] = ((point[0]+ center[0]), (point[1]+ center[1]))



examp_posit =  (903, 95, 61, 70)
def main():
    None    



def zero_position(num, posit): #  x,y,h,w
    orig, result = calculate(posit)
    posit_in = (36 - roule.index(int(num)))
    index = result[posit_in]
    return index, points[index]


def calculate(posit2):
    orig2 = find_near(posit2, False)
    print(orig2)
    ind = points.index(orig2) #738

    number = round(can/37)
    result = []
    for _ in range(37):
        ind += number
        if ind > len(points):
            ind = ind - len(points)
        result.append(ind)
    dif = [0, 0, 0, -1, -3, -3, -4, -5, -6,
            -6, -5, -5, -5, -5, -3, -3, -4, 0,
            0, 2, 4, 4, 6, 6, 6, 5, 4,
                5, 4, 3,2, 2, 2, 1, 1, 0, 0]
    base = 738
    if ind < base:
        difference = ind+1000-base
    else:
        difference = ind - base
    if difference == 0:
        difference = 1
    prop = int(36*(difference/1000))

    dif2 = dif.copy()
    dif_use = delay(dif2, prop)
    for i in range(len(result)):
        result[i] = int(result[i]) + int(dif_use[i])
    return orig2, result

def delay(list_r, numbers):
    for _ in range(numbers):
        list_r.append(list_r.pop(0))
    return list_r

def mean(pos_4): # pos_4 x1,y1,width, heigth
    #if the format is x1,y1,x2,y2 pmean = ((pos_4[0] + pos_4[2])/2, (pos_4[1] + pos_4[3])/2)
    pmean = ((pos_4[0]*2 + pos_4[2])/2, (pos_4[1]*2 + pos_4[3])/2)
    return pmean

def find_near(pos_3, IND): # 
    #IND to return the point or the point and index
    point_m = mean(pos_3)
    n = 0
    breakk = False
    while True:
        n += 1
        for point in points:
            if (point_m[0]+n) > point[0] > (point_m[0]-n):
                if (point_m[1]+n) > point[1] > (point_m[1]-n):
                    point_r = point
                    breakk = True
                    break
        if breakk:
            break
    if IND:
        ind = points.index(point_r) 
        return point_r, ind
    else:
        return point_r
    
def calc_dist(x,y):
    x = (x[0]-center[0], x[1]-center[1])
    y = (y[0]-center[0], y[1]-center[1])
    if (abs(x[0]),abs(x[1])) != (abs(y[0]),abs(y[1])):
        ang = angle_between_vectors(x,y)
        dist = circunf * ang/360
    else:
        dist = 10000
    return dist

def angle_between_vectors(u, v):
    dot_product = sum(i*j for i, j in zip(u, v))

    norm_u = math.sqrt(sum(i**2 for i in u))
    norm_v = math.sqrt(sum(i**2 for i in v))
    cos_theta = dot_product / (norm_u * norm_v)
    angle_rad = math.acos(cos_theta)
    angle_deg = math.degrees(angle_rad)
    return angle_deg

def find_nearest_2(pos_b): # 
    point_m = mean(pos_b)
    print(point_m)
    n = 0
    dist_m = 100000
    point_r = None
    for point in points:
        dist = calc_dist(point_m, point)
        if dist < dist_m:
            dist_m = dist
            point_r = point
    ind = points.index(point_r) 
    return point_r, ind

if __name__ == "__main__":
    main()
