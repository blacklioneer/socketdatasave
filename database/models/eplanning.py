from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime, create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()  # 创建基类


class Eplanning(Base):
    __tablename__ = 'eplanning'  # 指定表名
    id = Column(Integer, primary_key=True)
    eid = Column(Integer, nullable=False)
    ordernum = Column(String(255), nullable=False)
    suppliesnum = Column(String(255), nullable=False)
    order = Column(Integer, nullable=False)
    finished = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)
    unqualified = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)


class Error(Base):
    __tablename__ = 'error'  # 指定表名
    id = Column(Integer, primary_key=True)
    eid = Column(Integer, nullable=False)
    errorid = Column(Integer, nullable=False)
    error = Column(DateTime, nullable=False)
    status = Column(Integer, nullable=False)
    type = Column(Integer, nullable=False)


class Estatus(Base):
    __tablename__ = 'estatus'  # 指定表名
    eid = Column(Integer, primary_key=True)
    ename = Column(String, nullable=False)
    oee = Column(Integer, nullable=False)
    estatus = Column(Integer, nullable=False)
    mstatus = Column(Integer, nullable=False)
    finished = Column(Integer, nullable=False)
    run = Column(Integer, nullable=False)
    pause = Column(Integer, nullable=False)
    error = Column(Integer, nullable=False)
    offline = Column(Integer, nullable=False)
    updatetime = Column(Integer, nullable=False)


class Systemconnect(Base):
    __tablename__ = 'systemconnect'  # 指定表名
    eid = Column(Integer, primary_key=True)
    ip = Column(String(255), nullable=False)
    status = Column(Integer, nullable=False)
    connection = Column(Integer, nullable=False)


class Transmission(Base):
    __tablename__ = 'transmission'  # 指定表名
    eid = Column(Integer, primary_key=True)
    remain = Column(Integer, nullable=False)
    material = Column(Integer, nullable=False)
    transmission = Column(Integer, nullable=False)

#初始化数据库连接
engine = create_engine('postgresql+psycopg2://postgres:xbc961031@localhost:5432/ammo')
Session = sessionmaker(bind=engine)
session = Session()