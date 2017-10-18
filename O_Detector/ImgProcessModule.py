import numpy as np
import copy

def CreatMask(Dmax,Dmin):
    '''Dmin:掩膜最大宽度
    Dmax:掩膜内部宽度
    '''
    if ~Dmin%2&~Dmax%2:
        print 'Dmin and Dmax must be a odd number!'
        return None
    mask=np.ones((Dmax,Dmax),np.uint8)
    inermask=np.zeros((Dmin,Dmin),np.uint8)
    delta=(Dmax-Dmin)/2
    bbb=delta+Dmin
    mask[delta:bbb,delta:bbb]=mask[delta:bbb,delta:bbb]&inermask
    return mask

def HoughTransform(args):
    'Hough Transform'
    img=args[0]
    Dmax=args[1]
    Dmin=args[2]
    rho=args[3]
    threshold=args[4]
    zone=args[5]
    Ttheta = 0.1
    Trho = 1
    Tl = 0.1
    thr=1
    Talpha=0.01
    Tlen=5500
    theta = np.pi / 180

    imgshape = img.shape
    # imgxfirst = zone[0]
    # imgxlast = zone[1]
    # imgylast = imgshape[1] - Dmax
    imgyfirst = zone[0]
    imgylast = zone[1]
    imgxlast = imgshape[0] - Dmax
    mask = CreatMask(Dmax,Dmin)
    X_tran = ((Dmax - 1) / 2)
    rhomax =X_tran
    rhostep=np.arange((Dmin - 1) / 2,rhomax+rho,rho)
    thetazone1=np.arange(0,np.pi*3/180,theta)
    thetazone2=np.arange(np.pi*87/180,np.pi*93/180,theta)
    thetazone3 = np.arange(np.pi*177/180 , np.pi * 183/180, theta)
    thetazone4 = np.arange(np.pi*267/180 , np.pi * 273/180, theta)
    thetazone5 = np.arange(np.pi*357/180 , np.pi * 2, theta)
    thetastep=np.append(thetazone1,thetazone2)
    thetastep=np.append(thetastep,thetazone3)
    thetastep = np.append(thetastep, thetazone4)
    thetastep = np.append(thetastep, thetazone5)
    # Cumtable=np.zeros((rhostep.shape[0],thetastep.shape[0]))
    costable=np.cos(thetastep)
    sintable=np.sin(thetastep)
    rhostepshape=rhostep.shape[0]
    thetastepshape=thetastep.shape[0]
    lines=[]
    Tl = Tl * 0.5
    Pk = []
    rects = []
    pi_2=np.pi/2
    print "Start finding!"
    # for t in xrange(imgxfirst,imgxlast):
    #     for l in xrange(imgylast):
    for t in xrange(imgxlast):
        for l in xrange(imgyfirst,imgylast):
            roi=img[t:t+Dmax,l:l+Dmax]
            roi=np.bitwise_and(roi,mask)
            regionmap = np.transpose(np.nonzero(roi))
            if regionmap.shape[0]<Tlen:
                continue
            coor = regionmap - X_tran
            for i in xrange(rhostepshape):
                for j in xrange(thetastepshape):
                    count=coor.dot(np.array([[costable[j]],[sintable[j]]]))
                    count=np.abs(count-rhostep[i])
                    count=count<thr
                    Cum=np.count_nonzero(count)
                    # Cumtable[i,j]=Cum
                    if Cum>threshold:
                        # lines[0]---rho  lines[1]---theta  lines[2]---Cum
                        lines.append((rhostep[i],thetastep[j],Cum))
            length1 = lines.__len__()
            ra = range(0, length1)

            while ra.__len__():
                i = ra[0]
                rb = ra[1:]
                for j in rb:
                    delta1 = np.abs(lines[i][0] - lines[j][0]) < Trho
                    delta2 = np .abs(np.abs(lines[i][1] - lines[j][1]) - np.pi) < Ttheta
                    # delta3 = np.abs(lines[i][2] - lines[i][2]) < Tl*(lines[i][2] + lines[i][2])
                    # if delta1&delta2&delta3:
                    if delta1 & delta2:
                        alpha=0.5*np.abs(lines[i][1]+lines[j][1]-np.pi)
                        xi=(lines[i][0]+lines[j][0])
                        Pk.append((alpha,xi))
                        ra.remove(j)
                ra.remove(i)
            lines=[]# clear the lines after used
            length2 = Pk.__len__()
            if length2<2:
                continue
            # recttemp=[(0,0),0,0,0]
            ra = range(0, length2)
            while ra.__len__():
                i = ra[0]
                rb = ra[1:]
                for j in rb:
                    temp = np.abs(np.abs(Pk[i][0] - Pk[j][0]) - pi_2)
                    if temp < Talpha:
                        if Pk[i][0]>Pk[j][0]:
                            rects.append(((t + X_tran, l + X_tran), Pk[j][0], Pk[i][1],Pk[j][1]))
                        else:
                            rects.append(((t + X_tran, l + X_tran), Pk[i][0], Pk[j][1], Pk[i][1]))
                        break
                        # Removing Duplicated Rectangles
                ra.remove(i)
            Pk=[]
    return rects