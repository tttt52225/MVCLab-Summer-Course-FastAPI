import json 
import os 
import random
import shutil
from typing import Union
from fastapi import FastAPI, HTTPException, UploadFile, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from uuid import uuid4


class Note(BaseModel):
    task_name: str
    description: Union[str, None] = None
    priority: int 

class Enemy(BaseModel):
    name: str
    super_power: str
    description: Union[str, None] = None
    priority: int 

class NoteException(Exception):
    def __init__(self, id: str):
        self.id = id

class EnemyException(Exception):
    def __init__(self, name: str):
        self.name = name

class FileException(Exception):
    def __init__(self, name):
        self.name = name

app = FastAPI()

my_file_names = []

notes = []
notes_advices = [ 
    "I'm gonna put some dirt in your eye!",    
    "I missed the part where that's my problem.",
    "You want forgiveness? Get religion.",
    "I'm gonna put some dirt in your eye!",    
    "I missed the part where that's my problem.",
    "You want forgiveness? Get religion.",
    "I'm gonna put some dirt in your eye!",    
    "I missed the part where that's my problem.",
    "You want forgiveness? Get religion.",
    "Look at little Goblin Junior. Gonna cry?",
    "I am really gonna enjoy this...",
    "Who am I? You sure you want to know?",
    "That's a cute outfit! Did your husband give it to you?",
    "He despised you. You were an embarassment to him.",
    "You should've thought of that earlier.",
    "I am really gonna enjoy this..."
]
notes_file = 'notes.json'

enemies = []
enemies_file = 'enemies.json'

if os.path.exists(notes_file):
    with open(notes_file, "r") as f:
        notes = (json.load(f))

if os.path.exists(enemies_file):
    with open(enemies_file, "r") as f:
        enemies = (json.load(f))

@app.exception_handler(NoteException)
def note_exception_handler(request:Request, exc: NoteException):
    return JSONResponse (
        status_code= 404,
        content= {
            'Message' : f'Oops ! Looks like I do not have note with id == {exc.id}, no work today!'
        }
    )

@app.exception_handler(EnemyException)
def enemy_exception_handler(request:Request, exc: EnemyException):
    return JSONResponse (
        status_code= 404,
        content= {
            'Message' : f'Oops ! Looks like I do not have enemy named {exc.name}, no work today!'
        }
    )

@app.exception_handler(EnemyException)
def enemy_exception_handler(request:Request, exc: EnemyException):
    return JSONResponse (
        status_code= 409,
        content= {
            'Message' : f'Oops ! File named {exc.name} upload fail, try another one!'
        }
    )

@app.get("/")
def root():
    return {"message": "With great power comes no responsibility"}

@app.get("/notes/{id}")
def findNotes(id: str):
    res = None
    for note in notes:
        if note["id"] == id:
            res = note
    if not res:
        raise NoteException(id=id)
    return res

@app.get("/enemies/{name}")
def randomNotes(name: str):
    res = None
    for enemy in enemies:
        if enemy["name"] == name:
            res = enemy
            break
    if not res:
        raise EnemyException(name=name)
    return {"Enemy I have to fight today, ... maybe tomorrow ?": res}

@app.get("/notes-all")
def getNotes():
    return {'Works only I can handle, ... maybe Miles can try some of these ?' : notes}

@app.get("/enemies-all")
def getEnemies():
    print(enemies)
    return {'Enemies only I can defeat, ... maybe Miles can try some of these ?' : enemies}

@app.get("/my-mottos")
def myMottos():
    return random.choice(notes_advices)

@app.post('/add-notes')
def create_note(note: Note):
    note_dict = note.dict()
    note_id = uuid4().hex 
    note_dict.update({"id":note_id})
    notes.append(note_dict)
    with open(notes_file, "w") as f:
        json.dump(notes, f, indent=4)
    return note_dict

@app.post('/add-enemy')
def create_enemy(enemy: Enemy):
    enemy_dict = enemy.dict()
    enemy_id = uuid4().hex 
    enemy_dict.update({"id":enemy_id})
    enemies.append(enemy_dict)
    with open(enemies_file, "w") as f:
        json.dump(enemies, f, indent=4)
    return enemy_dict

@app.post('/upload')
def Upload_file(file: Union[UploadFile, None] = None):
    if not file: return {"message" : "No file upload"}
    try:
        file_location = './' + file.filename
        with open(file_location, "wb") as f:
            shutil.copyfileobj(file.file, f)
            file.close()
        my_file_names.append(file.filename)
        return {"Result" : "OK"}
    except:
        raise FileException(name=f'Upload File {file.filename}')


