__author__ = "mlovati"
import random as rnd
deltalimit = 0
raw = open("C:/Users/Marco/Desktop/paintmatic/dipinto.ppm","r")
raw2 = raw.read()
lines = raw2.split("\n")
width = int(lines[1].split(" ")[0])
height = int(lines[1].split(" ")[1])
matrix_toedit = [[[]for m in range (0,width)]for n in range(0,height)]
for c in range(0,height):
    for b in range (0,width):
        matrix_toedit[c][b] = ["0","0","0"]
def makemat(list):
    width = int(list[1].split(" ")[0])
    height = int(list[1].split(" ")[1])
    mapa = list[3:]
    matrix = [[[]for m in range (0,width)]for n in range(0,height)]
    counter = 0
    c = 0
    # write a matrix[c][b] len(matrix[c][b])= 3 = rgb c height b width
    while c < height:
        b = 0
        while b < width:
            a = 0
            while a <= 2:
                matrix[c][b].append(mapa[counter])
                a += 1
                counter += 1
            b += 1
        c += 1
    return matrix

def stroke(matrix,radius,coord_x,coord_y,red,green,blue):
    changingarea = []
    matrix_c =[[[[],[],[]]for g in range(0,len(matrix[0]))] for i in range(0,len(matrix))]
    for a in range(0,len(matrix)): #height
        for b in range(0,len(matrix[a])): #width
            if ((coord_x-b)**2+(coord_y-a)**2)**0.5 < radius:
                changingarea.append((a,b)) 
                matrix_c[a][b][0]=(str(red))
                matrix_c[a][b][1]=(str(green))
                matrix_c[a][b][2]=(str(blue))
            else:
                matrix_c[a][b] = list(matrix[a][b])
    return matrix_c,changingarea
def evastroke(matrix,radius,coord_x,coord_y):
    changingarea = []
    for a in range(0,len(matrix)): #height
        for b in range(0,len(matrix[a])): #width
            if ((coord_x-b)**2+(coord_y-a)**2)**0.5 < radius:
                changingarea.append((a,b)) 
    return changingarea

def writer(mat_export):
    canvas = open("C:/Users/Marco/Desktop/paintmatic/dipinto_edited.ppm","w")
    canvas.write(lines[0] + "\n")
    canvas.write(lines[1] + "\n")
    canvas.write(lines[2] + "\n")
    for a in range (0,height):
        for b in range (0,width):
            for c in range (0,3):
                canvas.write(mat_export[a][b][c] + "\n")

def evaluator(original,imitation,strokearea):
    longcount = []
    for i in strokearea:
        a = i[0]
        b = i[1]
        difference = []
        for c in range(0,3):
            d = int(original[a][b][c])
            if len(imitation) == len(original):
                e = int(imitation[a][b][c])
            else:
                e = imitation[c]
            f = abs(d-e)
            difference.append(f)
        g = sum(difference)
        longcount.append(g)
    difference = sum(longcount)
    return difference

