#basemodel
from pydantic import BaseModel
class CreateUser(BaseModel):
    pilotAlias:str
    emailId:str
    password:str

class Response(BaseModel):
    message:str
    data:list

class Login(BaseModel):
    username:str
    password:str
class Weapon(BaseModel):
    id:int
    name:str
    power: int
    power_against_shield: int
    level: int
    assets: dict
class Unlockables(BaseModel):
    id:str
    name : str
    xp_required:int
    unlockable_in_mission: int
    image: str
    description: str
    assets: dict
    power:list
class Mission(BaseModel):
    id:int
    name:str
    defend:list
    enemy:list
    rules:dict
    Description:str
    Reward:int
    level_required:int

    unlockables:list
class Earning(BaseModel):
    pilot_id:int
    xp_earned:int
    cerdit_balance:int

class Stats(BaseModel):

    days_in_space:int
    Missions_passed:int
    Missions_failed:int
    Overall_Rewards_earned:int
    Overall_Credits_earned:int
    Overall_Credits_spent:int
    Satellite_takedowns:int
    Spaceship_takedowns:int
    Rocket_takedowns:int
    
class Spaceship(BaseModel):
    id:int
    Image:str
    Assets:dict
    Name:str
    Description:str
    Upgrades_available:dict

class playerSpaceship(BaseModel):
    id:int
    Image:str
    Assets:dict
    Name:str
    Description:str
    Upgrades_available:dict
    Upgrades_so_far:dict

class Loginresponse(BaseModel):
    player_earning:dict 
    stats:dict
    Unlocked_Items:list
    spaceship:list
    mission:list



class Earningupdate(BaseModel):
    xp_earned:int
    cerdit_balanced:int



class Unlock(BaseModel):
    id:str	

class spaceshipupdate(BaseModel):
    Weapons_Upgrade:int
    Defense_Systems:int
    Engine_Enhancements:int
    Utility_Upgrades:int
    Support_Systems:int
  

class attribute(BaseModel):
    name:str
    value:int