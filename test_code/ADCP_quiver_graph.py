#DOES NOT WORK

import fileinput
import datetime
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#######################################################################################
#                                       TO DO:                                        #
#######################################################################################

#UPDATE chooseADCPbyPOSITION() FUNCTION TO TRANSLATE MAGNITUDE INTO A COLOR AND/OR A
#	LINE LENGTH (both as arrays that corresond to the xyzuvw...) USING A FOR LOOP AFTER
#	ALL THE POINTS HAVE BEEN CHOOSEN. THIS IS BECAUSE WE WANT THE MIN AND MAX OF THE 
#	MAGNITUDES WITHIN THE BOX, NOT OF THE TOTAL TRIP.
#	THIS COULD POSSIBLY BE COMBINED WITH THE GRAPHING STUFF BELOW...?
#		MAGNITUDES - scale = mm/s

#FOR PLOTTING WE WILL NEED TO COMBINE ALL THE X, Y, Z, U, V, W, AND magnitudes INTO
#	ONE BIG ARRAY... THAT CAN BE DONE IN A NESTED LOOP JUST BEFORE GRAPHING
#	AS WELL, WE WILL NEED TO LOOP THROUGH THE POINTS AND ASSOCIATED COLORS AND LENGTHS
#	SO THAT EACH 'QUIVER' WILL BE A DISTINCT COLOR
#		BASED OFF OF THIS, COULD WE CHOOSE BINNING AS WELL?
#			- AVERAGED OVER A CERTAIN DISTANCE?
#			- ONLY SELECT THAT BIN?

#CHANGE ALL OF THIS TO A CLASS STRUCTURE...

#######################################################################################
#                                     USER INPUT                                      #
#######################################################################################

#Bounding box will be an array of the following form:
#	BoundingBox = [upper_lat, lower_lat, upper_long, lower_long]
#This will be determined ahead of time, so that all parts of the graph match.
#	E.g. Windslow:
#		BoundingBox = [-1.0, -2.5, -174.25, -175.75]
#	General cruise track:
#		BoundingBox = [25, 0, -147, -172]
#However, since this is passed into our choosing by postion and
#vectorizing methods it will simply be called box
box = []

#Bin size variable? - work out averaging...

#######################################################################################
#                                 ADCP DATA PROCESSING                                #
#######################################################################################

#To combine bins 1-30 and 31-60... Put them in tuples and process in pairs.
#These files are originally only half the bins because they are so large.
all_adcp_files = [("ADCP_txt_files/ADCP_S261001_1-23_1-30.txt", "ADCP_txt_files/ADCP_S261001_1-23_31-60.txt"), ("ADCP_txt_files/ADCP_S261001_24-170_1-30.txt", "ADCP_txt_files/ADCP_S261001_24-170_31-60.txt"), ("ADCP_txt_files/ADCP_S261001_171-242_1-30.txt", "ADCP_txt_files/ADCP_S261001_171-242_31-60.txt"), ("ADCP_txt_files/ADCP_S261001_243-389_1-30.txt", "ADCP_txt_files/ADCP_S261001_243-389_31-60.txt"), ("ADCP_txt_files/ADCP_S261001_390-482_1-30.txt", "ADCP_txt_files/ADCP_S261001_390-482_31-60.txt"), ("ADCP_txt_files/ADCP_S261001_483-626_1-30.txt", "ADCP_txt_files/ADCP_S261001_483-626_31-60.txt")]

#Stuff I need from headers of the ADCP files:
#	"1st Bin Range (m) = "	18.68
#	"Bin Size (m) ="	10.00
start_depth = 18.68
depths = [(start_depth + (x * 10)) for x in range(0,60)]
#This builds the depths that each bin is at, though not all will always be used.

#"Database", collected from all fies
all_adcp_data = []
#Selected by location...
adcp_data_to_use = []