def hej(searchspace,deltalist,fitness_function, threshold = "empty"):
    # the threshold is the minimum value of the fitness function to proceed to the second delta
    def reachout(delta,centercoord):
        coordinates = {}
        coordinates["center"] = []
        for i in range(0,len(centercoord)):
            coordinates["center"].append(int(centercoord[i]))
        for i in searchspace:
            namepointl = "low "+str(searchspace.index(i))
            #coordinates[namepoint] = [int(coordinates["center"][g]) for g in range(0,len(coordinates["center"]))]
            coordinates[namepointl] = []
            for g in range(0,len(coordinates["center"])):
                coordinates[namepointl].append(int(coordinates["center"][g]))
            if int(delta*len(i)) < 1:
                coordinates[namepointl][searchspace.index(i)] -= int(1)
            else:
                coordinates[namepointl][searchspace.index(i)] -= int(delta*len(i))
            namepointh = "high "+str(searchspace.index(i))
            #coordinates[namepoint] = [int(coordinates["center"][g]) for g in range(0,len(coordinates["center"]))]
            coordinates[namepointh] = []
            for g in range(0,len(coordinates["center"])):
                coordinates[namepointh].append(int(coordinates["center"][g]))
            if int(delta*len(i)) < 1:
                coordinates[namepointh][searchspace.index(i)] += int(1)
            else:
                coordinates[namepointh][searchspace.index(i)] += int(delta*len(i))
        for i in coordinates.items():
            for g in range(0,len(i[1])):
                if i[1][g] > searchspace[g][-1]:
                    i[1][g] = searchspace[g][-1]
                if i[1][g] < searchspace[g][0]:
                    i[1][g] = searchspace[g][0]
        return coordinates 

    def findbest(coordict,fitness_function):
        deleturi = []
        for i in coordict.items():
            if i[0] != "center":
                counter = 0
                for g in i[1]:
                    if g == coordict["center"][i[1].index(g)]:
                        counter += 1
                if counter == len(i[1]):
                    deleturi.append(i[0])
        for i in deleturi:
            del coordict[i]
        maxname = "center"
        champion = float(fitness_function(coordict["center"]))
        listnames = []
        for i in coordict.keys():
            if i != "center":
                listnames.append(i)
        rnd.shuffle(listnames)
        # topchart = [[float(fitness_function(coordict[i])),i]for i in listnames]
        # sortedchart = sorted(topchart)
        # if champion >= sortedchart[-1][0]:
            # maxname = "center"
        # else:
            # maxname = sortedchart[-1][1]
        for i in listnames:
            if i != "center":
                challenger = float(fitness_function(coordict[i]))
                if challenger > champion:
                    maxname = i
                    champion = challenger
        return maxname
    
    level = 3
    counter = 0
    deltaind = 0
    while deltaind <= len(deltalist)-1:
        delta = deltalist[deltaind]
        below_threshold = "True"
        if counter >= level:
            coordinates = "null"
            break
        while below_threshold == "True":
            if counter >= level:
                below_threshold = "False"
                coordinates = "null"
                break
            else:
                below_threshold = "False"
                if delta == deltalist[0]:
                    center = []
                    for i in searchspace:
                            center.append(i[0]+int(len(i)*rnd.random()))
                while "hai" == "hai":
                    coordinates = reachout(delta,center)
                    best = findbest(coordinates,fitness_function)
                    if best == "center":
                        if delta != deltalist[-1]:
                            print("closer...")
                        deltaind += 1
                        break
                    else:
                        center = coordinates[best]
                        print("thinking...")
                if delta == deltalist[-1]:
                    if threshold != "empty":
                        if float(fitness_function(center)) < threshold:
                            print("wrong guess...")
                            below_threshold = "True"
                            deltaind = 0
                            delta = deltalist[deltaind]
                            counter +=1
    return coordinates

def fitnesspaint(inputlist):
    #lookhere = stroke(matrix_toedit,inputlist[0],inputlist[1],inputlist[2],inputlist[3],inputlist[4],inputlist[5])[1]#radius,coord_x,coord_y,red,green,blue
    lookhere = evastroke(matrix_toedit,inputlist[0],inputlist[1],inputlist[2])
    baseline = evaluator(matrix,matrix_toedit,lookhere)
    return baseline-evaluator(matrix,[inputlist[3],inputlist[4],inputlist[5]],lookhere)

matrix = makemat(lines)
searchspace = [[i for i in range(2,50)],[i for i in range(0,width+1)],[i for i in range(0,height+1)],[i for i in range(0,256)],[i for i in range(0,256)],[i for i in range(0,256)]]
deltalist = [1/3,1/6,1/12,0]
#minthreshold = -evaluator(matrix,matrix_toedit)

missedcount = -1
nostrokes = 0
strokelist = []
while missedcount <= nostrokes and nostrokes + missedcount <= 6000:
    coordinates = hej(searchspace,deltalist,fitnesspaint,1)
    if coordinates != "null":
        nostrokes += 1
        print("just stroked " + str(nostrokes))
        matrix_toedit = stroke(matrix_toedit,coordinates["center"][0],coordinates["center"][1],coordinates["center"][2],coordinates["center"][3],coordinates["center"][4],coordinates["center"][5])[0]
        #minthreshold = -evaluator(matrix,matrix_toedit)
        strokelist.append(coordinates["center"])
    else:
        missedcount += 1
        print("just missed " + str(missedcount))
print(nostrokes,missedcount,nostrokes-missedcount)
writer(matrix_toedit)
txtout = open("strokesjournal.dat","w")

for i in strokelist:
    for g in i:
        txtout.write(str(g)+",")
    txtout.write("\n")