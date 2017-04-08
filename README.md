iChat App with Mongo Database

to create db:
users collection: 

db.createCollection("users",{validator:{$or:[{ID:{$type:"int"}},{Fname:{$type:"string"}},{Lname:{$type:"string"}},{email:{$type:"string"}},{password:{$type:"string"}},{username:{$type:"string"}},{msgs:{$type:"int"}},{friends:{$type:"array"}},{groups:{$type:"array"}},{picurl:{$type:"string"}},{stat:{$in:["on","off"]}},{friend_requests:{$type:"array"}}]}})

groups collection:
db.createCollection("groups",{validator:{$or:[{ID:{$type:"int"}},{name:{$type:"string"}},{admin:{$type:"string"}},{members:{$type:"array"}},{picurl:{$type:"string"}}]}})

kindly follow these steps

1-start mongod

2-start the server => python3 main.py

3-open browser localhost:8888/login

4-sign up and enjoy



Team members                                   

-Aboubakr khedr  
-Ahmed magdy
-Nesma mamdouh  
-Mohmaed mahrous

Roles

chat client/server     =>      Ahmed magdy and Aboubakr khedr

UI + page handling + authentication => retrieving and inserting in database through tornado  => Nesma mamdouh

database and connecting database with tornado  => mohamed mahrous
