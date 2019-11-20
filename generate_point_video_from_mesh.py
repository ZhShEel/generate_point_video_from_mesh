import os
import sys
import argparse
import math
import random

parser = argparse.ArgumentParser()
parser.description = "input args: origin_mesh_file(-mesh) output_folder(-output) file_number(-number)\n"
parser.add_argument("-mesh", help = "format is .ply", dest="mesh_path")
parser.add_argument("-output", help = "target is a folder", dest="output_folder")
parser.add_argument("-number", help = "input a int", dest="file_number", type = int)
args = parser.parse_args()

mesh_path = args.mesh_path
output_folder = args.output_folder
file_number = args.file_number

mesh = open(mesh_path,"rb")
for i in range(4):
    line = mesh.readline()
vertex_number = int(line.split()[2])
for i in range(4):
    line = mesh.readline()
face_number = int(line.split()[2])
for i in range(2):
    line = mesh.readline()

#1.get the bounding box
min_x = 999999
min_y = 999999
min_z = 999999
max_x = -999999
max_y = -999999
max_z = -999999
for i in range(vertex_number):
    line = mesh.readline()
    x = float(line.split()[0])
    y = float(line.split()[1])
    z = float(line.split()[2])
    if x > max_x:
        max_x = x
    if x < min_x:
        min_x = x
    if y > max_y:
        max_y = y
    if y < min_y:
        min_y = y
    if z > max_z:
        max_z = z
    if z < min_z:
        min_z = z

#2.assume camera capsures points with uniform speed, then divide the whole bbx into several pieces,
#each time moves 1/8 of bbx's edge length
sub_bbx = []
for i in range(file_number):
    sub_bbx.append([0]*3)

z_divide = 20
x_divide = math.sqrt(file_number/z_divide)
y_divide = (file_number/z_divide)/x_divide

x_length = (max_x-min_x)/((1/8)*x_divide+1)
y_length = (max_y-min_y)/((1/8)*y_divide+1)
z_length = (max_z-min_z)/((1/8)*z_divide+1)

pos = 0
for x in range(int(x_divide)):
    for y in range(int(y_divide)):
        for z in range(int(z_divide)):
            sub_bbx[pos][0] = min_x + x*(1/8)*x_length
            sub_bbx[pos][1] = min_y + y*(1/8)*y_length
            sub_bbx[pos][2] = min_z + z*(1/8)*z_length
            pos = pos + 1

#3.uniform sampling of points in the bbx
for i in range(file_number):
    file_name = output_folder + '/' + str(i).zfill(8)+'.ply'
    print("creating ply file:" + file_name + "...")
    curr_bbx_min = sub_bbx[i]
    curr_bbx_max = [curr_bbx_min[0]+x_length, curr_bbx_min[1]+y_length, curr_bbx_min[2]+z_length]
    f = open(mesh_path,"rb")
    for i in range(10):
        l = f.readline()
    yes_pt = []
    for pt in range(vertex_number):
        l = f.readline()
        curr_x = float(l.split()[0])
        curr_y = float(l.split()[1])
        curr_z = float(l.split()[2])
        if curr_x > curr_bbx_min[0] and curr_x < curr_bbx_max[0] and curr_y > curr_bbx_min[1] and curr_y < curr_bbx_max[1] and curr_z > curr_bbx_min[2] and curr_z < curr_bbx_max[2]:
            yes_pt.append([curr_x,curr_y,curr_z])

    #we need 2000 pt each file maybe, sampling and write them to 'filename'
    pt_out = 2000
    out_pt = []
    random.shuffle(yes_pt)
    if len(yes_pt) < 1:
        continue
    if len(yes_pt) <= pt_out:
        out_pt = yes_pt
    else:
        out_pt = yes_pt[:2000]  
    
    w = open(file_name,'w')
    header = 'ply\nformat ascii 1.0\ncomment VCGLIB generated\nelement vertex '
    w.write(header)
    w.write(str(len(out_pt)))
    header = '\nproperty float x\nproperty float y\nproperty float z\nend_header\n'
    w.write(header)
    for j in range(len(out_pt)):
        w.write(str(out_pt[j][0])+' '+str(out_pt[j][1])+' '+str(out_pt[j][2])+'\n')
    w.close()
    f.close()





    
    
