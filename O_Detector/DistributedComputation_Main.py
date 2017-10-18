import DC_Job
import DC_Server
import cv2
import numpy as np
import ImgProcessModule as WH
import multiprocessing as mp
from matplotlib import pyplot as plt
import RemoveRe
import FindContours as FC

if __name__ == '__main__':

    jobnumber = 60
    PCnumber = 3
    ServerCPU = mp.cpu_count()
    Dmax = 1039
    Dmin = Dmax - 38
    server = DC_Server.DC_ServerClass(PCnumber - 1, "10.15.191.112")
    server.ServerInit()#"29t","30t","31t"]#,
    # ImgName=["32t","33t","34t","35t","36t","37t","38t","39t","40t","41t","43t","44t","45t","46t"]
    # ImgName = ["16t", "17t", "18t", "19t", "20t", "21t", "22t", "23t", "24t", "25t", "26t", "27t"]
    # for name in ImgName:
    # ImgName = ["7t","7d","8t","8d","9t","9d","10t","10d","11t","11d"]
    ImgName = ["11t", "11d"]
    for name in ImgName:
        e1 = cv2.getTickCount()
        # imgname = '44d'
        imgname = name
        imagefile = '..\\..\\images\\' + imgname + ".png"
        img = cv2.imread(imagefile, 0)
        # xlength = img.shape[0] - Dmax
        ylength = img.shape[1] - Dmax
        binaryImg = FC.findcontours(img)
        # left = xlength % jobnumber
        # step = int((xlength - left) / jobnumber)
        left = ylength % jobnumber
        step = int((ylength - left) / jobnumber)
        que = range(0, left * (step + 1), step + 1)
        # que2 = range(left * (step + 1), xlength + 1, step)
        que2 = range(left * (step + 1), ylength + 1, step)
        que.extend(que2)
        zone = []
        for i in xrange(len(que) - 1):
            zone.append((que[i], que[i + 1]))

        # server = DC_Server.DC_ServerClass(PCnumber - 1, "10.15.191.112")
        # server.ServerInit()

        for i in xrange(0, len(zone) - ServerCPU):
            job = DC_Job.DC_Job_class(i)
            job.Args = [binaryImg, Dmax, Dmin, 1, 400, zone[i]]
            server.Put_Job(job)
        print len(zone) - ServerCPU, " are put into the net"
        pool = mp.Pool()
        results = []
        for i in xrange(len(zone) - ServerCPU, len(zone)):
            result = pool.apply_async(
                WH.HoughTransform, ([binaryImg, Dmax, Dmin, 1, 400, zone[i]],))
            results.append(result)
        item = []
        resultscount = 0

        for res in results:
            temp = res.get()
            if temp == []:
                continue
            item.extend(temp)
            resultscount += 1
        print "The Server process get ", resultscount, " results"
        r = server.Get_Result()
        item.extend(r)

        # store no remove duplicated rectangles
        np.save("..\\rs\\result_nord_" + imgname + ".npy", item)
        # Removing Duplicated Rectangles
        finaresult = RemoveRe.ReDuRects(item)
        print finaresult
        np.save("..\\rs\\result_" + imgname + ".npy", finaresult)

        roi = []
        yiliao = []
        for rect in finaresult:
            L = np.sqrt(np.square(rect[2] / 2) + np.square(rect[3] / 2))
            temp = np.arccos(rect[2] / (2 * L))
            D1 = rect[0][1]
            D2 = rect[0][0]
            if rect[1] > np.pi / 4:
                gamar = rect[1] - temp
                delta = temp + rect[1] - np.pi / 2
                s1 = L * np.sin(gamar)
                s2 = L * np.sin(delta)
                c1 = L * np.cos(gamar)
                c2 = L * np.cos(delta)
                A = np.round([D1 + s1, D2 + c1])
                B = np.round([D1 + c2, D2 - s2])
                C = np.round([D1 - s1, D2 - c1])
                D = np.round([D1 - c2, D2 + s2])
            else:
                gamar = temp - rect[1]
                delta = temp + rect[1]
                s1 = L * np.sin(gamar)
                s2 = L * np.sin(delta)
                c1 = L * np.cos(gamar)
                c2 = L * np.cos(delta)
                A = np.round([D1 - s1, D2 + c1])
                B = np.round([D1 + s2, D2 + c2])
                C = np.round([D1 + s1, D2 - c1])
                D = np.round([D1 - s2, D2 - c2])
            pts = np.array([A, B, C, D], np.int32)
            pts = pts.reshape((-1, 1, 2))
            img1 = np.zeros(img.shape, np.uint8)
            cv2.fillConvexPoly(img1, pts, (255, 255, 255))
            img2 = ~img1
            tempimg = np.bitwise_and(img, img1)
            tempimg = tempimg + img2
            roi.append(tempimg)
            th = cv2.adaptiveThreshold(tempimg, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 221, 1)
            a = np.nonzero(~th)
            # size = float(img.shape[0] * img.shape[1])
            size = float(15980544)
            liao = float(len(a[0]))
            yiliao.append(liao / size)

        np.save("..\\rs\\result_nord_YL" + imgname + ".npy", yiliao)
        print yiliao
        e2 = cv2.getTickCount()
        time = (e2 - e1) / cv2.getTickFrequency()
        print "The program runs for a total of ", time, " seconds"
        j = 0
        for i in roi:
            cv2.imwrite("..\\rs\\rs\\result_" + imgname + str(j) + ".png", i)
            j += 1

