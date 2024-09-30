#Made by Ayden F. G. Hart
#Version 0.1

#Including used python libraries
import json
import png #from pypng
from sympy import *
from sympy.parsing.sympy_parser import parse_expr
import os
from pathlib import Path
from time import time

#Definining all of the functions used in the program
def ArraytoPNGFormat(data):
    #PURPOSE: Converts data array from solved equations into data that can be convered into a png
    #HOW IT WORKS: data show come in as an rectangular matrix with entries being an integer or a float

    #finding maximum and minimum values to normalize from (-1 to 1)
        #negative numbers become red, positive numbers become blue
    max = 0; min = 0; absmax = 0
    for row in data:
        for entry in row:
            if entry > max: max = entry
            if entry < min: min = entry
    if abs(min) > max: absmax = abs(min)
    else: absmax = max
    print(str(min) +' to' + str(max))

    #normalize input array in floats from -1 to 1
    normalizedarray = [] #this is the array that will have normalized values
    for row in data:
        newrow = []
        for entry in row:
            if entry > 0:
                newrow.append(float(entry/(absmax)))
            else:
                if min != 0:
                    newrow.append(float(entry/(absmax)))
                else:
                    newrow.append(float(entry))
        normalizedarray.append(newrow)
    
    #converts the normalized array into the format that the png module uses to generate an image.
    newpngformatarray = []
    for row in normalizedarray:
        newrow = ()
        for entry in row:
            newrow += ColorShader(entry) #apply color filter / shader
        newpngformatarray.append(newrow)
    return(newpngformatarray)

def ColorShader(value):
    #Purpose: converts a single value to a colored RGB PNG format.
    #Needs value to be between -1 to 1
    #Output needs to be an integer value, or else it causes png module to error.
    #print(isinstance(value, float))
    if isinstance(value, float) != True: return( (0,255,0)) #if value isn't a float, return a green pixel
    if value < -1 or value > 1: return((0,255,0)) #if values are outside of normalized range, return a green pixel
    if value < 0: return( (int(abs(value)*255),0,0) ) #negative numbers are shaded red
    else: return( (0,0, int(abs(value)*255))) #positive numbers are shaded blue

def RenderIntoPNG(data, newfilename):
    if newfilename.endswith(".png") != True:newfilename+=".png"
    newfilepath = os.path.join(os.getcwd(), newfilename)
    print("New image file will be: " + str(newfilepath))
    if len(data[0])%3 != 0: print("Invalid format width"); pass #will prevent some issues if input array is wrong size
    with open(newfilepath, 'wb') as imgfile:
        writer = png.Writer(int(len(data[0])/3), int(len(data)), greyscale=False)
        writer.write(imgfile, data)

def CalculateArray(size, center, targg):
    #size: [width,height]

   #Import compiled equations file.
        #load compiled.json
    compiledfilepath = os.path.join(os.getcwd(), "compiled.json")
    with open(compiledfilepath, 'r') as openfile:
        compiledfile = json.load(openfile)

    #create an empty rectangular array
    amplitudematrix = []
    rows = size[1]; columns = size[0]
    print (str(rows) + 'x' + str(columns) + ' matrix')
    starttime = time()
    xoffset = -int(columns/2) + center[0]; yoffset = -int(rows/2) - center[1]

    for i in range(rows): #looping through y values
        newrow = []
        for j in range(columns): #looping through x values
            k = 0
            #summing all equations outputs into a single amplitude for the point at which these calculations are happening
            for l in range(len(compiledfile)): #looping through all equations
                    #calculating amp and adding it.
                    k += CalculateValueAtPoint(compiledfile[l], j+xoffset, i+yoffset, targg)
            #debugging to show what (x,y) coordinate the program is at and what values is being associated at that point
            print("("+str(j+xoffset)+","+str(i+yoffset)+"): "+str(k)); newrow.append(k)
        amplitudematrix.append(newrow)

    #calculating the amount of time taken
    endtime = time()
    print("time elapsed: "+str(int(endtime-starttime))+"s")
    return(amplitudematrix)

    #parse each equation individually and add the values of all point to the things
    
def CalculateValueAtPoint(confinedeq,xarg,yarg,targ):
    equation = confinedeq["equation"]
    conditions = confinedeq["condition"]
    position = confinedeq["position"]
    zoom = 2; xarg = xarg/zoom; yarg = yarg/zoom
    x,y,r,t = symbols("x,y,r,t")
    #calculating radius as radius is used quite a lot
    rvalue = N(sqrt((xarg-position[0])**2 + (yarg-position[1])**2))
    validatpoint = True #Start assuming conditions are true.
    #loop through all of the provided conditions for the equations
    for condition in conditions:
        #parsing the condition string into a sympy equation
        condition = parse_expr(condition)

        #if the condition is incorrect at the coordinates, then the equation is not valid.
        if condition.subs({x: xarg, y: yarg, r: rvalue, t:targ}) == False: validatpoint=False
    #if all of the conditions are true, return the equations with the values subbed.
    if validatpoint == True:
        try:
            return(round(float(parse_expr(equation).subs({x: xarg, y: yarg, r: rvalue,t:targ})),6))
        except:
            print("Calculation Error in C.V.a.P.")
            return(0)
    #if the conditions arent meant, return a 0
    else: return(0)

#Import configs to determine what the program will do
    #Will it import a setup and compile?
    #Run type
        # 0 = render
        # 1 = solve eqs, render
        # 2 = import setup file compile, solve eqs, render

#Importing setup file to run

#Compiling setup file into a setup of equations to run
    #Save set of compiled equations to a compiled.json file

#Solving the equation set from compiled.py at all of the points that will be rendered

#Rendering all of the outputs into an image
 
computeddataarray = CalculateArray([32,32],[20,20],0)
#print(computeddataarray)
RenderIntoPNG(ArraytoPNGFormat(computeddataarray), "TestOutput")
