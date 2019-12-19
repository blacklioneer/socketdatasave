from database.threads import equipmentfinisheddata
import threading
from multiprocessing import Process

if __name__ == '__main__':
    p1 = Process(target=equipmentfinisheddata, args=(1,))
    p2 = Process(target=equipmentfinisheddata, args=(2,))
    p3 = Process(target=equipmentfinisheddata, args=(3,))
    p4 = Process(target=equipmentfinisheddata, args=(4,))
    p5 = Process(target=equipmentfinisheddata, args=(5,))
    p6 = Process(target=equipmentfinisheddata, args=(6,))
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
    p6.start()