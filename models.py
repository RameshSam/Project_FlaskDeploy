from sqlalchemy import create_engine , Column , ForeignKey , String , Integer , LargeBinary
from sqlalchemy.orm import sessionmaker , declarative_base
import os , cv2

Base = declarative_base()

class Person_Details(Base):
    __tablename__ = "Empolyee"
    reg = Column("reg",Integer,primary_key =True)
    name = Column("name",String(50),nullable=False,unique=False)
    email = Column("email",String(100),nullable=False,unique=False)
    password = Column("password",String(50),nullable=False,unique=False)

    def __init__(self , reg , name , email , password):
        self.reg = reg
        self.name = name
        self.email = email
        self.password = password
    
    def __repr__(self):
        return f" ({self.reg}) Name : {self.name} Email_Id : {self.email} (Password : {self.password})"

class Store_Image(Base):
    __tablename__ = "images"
    id = Column("id",Integer,primary_key=True)
    Img_Name = Column(String )
    Img = Column(LargeBinary)
    Img_encoding = Column(LargeBinary)
    reg = Column("reg", Integer , ForeignKey("Empolyee.reg"))

    def __init__(self ,Img_encoding , Img_Name ,  img , reg):
        self.Img_Name = Img_Name
        self.Img = Img
        self.Img_encoding = Img_encoding
        self.reg = reg 

    def __repr__(self):
        list_ = []
        list_.append(self.Img_Name)
        list_.append(self.Img)
        list_.append(self.Img_encoding)
        list_.append(self.reg)
        return list_
     
path = f"sqlite:///{os.getcwd()}/mydb.db"
engine = create_engine(path,echo = True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
s = Session()

def database(temp,name,img,img_Encode):
    p = Store_Image(name,img,img_Encode,temp.reg)
    s.add(p)
    s.commit()
    s.close()