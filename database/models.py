"""
传输资源管理平台 - 数据库模型
只导入4个机房的业务板使用情况
"""
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class BusinessBoard(Base):
    """机房业务板使用情况"""
    __tablename__ = 'business_boards'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    room_name = Column(String(50), nullable=False, index=True, comment='机房名称')
    device_brand = Column(String(50), comment='设备品牌')
    device_model = Column(String(50), comment='设备型号')
    device_code = Column(String(100), comment='设备编号')
    slot = Column(Integer, comment='槽位')
    board_model = Column(String(50), comment='板卡型号')
    usage_status = Column(Text, comment='使用状况')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class WavelengthConnection(Base):
    """波长连接表（云立方-常熟等）"""
    __tablename__ = 'wavelength_connections'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    sheet_name = Column(String(50), nullable=False, comment='Sheet名称')
    plane = Column(String(50), comment='平面')
    local_network_device = Column(String(100), comment='本端数通设备')
    local_network_port = Column(String(50), comment='本端数通端口号')
    local_ip = Column(String(50), comment='本端接口IP')
    otn_tributary_port = Column(String(50), comment='OTN支路侧端口号')
    a_transmission_device = Column(String(100), comment='A端传输设备')
    otn_line_port_a = Column(String(50), comment='A端OTN线路侧端口号')
    wavelength = Column(String(20), comment='波长')
    otn_line_port_z = Column(String(50), comment='Z端OTN线路侧端口号')
    z_transmission_device = Column(String(100), comment='Z端传输设备')
    otn_tributary_port_z = Column(String(50), comment='Z端OTN支路侧端口号')
    remote_ip = Column(String(50), comment='对端接口IP')
    remote_network_port = Column(String(50), comment='对端数通端口号')
    remote_room_device = Column(String(100), comment='对端机房设备')
    remark = Column(String(200), comment='备注')
    other = Column(String(100), comment='其他')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

def init_db(db_path='transmission_resource.db'):
    """初始化数据库"""
    engine = create_engine(f'sqlite:///{db_path}', echo=False)
    Base.metadata.create_all(engine)
    return engine

def get_session(engine):
    """获取数据库会话"""
    Session = sessionmaker(bind=engine)
    return Session()