def processADCPfiles():
	#Takes ens number, date, and location from first file
	#	(second should be the same)
	metadata = []
	#Get directions and magnitudes from first file - bins 1-30
	first_directions = []
	first_magnitudes = []
	#Get directions and magnitudes from second file - bins 31-60
	second_directions = []
	second_magnitudes = []
	#The 1-30 and 31-60 files have been paired as tuples
	for file_pair in all_adcp_files:
		#The enumeration allows me to skip header and blank lines...
		#Could read as a tsv, but it was finicky when trying the csv library so,
		for i, line in enumerate(fileinput.input(file_pair[0])): #use standard file input
			row = line.split('\t') #and split by tabs
			data = [] #temporary data holder for ens, date, and location
			if i > 15: #skip header lines - unnecessary
				data.append(int(row[0])) #ensemble number
				#To give it proper datetime format, otherwise it is just '15' for 2015
				year = (int(row[1]) + 2000)
				#Format the year, month, day etc. as a datetime unit
				date = datetime.datetime(year, int(row[2]), int(row[3]),
								int(row[4]), int(row[5]), int(row[6]), 0)
				data.append(date)
				positions = row[159:163]
				#The positions are at the end of the row...
				positions[3] = positions[3].strip('\r\n')
				#We could add the positions as is from the file, but the file gives
				#us a first coordinate, and a last coordinate, so to map this we want
				#the midpoint of the two...
				latitude = (float(positions[0]) + float(positions[2])) / 2
				longitude = (float(positions[1]) + float(positions[3])) / 2
				data.append([latitude, longitude])
				metadata.append(data)
				#Gets the direction and magnitude of the first 30 bins...
				first_directions.append(row[129:159])
				first_magnitudes.append(row[99:129])
		#Looking at the second file in the pair... (ens = ens, bins != bins)
		for i, line in enumerate(fileinput.input(file_pair[1])):
			row = line.split('\t')
			if i > 15:
				#Gets the direction and magnitude of the second 30 bins...
				second_directions.append(row[129:159])
				second_magnitudes.append(row[99:129])
	#Then combine all of the metadata, directions, and magnitudes
	for i in range(0, len(metadata)):
		#I could make all of the parts (ens, date, position...) into variables,
		#and then append them in the form [ens, date, ...] to all_adcp_data, but
		#appending them to temp works just as well and I have commented what
		#the various parts of these arrays are.
		temp = []
		temp.append(metadata[i][0]) #ens
		temp.append(metadata[i][1]) #date
		dir = []
		mag = []
		for j in range(0,2): #To distinguish between the two files
			for k in range(0,30):
				if j == 0:
					dir.append(float(first_directions[i][k]))
					mag.append(float(first_magnitudes[i][k]))
				if j == 1:
					#to address - BUG: NOT ALL DEPTHS HAVE DIRECTIONS...
					if second_directions[i][k] != '':
						dir.append(float(second_directions[i][k]))
						mag.append(float(second_magnitudes[i][k]))
		temp.append(metadata[i][2]) #positions: [lat, long]
		temp.append(depths[0:len(dir)]) #Z, adjusted to number of valid depths
		temp.append(dir)
		temp.append(mag)
		all_adcp_data.append(temp)

#Self explanitory... Only chooses the bits of data that fit within our graph
#Calls on vectorize because at this point we know what the box will be,
#and we might as well kill two birds with one stone...
def chooseADCPbyPOSITION(BoundingBox):
	max_mag = 0
	min_mag = 1000
	for data in all_adcp_data:
		if data[2][1] < BoundingBox[2] and data[2][1] > BoundingBox[3]:
			if data[2][0] < BoundingBox[0] and data[2][0] > BoundingBox[1]:
				ens = data[0]
				date = data[1]
				#Make it the size of dir array, could use the depths, dir, or mag
				#because they are all three already agjusted. I choose 3 arbitrarily.
				#THIS COULD ALSO BE VARIABLE BASED ON THE BIN SIZE...
				X = [data[2][0]] * len(data[3])
				Y = [data[2][1]] * len(data[3])
				Z = data[3]
				[U, V] = vectorizeADCParrows(BoundingBox, [data[2][0],data[2][1]], data[4])
				W = Z
				magnitudes = data[5]
				if max_mag > max(magnitudes):
					max_mag = max(magnitudes)
				if min_mag < min(magnitudes):
					min_mag = min(magnitudes)
				adcp_data_to_use.append([ens, date, X, Y, Z, U, V, W, magnitudes])
	for i in range(0,len(adcp_data_to_use)):
		#Translate magnitudes to length and colors...
		#Possibly use white to red? or blue to red...
		adcp_data_to_use[i][9]

