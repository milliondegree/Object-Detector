import time, sys, Queue
from multiprocessing.managers import BaseManager
import multiprocessing as mp
import ImgProcessModule as WH

class DC_WorkClass:
    def __init__(self,ip="10.15.191.114",port=5000,key="wocao"):
        self.__ServerIP=ip
        self.__Port=port
        self.__Key=key
        self.Works=[]

    def WorkerInit(self):
        BaseManager.register('get_job_queue')
        BaseManager.register('get_result_queue')

        print('Connect to server %s...' % self.__ServerIP)
        m = BaseManager(address=(self.__ServerIP, self.__Port), authkey=self.__Key)
        m.connect()
        self.__jobs = m.get_job_queue()
        self.__result = m.get_result_queue()

    def GetJobs(self):
        worknumber=mp.cpu_count()
        for i in xrange(worknumber):
            try:
                self.Works.append(self.__jobs.get(timeout=2))
            except Queue.Empty:
                print('task queue is empty.')
        print "get ",self.Works.__len__()," jobs"

    def RunWork(self):
        pool=mp.Pool()
        results=[]
        for i in self.Works:
            result = pool.apply_async(WH.HoughTransform, (i.Args,))
            results.append(result)
        item = []
        for i in results:
            temp=i.get()
            if temp==[]:
                continue
            item.extend(temp)
        self.__result.put(item)
        print "put ",item.__len__()," results into the queue"