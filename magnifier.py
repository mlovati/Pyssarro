def writer(mat_export):
	canvas = open("C:/Users/Marco/Desktop/paintmatic/dipinto_magnified.ppm","w")
	canvas.write(lines[0] + "\n")
	canvas.write(str(width) +" "+ str(height) + "\n")
	canvas.write(lines[2] + "\n")

	for a in range (0,height):
		for b in range (0,width):
			for c in range (0,3):
				canvas.write(mat_export[a][b][c] + "\n")

def stroke(matrix,radius,coord_x,coord_y,red,green,blue):
	matrix_c =[[[]for g in range(0,len(matrix[0]))] for i in range(0,len(matrix))]
	for a in range(0,len(matrix)):
		for b in range(0,len(matrix[a])):
			matrix_c[a][b] = matrix[a][b][0:len(matrix[a][b])]
	for c in range(0,height):
		for b in range (0,width):
			if ((coord_x-b)**2+(coord_y-c)**2)**0.5 < radius:
				#if (c**2+b**2)**0.5 < radius:
				matrix_c[c][b][0]=(str(red))
				matrix_c[c][b][1]=(str(green))
				matrix_c[c][b][2]=(str(blue))
	return matrix_c

raw = open("C:/Users/Marco/Desktop/paintmatic/dipinto.ppm","r")
raw2 = raw.read()
lines = raw2.split("\n")
width = int(lines[1].split(" ")[0])
height = int(lines[1].split(" ")[1])

raw_instructions = open("C:/Users/Marco/Desktop/paintmatic/strokesjournal.dat","r")
raw_inst2 = raw_instructions.read()
lines_inst = raw_inst2.split("\n")
del lines_inst[-1]
strokelist = []#[] for i in range(0,len(lines_inst))]
for a in lines_inst:
	strokelist.append(lines_inst[lines_inst.index(a)].split(",")[:-1])

magnification = 10
height = height * magnification
width = width * magnification
matrix_mag = [[[]for m in range (0,width)]for n in range(0,height)]
for c in range(0,height):
	for b in range (0,width):
		greyscale = str(int(c*b/(height*width)*255))
		matrix_mag[c][b] = ["0","0","0"]

for i in strokelist:
	print(i)
	for g in range(0,len(i)-3):
		i[g] = float(float(i[g]) * magnification)
	matrix_mag = stroke(matrix_mag, i[0], i[1], i[2], i[3], i[4], i[5])
writer(matrix_mag)