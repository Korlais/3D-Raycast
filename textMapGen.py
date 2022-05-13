import random

def mapGen(theFile, theLen, wallChance):
	#randomly generates characters and saves it to the specificed file
	#will always generate a one-character-wide border
	wallChance = 100/wallChance
	str = ""
	theMap = open(theFile, "w")

	for y in range(theLen): 

		if (y == 0) or (y==theLen-1):	#if it's the top or bottom row, make a border
			str += "X" * theLen

		for x in range(theLen):
			character = random.randint(0, wallChance)

			if (y != 0) and (y != theLen-1):	#does not generate new walls if there's already a top or bottom border
				if (character == 0) or (x % theLen == 0) or (x % theLen == theLen-1):	#generates wall at first and last position of every line to create borders
					str += "X"
				else:
					str += "_"
		str += "\n"
	theMap.write(str)