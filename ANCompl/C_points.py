import cv2 as cv
import csv
version = 3
name_csv= f"ANResource/points-v{version}.csv"

def main():
    camera = cv.VideoCapture("ANResource\VIDEO-MP4\RESULT-INPUT.mp4")
    ok, image = camera.read() # Grabs, decodes and returns the next video frame.
    i = 0
    cv.imshow("JUST EXAMPLE", image)
    cv.waitKey(0)


    points_or = [[([524, 1025],[660,1045]), ([500, 1005],[650,1025]),   ([480, 985],[625,1005])],
                 [([300, 500],[430, 580])],    
                [ ([548, 20],[685, 40]),([522, 40],[665, 60]),([505, 60],[650, 75])],

                    [([1200, 20],[1365, 40]),([1215, 40],[1385, 60]),([1225, 60],[1405, 75])],
                    [( [1485, 500],  [1615, 580])],
                     [ ([1300,975], [1453,995]),([1280,995], [1432,1015]), ([1260,1015], [1410,1035])]]
    
    extra_p1 = [[[1029, 519], [1008, 497]], [[570, 298]], [[57,516],[35,543]],   [[57,1393],[35,1372]], [[570, 1617]],[[1000,1437],[1021,1416]]] # y,x
    
    extra_p2 = [[[985, 640], [995, 650]], [[550, 440], [530, 440]], [[78,653],[72,665]],   
                      
                      [[72,1210],[62,1195]], [[550, 1475], [530, 1475]], [[985,1280],[995,1260]] ]

    points = create_points(points_or)
    for i, list in enumerate(points):
        for point4 in extra_p1[i]:
            list.append(point4)
        for point4 in extra_p2[i]:
            list.append(point4)
    if True:
        image_show3 = image.copy()
        for j in points:
            c = 0
            for point4 in j:
                c += 5
                if c > 255:
                    c = 0
                cv.rectangle(image_show3, (point4[1], point4[0]), (point4[1], point4[0]), (c,255-c,0), thickness=4 )
                    
        for group in extra_p2:
            for point in group:
                cv.rectangle(image_show3, (point[1], point[0]), (point[1], point[0]), (255,0,255), thickness=5 )
        cv.imshow("SHOW POINTS", image_show3)
        cv.waitKey(0)

        with open(name_csv, mode='w', newline='') as file:
            writer = csv.writer(file)
            for sublist in points:
                for point in sublist:
                    writer.writerow(point)
                writer.writerow("000")

def create_points(points_or2):
    
    ret_points = []
    for group in points_or2:	
        p_temp = []
        for gpoints in group:
            ratiox = ((gpoints[1][0]-gpoints[0][0])/10 )
            ratioy = ((gpoints[1][1]-gpoints[0][1])/10 )
            dx = int((gpoints[1][0] - gpoints[0][0]) / ratiox)
            dy = int((gpoints[1][1] - gpoints[0][1]) / ratioy)
            
            for ix in range(int(ratiox)): # 
                x = gpoints[0][0] + ix * dx + int(dx*2/3)
                for iy in range(int(ratioy)):
                    y = gpoints[0][1] + iy * dy + int(dy/2)
                    p_temp.append((y, x))
        ret_points.append(p_temp)
    return ret_points
if __name__ == '__main__':
    main()