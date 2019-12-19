from socket import *
from ..models import Estatus, Systemconnect, Eplanning, Transmission,session
import time


def reset():  #####清空estatus表内的日变化数据
    dataSorce = session.query(Estatus).filter().all()
    for i in range(len(dataSorce)):
        dataSorce[i].run = 0
        dataSorce[i].pause = 0
        dataSorce[i].error = 0
        dataSorce[i].offline = 0
        dataSorce[i].finished = 0
    session.commit()