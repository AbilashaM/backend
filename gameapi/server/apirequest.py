#api endpoints
from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from model import (model,pwd)
from server import db
from pydantic import BaseModel
#router
user=APIRouter()

# register user

@user.post('/register_Player')
async def create_user(user_data : model.CreateUser):
    encoded_password = pwd.encode_password(user_data.password)
    user_data.password = encoded_password 
    result = await db.add_user(user_data.__dict__)      
    response = model.Response(message=result,data=[])
    return jsonable_encoder(response.__dict__)

# login user
@user.post("/login")
async def login(user_data:model.Login): 
    result = await db.check_user(user_data.username,user_data.password)      
    return jsonable_encoder(result)

#update player earning detail

@user.post("/earning_update/{pilotAlias}")
async def earningUpdate(pioltAlias:str,playerEarning:model.Earningupdate):
    result= await db.update_playerEarning(pioltAlias,playerEarning.__dict__)
    response = model.Response(message=result,data=[])
    return jsonable_encoder(response.__dict__)

#update stats detail

@user.post("/{pilotAlias}/stats_update")
async def StatsUpdate(PioltAlias:str,stats_update:model.Stats):
    result= await db.stats_update(PioltAlias,stats_update.__dict__)
    response = model.Response(message=result,data=[])
    return jsonable_encoder(response.__dict__)

#spaceship update

@user.post("/{pilotAlias}/spaceships/{id}/spaceship_update")
async def spaceshipUpdate(pilotAlias:str,id:int,update:model.spaceshipupdate):
    result= await db.update_spaceship(pilotAlias,id,update.__dict__)
    response = model.Response(message=result,data=[])
    return jsonable_encoder(response.__dict__)

#get weapon details

@user.get("/weapons")
async def weapons():
    result= await db.get_weapons()
    response = model.Response(message="success",data=result)
    return jsonable_encoder(response.__dict__)

#get mission details
@user.get("/mission")
async def mission():
    result= await db.get_mission()
    response = model.Response(message="success",data=result)
    return jsonable_encoder(response.__dict__)

#update mission status

@user.post("/{pilotAlias}/mission_update")
async def missionUpdate(pilotAlias:str,id:model.Unlock):
    result= await db.missionUpdate(pilotAlias,id.__dict__)
    response = model.Response(message=result,data=[])
    return jsonable_encoder(response.__dict__)

#get unlockable
@user.get("/unlockable")
async def unlockable():
    result= await db.get_unlockable()
    response = model.Response(message="success",data=result)
    return jsonable_encoder(response.__dict__)

#unlock item
@user.post("/{pilotAlias}/unlock_item")
async def unlockItem(PioltAlias:str,Unlockitem:model.Unlock):
    result= await db.unlockItem(PioltAlias,Unlockitem.__dict__)
    response = model.Response(message=result,data=[])
    return jsonable_encoder(response.__dict__)


#get spaceship details

@user.get("/spaceship")
async def spaceship():
    result= await db.get_spaceship()
    response = model.Response(message="success",data=result)
    return jsonable_encoder(response.__dict__)

#@user.get("/{id}")
#async def a(id:str):
   # a=pwd.encode_password(id)
    #return a
#@user.post("/insert-data")
#async def insert_data(data: list[model.attribute]):
    #return "hello"
