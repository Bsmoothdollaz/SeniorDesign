import queue

class POI:
	def __init__(self,x, y, z):
		self.x = x
		self.y = y
		self.z = z


test = POI(1,1,1)

locations = {
	'A': test
}

def navigateDrone(coords=None, location=None):




	if coords is None and location is None:
		return -1

	if location:
		temp_coords = None
		for loc in locations:
			if loc == location:
				temp_coords = locations[loc]
	else:
		temp_coords = coords



	return 1


a -> 0,0
b -> 1,0
also input any coords we want within range

q = queue.Queue()
items = [takeoff, pathfind to A, land, pickup package, takeoff, pathfind to Home, land, drop package, takeoff, pathfind to B,
	 land, pickup package, takeoff, pathfind to Home, land, drop package, DONE]

# execute preflight tasks
while !q.isEmpty():
# each instruction must be completed before the next can be polled from the queue
	curr_instruction = q.poll()
	if curr_instruction == ‘takeoff’:
		tello.takeoff()
	elif curr_instruction = ‘land’:
		tello.land()
	elif curr_instruction = pathfind to’:
		return_val = navigateDrone(location='A')
pathfind to A, lan