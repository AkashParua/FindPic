import pinecone
import os
from dotenv import load_dotenv
from vectorize2 import vectorize
import shutil
from typing import List
from fastapi import FastAPI , UploadFile , File 
from fastapi.responses import JSONResponse,FileResponse

def configure():
    load_dotenv()

configure()

app = FastAPI()
pinecone.init(api_key= os.getenv('api_key') ,type= os.getenv('type'))
index = pinecone.Index('vectorimages')
app = FastAPI()

@app.post("/uploadimage")
async def create_upload_file(file: UploadFile = File(...)):
    with open(os.path.join("Images", file.filename), "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    vector_image = vectorize('Images',file.filename)
    data = (file.filename , vector_image )
    index.upsert(vectors=[data])
    return {"filename": file.filename}
    
@app.get('/search/{k}')
async def search_image(k:int , file: UploadFile = File(...) ):
    with open(os.path.join("QueryImages", file.filename), "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    vector_image = vectorize('QueryImages',file.filename)
    results = index.query(vector_image, top_k=k , include_metadata=True)
    print(results)
    return FileResponse(os.path.join('Images',results['matches'][k-1]['id']))

@app.delete('/delete/{filename}')
async def delete_image(filename : str):
    try:
        os.remove(os.path.join(os.getcwd(),'Images',filename))
        delete_response = index.delete(ids=[filename])
        return JSONResponse(content={"removed": True} , status_code = 200)
    except FileNotFoundError :
        return JSONResponse(content={"removed": False , "error message": "FIle not found"}, status_code =404)
    
@app.post("/savefromScrapedImages")
async def save_all() :
       directory = 'ScrapedImages'
       for filename in os.listdir(directory):
            if os.path.isfile(os.path.join('Images',filename)):
                print('file already saved')
                continue
            shutil.copy(os.path.join('ScrapedImages',filename),os.path.join('Images',filename))
            vector_image = vectorize('Images',filename)
            data = (filename , vector_image )
            index.upsert(vectors=[data])
            print(f'{filename} saved to database')
        
       
    
    
    

    

    

