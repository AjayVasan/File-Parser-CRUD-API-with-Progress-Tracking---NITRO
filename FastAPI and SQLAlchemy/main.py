from fastapi import FastAPI , HTTPException , Depends
from sqlalchemy import Integer , create_engine , Column , String , Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session , sessionmaker
from fastapi import FastAPI, UploadFile
from datetime import datetime
from llama_index.core import SimpleDirectoryReader
import requests
from pydantic import BaseModel
import os


app = FastAPI(title="Testing SQLAlchemy")


engine = create_engine("sqlite:///test.db")
SessionLocal = sessionmaker(autoflush=False , bind=engine)
base = declarative_base()

#database Model 
class model(base):
    __tablename__ = "File_Data"
    Fid = Column(Integer , primary_key=True , index=True, unique=True)
    Fname = Column(String(100), nullable=False)
    Fstatus= Column(Integer,nullable=False)
    Fdate = Column(String(100),unique=True, nullable=False)
    Fprog = Column(String(100), nullable=False)
    
class content(base):
    __tablename__ = "File_Content"
    index = Column(Integer,primary_key=True,index=True,nullable=False)
    Fid = Column(Integer,nullable=False)
    Fname = Column(String, nullable=False) 
    Pagenum = Column(Integer, nullable=False)
    Content = Column(Text)

base.metadata.create_all(engine)

# class ContentSchema(BaseModel):
#     id: int
#     Fname: str
#     Pagenum: int
#     Content: str

#     class Config:
#         from_attributes = True

class fileupload(BaseModel):
    Fname : str
    Fstatus : str
    Fprog : str
    Fdate : str

class fileresponce(BaseModel):
    Fid : int
    Fname : str
    Fstatus : str
    Fprog : str
    Fdate : str

    class Config:
        from_attributes = True

def chk_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

chk_db()

@app.get("/")
def root():
    return {"message":"Testing integration of SQLAlchemy with FastAPI"}

@app.get("/file")
def get_spec(fid:int = None , db:Session = Depends(chk_db)):
    if fid:
        file = db.query(model).filter(model.Fid == fid).first()
        if not file:
            raise HTTPException(status_code=404, detail="File not found!")
        return file
    if db.query(model).all():
        return db.query(model).all()
    else:
        return {"message":"No data in the database"}


@app.get("/file/data/{fid}")
async def getone(fid:int , db:Session = Depends(chk_db)):
    if db.query(model).filter(model.Fid == fid).first():
        reader = SimpleDirectoryReader(input_files=["./uploads/" + db.query(model).filter(model.Fid == fid).first().Fname])
        serialized_docs = []
        documents = reader.load_data()
        for doc in documents:
            ne = content()
            ne.Fid = fid
            ne.Fname = db.query(model).filter(model.Fid == fid).first().Fname
            ne.Pagenum = int(doc.metadata["page_label"])
            ne.Content = doc.text
            db.add(ne)
        db.commit()
        db.refresh(ne)
        return db.query(content).filter(content.Fid == fid).all()
    else:
        raise HTTPException(status_code=404, detail="File not found!")


            


@app.post("/file",response_model=fileresponce)
async def upload(file : UploadFile , db:Session = Depends(chk_db)):
    if db.query(model).filter(model.Fname == file.filename).first():
        raise HTTPException(status_code=404, detail="File already Exists!")
    
    nf = model()
    nf.Fname = file.filename
    nf.Fdate = datetime.now()
    nf.Fstatus = file.content_type
    try: 
        UPLOAD_DIR = "uploads"
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        f_p = os.getcwd()+"/uploads/"+file.filename 
        f =  open(f_p,"wb")
        f.write(file.file.read())
        m = "File upload sucess"
    except:
        m = "File upload falied!"
    finally:
        f.close()
    # return {"message":"New File Uploaded Successfully"}
    nf.Fprog = m
    db.add(nf)
    db.commit()
    db.refresh(nf)
    return nf


@app.delete("/file/del")
def delete(fid:int = None, db:Session = Depends(chk_db)):
    if fid:
        if db.query(model).filter(model.Fid == fid).first():
            f_n = db.query(model).filter(model.Fid == fid).first().Fname
            if delete_ele(f_n):
                db.query(model).filter(model.Fid == fid).delete()
                db.query(content).filter(content.Fid == fid).delete()
                db.commit()
                return {"message": f"File with id {fid , f_n} deleted successfully"}
        raise HTTPException(status_code=404, detail="File not found!")
    else:
        if db.query(model).all() and db.query(content).all():
            files = db.query(model).all()
            for f in files:
                if delete_ele(f.Fname):
                    pass 
                else:
                    return {"message":"File mismatch from db and os"}
            db.query(model).delete()
            db.query(content).delete()
            db.commit()
            return {"message":"All data wiped from the database successfully"}
        else:
            return {"message":"No data in the database"}
        

def delete_ele(name:str):
    
    file_path = os.getcwd()+"/uploads/"+name
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False
