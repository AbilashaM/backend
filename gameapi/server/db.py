#database 
import mysql.connector
from model import constant
import json
from json.decoder import JSONDecodeError
from model.pwd import verify_password
from model import (model,function,pwd)
from fastapi.encoders import jsonable_encoder

#database connection
con = mysql.connector.connect(
   host="localhost",
   port=3306,
   user="abilashaM",
   password="Murugan*10",
   database="api",
)

#tables
users_table = "user"
weapon_table="weapons"
unlockable_table="unlockables"
mission_table="mission"
earning_table="player_earning"
spaceship_table="spaceship"
stats_table="stats"
unlock_table="unlock_item"
playerSpaceship_table="player_spaceship"
completedmission_table="complete_mission"
#REGISTER USER

# add new user
async def add_user(new_user):
    cursor = con.cursor()
    query = "SELECT * FROM {} WHERE {} = %s".format(users_table, constant.EMAILID)
    cursor.execute(query, (new_user['emailId'],))
    result = cursor.fetchone()
    if not result:
        insert_query = "INSERT INTO {} ({}, {}, {}) VALUES (%s, %s, %s)".format(
            users_table, "pilotAlias", constant.EMAILID, "password"
        )
        cursor.execute(
            insert_query,
            (new_user['pilotAlias'], new_user['emailId'], new_user['password'])
        )
        con.commit()
        return "Pilot recruited successfully"
    else:
        return "Pilot already exists"

#LOGIN USER

# check userid nd password   
    
async def check_user(username, password): 
    cursor = con.cursor()
    query = "SELECT * FROM {} WHERE {} = %s OR {}=%s".format(users_table, "pilotAlias",constant.EMAILID)
    params=(username,username)
    cursor.execute(query, params)
    result = cursor.fetchone()
    data=[]
    if not result:
        msg="user does not exist"
        
    else:
        stored_pilotalias,_,stored_password=result
        result=verify_password(password,stored_password)
        if not result:
           msg="password incorrect"
        else:
            msg="access granted"
            data=await login(stored_pilotalias)
    response = model.Response(message=msg,data=data)
    return response

# generate response for login

async def login(pilotalias):
    playerEarning= await get_earning(pilotalias)  
    stats= await get_stats(pilotalias) 
    unlocked= await get_locked(pilotalias)
    spaceships= await get_playerSpaceship(pilotalias)
    mission= await get_complete_mission(pilotalias)

    data=[]
    login=model.Loginresponse(
        player_earning=playerEarning,
        stats=stats,
        Unlocked_Items= unlocked,
        spaceship=spaceships,
        mission=mission
    )
    a=jsonable_encoder(login.__dict__)
    data.append(a)
    return data

#PLAYER EARNING

# get player earning detail  
  
async def get_earning(pilotalias):
    cursor=con.cursor()
    query="SELECT * from {} WHERE {}= %s".format(earning_table,"pilotAlias")
    params=(pilotalias,)
    cursor.execute(query, params)
    result = cursor.fetchone()
    if result:
        earning=model.Earning(
            pilot_id=result[1],
            xp_earned=result[2],
            cerdit_balance=result[3]
        )
        playerearning=jsonable_encoder(earning)
    else:
        playerearning={}

    return(playerearning)

#update player Earning 

async def update_playerEarning(pilot,userdata):

    cursor=con.cursor()
    query="SELECT * from {} WHERE {}= %s".format(earning_table,"pilotAlias")
    params=(pilot,)
    cursor.execute(query, params)
    result = cursor.fetchone()
    if result:
        update_query= "UPDATE {} SET {}=%s,{}=%s WHERE {}=%s".format(earning_table,"xp_earned","cerdit_balanced","pilotAlias")
        params=(userdata["xp_earned"],userdata["cerdit_balanced"],pilot)

        cursor.execute( update_query,params )
        con.commit()
        if cursor.rowcount > 0:
         return"Update successful"
        else:
         return "No rows updated"
    else:
        return "error"

#STATS

# get stats detail  
     