#Creates the positions of where the current direction hits the edge
#	of our bounding box. One set of arrows per lat x long.
def vectorizeADCParrows(BoundingBox, ADCP_position, ADCP_degrees):
	#Grabs positions from bounding box...
	upper_lat = BoundingBox[0]
	lower_lat = BoundingBox[1]
	upper_long = BoundingBox[2]
	lower_long = BoundingBox[3]
	#Decide bounds for 8 "ranges of angles" (There are 8 "ranges of angles" because
	#we only know our position within the bounding box and the position of the box
	#itself, and to have a vector point at something within the graph we need it
	#to point at an edge. So, to accomplish this we need to keep the calculations
	#limited to our box, and to do so we need triangles. There may be other ways
	#to do this, but when drawing a box with a single point in it and that point
	#is pointing in a direction, the easy way I could imagine to find a second
	#point for the line - because as we know a line has at least 2 points - was
	#by using the edges of the box. And from that, to figure out position on an
	#edge, the only information to use comes from distances to those sides and
	#the angle of the current. In all, this divides the bounding box up into 8
	#triangles... There might be a way to do this with 4 triangles but for the
	#time being this works.):
	#	First, for lack of redundancy, we get the lengths from our position
	#	to various edges:
	ADCP_lat = ADCP_position[0]
	ADCP_long = ADCP_position[1]
	dist_to_uplat = upper_lat - ADCP_lat
	dist_to_lolat = ADCP_lat - lower_lat
	dist_to_uplon = upper_long - ADCP_long
	dist_to_lolon = ADCP_long - lower_long
	#	These are used as the adjacent side in our triangles to help find the
	#	opposite side:
	#		tan(theta) = opp/adj          OR          adj * tan(theta) = opp
	#	We then make our quadrant dividers which correspond to cardinal directions:
	oct_1_theta = 270.0 #Due West
	oct_3_theta = 0.0 #Due North
	oct_5_theta = 90.0 #Due East
	oct_7_theta = 180.0 #Due South
	#	Then we find the divisions of those quadrants (the octants):
	#		These dirrectly correspond to the corners the bounding box
	oct_2_X = dist_to_uplat/dist_to_lolon
	oct_2_theta = oct_1_theta + math.degrees(math.atan(oct_2_X))
	oct_4_X = dist_to_uplat/dist_to_uplon
	oct_4_theta = math.degrees(math.atan(oct_4_X))
	oct_6_X = dist_to_lolat/dist_to_uplon
	oct_6_theta = oct_5_theta + math.degrees(math.atan(oct_6_X))
	oct_8_X = dist_to_lolat/dist_to_lolon
	oct_8_theta = oct_1_theta - math.degrees(math.atan(oct_8_X))
	#Now we process all of the current directions to determine the coordinates
	#in which they hit an edge. These are labeled U and V becuase when graphing
	#X, Y, and Z correspond to longitude, latitude, and depths. For creating
	#vectors (or as matplotlib calls this kind of 3D graph quivers), we then need
	#U, V, and W which are the longitude, latitude, and depth at which our vector
	#hits an edge. W will always equal Z because we cannot discern any upward
	#movement of current. If we can, then we will have to write an algorithm for
	#adjusting this...
	U = [] #longitude of where line will point (on an edge of the box)
	V = [] #latitude of where line will point...
	for i in range(0,len(ADCP_degrees)):
		#The order in which these triangular 'octants' are evaluated is relatively
		#	arbitrary, as it is based off of the numbering system I used when drawing
		#	out the possible coordinate grid... However, within each octant, I wanted
		#	to use the same trigonometric formula for finding where the direction of
		#	current would hit an edge. So, each octant has a slightly different format
		#	for calculating the position of where we hit an edge, but they all use the
		#	same oppositeSide() formula. 8 of these if statements below are when an
		#	angle hits our precalculated octant division, and as such corresponds to
		#	either a cardinal direction, or a corner of the bounding box. Otherwise,
		#	the oppositeSide() formula is used to calculate position.
		#Due West
		if ADCP_degrees[i] == oct_1_theta:
			U.append(lower_long)
			V.append(ADCP_lat)
		#Angles between due west and top left of bounding box
		elif ADCP_degrees[i] > oct_1_theta and ADCP_degrees[i] < oct_2_theta:
			adjusted_angle = ADCP_degrees[i] - oct_1_theta
			return_lat = ADCP_lat + oppositeSide(adjusted_angle, dist_to_lolon)
			U.append(lower_long)
			V.append(return_lat)
		#Top left corner of bounding box
		elif ADCP_degrees[i] == oct_2_theta:
			U.append(lower_long)
			V.append(upper_lat)
		#Angles between top left of bounding box and due north
		elif ADCP_degrees[i] > oct_2_theta:
			#normally: adjusted_angle = ADCP_degrees[i] - oct_2_theta, but we want the
			#other side of the split and the top angle is 0.0, not 360 (which we need).
			adjusted_angle = 360.0 - ADCP_degrees[i]
			return_lon = ADCP_long - oppositeSide(adjusted_angle, dist_to_uplat)
			U.append(return_lon)
			V.append(upper_lat)
		#Due North
		elif ADCP_degrees[i] == oct_3_theta:
			U.append(ADCP_long)
			V.append(upper_lat)
		#Angles between due north and top right of bounding box 
		elif ADCP_degrees[i] > oct_3_theta and ADCP_degrees[i] < oct_4_theta:
			#normally: adjusted_angle = ADCP_degrees[i] - oct_3_theta, but it's 0...
			return_lon = ADCP_long + oppositeSide(ADCP_degrees[i], dist_to_uplat)
			U.append(return_lon)
			V.append(upper_lat)
		#Top right corner of bounding box
		elif ADCP_degrees[i] == oct_4_theta:
			U.append(upper_long)
			V.append(upper_lat)
		#Angles between top right corner of bounding box and due east
		elif ADCP_degrees[i] > oct_4_theta and ADCP_degrees[i] < oct_5_theta:
			adjusted_angle = oct_5_theta - ADCP_degrees[i]
			return_lat = ADCP_lat + oppositeSide(adjusted_angle, dist_to_uplon)
			U.append(upper_long)
			V.append(return_lat)
		#Due East
		elif ADCP_degrees[i] == oct_5_theta:
			U.append(upper_long)
			V.append(ADCP_lat)
		#Angles between due east and bottom right corner of bounding box
		elif ADCP_degrees[i] > oct_5_theta and ADCP_degrees[i] < oct_6_theta:
			adjusted_angle = ADCP_degrees[i] - oct_5_theta
			return_lat = ADCP_lat - oppositeSide(adjusted_angle, dist_to_uplon)
			U.append(upper_long)
			V.append(return_lat)
		#Bottom right corner of bounding box
		elif ADCP_degrees[i] == oct_6_theta:
			U.append(upper_long)
			V.append(lower_lat)
		#Angles between bottom right corner of bounding box and due south
		elif ADCP_degrees[i] > oct_6_theta and ADCP_degrees[i] < oct_7_theta:
			adjusted_angle = oct_7_theta - ADCP_degrees[i]
			return_lon = ADCP_long + oppositeSide(adjusted_angle, dist_to_lolat)
			U.append(return_lon)
			V.append(lower_lat)
		#Due South
		elif ADCP_degrees[i] == oct_7_theta:
			U.append(ADCP_long)
			V.append(lower_lat)
		#Angles between due south and bottom left corner of bounding box
		elif ADCP_degrees[i] > oct_7_theta and ADCP_degrees[i] < oct_8_theta:
			adjusted_angle = ADCP_degrees[i] - oct_7_theta
			return_lon = ADCP_long - oppositeSide(adjusted_angle, dist_to_lolat)
			U.append(return_lon)
			V.append(lower_lat)
		#Bottom left corner of bounding box
		elif ADCP_degrees[i] == oct_8_theta:
			U.append(lower_long)
			V.append(lower_lat)
		#Angles between bottom left corner of bounding box and due west
		elif ADCP_degrees[i] > oct_8_theta and ADCP_degrees[i] < oct_1_theta:
			adjusted_angle = oct_1_theta - ADCP_degrees[i]
			return_lat = ADCP_lat - oppositeSide(adjusted_angle, dist_to_lolon)
			U.append(lower_long)
			V.append(return_lat)
	return [U, V]

