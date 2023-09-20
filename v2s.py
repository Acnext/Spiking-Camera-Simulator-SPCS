import numpy as np
import argparse
import math
import scipy
import struct
from scipy import integrate
import cv2  # 利用opencv读取图像
import matplotlib.pyplot as plt 
from PIL import Image
import copy
#w，h is resolution of image，frame_tot is total number of images，file_name is the directory of image
def get_spike(in_filepath = "E:\\image\\crash\\", out_filepath = "E:\\image\\crash\\spike\\", w = 400, h = 250, threshold = 256,  frame_start = 145000, frame_end = 145000 + 500):
    accumulator = np.zeros((h, w))
    byte = 0
    pos = 0
    f = open(out_filepath + "test.dat", 'wb')
    for i in range(frame_start, frame_end + 1):
        print(i)
        num = str(i).zfill(4) #自动补0 总共补成到5位
        img_str = in_filepath + num + ".png"
        print(img_str)
        img = np.array(Image.open(img_str).convert('L').resize((w, h),Image.ANTIALIAS))
        #img.show()
        print(img.shape)
        for a in range(h):
            for b in range(w):
                #print(b)
                #print(img[a][b])
                accumulator[a][b] += img[a][b]
                if accumulator[a][b] >= threshold:
                    accumulator[a][b] -= threshold
                    byte = byte | (1 << (pos))
                pos += 1
                #print(i)
                if pos == 8:
                    pos = 0
                    temp = struct.pack('B', byte)
                    #print(byte)
                    #print(struct.unpack('B', temp))
                    byte = 0
                    f.write(temp)
        if pos != 0:
            pos = 0
            temp = struct.pack('B', byte)
            byte = 0
            f.write(temp)
    f.close()
    return
#get_spike("D:\\lwhu\\gt\FlowDataset\\cook\\", "D:\\lwhu\\gt\FlowDataset\\cook\\", 800, 500, 400, 0, 4000)
"""
for i in range(100):
    file = "D:\\lwhu\\gt\FlowDataset\\pretrain_quick\\" + str(i) + "\\"
    print(i)
    get_spike(file, file, 800, 500, 400, 0, 500)
    """
"""if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-W", "--width")
    parser.add_argument("-H", "--height")
    parser.add_argument("-phi", "--threshold")
    parser.add_argument("--frame_tot")
    parser.add_argument("--file_name")
    args = parser.parse_args()
    get_spike(args.W, args.H, args.phi, args.frame_tot, args.file_name)
"""