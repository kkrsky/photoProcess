
## BMP import
#bmp structure refs : https://www.setsuki.com/hsp/ext/bmp.htm
#refs : https://www.tutimogura.com/python-bitmap-read/
import sys
import pandas as pd #for make a histgram data
import numpy as np
import matplotlib.pyplot as plt
import csv
# import pprint
import math

#####################
#variables
#####################
filePath_input=r"C:\Users\紅林亮平\OneDrive - Shizuoka University\【静岡大学】\【大学講義】\5年生(M1)\講義\後期\火3 画像情報処理論\testPython\demo.bmp"#"/Users/kkrsky/OneDrive - Shizuoka University/【静岡大学】/【大学講義】/5年生(M1)/講義/後期/火3 画像情報処理論/testPython/demo.bmp"#"C:\dev\testPython\demo.bmp"
filePath_output=r"C:\Users\紅林亮平\OneDrive - Shizuoka University\【静岡大学】\【大学講義】\5年生(M1)\講義\後期\火3 画像情報処理論\testPython\output.bmp"#"/Users/kkrsky/OneDrive - Shizuoka University/【静岡大学】/【大学講義】/5年生(M1)/講義/後期/火3 画像情報処理論/testPython/output.bmp"#"C:\dev\testPython\output.bmp"
class FileController():
    def __init__(self):
        #setter
        self.filePath_input=None
        self.filePath_output=None

        #inner
        self.fr=None
        self.fw=None
        self._by={
            "bfType"        :2,
            "bfSize"        :4,
            "bfReserved1"   :2,
            "bfReserved2"   :2,
            "bfOffBits"     :4,
            "bcSize"        :4,
            "bcWidth"       :4,
            "bcHeight"      :4,
            "bcPlanes"      :2,
            "bcBitCount"    :2,
            "biCompression" :4,
            "biSizeImage"   :4,
            "biXPixPerMeter":4,
            "biYPixPerMeter":4,
            "biClrUsed"     :4,
            "biCirImportant":4,
            "imageData"     :None
            }
        self._all=None
        self._in=None
        self._out=None
        self.outputImageData=None
        self.plot_x=None
        self.plot_y=None
        self.plot_all=None

        
        #state
        self.is24bitColor=False
        self.is32bitVolor=False

    def setFilePath_input(self,path):
        self.filePath_input=path
    def setFilePath_output(self,path):
        self.filePath_output=path

    def test(self):
        self.tes()

    def start(self):
        self.initReadFile()
        self.readFileInfo()
        self.checkErorr()
        self.dataProcess()
        self.initWriteFile()
        self.writeFileInfo()
        self.closeReadFile()
        self.closeWriteFile()
        

        # self.tes2()

    #####################
    # data pocess system
    #####################
    def dataProcess(self):
        imageData=[int(v) for v in self.outputImageData]
        self.makePixcelFrequency(imageData)
        if(self.is24bitColor):
            #24bit color
            #self.binarization24()
            self.linerGrayLevelTransformation(24)
            
        elif(self.is32bitColor):
            #32bit color
            self.linerGrayLevelTransformation(32)
            # self.binarization32()
            pass
        else:
            print("error: bitColor state is incorrect")
    def binarization24(self):
        imageData=[int(v) for v in self.outputImageData]
        #[R,G,B,R,G,B,...]
        # self.makePixcelFrequency(imageData)
        gray=self.color2grayscall(imageData,24)
        binal=self.gray2binarization(gray,50)
        self.outputImageData=bytes(binal)
    def binarization32(self):
        imageData=[int(v) for v in self.outputImageData]
        #[R,G,B,None,R,G,B,None,...]
        # self.makePixcelFrequency(imageData)
        gray=self.color2grayscall(imageData,32)
        binal=self.gray2binarization(gray,50)
        self.outputImageData=bytes(binal)

    def initPlotAll(self,imageData_int):
        plot_x=list()
        plot_y=list()
        plotContainer=list()
        container=pd.Series(imageData_int)

        for point in container.value_counts(normalize=True).iteritems():
            plotContainer.append(point)
        plotContainer=sorted(plotContainer,key=lambda x:x[0])
        return plotContainer
        
    def makePixcelFrequency(self,imageData):
        #if(self.plot_all==None):
        plotContainer=self.initPlotAll(imageData)
        plot_x=[pl[0] for pl in plotContainer]
        plot_y=[pl[1] for pl in plotContainer]
        self.plot_all=plotContainer
        self.plot_x=plot_x
        self.plot_y=plot_y
        # container.to_csv('./pixcel-frequency.csv')

        #グラフ共通設定
        flg=10  # 凡例のフォントサイズ
        fti=20 # タイトルのフォントサイズ  

        # plt.rcParams["font.size"] = 20
        plt.rcParams['font.family'] ='sans-serif'

        #グラフ初期化
        fig = plt.figure(figsize=(8, 8))
        ax1 = fig.add_subplot(111)

        #グラフ作成
        ax1.plot(self.plot_x,self.plot_y)

        #グラフ設定
        ax1.set_title("Bit-Frequency",fontsize=fti)
        ax1.set_xlabel("Bit",fontsize=fti)
        ax1.set_ylabel("Normalized Frequency",fontsize=fti)
        ax1.set_xlim(0,255)
        ax1.set_ylim(ymin=0)
        # ax1.set_xlim(auto=True)
        # ax1.set_ylim(auto=True)

        #グラフ描画
        plt.show()
        

    def color2grayscall(self,imageData_int,bitType):
        BIT_COROR=None
        result=list()
        sumPixcel=None

        if(bitType==32):
            BIT_COROR=4
        elif(bitType==24):
            BIT_COROR=3
        
        sumPixcel=0
        for i in range(len(imageData_int)):
            if(i==0):
                sumPixcel+=imageData_int[i]
            elif(i%BIT_COROR==0):
                
                ratio=sumPixcel/(255*3)
                grayPixcel=math.floor(255*ratio)
                result.append(grayPixcel)
                result.append(grayPixcel)
                result.append(grayPixcel)
                if(bitType==32):
                    result.append(0)

                sumPixcel=0
                sumPixcel+=imageData_int[i]
            else:
                sumPixcel+=imageData_int[i]
        return result
    def gray2binarization(self,imageData,thresold):
            result=list()
            for v in imageData:
                if(v>=thresold):
                    result.append(255)
                else:
                    result.append(0)
            return result
    def linerGrayLevelTransformation(self,bitColor):
        #濃度線形変換


        plot_sorted=None
        minPlot_x=None
        maxPlot_x=None
        transferRate=None
        imageData_liner=None
        plot_all=None

        outputImageData_int=[int(v) for v in self.outputImageData]
       
        
        #濃度の最大/最小値を求める
        plot_all=self.initPlotAll(outputImageData_int)
        
        plot_sorted=sorted(plot_all,key=lambda x:x[1])
        maxPlot_x=plot_sorted[0][0]
        transferRate=255/maxPlot_x

        plot_sorted_r=sorted(self.plot_all,key=lambda x:x[1],reverse=True)
        minPlot_x=plot_sorted_r[0][0]
        print("min plot:{} max plot: {}".format(minPlot_x,maxPlot_x))

        #画像データ書き換え
        imageData_liner=[math.floor((int(v)-minPlot_x)*transferRate) for v in self.outputImageData]

        self.makePixcelFrequency(imageData_liner)
        self.outputImageData=bytes(imageData_liner)
        
        

        

    def tes(self):
        # lis=list()
        # tes=self.outputImageData
        # for v in range(8):
        #     lis.append(int(tes[v]))
        # print(lis)
        # print(self._in["bcBitCount"])
        #tes2 = [int(v*0.5) for v in tes]
        # tes3 = bytes(tes2)


        # x = np.linspace(0,10,100)
        # y = x
        # plt.plot(x,y)
        # plt.show()


        # self.outputImageData=tes3

        # ts = pd.Series(np.random.randn(1000),index=pd.date_range('1/1/2000', periods=1000))
        # ts = ts.cumsum()
        # ts.plot()
        # plt.show()

        # # データ生成
        # x = np.linspace(0, 10, 100)
        # y = x + np.random.randn(100) 

        # # Figureの初期化
        # fig = plt.figure(figsize=(10, 10)) #...1

        # # Figure内にAxesを追加()
        # ax = fig.add_subplot(111) #...2
        # # ax = fig.add_axes([0.2,0.2,0.5,0.5])
        # ax.plot(x, y, label="test") #...3

        
        # # 凡例の表示
        # plt.legend()


        # データ生成
        x = np.linspace(0, 10, 100)
        y1 = np.sin(x)
        y2 = np.cos(x)

        # プロット領域(Figure, Axes)の初期化
        fig = plt.figure(figsize=(12, 8))
        ax1 = fig.add_subplot(131)
        ax2 = fig.add_subplot(132)
        ax3 = fig.add_subplot(133)

        # 棒グラフの作成
        ax1.bar([1,2,3],[3,4,5])
        ax2.barh([0.5,1,2.5],[0,1,2])
        ax3.scatter(y1, y2)

        # 水平線、垂直線を入れる
        ax3.axhline(0.45)
        ax3.axvline(0.65)

        ax2.grid()
        ax2.set_xlabel("tesX")
        ax2.set_ylabel("tesY")
        ax2.set_xlim(0.0,5,0)
        ax2.set_ylim(0.0,6.5)

        plt.show()
    def tes2(self):
        lis=list()
        tes=[v*10 for v in range(5,10)]
        for v in range(5,10):
            lis.append(v*10)
        print(math.floor(400/(3*10)))
    
    #####################
    # file read/write system
    #####################
    
    def initReadFile(self):
        if(self.filePath_input==None):
            print("error: call setFilePath_input")
            sys.exit()
        #file read
        try:
            self.fr = open(self.filePath_input,"rb")
        except FileNotFoundError:
            print("error: [{}] file is not found".format(self.filePath_input))
            sys.exit()
        except:
            print("error")
    def readFileInfo(self):
        
        #header
        bfType          =self.fr.read(2) #識別文字
        bfSize          =self.fr.read(4) #ファイルサイズ
        bfReserved1     =self.fr.read(2) #予約
        bfReserved2     =self.fr.read(2) #予約
        bfOffBits       =self.fr.read(4) #ヘッダサイズ

        #info header
        bcSize          =self.fr.read(4) #情報サイズ
        bcWidth         =self.fr.read(4) #width
        bcHeight        =self.fr.read(4) #height
        bcPlanes        =self.fr.read(2) #画数(1)
        bcBitCount      =self.fr.read(2) #色ビット数 (256 色ビットマップ ＝ 8)
        biCompression   =self.fr.read(4) #圧縮方式
        biSizeImage     =self.fr.read(4) #圧縮サイズ
        biXPixPerMeter  =self.fr.read(4) #水平解像度 (96dpi ならば3780)
        biYPixPerMeter  =self.fr.read(4) #垂直解像度 (96dpi ならば3780)
        biClrUsed       =self.fr.read(4) #色数
        biCirImportant  =self.fr.read(4) #重要色数
        imageData       =self.fr.read()

        #make a variable data
        bfType_str        = bfType.decode()
        bfOffBits_int     = int.from_bytes(bfOffBits,     "little")
        bcSize_int        = int.from_bytes(bcSize,        "little")
        bcWidth_int       = int.from_bytes(bcWidth,       "little")
        bcHeight_int      = int.from_bytes(bcHeight,      "little")
        bcBitCount_int    = int.from_bytes(bcBitCount,    "little")
        biCompression_int = int.from_bytes(biCompression, "little")
        print ("(Width,Height)=(%d,%d)" % (bcWidth_int,bcHeight_int))
        
        self._all={
            "bfType":bfType,
            "bfSize":bfSize,
            "bfReserved1":bfReserved1,
            "bfReserved2":bfReserved2,
            "bfOffBits":bfOffBits,

            "bcSize":bcSize,
            "bcWidth":bcWidth,
            "bcHeight":bcHeight,
            "bcPlanes":bcPlanes,
            "bcBitCount":bcBitCount,
            "biCompression":biCompression,
            "biSizeImage":biSizeImage,
            "biXPixPerMeter":biXPixPerMeter,
            "biYPixPerMeter":biYPixPerMeter,
            "biClrUsed":biClrUsed,
            "biCirImportant":biCirImportant,
            
        }
        self.outputImageData=imageData
        
        #for edit
        self._in={
            "bfType":bfType_str,
            "bfOffBits":bfOffBits_int,
            "bcSize":bcSize_int,
            "bcWidth":bcWidth_int,
            "bcHeight":bcHeight_int,
            "bcBitCount":bcBitCount_int,
            "biCompression":biCompression_int,
            }
        self.printDectional(self._in)
        #print(_in)  
    def initWriteFile(self):
        #file read
        if(self.filePath_output==None):
            print("error: call setFilePath_output")
            sys.exit()
        self.fw = open(self.filePath_output,"wb")   
    def writeFileInfo(self):
        
        #_in to _out (to binary)
        self._out={}
        for key in self._in:
            if(key=="bfType"):
                self._out[key]=self._in[key].encode()
            else:
                self._out[key]=self.int2Bytes(self._in[key],self._by[key])
        
        #write here
        self.fw.write(self._out["bfType"])
        self.fw.write(self._all["bfSize"])
        self.fw.write(self._all["bfReserved1"])
        self.fw.write(self._all["bfReserved2"])
        self.fw.write(self._out["bfOffBits"])
        self.fw.write(self._out["bcSize"])
        self.fw.write(self._out["bcWidth"])
        self.fw.write(self._out["bcHeight"])
        self.fw.write(self._all["bcPlanes"])
        self.fw.write(self._out["bcBitCount"])
        self.fw.write(self._out["biCompression"])
        self.fw.write(self._all["biSizeImage"])
        self.fw.write(self._all["biXPixPerMeter"])
        self.fw.write(self._all["biYPixPerMeter"])
        self.fw.write(self._all["biClrUsed"])
        self.fw.write(self._all["biCirImportant"])
        self.fw.write(self.outputImageData)
    def closeReadFile(self):
        self.fr.close()
    def closeWriteFile(self):
        self.fw.close()
    def checkErorr(self):
        #check error
        if(self._in["bfType"] != "BM"):
            print("error: file is not .bmp")
            sys.exit()
        if(self._in["bcBitCount"] == 24):
            self.is24bitColor=True
        elif(self._in["bcBitCount"] == 32):
            self.is32bitColor=True
        else:
            print("error: bcBitCount must be 24 or 32")
            sys.exit()
    
    #####################
    #util
    #####################
    def int2Bytes(self,intVal,length):
        return intVal.to_bytes(length,"little")
    def printDectional(self,dicts):
        for dic in dicts:
            print("{} : {}".format(dic,dicts[dic]))


def main():
    FC=FileController()
    FC.setFilePath_input(filePath_input)
    FC.setFilePath_output(filePath_output)
    FC.start()
    # FC.test()


if __name__ == "__main__":
    main()