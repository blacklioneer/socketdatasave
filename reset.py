from database.threads import reset
from multiprocessing import Process

if __name__ == '__main__':
    p1 = Process(target=reset)
    p1.start()