async def get_stats(pilotalias):
    cursor=con.cursor()
    query="SELECT * from {} WHERE {}= %s".format(stats_table,"pilotAlias")
    params=(pilotalias,)
    cursor.execute(query, params)
    result = cursor.fetchone()
    if result:
        stat=model.Stats(
            days_in_space=result[1],
            Missions_passed=result[2],
            Missions_failed=result[3],
            Overall_Rewards_earned=result[4],
            Overall_Credits_earned=result[5],
            Overall_Credits_spent=result[6],
            Satellite_takedowns=result[7],
            Spaceship_takedowns=result[8],
            Rocket_takedowns=result[9]  )
        stats=jsonable_encoder(stat)
    else:
        stats={}
    return(stats)

#update states detail

async def stats_update(pilot,user_data):
   

    cursor=con.cursor()
    query="SELECT * from {} WHERE {}= %s".format(stats_table,"pilotAlias")
    params=(pilot,)
    cursor.execute(query, params)
    result = cursor.fetchone()
    if result:
        update_query = "UPDATE {} SET {}= %s,{}= %s,{}= %s,{}= %s,{}= %s,{}= %s,{}= %s,{}= %s,{}= %s WHERE {}=%s".format( stats_table,
                                                                                                                          "days_in_space",
                                                                                                                          "Missions_passed",
                                                                                                                          "Mission_failed",
                                                                                                                          "Overall_Rewards_earned",
                                                                                                                          "Overall_Credits_earned",
                                                                                                                          "Overall_Credits_spent",
                                                                                                                          "Satellite_takedowns",
                                                                                                                          "Spaceship_takedowns",
                                                                                                                          "Rocket_takedowns",
                                                                                                                          "pilotAlias")
        params = (
        user_data['days_in_space'],
    user_data["Missions_passed"],
    user_data["Missions_failed"],
    user_data["Overall_Rewards_earned"],
    user_data["Overall_Credits_earned"],
    user_data["Overall_Credits_spent"],
    user_data["Satellite_takedowns"],
    user_data["Spaceship_takedowns"],
    user_data["Rocket_takedowns"],
    pilot,
)
    else:
        cursor=con.cursor()
        query="SELECT {} from {} WHERE {}= %s".format("pilotAlias",users_table,"pilotAlias")
        params=(pilot,)
        cursor.execute(query, params)
        result = cursor.fetchone()
        if result:
                update_query = "INSERT {} ({},{},{},{},{},{},{},{},{},{}) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)".format(stats_table,"pilotAlias",
                                                                                                                            "days_in_space",
                                                                                                                            "Missions_passed",
                                                                                                                            "Mission_failed",
                                                                                                                            "Overall_Rewards_earned",
                                                                                                                            "Overall_Credits_earned",
                                                                                                                            "Overall_Credits_spent",
                                                                                                                            "Satellite_takedowns",
                                                                                                                            "Spaceship_takedowns",
                                                                                                                            "Rocket_takedowns",
                                                                                                                            )
                params = (
                    pilot,
                user_data['days_in_space'],
            user_data["Missions_passed"],
            user_data["Missions_failed"],
            user_data["Overall_Rewards_earned"],
            user_data["Overall_Credits_earned"],
            user_data["Overall_Credits_spent"],
            user_data["Satellite_takedowns"],
            user_data["Spaceship_takedowns"],
            user_data["Rocket_takedowns"],)
                
        else:
            return "error"

    cursor.execute( update_query,params )
    con.commit()
    if cursor.rowcount > 0:
        return"Update successful"
    else:
        return "No rows updated"
    

#SPACESHIP

# get all spaceship detail  
     
async def get_spaceship():
    cursor=con.cursor()
    cursor.execute("SELECT * from {}".format(spaceship_table))
    result = cursor.fetchall()
    spaceship=[]
    for row in result:
        up_avail=function.todict(row[5])
        asset=function.todict(row[2])

        spaceships=model.Spaceship(
            id= row[0],
            Image=row[1],
            Assets= asset,
            Name= row[3],
            Description= row[4],
            Upgrades_available= up_avail,
        )

        spaceship.append(spaceships)

    return spaceship
# get player spaceship detail  
     
