#Áramkör szimuláció
#
#Készíts programot, ami leszimulálja az erőforrások lefoglalását és felszabadítását a JSON fájlban megadott topológia, kapacitások
#és igények alapján!
#
#Teszteléshez json file: cs1.json
#
#Script paraméterezése: python3 client.py cs.json
#
#A program kimenete:
#
# esemény sorszám. < esemény név >: < node1 > <-> < node2 > st:< szimuálciós idő > [- < sikeres/sikertelen >] 
#
#Pl.:
#
#1. igény foglalás: A<->C st:1 – sikeres
#2. igény foglalás: B<->C st:2 – sikeres
#3. igény felszabadítás: A<->C st:5
#4. igény foglalás: D<->C st:6 – sikeres
#5. igény foglalás: A<->C st:7 – sikertelen
#


import json
import sys
import subprocess

file = open(sys.argv[1], "r")
data = json.load(file)
file.close()
duration = data["simulation"]["duration"]
szamlalo = 1
nem_utkozik = [
    "ACBC",
    "BCAC",
    "BCAD",
    "BCDC",
    "CADC",
    "ADBC",
    "DCCA",    
    "DCBC"
]

def s(a, b, c, d):
    str = ""
    str+=a
    str+=b
    str+=c
    str+=d
    return str

def true(k):
    t = True
    for i in k:
        if i == False:
            return False
    return t

igaze = []
def isPairs(a, b, c, d):
    for i in nem_utkozik:
        if i == s(a, b, c, d):
            return True

#print(true([True, True, False]))
sns = True
futo = []
for i in range(0, duration):
    for j in range(0, len(data["simulation"]["demands"])):
        time1 = data["simulation"]["demands"][j]["start-time"]
        time2 = data["simulation"]["demands"][j]["end-time"]
        A = data["simulation"]["demands"][j]["end-points"][0]
        B = data["simulation"]["demands"][j]["end-points"][1]
        if i == data["simulation"]["demands"][j]["start-time"]:
            if len(futo) == 0:
                print(szamlalo, 'igeny foglalas:', A, "<->", B, 'st:', time1, "sikeres")
                futo.append([A, B])
                szamlalo+=1
                #print(futo)
            else:
                for z in range(0, len(futo)):
                    sns = isPairs(A, B, futo[z][0], futo[z][1])
                if sns:
                    print(szamlalo, 'igeny foglalas:', A, "<->", B, 'st:', time1, "sikeres")
                    futo.append([A, B])
                    szamlalo+=1
                    #print(futo)
                else:
                    print(szamlalo, "igeny foglalas: ", A, "<->", B, "st:", time1, "sikertelen")
                    szamlalo+=1
                    #print(futo)
        elif i == data["simulation"]["demands"][j]["end-time"] and [A, B] in futo:
            print(szamlalo, 'igeny felszabaditas:', A, "<->", B, 'st:', time2)
            futo.remove([A, B])
            szamlalo += 1 
            #print(futo)         


# Említett cs1.json file tartalma:
'''
{
	"end-points": [ "A", "B", "C", "D" ],
	"switches": [ "S1", "S2", "S3", "S4" ],
	"links" : [
		{
			"points" : [ "A", "S1" ],
			"capacity" : 10.0
		},
                {
                        "points" : [ "B", "S2" ],
                        "capacity" : 10.0
                },
                {
                        "points" : [ "D", "S4" ],
                        "capacity" : 10.0
                },
                {
                        "points" : [ "S1", "S4" ],
                        "capacity" : 10.0
                },
                {
                        "points" : [ "S1", "S3" ],
                        "capacity" : 10.0
                },
                {
                        "points" : [ "S2", "S3" ],
                        "capacity" : 10.0
                },
                {
                        "points" : [ "S4", "C" ],
                        "capacity" : 10.0
                },
                {
                        "points" : [ "S3", "C" ],
                        "capacity" : 10.0
                }
	],
	"possible-circuits" : [
		["D", "S4", "C"],
		["C", "S4", "D"],
		["A", "S1", "S4", "C"],
		["A", "S1", "S3", "C"],
		["C", "S4", "S1", "A"],
		["C", "S3", "S1", "A"],
		["B", "S2", "S3", "C"],
		["C", "S3", "S2", "B"],
		["B", "S2", "S3", "S1", "A"],
		["A", "S1", "S3", "S2", "B"],
		["D", "S4", "S1", "S3", "S2", "B"],
		["B", "S2", "S3", "S1", "S4", "D"],
		["A", "S1", "S4", "D"],
		["D", "S4", "S1", "A"]
	],
	"simulation" : {
		"duration" : 11,
		"demands" : [
			{
				"start-time" : 1,
				"end-time" : 5,
				"end-points" : ["A", "C"],
				"demand" : 10.0
			},
			{
				"start-time" : 2,
				"end-time" : 10,
				"end-points" : ["B", "C"],
				"demand" : 10.0
			},
                        {
                                "start-time" : 6,
                                "end-time" : 10,
                                "end-points" : ["D", "C"],
                                "demand" : 10.0
                        },
                        {
                                "start-time" : 7,
                                "end-time" : 10,
                                "end-points" : ["A", "C"],
                                "demand" : 10.0
                        }
		]
	}
}
'''