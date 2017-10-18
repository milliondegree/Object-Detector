import numpy as np
import copy

def ReDuRects(rects):
    upset=[]
    downset=[]
    flag=False
    rects.sort(key=lambda re:re[0][0])
    seed = rects[0][0][0]
    for item in rects:
        if np.abs(seed-item[0][0])<20:
            if flag:
                downset.append(item)
            else:
                upset.append(item)
        else:
            seed=item[0][0]
            flag=True
    result=[]
    upset.sort(key=lambda re: re[0][1])
    seed1 = upset[0][0][1]
    result.append(upset[0])
    for item in upset:
        if np.abs(seed1-item[0][1])<20:
            pass
        else:
            seed1=item[0][1]
            result.append(item)
    if downset!=[]:
        downset.sort(key=lambda re: re[0][1])
        seed1 = downset[0][0][1]
        result.append(downset[0])
        for item in downset:
            if np.abs(seed1 - item[0][1]) < 20:
                pass
            else:
                seed1 = item[0][1]
                result.append(item)
    return result
if __name__ == '__main__':
    imgname="23part"
    rs=(np.load("..\\results\\result_nord_"+imgname+".npy")).tolist()
    print ReDuRects(rs)
