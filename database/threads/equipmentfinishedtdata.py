from socket import *
from ..models import Estatus, Systemconnect, Eplanning, Transmission, session

import time



##从数据库获取设备ip
def getip(eid):
    dataSorce = session.query(Systemconnect).filter(Systemconnect.eid == eid).first()
    return dataSorce.ip

###从数据库获取监测状态
def getstatus(eid):
    dataSorce = session.query(Systemconnect).filter(Systemconnect.eid == eid).first()
    return dataSorce.status


    
####开启线程，id为对应设备号
def equipmentfinisheddata(id):
    #### 程序执行段
    formalstatus = 5  ### 初始状态
    start_time = time.perf_counter()  ##### 开始计时
    PORT = 62937
    BUFSIZE = 2048
    while True:
        findfinished = 0  ###加工完成状态检测
        HOST = getip(id)
        ADDR = (HOST, PORT)
        tcpCliSock = socket(AF_INET, SOCK_STREAM)
        try:
            tcpCliSock.connect(ADDR)
            cmd = '<blocks><auto>yes</auto><req>yes</req><sub>servo</sub></blocks>\n<ncda><req>yes</req><auto>yes</auto><st>nc1</st><var>ncstate</var></ncda>\n<alarm><req>yes</req><auto>yes</auto><st>nc1</st></alarm>\n'  # 程序段请求
            tcpCliSock.send(cmd.encode())
            dataSorce_c = session.query(Systemconnect).filter(Systemconnect.eid == id).first()
            dataSorce_c.connection = 1
            session.commit()
            global flag
            flag =getstatus(id)
            while flag:
                if getstatus(id) != 1 or getip(id) != HOST:
                    dataSorce_e = session.query(Estatus).filter(Estatus.eid == id).first()
                    dataSorce_e.estatus = 3
                    dataSorce_e.mstatus = 3 ###机械手和设备状态设为离线
                    end_time = time.perf_counter()
                    status_time = round((end_time - start_time) * 1000, 0) #####时间记录
                    if formalstatus == 0:
                        dataSorce_e.run += status_time
                    elif  formalstatus == 2:
                        dataSorce_e.error += status_time
                    elif formalstatus == 1:
                        dataSorce_e.pause += status_time
                    elif formalstatus == 5:
                        dataSorce_e.offline += status_time
                    session.commit()
                    tcpCliSock.close()
                    ### 不监测时状态设置为离线
                    formalstatus = 5
                    start_time = end_time
                    print('取消监测')
                    break  #### 如果设备ip变化或者检测状态设置为关闭 跳出该循环监测设备状态和ip
                xml_data = tcpCliSock.recv(BUFSIZE).decode('gb2312')
                session.commit()
                #### 监测加工量并对数据库进行操作
                if xml_data .find('<block7>') != -1:
                    currentblockdata = xml_data[xml_data.find('<block7>') + 9: xml_data.find('</block7>')]
                    if currentblockdata.find('M30') != -1:
                        dataSorce_p = session.query(Eplanning).filter(Eplanning.eid == id).filter(Eplanning.status == 1).first()###计划任务表
                        dataSorce_p.finished += 1
                        dataSorce_e = session.query(Estatus).filter(Estatus.eid == id).first()
                        dataSorce_e.finished += 1
                        dataSorce_t = session.query(Transmission).filter(Transmission.eid == id).first() ####物料配送表
                        dataSorce_t.remain = dataSorce_p.order - dataSorce_p.finished ###剩余加工量写入
                        dataSorce_t.material -= 1         ####剩余棒料-1
                        findfinished = 1  ####监测完成标记为1
                        session.commit() ###上传更新数据库
                        print('加工完成量+1')
                #####设备报警监测，不知是否需要，需要还要对数据库操作
                if xml_data.find('<prio>') != -1:
                    timedata = xml_data[xml_data.find('<tm>')+4: xml_data.find('</tm>')]####报警时间，世纪秒
                    priority = xml_data[xml_data.find('<prio>')+6: xml_data.find('</prio>')]#####报警优先级
                    errorid = xml_data[xml_data.find('<no>')+4: xml_data.find('</no>')]#####报警号
            ####设备状态计数及设备状态记录
                ###状态时间记录
                if xml_data.find('<ncstate>') != -1:
                    currentstatus = int(xml_data[xml_data.find('<ncstate>') + 9:xml_data.find('</ncstate>')])
                    if currentstatus != formalstatus:
                        datebase_time = session.query(Estatus).filter(Estatus.eid == id).first() ####查找设备状态对应数据
                        end_time = time.perf_counter()
                        status_time = round((end_time - start_time) * 1000, 0)
                        if formalstatus <= 1:
                            if currentstatus == 0 and findfinished == 1:
                                datebase_time.mstatus = 0 ###机械状态设为运行
                                findfinished = 0  #####完成量标记设为0
                            elif currentstatus == 1:
                                datebase_time.mstatus = 1 #####机械手状态设置为待机
                            datebase_time.run += status_time
                        elif 2 <= formalstatus <= 3:
                            datebase_time.error += status_time
                        elif formalstatus == 4:
                            datebase_time.pause += status_time
                        elif formalstatus == 5:
                            datebase_time.offline += status_time
                        start_time = end_time
                        formalstatus = currentstatus
                        if formalstatus <= 1:
                            datebase_time.estatus = 0
                        elif 2 <= formalstatus <= 3:
                            datebase_time.mstatus = 2  #####机械手状态设置为待机
                            datebase_time.estatus = 2
                        elif formalstatus == 4:
                            datebase_time.estatus = 1
                        elif formalstatus == 5:
                            datebase_time.estatus = 3
                        session.commit()
        except Exception as e:  ###如果连接失败
            print(id, ' is disconnect')
            print(e)
            datebase_time = session.query(Estatus).filter(Estatus.eid == id).first() ###寻找数据库相应条目
            end_time = time.perf_counter()
            status_time = round((end_time - start_time) * 1000, 0)
            if formalstatus <= 1:
                datebase_time.run += status_time
            elif 2 <= formalstatus <= 3:
                datebase_time.error += status_time
            elif formalstatus == 4:
                datebase_time.pause += status_time
            elif formalstatus == 5:
                datebase_time.offline += status_time
            dataSorce_c = session.query(Systemconnect).filter(Systemconnect.eid == id).first()
            dataSorce_e = session.query(Estatus).filter(Estatus.eid == id).first()
            dataSorce_e.estatus = 3
            dataSorce_e.mstatus = 3
            dataSorce_c.connection = 0
            session.commit()
            start_time = end_time
            formalstatus = 5  ###状态设置为关机
            print('connect request will restart in 10 sec')
            time.sleep(10)    ###休眠10second


