
## BMP import
#bmp structure refs : https://www.setsuki.com/hsp/ext/bmp.htm
#refs : https://www.tutimogura.com/python-bitmap-read/
import sys

#####################
#variables
#####################
filePath_input=r"C:\dev\testPython\input.bmp"
filePath_output=r"C:\dev\testPython\output.bmp"

def main():
    #####################
    #file import
    #####################
    try:
        fr = open(filePath_input,"rb")
        fw = open(filePath_output,"wb")
    except FileNotFoundError:
        print("error: [input.bmp] file is not found")
        sys.exit()

    #####################
    #BMP data read
    #####################
    _by={
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

    #header
    bfType          =fr.read(2) #識別文字
    bfSize          =fr.read(4) #ファイルサイズ
    bfReserved1     =fr.read(2) #予約
    bfReserved2     =fr.read(2) #予約
    bfOffBits       =fr.read(4) #ヘッダサイズ

    #info header
    bcSize          =fr.read(4) #情報サイズ
    bcWidth         =fr.read(4) #width
    bcHeight        =fr.read(4) #height
    bcPlanes        =fr.read(2) #画数(1)
    bcBitCount      =fr.read(2) #色ビット数 (256 色ビットマップ ＝ 8)
    biCompression   =fr.read(4) #圧縮方式
    biSizeImage     =fr.read(4) #圧縮サイズ
    biXPixPerMeter  =fr.read(4) #水平解像度 (96dpi ならば3780)
    biYPixPerMeter  =fr.read(4) #垂直解像度 (96dpi ならば3780)
    biClrUsed       =fr.read(4) #色数
    biCirImportant  =fr.read(4) #重要色数
    imageData       =fr.read()

    #make a variable data
    bfType_str        = bfType.decode()
    bfOffBits_int     = int.from_bytes(bfOffBits,     "little")
    bcSize_int        = int.from_bytes(bcSize,        "little")
    bcWidth_int       = int.from_bytes(bcWidth,       "little")
    bcHeight_int      = int.from_bytes(bcHeight,      "little")
    bcBitCount_int    = int.from_bytes(bcBitCount,    "little")
    biCompression_int = int.from_bytes(biCompression, "little")
    print ("(Width,Height)=(%d,%d)" % (bcWidth_int,bcHeight_int))
    
    #for edit
    _in={
        "bfType":bfType_str,
        "bfOffBits":bfOffBits_int,
        "bcSize":bcSize_int,
        "bcWidth":bcWidth_int,
        "bcHeight":bcHeight_int,
        "bcBitCount":bcBitCount_int,
        "biCompression":biCompression_int,
        }
    #print(_in)

    #check error
    if(bfType_str!="BM"):
        print("error: file is not .bmp")
        sys.exit()


    #####################
    #BMP data output
    #####################

    #_in to _out (to binary)
    _out={}
    for key in _in:
        if(key=="bfType"):
            _out[key]=_in[key].encode()
        else:
            _out[key]=_in[key].to_bytes(_by[key],"little")

    #write here
    fw.write(_out["bfType"])
    fw.write(bfSize)
    fw.write(bfReserved1)
    fw.write(bfReserved2)
    fw.write(_out["bfOffBits"])
    fw.write(_out["bcSize"])
    fw.write(_out["bcWidth"])
    fw.write(_out["bcHeight"])
    fw.write(bcPlanes)
    fw.write(_out["bcBitCount"])
    fw.write(_out["biCompression"])
    fw.write(biSizeImage)
    fw.write(biXPixPerMeter)
    fw.write(biYPixPerMeter)
    fw.write(biClrUsed)
    fw.write(biCirImportant)
    fw.write(imageData) 

    #####################
    #file close
    #####################
    fr.close()
    fw.close()

if __name__ == "__main__":
    main()