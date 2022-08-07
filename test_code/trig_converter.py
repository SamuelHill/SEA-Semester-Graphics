import math

#One set of arrows per lat x long. Depth and degree may become a 2D array.
def vectorizeADCParrows(BoundingBox, ADCP_lat, ADCP_long, ADCP_depth, ADCP_degree):
	#To keep variable passing short, bounding box will be an
	#array of the following form: (will be determined ahead, to match graph)
	#	BoundingBox = [upper_lat, lower_lat, upper_long, lower_long]
	upper_lat = BoundingBox[0]
	lower_lat = BoundingBox[1]
	upper_long = BoundingBox[2]
	lower_long = BoundingBox[3]
	#Decide bounds for 8 ranges of angles:
	#	First, for simplisity and lack of duplication: (side lengths)
	dist_to_uplat = upper_lat - ADCP_lat
	dist_to_lolat = ADCP_lat - lower_lat
	dist_to_uplon = upper_long - ADCP_long
	dist_to_lolon = ADCP_long - lower_long
	#	These are used as the opposite and adjacent in place of:
	#		oct_2_opp = upper_lat - lat
	#		oct_2_adj = long - lower_long
	#		oct_2_X = oct_2_opp/oct_2_adj
	#	Starting at the upper left and moving to the quadrant dividers:
	oct_1_theta = 270.0
	oct_3_theta = 0.0
	oct_5_theta = 90.0
	oct_7_theta = 180.0
	#	Then finding the divisions of those quadrants (the octants):
	oct_2_X = dist_to_uplat/dist_to_lolon
	oct_2_theta = oct_1_theta + math.degrees(math.atan(oct_2_X))
	oct_4_X = dist_to_uplat/dist_to_uplon
	oct_4_theta = math.degrees(math.atan(oct_4_X))
	oct_6_X = dist_to_lolat/dist_to_uplon
	oct_6_theta = oct_5_theta + math.degrees(math.atan(oct_6_X))
	oct_8_X = dist_to_lolat/dist_to_lolon
	oct_8_theta = oct_1_theta - math.degrees(math.atan(oct_8_X))
	
	if ADCP_degree == oct_1_theta:
		return [ADCP_lat, lower_long, ADCP_depth]
	elif ADCP_degree > oct_1_theta and ADCP_degree < oct_2_theta:
		adjusted_angle = ADCP_degree - oct_1_theta
		return_lat = ADCP_lat + oppositeSide(adjusted_angle, dist_to_lolon)
		return [return_lat, lower_long, ADCP_depth]
	elif ADCP_degree == oct_2_theta:
		return [upper_lat, lower_long, ADCP_depth]
	elif ADCP_degree > oct_2_theta:
		#normally: adjusted_angle = ADCP_degree - oct_2_theta, but we want the
		#other side of the split and the top angle is 0.0, not 360 (which we need).
		adjusted_angle = 360.0 - ADCP_degree
		return_lon = ADCP_long - oppositeSide(adjusted_angle, dist_to_uplat)
		return [upper_lat, return_lon, ADCP_depth]
	elif ADCP_degree == oct_3_theta:
		return [upper_lat, ADCP_long, ADCP_depth]
	elif ADCP_degree > oct_3_theta and ADCP_degree < oct_4_theta:
		#normally: adjusted_angle = ADCP_degree - oct_3_theta, but it's 0...
		return_lon = ADCP_long + oppositeSide(ADCP_degree, dist_to_uplat)
		return [upper_lat, return_lon, ADCP_depth]
	elif ADCP_degree == oct_4_theta:
		return [upper_lat, upper_long, ADCP_depth]
	elif ADCP_degree > oct_4_theta and ADCP_degree < oct_5_theta:
		adjusted_angle = oct_5_theta - ADCP_degree
		return_lat = ADCP_lat + oppositeSide(adjusted_angle, dist_to_uplon)
		return [return_lat, upper_long, ADCP_depth]
	elif ADCP_degree == oct_5_theta:
		return [ADCP_lat, upper_long, ADCP_depth]
	elif ADCP_degree > oct_5_theta and ADCP_degree < oct_6_theta:
		adjusted_angle = ADCP_degree - oct_5_theta
		return_lat = ADCP_lat - oppositeSide(adjusted_angle, dist_to_uplon)
		return [return_lat, upper_long, ADCP_depth]
	elif ADCP_degree == oct_6_theta:
		return [lower_lat, upper_long, ADCP_depth]
	elif ADCP_degree > oct_6_theta and ADCP_degree < oct_7_theta:
		adjusted_angle = oct_7_theta - ADCP_degree
		return_lon = ADCP_long + oppositeSide(adjusted_angle, dist_to_lolat)
		return [lower_lat, return_lon, ADCP_depth]
	elif ADCP_degree == oct_7_theta:
		return [lower_lat, ADCP_long, ADCP_depth]
	elif ADCP_degree > oct_7_theta and ADCP_degree < oct_8_theta:
		adjusted_angle = ADCP_degree - oct_7_theta
		return_lon = ADCP_long - oppositeSide(adjusted_angle, dist_to_lolat)
		return [lower_lat, return_lon, ADCP_depth]
	elif ADCP_degree == oct_8_theta:
		return [lower_lat, lower_long, ADCP_depth]
	elif ADCP_degree > oct_8_theta and ADCP_degree < oct_1_theta:
		adjusted_angle = oct_1_theta - ADCP_degree
		return_lat = ADCP_lat - oppositeSide(adjusted_angle, dist_to_lolon)
		return [return_lat, lower_long, ADCP_depth]

def oppositeSide(inner_angle, scalar):
	return math.tan(math.radians(inner_angle)) * scalar

###############################################################################
#                                 METHOD CALL                                 #
###############################################################################

#ADCP data:
#	ADCP_lat = -1.75
#	ADCP_long = -175.0
#	ADCP_depth = 0
#	ADCP_degree = 300
#	*Not yet sure about magnitude...*
#	ADCP_mag = 12

for x in range(0,360):
	UVW = vectorizeADCParrows([-1.0, -2.5, -174.25, -175.75], -1.75, -175.0, 0.0, x)
	print UVW