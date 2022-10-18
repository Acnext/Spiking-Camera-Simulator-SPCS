import sys
#print(sys.path)
#sys.path.append("C:\\Users\\Administrator\\AppData\\Roaming\\Python\\Python310\\site-packages\\")
import bpy
import random
import numpy as np
import os
import spline
import v2s
import v2e
import count_area
import math
import boundingbox as bbx
import add_flash_of_light as LED
#import read_exr
from bpy import context
def get_texture(bk, cnt = 0):# add texture to material; 0 mean that node need to be added ; 1 only need to link
    for i in range(len(bpy.data.materials)):
        #print(bpy.data.materials[i])
        #print(bpy.data.materials[i].node_tree)
        if bpy.data.materials[i].node_tree is not None:
            if i == 0:
                num = random.randint(0, bk - 1)
            else:
                num = random.randint(bk, len(bpy.data.images) - 3)
            #num = i
            bpy.data.materials[i].node_tree.nodes.new(type="ShaderNodeTexImage")
            bpy.data.materials[i].node_tree.nodes["Image Texture"].image = bpy.data.images[num]
            bpy.data.materials[i].node_tree.links.new(
            bpy.data.materials[i].node_tree.nodes["Image Texture"].outputs['Color'], 
            bpy.data.materials[i].node_tree.nodes["Principled BSDF"].inputs['Base Color'])
    return
#参数:
#position 用于存放car可行的位置 用(x1, x2, y1, y2) 表示可行范围 xian zai shi zhi xian
def get_scene(path_scene = "", path_obj = "", path_texture = "", num_obj = 1, is_action = True, num_action = -1,  texture_background = 10,frame_start = 0, frame_end = 1, camera_pos = (0, 0, 0)):
    if num_action == -1:
        num_action = frame_end - frame_start
    list_obj = os.listdir(path_obj)
    print(list_obj)
    random.shuffle(list_obj)  #is getting obj in random order
    temp_obj = [] #selected random objects
    temp_cnt = 0 #all temp_cnt is only used to comput number like this (can not as "for in range")
    samples = np.zeros((num_obj, num_action, 3))
    samples_r = np.zeros((num_obj, num_action, 3))
    for i in list_obj:
        temp_obj.append(i)
        temp_cnt += 1
        if temp_cnt >= num_obj:
            break
    temp_obj.sort()
    for t, i in enumerate(temp_obj):
        print(path_obj + i)
        if i.endswith(".dae") == True:
            bpy.ops.wm.collada_import(filepath = path_obj + i)
        elif i.endswith(".fbx") == True:
            bpy.ops.import_scene.fbx(filepath = path_obj + i)
        temp_z = random.uniform(5, camera_pos[2]-25)
        temp_x = (camera_pos[0] + random.uniform(-30, 30)) * (temp_z) / camera_pos[2]
        temp_y = (camera_pos[1] + random.uniform(-30, 30)) * temp_z / camera_pos[2] + random.uniform(-5, 5)
        sample_points1 = spline.get_node(step_size = random.uniform(0.0003,0.0006), rand_num = 5, num_action = num_action)
        samples[t,:,:] = sample_points1[0:num_action,:]
        sample_points2 = spline.get_node(step_size = random.uniform(0.0003,0.0006), rand_num = 5, num_action = num_action)
        samples_r[t,:,:] = sample_points2[0:num_action,:]
        samples[t,:,0] += temp_x
        samples[t,:,1] += temp_y
        samples[t,:,2] += temp_z
    bpy.ops.wm.collada_import(filepath = path_scene + "background.dae")#背景板
    list_texture = os.listdir(path_texture)
    for i in list_texture:
        bpy.data.images.load(path_texture + i)
    get_texture(bk = texture_background, cnt = 0)
    return samples, samples_r, 0, 0, 0#yun dong gui ji and suo ding wei zhi
if __name__=="__main__":
    display = get_scene(path_scene = "D:/work/vidar-project/Cycle(python)/drive_dynamic/scene/", path_obj = "D:/work/vidar-project/Cycle(python)/drive_dynamic/obj/", road_position = [(-242.426, 225.962, -203.6 - 6.6, -203.6 + 6.6)])
    print(len(display))