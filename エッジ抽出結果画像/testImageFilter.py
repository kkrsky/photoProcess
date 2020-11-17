#-*- coding:utf-8 -*-
import cv2
import numpy as np

# load image (grayscale)
# 入力画像をグレースケールで読み込み
# inputPath=r'/Users/kkrsky/OneDrive - Shizuoka University/【静岡大学】/【大学講義】/5年生(M1)/講義/後期/火3 画像情報処理論/testPython/input.bmp'
# outputPath=r'/Users/kkrsky/OneDrive - Shizuoka University/【静岡大学】/【大学講義】/5年生(M1)/講義/後期/火3 画像情報処理論/testPython/output.bmp'
gray = cv2.imread(inputPath, 0) 

# kernel of blur filter
# カーネル（縦方向の輪郭検出用）
kernel = np.array([[1/9, 1/9, 1/9],
                   [1/9, 1/9, 1/9],
                   [1/9, 1/9, 1/9]])
kernel_x=np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
kernel_y=np.array([[-1,-2,-1],[0,0,0],[1,2,1]])
filterData1=np.array([[-1,0,1]]*3)
filterData2=np.array([[1,1,1],[0,0,0],[-1,-1,-1]])
filterData3=np.array([[0,1,1],[-1,0,1],[-1,-1,0]])
filterData4=np.array([[1,1,0],[1,0,-1],[0,-1,-1]])
filterData7=np.array([[0,1,0],[1,-4,1],[0,1,0]])

# Spatial filtering
# 方法2(OpenCVで実装)
# dst = cv2.filter2D(gray, -1, filterData5)
# dst = cv2.filter2D(dst, -1, filterData6)

gray_x = cv2.filter2D(gray,cv2.CV_64F, kernel_x)
gray_y = cv2.filter2D(gray,cv2.CV_64F, kernel_y)
# dst = np.sqrt(gray_x ** 2 + gray_y ** 2)

def filter2d(src, kernel):
    # カーネルサイズ
    m, n = kernel.shape

    # 畳み込み演算をしない領域の幅
    d = int((m-1)/2)
    h, w = src.shape[0], src.shape[1]

    # 出力画像用の配列（要素は全て0）
    dst = np.zeros((h, w))

    for y in range(d, h - d):
        for x in range(d, w - d):
            # 畳み込み演算
            dst[y][x] = np.sum(src[y-d:y+d+1, x-d:x+d+1]*kernel)

    return dst
gray_x = filter2d(gray, kernel_x)
gray_y = filter2d(gray, kernel_y)
gray_1 = filter2d(gray, filterData1)
gray_2 = filter2d(gray, filterData2)
gray_3 = filter2d(gray, filterData3)
gray_4 = filter2d(gray, filterData4)
dst = np.sqrt(gray_1 ** 2 + gray_2 ** 2+ gray_3 ** 2+ gray_4 ** 2)
# dst=abs(gray_1)+abs(gray_2)+abs(gray_3)+abs(gray_4)
# dst=abs(gray_1+gray_2+gray_3+gray_4)
# dst=gray_x+gray_y


gray_7 = filter2d(gray, filterData7)
# dst = np.sqrt(gray_7 ** 2)


# output
# 結果を出力
cv2.imwrite(outputPath, dst)
print('done')