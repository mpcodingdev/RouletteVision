import cv2 as cv
import numpy as np
import glob
import cv2
from ANCompl.ret_frame import ret_fr

def main():
    None

SHOWW = False

def match1util(vr):
    template_dir="ANResource/NU/*"
    ok, or_image1 = ret_fr(vr, 0)
    y= 115
    x= 800
    h= 110
    w= 310
    print(or_image1.shape)
    
    threshold = 0.6
    or_image1 = cv.resize(or_image1, (1920, 1080))
    or_image = or_image1[y:y+h, x:x+w].copy()
    
    if (or_image1.shape) == (1080, 1920, 4):
        or_image = np.delete(or_image, 3,2) # deletes from the third dimension the 4th array, from (90, 270, 4) to (90, 270, 3)
    if SHOWW:
        or_image1cop = or_image1.copy()
        cv.imshow("SHOW1", or_image1cop)
        cv.waitKey(0)
    while True:
        for path in glob.glob(template_dir):
            template = cv.imread(path, cv.IMREAD_UNCHANGED)
            if (template.shape[2]) == 4:
                template = np.delete(template, 3,2) 
            result = cv.matchTemplate(or_image, template, cv.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
            if SHOWW:
                    or_image1cop = or_image.copy()
                    cv.imshow("SHOW2", or_image1cop)
                    cv.waitKey(0)
            print("max_val"*1, max_val)
            if max_val >= threshold:
                print(path)
                num = (path.split("NUM")[1]).replace(".png", "")
                needle_w = template.shape[1]
                needle_h = template.shape[0]
                top_left = max_loc
                bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)
                
                top_left_total = (top_left[0] + int(( x)), top_left[1] + int(( y)))
                
                r_box = (top_left_total[0], top_left_total[1], needle_w, needle_h)

                if (or_image1.shape) == (1080, 1920, 4):
                    or_image1 = np.delete(or_image1, 3,2)

                print(num, r_box)
                return num, r_box
                #return num, r_box, or_image1
        
        return None, None
            
if __name__ == "__main__":
    main()