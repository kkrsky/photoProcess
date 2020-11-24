import numpy as np

def convert_1d_to_2d(l, cols):
            return [l[i:i + cols] for i in range(0, len(l), cols)]

# arr=list(range(0,25,4))
arr=[[v]*4 for v in range(25)]
arr=np.array(arr)
arr=arr.flatten().tolist()
arr2=np.random.randn(10,2)
arr3=list(range(10))
arr4=np.array(list(range(10))).reshape(-1,5)
# arr.insert(0,-1)
lis=[1,2,3,4]
cols=2
X=[[1,2],[3,4]]
labels_=[1,2]
# del arr[3::4]


def makeColorField(imageData_int,bitColor=0):
        print(bitColor)
        #field[col][row][RGB]
        if(bitColor==32):
            bitColorVal=4
            del imageData_int[3::4]
        elif(bitColor==24):
            bitColorVal=3

       
        imageData_int=np.array(imageData_int)
        return imageData_int.reshape(-1,3)
# tes2=makeColorField(arr)
# print(tes2)
print(arr4.shape[0])

print(lis[1:2])