async def get_playerSpaceship(pilotalias):
    cursor=con.cursor()
    query="SELECT * FROM spaceship JOIN player_spaceship ON spaceship.id = player_spaceship.id WHERE player_spaceship.pilotalias =%s"
    params=(pilotalias,)
    cursor.execute(query,params)
    result= cursor.fetchall()
    spaceship=[]
    for row in result:
        up_avail=function.todict(row[5])
        asset=function.todict(row[2])
        cursor1=con.cursor()
        cursor1.execute("SELECT upgrade_so_far FROM player_spaceship WHERE id =%s",(row[0],))
        result1=cursor1.fetchone()
        if result1:
            up_current=function.todict(result1[0])
        spaceships=model.playerSpaceship(
            id= row[0],
            Image=row[1],
            Assets= asset,
            Name= row[3],
            Description= row[4],
            Upgrades_available= up_avail,
            Upgrades_so_far=up_current
        )
        spaceship.append(spaceships)

    return spaceship


#update spaceship

async def update_spaceship(pioltAlias,id,userdata):
    json_data=json.dumps(userdata)
    result1=check_data(userdata,id)
    if result1[0]:
        cursor=con.cursor()
        cursor.execute("SELECT {} FROM {} WHERE {}=%s AND {}=%s".format("id",playerSpaceship_table,"pilotAlias","id"), (pioltAlias,id))
        result = cursor.fetchone() 
        if result:
            query="UPDATE {} SET {}=%s WHERE {}=%s AND {}=%s".format(playerSpaceship_table,"upgrade_so_far","pilotAlias","id")
            params=(json_data,pioltAlias,id)  
            cursor.execute(query, params)
            con.commit()
            
        else:
            result=check_id(pioltAlias,id,spaceship_table)
            if result:
                query="INSERT {} ({},{},{}) VALUES(%s,%s,%s)".format(playerSpaceship_table,"pilotAlias","id","upgrade_so_far")
                params=(pioltAlias,id,json_data,)
                cursor.execute(query, params)
                con.commit()
            else:
                return "wrong info" 

        if cursor.rowcount > 0:
            return"Update successful"
        else:
            return "No rows updated"
    else:
        return result1[1]

#WEAPONS

#get all weapon detail

async def get_weapons():
    cursor=con.cursor()
    query="SELECT * FROM {}".format(weapon_table)
    cursor.execute(query)
    result = cursor.fetchall()
    weapons=[]
    for row in result:
        assets_dict=function.todict(row[5])
        
        weapon = model.Weapon(
            id=row[0],
            name=row[1],
            power=row[2],
            power_against_shield=row[3],
            level=row[4],
            assets=assets_dict
        )
        weapons.append(weapon)
    

    return weapons

# MISSION

#get all mission detail

async def get_mission():
    cursor=con.cursor()
    query="SELECT * FROM {}".format(mission_table)
    cursor.execute(query)
    result = cursor.fetchall()
    mission=[]

    for row in result:
        rule_dict=function.todict(row[4])
        defendlist=function.tolist(row[2])
        enemylist=function.tolist(row[3])
        cursor1=con.cursor()
        unlock_query="SELECT id FROM {} WHERE {} = %s;".format(unlockable_table,"id")
        id=pwd.encode_password(row[0])
        
        params=(id,)
        cursor1.execute(unlock_query,params)
        ids = [row1[0] for row1 in cursor1.fetchall()]
        unlock = model.Mission(
            id=row[0],
            name=row[1],
            Description=row[5],
            Reward=row[6],
            level_required=row[7],
            rules=rule_dict,
            enemy=enemylist,
            defend=defendlist,
            unlockables=ids

        
        )
        mission.append(unlock)
    return mission

#update mission status

