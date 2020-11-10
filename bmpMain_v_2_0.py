
## BMP import
#bmp structure refs : https://www.setsuki.com/hsp/ext/bmp.htm
#refs : https://www.tutimogura.com/python-bitmap-read/
import sys
import pandas as pd #for make a histgram data
# import numpy as np
import csv
import pprint
import math

#####################
#variables
#####################
filePath_input=r"C:\dev\testPython\tes.bmp"
filePath_output=r"C:\dev\testPython\output.bmp"
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
        
        #state
        self.is24bitColor=False
        self.is32bitVolor=False

    def setFilePath_input(self,path):
        self.filePath_input=path
    def setFilePath_output(self,path):
        self.filePath_output=path

    def start(self):
        self.initReadFile()
        self.readFileInfo()
        self.checkErorr()
        self.dataProcess()
        # self.tes2()
        self.initWriteFile()
        self.writeFileInfo()
        self.closeReadFile()
        self.closeWriteFile()
        



    #####################
    # data pocess system
    #####################
    def dataProcess(self):
        if(self.is24bitColor):
            #24bit color
            self.binarization24()
            pass
        elif(self.is32bitColor):
            #32bit color
            self.binarization32()
        else:
            print("error: bitColor state is incorrect")
    def binarization24(self):
        imageData=[int(v) for v in self.outputImageData]
        #[R,G,B,R,G,B,...]
        self.makePixcelFrequency(imageData)
        gray=self.color2grayscall(imageData,24)
        binal=self.gray2binarization(gray,50)
        self.outputImageData=bytes(binal)
    def binarization32(self):
        imageData=[int(v) for v in self.outputImageData]
        #[R,G,B,None,R,G,B,None,...]
        self.makePixcelFrequency(imageData)
        gray=self.color2grayscall(imageData,32)
        binal=self.gray2binarization(gray,50)
        self.outputImageData=bytes(binal)

    def makePixcelFrequency(self,imageData):
        
        container=pd.Series(imageData).value_counts(normalize=True)
        container.to_csv('./pixcel-frequency.csv')
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
   
    def tes(self):
        lis=list()
        tes=self.outputImageData
        for v in range(8):
            lis.append(int(tes[v]))
        print(lis)
        print(self._in["bcBitCount"])
        #tes2 = [int(v*0.5) for v in tes]
        # tes3 = bytes(tes2)
        
        # self.outputImageData=tes3
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


if __name__ == "__main__":
    main()