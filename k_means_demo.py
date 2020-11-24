from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans

#サンプルを定義
a = [0.0,0.0,0.0]
b = [0.1,0.1,0.1]
c = [1.0,1.0,1.0]
d = [0.9,0.8,0.7]
e = [1.0,0.0,0.0]
f = [0.9,0.1,0.1]
dots=np.random.randn(100, 3)

# dots = np.array([a,b,c,d,e,f,g,h,i])

X = dots[:,0]#各サンプルのx座標
Y = dots[:,1]
Z = dots[:,2]


#初期プロットの表示
# fig = plt.figure()
# ax = Axes3D(fig)
# ax.scatter3D(X,Y,Z)
# plt.show()

#クラスタの個数
num_cluster = 3

#k-means法
km = KMeans(n_clusters=num_cluster,
            init='random',
            n_init=10,
            max_iter=300,
            tol=1e-04,
            random_state=0
            )
y_km = km.fit_predict(dots)#y_kmにクラスタの番号が保存される


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
#     # ax.scatter3D(x,y,z)
#     ax.scatter(x, y, z, s = 40, c = "green")

# plt.show()

#大量データに対応できるように改良
#クラスタ毎に分類

CLUSTER=[[[X[label_i],Y[label_i],Z[label_i]] for label_i,label in enumerate(y_km) if label==class_i] for class_i in range(num_cluster) ]
# class1=[[X[label_i],Y[label_i],Z[label_i]] for label_i,label in enumerate(y_km) if label==0]
# class2=[[X[label_i],Y[label_i],Z[label_i]] for label_i,label in enumerate(y_km) if label==1]
# class3=[[X[label_i],Y[label_i],Z[label_i]] for label_i,label in enumerate(y_km) if label==2]

# CLUSTER=[class1,class2,class3]
#グラフを描画
fig = plt.figure()
ax = Axes3D(fig)
colorList=["blue","red","green"]
for label_i,c in enumerate(CLUSTER):#各クラスタ毎に
    c=np.array(c)
    x = c[:,0]#各サンプルのx座標
    y = c[:,1]
    z = c[:,2]
    # ax.scatter(x, y, z, s = 10, c = colorList[label_i])
    ax.scatter(x, y, z, s = 10)


plt.show()