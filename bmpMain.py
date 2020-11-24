
## BMP import
#bmp structure refs : https://www.setsuki.com/hsp/ext/bmp.htm
#refs : https://www.tutimogura.com/python-bitmap-read/
import sys
import pandas as pd #for make a histgram data
import numpy as np #数値計算用
import matplotlib.pyplot as plt #グラフ描画
import csv
import itertools #配列処理用
from mpl_toolkits.mplot3d import Axes3D #3Dグラフ表示用


# import pprint
import math

#####################
#variables
#####################
filePath_input=r"C:\Users\紅林亮平\OneDrive - Shizuoka University\【静岡大学】\【大学講義】\5年生(M1)\講義\後期\火3 画像情報処理論\testPython\test5.bmp"#"/Users/kkrsky/OneDrive - Shizuoka University/【静岡大学】/【大学講義】/5年生(M1)/講義/後期/火3 画像情報処理論/testPython/demo.bmp"#"C:\dev\testPython\demo.bmp"
# filePath_input=r'/Users/kkrsky/OneDrive - Shizuoka University/【静岡大学】/【大学講義】/5年生(M1)/講義/後期/火3 画像情報処理論/testPython/demo.bmp'
# filePath_input=r'/Users/kkrsky/OneDrive - Shizuoka University/【静岡大学】/【大学講義】/5年生(M1)/講義/後期/火3 画像情報処理論/testPython/input.bmp'
# filePath_output=r'/Users/kkrsky/OneDrive - Shizuoka University/【静岡大学】/【大学講義】/5年生(M1)/講義/後期/火3 画像情報処理論/testPython/output.bmp'
filePath_output=r"C:\Users\紅林亮平\OneDrive - Shizuoka University\【静岡大学】\【大学講義】\5年生(M1)\講義\後期\火3 画像情報処理論\testPython\output.bmp"#"/Users/kkrsky/OneDrive - Shizuoka University/【静岡大学】/【大学講義】/5年生(M1)/講義/後期/火3 画像情報処理論/testPython/output.bmp"#"C:\dev\testPython\output.bmp"
class KMeans():
    def __init__(self,n_clusters=8,max_iter=300,field=[["xyz"],["xyz"],["xyz"]],bitColorVal=0,_in=0):
        #field=[["X"],["Y"],["Z"]]
        self.n_clusters=n_clusters
        self.max_iter=max_iter
        self.field=field
        self.bitColorVal=bitColorVal
        self._in=_in

        self.centerArry=None #[[x,y,z],[],...]
        self.labelList=None

        self.colorFieldLabeledArry_output=None
        self.colorField_output=None
        pass

    def start(self):
        self.init()
        self.doCalc()
        # self.createOutput_imageField_gray()
        self.createOutput_labeledArry()
        self.createOutput_imageField_filter()
        pass
    
    #init
    def init(self):
        #中心点生成
        self.initCenterPoint()
        self.field=np.array(self.field)

        #ラベルリスト初期化
        self.labelList=np.zeros(len(self.field))

    def initCenterPoint(self):
        #test
        # self.centerArry=[[100,100,100]]
        # self.centerArry=np.array([[0,0,0],[50,50,50],[100,100,100]])
        # self.centerArry=np.random.randn(self.n_clusters,3)
        self.centerArry=np.random.randint(0,255,(self.n_clusters,3))
        #random

    #calc
    def doCalc(self):
        cnt=0
        labels_prev=None
        while(cnt<self.max_iter and not (self.labelList == labels_prev).all()):
            # centerArry_prev=[v for v in self.centerArry]
            self.createLabel()
            self.calcMean()
            
            #counter
            labels_prev=self.labelList
            cnt+=1

        
        pass
 
    def calcDistance(self,xyz,center):
        xyz=np.array(xyz)
        center=np.array(center)
        return np.sum((xyz-center)**2)

    def calcMean(self):
        for label_i in range(self.n_clusters):
            self.centerArry[label_i,:]=self.field[self.labelList==label_i,:].mean(axis=0)
        pass

    def createLabel(self):
        for data_i in range(len(self.field)):
            xyz=self.field[data_i]
            distanceArry=[self.calcDistance(xyz,center) for center in self.centerArry]
            minCenter_i=np.argmin(distanceArry)
            self.labelList[data_i]=minCenter_i
        self.labelList=np.array(self.labelList,dtype="int32")
        # print("labelList",self.labelList)
        
    def createOutput_labeledArry(self):
        # self.colorFieldLabeledArry_output=np.zeros((self.n_clusters,3))
        # for label_i in range(self.n_clusters):
        #     # self.colorFieldLabeledArry_output=np.insert(self.colorFieldLabeledArry_output,label_i,[self.field[data_i] for data_i,label in enumerate(self.labelList) if label==label_i],axis=0)
        #     self.colorFieldLabeledArry_output[label_i,:]=self.field[self.labelList==label_i,:]
        # return self.colorFieldLabeledArry_output
        self.colorFieldLabeledArry_output=[[self.field[data_i] for data_i,label in enumerate(self.labelList) if label==label_i] for label_i in range(self.n_clusters)]
        # return self.colorFieldLabeledArry_output
    def createOutput_imageField_gray(self):
        # grayColorList=[204]*(self.n_clusters)
        grayColorList=list(range(0,256,math.floor(255/(self.n_clusters-1))))
        output=[[grayColorList[label_i]]*3  for label_i in self.labelList]
        output=np.array(output)
        self.colorField_output=output.flatten().tolist()
    def createOutput_imageField_filter(self):
        labelList2D=None
        labelList=None

        def convolution(imageData2D,filterArry):
            #filterは3x3の配列
            colMax=len(imageData2D)
            rowMax=len(imageData2D[0])
            colMax_i=colMax-1
            rowMax_i=rowMax-1

            imageData2D_out=[[0 for rowItem in col] for col in imageData2D]
            for col_i in range(1,colMax-1):
                for row_i in range(1,rowMax-1):

                    #filter
                    for col_i_fil in range(-1,2):
                        for row_i_fil in range(-1,2):
                            imageData2D_out[col_i][row_i]+=filterArry[col_i_fil+1][row_i_fil+1]*imageData2D[col_i+col_i_fil][row_i+row_i_fil]
            return imageData2D_out
        def conbineArry(*args):
            args=list(args)
            argsLen=len(args)
            output=None
            maxItem_i=None
            maxItem=None
            #前提：argsは同じ配列の長さ
            for i in range(argsLen):
                args[i]=np.array([[rowItem**2 for rowItem in col] for col in args[i]])
                
            output=args[0]
            for i in range(1,argsLen):
                output+=args[i]
            output=np.sqrt(output)
            output=[[255 if rowItem>0 else rowItem for rowItem in col] for col in output]
            return output
            pass
        filterArry=[[0,0,0],[0,-1,1],[0,0,0]]
        # labelList=[[v]*self.bitColorVal for v in self.labelList]
        labelList=self.labelList[:]
        labelList=[255 if(labelList[i]==labelList[i-1]) else 0 for i in range(1,len(labelList))]

        # for i in range(1,len(labelList)):
        #     if(labelList[i]==labelList[i-1]):
        #         labelList[i]=255
        #     else{
        #         labelList[i]=0
        #     }

        #     # if()
        #     # for center in self.centerArry:


        # labelList=np.array(labelList)
        # labelList=labelList.flatten().tolist()
        # labelList2D=self.makeImage2D(labelList)
        # labelList2D=convolution(labelList2D,filterArry)
        # labelList2D=conbineArry(labelList2D)
        # labelList2D=np.array(labelList2D)
        # labelList2D=labelList2D.flatten()
        out=self.color2grayscallRegain(labelList)
        self.colorField_output=out
    def getResult_labeledArry(self):
        return self.colorFieldLabeledArry_output
    def gerResult_imageField(self):
        return self.colorField_output
    
    #utils
    def makeImage2D(self,imageData_int):
        

        bcHeight=self._in["bcHeight"]
        bcWidth=self._in["bcWidth"]
        # def convert_1d_to_2d(l, cols):
        #     return [l[i:i + cols] for i in range(0, len(l), cols)]
        # out=convert_1d_to_2d(imageData_int,bcWidth*self.bitColorVal)
        
        # imageData_int=np.array(imageData_int)
        # # out=imageData_int.reshape(bcHeight,-1)
        # out=imageData_int.reshape(-1,bcWidth)

        out=[imageData_int[i:i+bcWidth] for i in range(0,len(imageData_int),bcWidth) if(i%bcWidth==0 and i!=0)]
        
        
        print("convert [imageData] to [imageData2D] height:",len(out),"width:",len(out[0]))
        return out
    
    def color2grayscallRegain(self,gray_compressed):
        BIT_COROR=None
        result=list()


        
        result=[[v]*self.bitColorVal for v in gray_compressed]
        result=np.array(result)
        result=result.flatten().tolist()

        # print('result',result)
        return result
    #全点から、中心からの距離で最小となる点を抽出、ラベリング
    #ー＞indexで走査

    #ラベリングしたクラスターのx,y,zの平均値を出して中心点を移動させる

    #
    



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
        
        if(self.is24bitColor):
            #24bit color
            # self.binarization24()
            # self.linerGrayLevelTransformation(24)
            # self.color2grayscall2(24)
            # self.edgeFeatureExtraction2(24)
            # self.KMeans_Lib(24)
            self.ImageSegmentation(24)


            # imageData=[int(v) for v in self.outputImageData]
            # tes=self.color2grayscallCompress2(imageData,24)
            # self.outputImageData=bytes(self.color2grayscallRegain(tes,24))

            pass
        elif(self.is32bitColor):
            #32bit color
            # self.binarization32()
            # self.linerGrayLevelTransformation(32)
            # self.color2grayscall2(32)
            # self.edgeFeatureExtraction2(32)
            # self.KMeans_Lib(32)
            self.ImageSegmentation(32)


            pass
        else:
            print("error: bitColor state is incorrect")

        imageData=[int(v) for v in self.outputImageData]
        self.makePixcelFrequency(imageData)

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
        # plot_x=list()
        # plot_y=list()
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
        # flg=10  # 凡例のフォントサイズ
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
    def color2grayscall2(self,bitType):
        BIT_COROR=None
        result=list()
        sumPixcel=None
        bcWidth=self._in["bcWidth"]
        if(bitType==32):
            BIT_COROR=4
        elif(bitType==24):
            BIT_COROR=3

        imageData_int=[int(v) for v in self.outputImageData]
        # def convert_1d_to_2d(l, cols):
        #     return [l[i:i + cols] for i in range(0, len(l), cols)]

        # imageData_arry=convert_1d_to_2d(imageData_int,bcWidth*BIT_COROR)
        # imageData_arry=np.array(imageData_arry)
        # # print(len(imageData_arry),len(imageData_arry[0]))
        # imageData_arry2=[]
        # for i in range(len(imageData_arry)):
        #     # arr=np.sum(imageData_arry[i])/3
        #     imageData_arry2.append(convert_1d_to_2d(imageData_arry[i],BIT_COROR))
        #     # tes[i]=convert_1d_to_2d(imageData_arry[i],BIT_COROR)
        # # print(imageData_arry2[0][0])
        # imageData_arry2=np.array(imageData_arry2)
        # for height in imageData_arry2:
        #     for width in height:
        #         sumItem=0
        #         for item in width:
        #             sumItem+=item
        #         insItem=sumItem/3
        #         for i in range(len(width)):
        #             # item=insItem
        #             width[i]=insItem
        #             if(BIT_COROR==4 and i%(BIT_COROR-1)==0 and i!=0):
        #                 width[i]=0

        # for height in imageData_arry2:
        #     for width in height:
        #         width.flatten()
        #     height.flatten()

        # # print(imageData_arry2[1][1])
        # imageData_arry=imageData_arry2.flatten()
        # imageData_arry.tolist()

        # print(len(imageData_arry),imageData_arry[:10])
        # print(len(tes),len(tes[0]),len(tes[0][0]))
        print('ren',len(imageData_int))
        result=[255 for v in range(len(imageData_int))]
        sumPixcel=0
        for i in range(len(imageData_int)):
            # if(i==0):
            #     sumPixcel+=imageData_int[i]
            if(i%(BIT_COROR)==0 and i!=0):

                ratio=sumPixcel/(255*3)
                grayPixcel=math.floor(255*ratio)
                
                # result.append(grayPixcel)
                # result.append(grayPixcel)
                # result.append(grayPixcel)
                if(bitType==24):
                    result[i-2]=grayPixcel
                    result[i-1]=grayPixcel
                    result[i]=grayPixcel
                if(bitType==32):
                    # result.append(0)
                    result[i-3]=grayPixcel
                    result[i-2]=grayPixcel
                    result[i-1]=grayPixcel
                    result[i]=grayPixcel


                # if(i<10):
                #     print(i-3,i-2,i-1,i)


                sumPixcel=0
                sumPixcel+=imageData_int[i]

                
            else:
                sumPixcel+=imageData_int[i]

            # if(i==len(imageData_int)-5):
            #     # print('gray',len(result))

        
        # print('gray',len(result))
        self.outputImageData=bytes(result)
        # return resultresult
    def color2grayscallCompress(self,imageData_int,bitType):
        BIT_COROR=None
        result=list()
        sumPixcel=None

        if(bitType==32):
            BIT_COROR=4
        elif(bitType==24):
            BIT_COROR=3

        X4=[v for i,v in enumerate(imageData_int) if(i!=0 and i%BIT_COROR==0)]
        
        
        sumPixcel=0
        for i in range(len(imageData_int)):
            if(i==0):
                sumPixcel+=imageData_int[i]
            elif(i%BIT_COROR==0):
                
                ratio=sumPixcel/(255*3)
                grayPixcel=round(255*ratio)
                result.append(grayPixcel)
                # result.append(grayPixcel)
                # result.append(grayPixcel)
                # if(bitType==32):
                #     result.append(0)

                sumPixcel=0
                sumPixcel+=imageData_int[i]
            else:
                sumPixcel+=imageData_int[i]
        # print('gray compressed',result)
        return result
        return X4
    def color2grayscallCompress2(self,imageData_int,bitType):
        res=list()
        for i in range(len(imageData_int)):
            if(i==0):
                pass
            elif(i%bitType==0):
                res.append(imageData_int[i])
        return res
    def color2grayscallRegain(self,gray_compressed,bitType):
        BIT_COROR=None
        result=list()

        if(bitType==32):
            BIT_COROR=4
        elif(bitType==24):
            BIT_COROR=3
        
        result=[[v]*BIT_COROR for v in gray_compressed]
        result=np.array(result)
        result=result.flatten().tolist()

        # print('result',result)
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
    def edgeFeatureExtraction2(self,bitColor):
        outputImageData_int=None
        resultImageData_int=None
        imageData2D=None
        imageLength=None
        calWidth=None
        bitColorVal=None
        bcHeight=self._in["bcHeight"]
        bcWidth=self._in["bcWidth"]
        if(bitColor==32):
            bitColorVal=4
        elif(bitColor==24):
            bitColorVal=3
            
        def convolution(imageData2D,filterArry):
            #filterは3x3の配列
            colMax=len(imageData2D)
            rowMax=len(imageData2D[0])
            colMax_i=colMax-1
            rowMax_i=rowMax-1
            # arr=[len(imageData2D[i]) for i in range(colMax)]
            # print(arr)

            imageData2D_out=[[0 for rowItem in col] for col in imageData2D]
            # print('imageData2D_out',imageData2D_out[0])
            
            # for col_i in range(0,colMax):
            #     for row_i in range(0,rowMax):
            for col_i in range(1,colMax-1):
                for row_i in range(1,rowMax-1):

                    #filter
                    for col_i_fil in range(-1,2):
                        for row_i_fil in range(-1,2):
                            # col_i_fil_main=col_i_fil
                            # row_i_fil_main=row_i_fil
                            # if row_i==0 and row_i_fil==-1:
                            #     #左部のはみ出している部分
                            #     row_i_fil_main=0
                            # if col_i==0 and col_i_fil==-1:
                            #     #上部のはみ出している部分
                            #     col_i_fil_main=0
                            
                            # if row_i==rowMax_i and row_i_fil==1:
                            #     #右部のはみ出している部分
                            #     row_i_fil_main=0
                            # if col_i==colMax_i and col_i_fil==1:
                            #     #下部のはみ出している部分
                            #     col_i_fil_main=0

                            #col,row: 148 199 fill: 1 1 ref: 149 200
                            # print('col,row:',col_i,row_i,'fill:',col_i_fil,row_i_fil,'ref:',col_i+col_i_fil,row_i+row_i_fil)
                            # imageData2D_out[col_i][row_i]+=filterArry[col_i_fil+1][row_i_fil+1]*imageData2D[col_i+col_i_fil_main][row_i+row_i_fil_main]
                            imageData2D_out[col_i][row_i]+=filterArry[col_i_fil+1][row_i_fil+1]*imageData2D[col_i+col_i_fil][row_i+row_i_fil]
          
            # for col_i in range(1,colMax-1):
            #     for row_i in range(1,rowMax-1):

            #         #filter
            #         for col_i_fil in range(-1,2):
            #             for row_i_fil in range(-1,2):
            #                 # pass
            #                 imageData2D_out[col_i][row_i]+=filterArry[col_i_fil+1][row_i_fil+1]*imageData2D[col_i+col_i_fil][row_i+row_i_fil]
            return imageData2D_out
        def conbineArry(*args):
            args=list(args)
            argsLen=len(args)
            output=None
            maxItem_i=None
            maxItem=None
            #前提：argsは同じ配列の長さ
            for i in range(argsLen):
                # args[i]=np.array([[abs(rowItem) for rowItem in col] for col in args[i]])
                args[i]=np.array([[rowItem**2 for rowItem in col] for col in args[i]])
                
            output=args[0]
            for i in range(1,argsLen):
                output+=args[i]

            output=np.sqrt(output)

            maxItem_i=np.argmax(output)
            maxItem=output.flatten()[maxItem_i]
            # if maxItem>255*1.5:
            #     maxItem*=0.5
            #     output=(output/maxItem)*255
            maxItem*=0.5
            output=(output/maxItem)*255
            output=output.tolist()
            output=[[255 if rowItem>255 else round(rowItem) for rowItem in col] for col in output]
            return output
            
            # print(output)
        def filter_Krish(imageData2D):
            #Krish operator
            filterData1=[[-1,0,1]]*3
            filterData2=[[1,1,1],[0,0,0],[-1,-1,-1]]
            filterData3=[[0,1,1],[-1,0,1],[-1,-1,0]]
            filterData4=[[1,1,0],[1,0,-1],[0,-1,-1]]

            filterData1_res=convolution(imageData2D,filterData1)
            filterData2_res=convolution(imageData2D,filterData2)
            filterData3_res=convolution(imageData2D,filterData3)
            filterData4_res=convolution(imageData2D,filterData4)

            output=conbineArry(filterData1_res,filterData2_res,filterData3_res,filterData4_res)
            # print(filterData1_res[5])
            # print(tes)
            return output
        def filter_Sobel(imageData2D):
            #Sobel operator
            filterData5=[[-1,0,1],[-2,0,2],[-1,0,1]]
            filterData6=[[-1,-2,-1],[0,0,0],[1,2,1]]

            filterData5_res=convolution(imageData2D,filterData5)
            filterData6_res=convolution(imageData2D,filterData6)

            output=conbineArry(filterData5_res,filterData6_res)
            return output
        def filter_Laplacian(imageData2D):
            #Laplacian operator
            filterData7=[[0,1,0],[1,-4,1],[0,1,0]]

            filterData7_res=convolution(imageData2D,filterData7)
            output=conbineArry(filterData7_res)

            return output
        def filter_test(imageData2D):
            #Laplacian operator
            # filterData7=[[1,1,1],[1,0,1],[1,1,1]]
            # filterData7=np.array([[0,0,0],[0,1,0],[0,0,0]])
            # filterData7=np.array([[1,1,1],[1,0,1],[1,1,1]])/9
            filterData7=[
                [1,0,-1],
                [2,0,-2],
                [1,0,-1]
                ]
            filterData8=[
                [1,2,1],
                [0,1,0],
                [-1,-2,-1]
                ]
            # filterData8=[[0,0,-1],[0,1,0],[-1,0,0]]
            filterData7_res=convolution(imageData2D,filterData7)
            filterData8_res=convolution(imageData2D,filterData8)
            output=conbineArry(filterData7_res,filterData8_res)

            return output
        def filter_test2(imageData2D):
            
            #Laplacian operator
            # filterData7=[[1,1,1],[1,0,1],[1,1,1]]
            filterData7=np.array([[0,0,0],[0,5,0],[0,0,0]])
            # filterData7=np.array([[1,1,1],[1,1,1],[1,1,1]])/20
            # filterData8=[[0,0,-1],[0,1,0],[-1,0,0]]

            imageData2D=convolution(imageData2D,filterData7)
            # imageData2D=convolution(imageData2D,filterData8)
            output=conbineArry(imageData2D)

            return output
        def filter_move(imageData2D,*,mx=0,my=0,bitColorVal=0,isInit=False):
            if(isInit==False or isInit==None):
                mx*=bitColorVal
            if(mx==0 and my==0):
                return imageData2D
            else:
                print('loop',mx,my)
                if(mx!=0):
                    if(mx<0):
                        mx=abs(mx)
                        filterData=[[0,0,0],[0,0,1],[0,0,0]]
                    else:
                        filterData=[[0,0,0],[1,0,0],[0,0,0]]
                    imageData2D=convolution(imageData2D,filterData)
                    mx-=1
                    # imageData2D=conbineArry(filterData_res)
                
                if(my!=0):
                    if(my<0):
                        my=abs(my)
                        filterData=[[0,0,0],[0,0,0],[0,1,0]]
                    else:
                        filterData=[[0,1,0],[0,0,0],[0,0,0]]
                    imageData2D=convolution(imageData2D,filterData)
                    my-=1
                    # output=conbineArry(filterData1_res)
                # filterData=[[1,0,mx],[0,1,my],[0,0,1]]
                # filterData1=[[0,-1,0],[-1,5,-1],[0,-1,0]]
                # filterData1=[[0,0,0],[0,0,1],[0,0,0]]
                # filterData2=[[0,0,0],[0,0,1],[0,0,0]]
                # filterData3=[[0,0,0],[0,0,1],[0,0,0]]
                # filterData4=[[0,0,0],[0,0,1],[0,0,0]]
                # filterData2_res=convolution(imageData2D,filterData2)
                # filterData3_res=convolution(imageData2D,filterData3)
                # filterData4_res=convolution(imageData2D,filterData4)
                # output=conbineArry(filterData1_res,filterData2_res,filterData3_res,filterData4_res)
                # output=conbineArry(filterData1_res,filterData2_res,filterData3_res)
                # output=conbineArry(filterData1_res)
            return filter_move(imageData2D,mx=mx,my=my,isInit=True)
        
        outputImageData_int=[int(v) for v in self.outputImageData]
        imageLength=len(outputImageData_int)

        #データチェック
        
        calWidth=imageLength/bitColorVal/bcHeight
        calWidth=int(calWidth)

        if(bcWidth==calWidth):
            pass
        else:
            print("error: not same bcWidth and calWidth")
            print("bcWidth:",bcWidth,"calWidth:",calWidth)
            # calWidth=math.floor(calWidth)
            calWidth=bcWidth

        #データ二次元配列化
        # imageData2D=[[outputImageData_int[(height_i+1)*(width_i+1)] for width_i in range(calWidth)] for height_i in range(bcHeight)]
        imageData2D=[]
        # start_i=0
        # end_i=0
        # counter=0
        def convert_1d_to_2d(l, cols):
            return [l[i:i + cols] for i in range(0, len(l), cols)]
        # def convert_1d_to_2d_rows(l, rows):
        #     return convert_1d_to_2d(l, len(l) // rows)
        imageData2D=convert_1d_to_2d(outputImageData_int,bcWidth*bitColorVal)



        #二次元データ処理
        print("データ総数:",len(outputImageData_int),"height:",len(imageData2D),"width:",len(imageData2D[1]),len(imageData2D[149]))

        # imageData2D=filter_Krish(imageData2D)
        # imageData2D=filter_Krish2(imageData2D)
        # imageData2D=filter_Sobel(imageData2D)
        # imageData2D=filter_Sobel2(imageData2D)
        # imageData2D=filter_Laplacian(imageData2D)
        imageData2D=filter_test(imageData2D)
        # imageData2D=filter_Sobel(imageData2D)
        # imageData2D=filter_test(imageData2D)
    
        #二次元データから元のデータへ復元
        resultImageData_int=list(itertools.chain.from_iterable(imageData2D))

        self.outputImageData=bytes(resultImageData_int)
        pass
    def ImageSegmentation(self,bitColor):
        #三次元マップ
        #k-means法(ラベリング)
        #エッジ抽出
        colorField=None
        imageData_int=None
        bcHeight=self._in["bcHeight"]
        bcWidth=self._in["bcWidth"]
        if(bitColor==32):
            bitColorVal=4
        elif(bitColor==24):
            bitColorVal=3

        imageData_int=[int(v) for v in self.outputImageData]
        colorField=self.makeColorField(imageData_int,bitColor)
        # field=[[0,100,200],[0,100,200],[0,100,200]]
        # field=[[0,0,0],[25,25,25],[100,100,100],[75,75,75],[200,200,200]]
        # colorField=np.floor(np.random.randn(100,3)*100)
        # field=(np.array(range(260440*3))/100).reshape(-1,3)
        # field=(np.array(range(1000*3))/100).reshape(-1,3)
        # print(len(field))
        # print(field[:5])
        # print(len(colorField),len(colorField[-1:]))
        km=KMeans(n_clusters=8,max_iter=300,field=colorField,bitColorVal=bitColorVal,_in=self._in)
        km.start()
        colorFieldArry=km.getResult_labeledArry()
        imageData_int=km.gerResult_imageField()
        self.outputImageData=bytes(imageData_int)
        # print("tes",tes)
        self.makeColorFieldGraph(colorFieldArry)
    
    def makeImage2D(self,imageData_int,bitColor):
        bitColorVal=None

        bcHeight=self._in["bcHeight"]
        bcWidth=self._in["bcWidth"]
        if(bitColor==24):
            bitColorVal=3
        elif(bitColor==32):
            bitColorVal=4
        
        imageData_int=np.array(imageData_int)
        out=imageData_int.reshape(-1,bcWidth*bitColorVal)
        print("convert [imageData] to [imageData2D] height:",len(out),"width:",len(out[0]))
        return out

    def makeColorField(self,imageData_int,bitColor):
        #imageData [data,data,...]
        # to 
        #colorField[pixcel_i][RGB]
        if(bitColor==32):
            del imageData_int[3::4]

       
        imageData_int=np.array(imageData_int)
        try:
            imageData_int=imageData_int.reshape(-1,3)
        except ValueError:
            print(ValueError,"use instate of np. reshape")
            imageData_int=[imageData_int[i:i+3] for i in range(0,len(imageData_int),3) if(i%3==0 and i!=0)]



        return imageData_int
    def makeColorFieldGraph(self,colorFieldArry):
        #colorFieldArry[[[pixcel_i][RGB]],...]
        #グラフを描画
        # CLUSTER=[[[X[label_i],Y[label_i],Z[label_i]] for label_i,label in enumerate(y_km) if label==class_i] for class_i in range(num_cluster) ]
        fig = plt.figure()
        ax = Axes3D(fig) 
        # ax.set_xlim(0,255)
        # ax.set_ylim(0,255)
        # ax.set_zlim(0,255)
        for data in colorFieldArry:#各クラスタ毎に
            # data=np.array(data)
            # tes=np.vsplit(data)
            x=[v[0] for v in data]#各サンプルのx座標
            y=[v[1] for v in data]
            z=[v[2] for v in data]

            ax.scatter(x, y, z, s = 10)
        plt.show()



    def KMeans_Lib(self,bitColor):
        from sklearn.cluster import KMeans
        from mpl_toolkits.mplot3d import Axes3D


        bitColorVal=None
        bcHeight=self._in["bcHeight"]
        bcWidth=self._in["bcWidth"]
        if(bitColor==32):
            bitColorVal=4
        elif(bitColor==24):
            bitColorVal=3

        outputImageData_int=[int(v) for v in self.outputImageData]
        imageLength=len(outputImageData_int)
        # print(imageLength)
        #データチェック
        
        calWidth=imageLength/bitColorVal/bcHeight
        calWidth=int(calWidth)

        if(bcWidth==calWidth):
            pass
        else:
            print("error: not same bcWidth and calWidth")
            print("bcWidth:",bcWidth,"calWidth:",calWidth)
            # calWidth=math.floor(calWidth)
            calWidth=bcWidth

        #データ二次元配列化
        # imageData2D=[[outputImageData_int[(height_i+1)*(width_i+1)] for width_i in range(calWidth)] for height_i in range(bcHeight)]
        imageData2D=[]
        # start_i=0
        # end_i=0
        # counter=0
        def convert_1d_to_2d(l, cols):
            return [l[i:i + cols] for i in range(0, len(l), cols)]
        # def convert_1d_to_2d_rows(l, rows):
        #     return convert_1d_to_2d(l, len(l) // rows)
        outputImageData_int=np.array(outputImageData_int)
        # imageData2D=convert_1d_to_2d(outputImageData_int,bitColorVal)
        imageData2D=outputImageData_int.reshape(-1,bitColorVal)
        dots = imageData2D
        # outputImageData_int=self.color2grayscallRegain(X,bitColor)
        # outputImageData_int2=imageData2D.flatten().tolist()
        # self.outputImageData=bytes(outputImageData_int2)
        X5=list()
        for i in range(len(outputImageData_int)):
            if(i==0):
                pass
            elif(i%bitColorVal==0):
                X5.append(outputImageData_int[i])
             
            
        X4=[v for i,v in enumerate(outputImageData_int) if(i!=0 and i%bitColorVal==0)]
        print(len(X4))
        X3=[line[0] for line in dots]
        X = dots[:,0]#各サンプルのx座標
        Y = dots[:,1]
        Z = dots[:,2]
        gray=[int(round((X[i]+Y[i]+Z[i])/3)) for i in range(len(X))]
        # print(len(X))


        #初期プロットの表示
        # fig = plt.figure()
        # ax = Axes3D(fig)
        # ax.scatter3D(X,Y,Z)
        # plt.show()

        #クラスタの個数
        num_cluster = 8

        #k-means法
        km = KMeans(n_clusters=num_cluster,
                    init='k-means++',
                    n_init=10,
                    max_iter=600,
                    tol=1e-04,
                    random_state=0
                    )
        y_km = km.fit_predict(dots)#y_kmにクラスタの番号が保存される
        
        # #グラフを描画
        # CLUSTER=[[[X[label_i],Y[label_i],Z[label_i]] for label_i,label in enumerate(y_km) if label==class_i] for class_i in range(num_cluster) ]
        # fig = plt.figure()
        # ax = Axes3D(fig) 
        # for label_i,c in enumerate(CLUSTER):#各クラスタ毎に
        #     c=np.array(c)
        #     x = c[:,0]#各サンプルのx座標
        #     y = c[:,1]
        #     z = c[:,2]
        #     ax.scatter(x, y, z, s = 10)
        # plt.show()


        colorList=list(range(0,256,math.floor(255/(num_cluster-1))))

        X2=[colorList[label] for label in y_km]
        # for data_i,label in enumerate(km.labels_):
        # outputImageData_int=self.color2grayscallRegain(X,bitColor)
        # outputImageData_int2=imageData2D.flatten().tolist()
        # self.outputImageData=bytes(outputImageData_int2)
        outputImageData_int=self.color2grayscallRegain(gray,bitColor)
        self.outputImageData=bytes(outputImageData_int)
            
        #     X=[v for v in ]q
        # print(y_km)
        # print("aa")
        # #クラスタ毎に分類
        # CLUSTER = [[[],[],[]] for _ in range(num_cluster)]
        # for i,v in enumerate(dots):#各ベクトルに対して
        #     for j in range(len(y_km)):#分類ラベルに対して
        #         if y_km[i] == j:#分類ラベルがjだったら
        #             CLUSTER[j][0].append(v[0])#クラスタjのx座標にベクトルvのx座標を入れる
        #             CLUSTER[j][1].append(v[1])
        #             CLUSTER[j][2].append(v[2])

        # #グラフを描画
        # fig = plt.figure()
        # ax = Axes3D(fig)
        # for i,c in enumerate(CLUSTER):#各クラスタ毎に
        #     x,y,z = c[0],c[1],c[2]#x,y,z座標
        #     ax.scatter3D(x,y,z)
        # plt.show()
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
        # tes=[v*10 for v in range(5,10)]
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
        imageData_int=[int(v) for v in imageData]
        print("total size:",len(imageData_int))
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