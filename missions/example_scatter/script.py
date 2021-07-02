from formations import scatter, vec
# start of my python script program file
import sbs

from random import randrange


# these variables persist for the life of the mission, and retain their data.  
# Functions that use them need to use the 'global' keyword to access them properly.
modeTimer = 0

asteroidList = []

def add_asteroids(sim, g, name):
	landmark = None
	for v in g:
		asteroidID = sim.make_new_passive("behav_asteroid", "Asteroid 1")
		asteroidList.append(asteroidID)
		asteroid = sim.get_space_object(asteroidID)
		#v = v.rand_offset(100)
		sim.reposition_space_object(asteroid, v.x, v.y, v.z)
		if landmark is None:
			landmark = sim.add_landmark(v.x, v.y+100,v.z, name, 0,1,0,1);



########################################################################################################
def  HandleScriptStart(sim):
	print("Script start ")
	# playerID will be a NUMBER, a unique value for every space object that you create.
	playerID = sim.make_new_player("behav_playership", "Battle Cruiser");

	# making a bounch of asteroids
	add_asteroids(sim, scatter.line(10, -2000,0,0, 2200,0, 1000,True), "line RND")
	add_asteroids(sim, scatter.ring(4,4, -2000,0,-1000, 800, 100, 0, 160,True), "ring rnd")
	add_asteroids(sim, scatter.ring_density([2, 4, 20], 2000,0,-1000, 800, 200, 0, 360,False), "ring density")
	add_asteroids(sim, scatter.sphere(50, 0,0,4000, 400), "sphere")
	add_asteroids(sim, scatter.sphere(50, -2000,0,2000, 200, 800, ring=True), "sphere-Ring")
	add_asteroids(sim, scatter.rect_fill(5,5,  2000,0, 4000, 500, 500, True), "Grid")
	add_asteroids(sim, scatter.box_fill(5,5,5,  -2000, 0, 4000, 500, 500,500), "Box")
			
	


########################################################################################################
def  HandleScriptTick(theSimulation):
	# print("Script Tick ")
	# c =  len(asteroidList)
	# # print("asteroidList size " + str(c))

	# # if there's an asteroid ID in the asteroidList
	# if c > 0:
	# 	# tell the code to delete that asteroid (by its unique ID)
	# 	# NOTE: delete_object is not a function within theSimulation
	# 	sbs.delete_object(asteroidList[-1])
	# 	# delete the ID number that I had in my asteroidList
	# 	del asteroidList[-1]
	pass



# end of my python script program file