#Used to determine the length of the opposite side of a triangle:
#	This is used because we know our position within the bounding box,
#	and with this we can determine our distances from the edges. As well,
#	the direction of the current in degrees is given by the ADCP. With
#	these two pieces of information we can find the length from our location
#	(carried over to the nearest relevant edge - for explanation look in
#	vectorizeADCParrows) to determine position of where the current hits an edge.
def oppositeSide(inner_angle, scalar):
	return math.tan(math.radians(inner_angle)) * scalar

###############################################################################
#                               METHOD CALLS:                                 #
#                               PREP DATABASE                                 #
###############################################################################

processADCPfiles() #prep all_adcp_data
#print all_adcp_data

#Just curious as to how many data points are in here
#data_points = 0
#for i in range(0,len(all_adcp_data)):
#	for j in range(0,len(all_adcp_data[i])):
#		data_points += 4 #metadata...
#		data_points += (len(all_adcp_data[i][3]) * 3)
#print data_points

#chooseADCPbyPOSITION(box) #prep adcp_data_to_use

###############################################################################
#                                   GRAPH                                     #
###############################################################################

#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')

#ax.quiver(X, Y, Z, U, V, W)
#	OR
#c = ['g','r','b']
#l = [1,2,3]
#for i in range(0,len(X_quiv)):
#	ax.quiver(X[i], Y[i], Z[i], U[i], V[i], W[i], length = l[i], colors = c[i])

#plt.show()