import DC_worker
import cv2
import numpy as np
import ImgProcessModule as WH
import multiprocessing as mp

if __name__ == '__main__':
    worker=DC_worker.DC_WorkClass()
    worker.WorkerInit()
    # address=("10.15.191.114",5000)
    # conn=mp.Client(address,authkey='wocao')
    # while True:
    #     str=conn.recv()
    #     if str=="Start":
    worker.GetJobs()
    worker.RunWork()
