# -*- coding: utf-8 -*-
# Distributed Computation
# Server Class
# Chen XuanHong 2017-2-10 in ZJU


import Queue
from multiprocessing.managers import BaseManager

class QueueManager(BaseManager):
    pass

def Return_job_queue():
    global Job_queue
    return Job_queue

def Return_result_queue():
    global Result_queue
    return Result_queue
Job_queue = Queue.Queue()
Result_queue = Queue.Queue()
class DC_ServerClass:
    # the ip of dc server
    IP="10.15.191.112"
    Port=5000
    Key="wocao"



    def __init__(self,pc,ip="10.15.191.112",port=5000,key="wocao",):
        self.Address=ip
        self.Port=port
        self.Key=key
        self.RemotePC=pc



    def ServerInit(self):
        QueueManager.register('get_job_queue', callable=Return_job_queue)
        QueueManager.register('get_result_queue', callable=Return_result_queue)

        manager = QueueManager(address=(self.IP, self.Port), authkey=self.Key)
        manager.start()

        self.__job = manager.get_job_queue()
        self.__result = manager.get_result_queue()

    def Put_Job(self,job):
        self.__job.put(job)

    def Put_Jobs(self,jobs):
        for job in jobs:
            self.__job.put(job)
        print "put",len(jobs),"jobs into the queue"

    def Get_Result(self):
        results=[]
        print "Waiting for remote results"
        for pc in xrange(self.RemotePC):
            results.extend(self.__result.get())
        length=len(results)
        print "%s results get"%length
        return  results