async def missionUpdate(pilot,userdata):
    id=userdata["id"]
    cursor=con.cursor()
    cursor.execute("SELECT {} FROM {} WHERE {}=%s AND {}=%s".format("id",completedmission_table,"id","pilotAlias"),(id,pilot))
    result=cursor.fetchone()
    if not result:
        cursor=con.cursor()
        result1= check_id(pilot,id,mission_table)
        if result1:
            cursor=con.cursor()
            query="INSERT INTO {} ({},{}) VALUES (%s,%s)".format(completedmission_table,"pilotAlias","id")
            params=(pilot,id)
            cursor.execute( query,params )
            con.commit()
            if cursor.rowcount > 0:
                return"Update successful"
            else:
                return "No rows updated"
    
        else:
            return "wrong info"
    else:
        return "duplicated value"

#get complete mission
async def get_complete_mission(pilot):
    cursor=con.cursor()
    query="SELECT {} FROM {} WHERE {}=%s".format("id",completedmission_table,"pilotAlias")
    params=(pilot,)
    cursor.execute(query, params)
    ids = [row[0] for row in cursor.fetchall()]
    return ids

#UNLOCKABLES

#get all unlockables

async def get_unlockable():
    cursor=con.cursor()
    query="SELECT * FROM {}".format(unlockable_table)
    cursor.execute(query)
    result = cursor.fetchall()
    unlockable=[]
    for row in result:
         assets_dict=function.todict(row[6])
    
         powerlist =function.tolist(row[7])
        

        
         unlock = model.Unlockables(
            id=row[0],
            name=row[1],
            xp_required=row[2],
           unlockable_in_mission=row[3],
            image=row[4],
            description=row[5],
            assets=assets_dict,
            power=powerlist
        )
         unlockable.append(unlock)
    

    return unlockable

#update unlock item

async def unlockItem(pilot,userdata):
    id=pwd.encode_password(userdata["id"])
    cursor=con.cursor()
    cursor.execute("SELECT {} FROM {} WHERE {}=%s AND {}=%s".format("id",unlock_table,"id","pilotAlias"),(id,pilot))
    result=cursor.fetchone()
    if not result:
        result= check_id(pilot,id,unlockable_table)
        if result:
            cursor=con.cursor()
            query="INSERT INTO {} ({},{}) VALUES (%s,%s)".format(unlock_table,"pilotAlias","id")
            id=pwd.encode_password(userdata["id"])
            params=(pilot,id)
            cursor.execute( query,params )
            con.commit()
            if cursor.rowcount > 0:
                return"Update successful"
            else:
                return "No rows updated"
    
        else:
            return "wrong info"
    else:
        return "duplicated value"
    
# get locked item

async def get_locked(pilotalias):
    

    cursor=con.cursor()
    #query="SELECT unlockables.id FROM unlockables LEFT JOIN unlock_item ON unlockables.id = unlock_item.id WHERE unlock_item.pilotAlias = %s AND unlock_item.id IS NULL"
    query="SELECT unlockables.id FROM unlockables WHERE unlockables.id NOT IN (SELECT unlock_item.id FROM unlock_item WHERE unlock_item.pilotAlias = %s)"
    #query="SELECT unlockables.id FROM unlockables,unlock_item WHERE unlockables.id != unlock_item.id and unlock_item.pilotAlias= %s "
    params=(pilotalias,)
    cursor.execute(query, params)
    ids = [row[0] for row in cursor.fetchall()]
    return ids



#check for id and pilotalias in tables

def check_id(pilot,id,table):
    cursor=con.cursor()
    cursor.execute("SELECT {} FROM {} WHERE {} = %s".format("pilotAlias",users_table,"pilotAlias"),(pilot,))
    user_id = cursor.fetchone()

    if user_id is None:
        return False

    cursor.execute("SELECT {} FROM {} WHERE {} = %s".format("id",table,"id"),(id,))
    result = cursor.fetchone()

    if result is None:
        
        return False

    
    return True


def check_data(userdata,id):
    cursor=con.cursor()
    cursor.execute("SELECT {} FROM {} WHERE {} = %s".format("upgrades_available",spaceship_table,"id"),(id,))
    result = cursor.fetchone()
    if result:
        upgrades_available = function.todict(result[0])  
        for key, value in userdata.items():
                if value > upgrades_available.get(key, float('inf')):
                    return False,"incorrect value"
                else:
                    return True,""
    else:
        return False,"incorrect id"