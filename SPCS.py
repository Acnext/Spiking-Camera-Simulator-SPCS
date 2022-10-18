#set language English
import sys
sys.path.append("c:\\users\\administrator\\appdata\\roaming\\python\\python310\\site-packages\\")
import bpy
import random
import numpy as np
import os
import spline
import v2s
import math
import scene_SPIFT
#import read_exr000000000
from bpy import context
def reset(is_texture, texture_path, is_hdr, hdr_path):
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=True)
    for material in bpy.data.materials:
        #print(material)if not material.users:
        bpy.data.materials.remove(material)
    for imgs in bpy.data.images:
        bpy.data.images.remove(imgs)
    if is_texture:
        list_texture = os.listdir(texture_path)
        for i in list_texture:
            bpy.data.images.load(texture_path + i)
    if is_hdr:
        list_hdr = os.listdir(hdr_path)
        for i in list_hdr:
            bpy.data.images.load(hdr_path + i)
def init_state(obj_id, x, y, z, kinds):
    if kinds == 0:#
        bpy.data.objects[obj_id].location[0]=x
        bpy.data.objects[obj_id].location[1]=y
        bpy.data.objects[obj_id].location[2]=z
    elif kinds == 1:
        bpy.data.objects[obj_id].rotation_euler[0]=x
        bpy.data.objects[obj_id].rotation_euler[1]=y
        bpy.data.objects[obj_id].rotation_euler[2]=z
    elif kinds == 2:
        bpy.data.objects[obj_id].scale[0]*=x
        bpy.data.objects[obj_id].scale[1]*=y
        bpy.data.objects[obj_id].scale[2]*=z
    return
def add_act(obj_id, samples_points, frame_start, frame_end, kinds = 0): #class_num records the class of scenes.
    pre_x = 0
    pre_y = 0
    pre_z = 0
    for t, i in enumerate(samples_points):
        if t >= frame_end - frame_start:
            break
        if kinds == 0:
            bpy.data.objects[obj_id].location[0] += (i[0] - pre_x)
            bpy.data.objects[obj_id].location[1] += (i[1] - pre_y)
            bpy.data.objects[obj_id].location[2] += (i[2] - pre_z)
            bpy.data.objects[obj_id].keyframe_insert(data_path="location", frame=(t + frame_start))
        elif kinds == 1:
            bpy.data.objects[obj_id].rotation_euler[0] += (i[0] - pre_x)
            bpy.data.objects[obj_id].rotation_euler[1] += (i[1] - pre_y)
            bpy.data.objects[obj_id].rotation_euler[2] += (i[2] - pre_z)
            bpy.data.objects[obj_id].keyframe_insert(data_path="rotation_euler", frame=(t + frame_start))
        pre_x = i[0]
        pre_y = i[1]
        pre_z = i[2]
    return
#0 related set
opt = lambda: None
opt.path_obj = 'E:\\image\\3d_model\\'
opt.path_scene = 'E:\\image\\3d_scene\\'
opt.class_num = 0#the class of scene. 0 means total random (SCFlow)
opt.is_close = 1
opt.is_action = True
opt.num_obj = 10#the number of random objs
opt.frame_end = 500
opt.frame_start = 0
opt.is_cycle = True
opt.is_texture = False
opt.is_hdr = False #use hdr
opt.is_track_to = True #camera
opt.is_motion_vector = True
opt.coded_motion_vector_outpath = "\\coded_motion_vector\\"
opt.motion_vector_outpath = "\\motion_vector\\"
opt.image_outpath = "E:\\image\\changbo\\"
opt.spike_outpath = "\\spike\\"
opt.texture_path = "E:\\image\\texture\\"
opt.texture_background = 30
opt.thres = 400 #ivs
#opt.thres_dvs = 0.01 #dvs
opt.w = 800
opt.h = 500#resolution of image
opt.spike_w = 800#resolution of spike frame
opt.spike_h = 500
#opt.dt = (5, 10, 20)  #generate gt every dt
opt.dt = [1, 5, 10]
#here frame_end is one T
#0. change basic set for datasets (they dont change for iteral)
bpy.data.scenes['Scene'].render.resolution_x = opt.w
bpy.data.scenes['Scene'].render.resolution_y = opt.h
dt_len = len(opt.dt)
#print(dt_len)
#ccc.a = a
if opt.is_cycle:
    bpy.data.scenes['Scene'].render.engine = "CYCLES"
    bpy.data.scenes['Scene'].cycles.device = "GPU"
    bpy.data.scenes['Scene'].view_layers["ViewLayer"].use_pass_vector = True
    bpy.data.scenes['Scene'].cycles.samples = 64
    bpy.context.scene.cycles.use_preview_denoising = True
    bpy.context.scene.cycles.use_denoising = True
    bpy.context.scene.cycles.use_adaptive_sampling = True
    bpy.context.scene.view_layers["ViewLayer"].pass_alpha_threshold = 0
    bpy.context.scene.use_nodes = True
    scene = bpy.context.scene
    bpy.context.scene.render.image_settings.color_mode = 'RGB'
    bpy.context.scene.render.image_settings.compression = 0
    if opt.is_motion_vector:
        nodes = scene.node_tree.nodes
        print(list(nodes))
        bpy.data.scenes["Scene"].node_tree.nodes["Composite"].use_alpha = True
        render_layers = nodes['Render Layers']
        sp_node = nodes.new("CompositorNodeSepRGBA")
        com_node = nodes.new("CompositorNodeCombRGBA")
        scene.node_tree.links.new(
            render_layers.outputs['Vector'],
            sp_node.inputs['Image']
        )
        scene.node_tree.links.new(
            sp_node.outputs['R'],
            com_node.inputs['R']
        )
        scene.node_tree.links.new(
            sp_node.outputs['G'],
            com_node.inputs['G']
        )
        scene.node_tree.links.new(
            sp_node.outputs['B'],
            com_node.inputs['B']
        )
        scene.node_tree.links.new(
            sp_node.outputs['A'],
            com_node.inputs['A']
        )
        #if os.path.exists(opt.image_outpath + str(cnt) + opt.motiona_vector_outpath) == False:
        #    os.mkdir(opt.image_outpath + str(cnt) + opt.motion_vector_outpath)
        vector_node = nodes.new("CompositorNodeOutputFile")
        #vector_node.base_path = opt.image_outpath + str(cnt) + opt.motion_vector_outpath
        vector_node.format.file_format = 'OPEN_EXR'
        vector_node.format.color_mode = 'RGBA'
        vector_node.format.compression = 100
        vector_node.format.color_depth = '32'
if opt.frame_end == -1:
    opt.frame_end = bpy.data.scenes['Scene'].frame_end
else:
    bpy.data.scenes['Scene'].frame_end = opt.frame_end
if opt.frame_start == -1:
    opt.frame_start = bpy.data.scenes['Scene'].frame_start
else:
    bpy.data.scenes['Scene'].frame_start = opt.frame_start
 #1. clear all previous thins
for cnt in range(1, 3):
    if os.path.exists(opt.image_outpath + str(cnt) + "\\") == False:
        os.mkdir(opt.image_outpath + str(cnt) + "\\")
    reset(is_texture = opt.is_texture, texture_path = opt.texture_path, is_hdr = opt.is_hdr, hdr_path = opt.hdr_path)
    #sensor
    bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(0, 0, 0), rotation=(0.948029, 5.48634e-08, -1.19141), scale=(1, 1, 1))
    camera = bpy.data.objects['Camera']
    context.scene.camera = context.object
    mx_x = random.uniform(-7,7)
    mx_y = random.uniform(-7,7)
    mx_z = random.uniform(30,35)
    samples = []
    samples_r = []
    track_x = 0
    track_y = 0
    track_z = 0
    datas = scene_SPIFT.get_scene(path_scene = opt.path_scene, path_obj = opt.path_obj, path_texture = opt.texture_path, num_obj = opt.num_obj, texture_background = opt.texture_background, frame_start = opt.frame_start, frame_end = opt.frame_end, camera_pos = (mx_x, mx_y, mx_z))
    samples = datas[0]
    samples_r = datas[1]
    track_x = datas[2]
    track_y = datas[3]
    track_z = datas[4]
    print("x is ", track_x)
    print("y is ", track_y)
    #3. set action
    #ccc.a = a
    if opt.is_track_to:
        track = camera.constraints.new(type = 'TRACK_TO')
        bpy.ops.object.empty_add(type='PLAIN_AXES')
        a = bpy.data.objects['Empty']
        a.location[0] = track_x
        a.location[1] = track_y
        a.location[2] = track_z
        print(bpy.data.objects[1])
        #return
        track.target = a#
        track.track_axis = "TRACK_NEGATIVE_Z"
        track.up_axis = "UP_Y"
        init_state('Camera', mx_x + track_x, mx_y + track_y, mx_z + track_z, 0)
        #tuple_v = add_motion(1, opt.frame_end, 1.3, opt.class_num, LED = 2)#vidarflow is 1.3 track is s 
        #add_motion('Empty', opt.frame_end, 1.3, opt.class_num, LED = 2)#vidarflow is 1.3 track is s
    #ccc.a = a
    for t in range(opt.num_obj + 1):
        temp_left = opt.frame_start
        temp_right = opt.frame_end
        if opt.is_action == False:
            temp_right = temp_left + 1
        if t == opt.num_obj:
            init_state('Camera', mx_x, mx_y, mx_z, 0)
            camera_pos = spline.get_node(step_size = random.uniform(0.0003,0.0006), rand_num = 5)
            print(camera_pos.shape)
            camera_pos[:, 0] += mx_x
            camera_pos[:, 1] += mx_y
            camera_pos[:, 2] += mx_z
            add_act('Camera', camera_pos, temp_left, temp_right, 0)
        else:
            add_act(t, samples[t,:,:], temp_left, temp_right, kinds = 0)
            add_act(t, samples_r[t,:,:], temp_left, temp_right, kinds = 1)# num 0 is background
    #random.shuffle(list_scene)
    #ccc.a = a
    bpy.data.scenes['Scene'].render.resolution_x = opt.w
    bpy.data.scenes['Scene'].render.resolution_y = opt.h
    bpy.data.scenes['Scene'].render.filepath = opt.image_outpath + str(cnt) + "\\"
    bpy.data.scenes['Scene'].render.image_settings.file_format = "PNG"
    pre_dt = 1
    #4.render data image,OF,spike...
    for dt in opt.dt:
        if opt.is_motion_vector:
            scene.node_tree.links.new(
                com_node.outputs['Image'],
                vector_node.inputs['Image']
            )
        old_type = bpy.context.area.type
        bpy.context.area.type = 'GRAPH_EDITOR'
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.graph.interpolation_type(type='LINEAR')
        bpy.context.space_data.pivot_point = 'CURSOR'
        bpy.context.scene.frame_current = 0
        bpy.ops.transform.resize(value=(1.0 / (dt / pre_dt), 1, 1))
        pre_dt = dt
        bpy.context.area.type = old_type
        if os.path.exists(opt.image_outpath + str(cnt) + "\\dt=" + str(dt)) == False:
             os.mkdir(opt.image_outpath + str(cnt) + "\\dt=" + str(dt))
             bpy.data.scenes['Scene'].render.filepath = opt.image_outpath + str(cnt) + "\\dt=" + str(dt) + "\\"
        else:
            bpy.data.scenes['Scene'].render.filepath = opt.image_outpath + str(cnt) + "\\dt=" + str(dt) + "\\"
        if opt.is_motion_vector == True:
            print("OF")
            if os.path.exists(opt.image_outpath + str(cnt) + "\\dt=" + str(dt) +opt.motion_vector_outpath) == False:
                os.mkdir(opt.image_outpath + str(cnt) + "\\dt=" + str(dt) +opt.motion_vector_outpath)
            vector_node.base_path = opt.image_outpath + str(cnt) + "\\dt=" + str(dt) +opt.motion_vector_outpath
            bpy.data.scenes['Scene'].frame_end = int(opt.frame_end / dt)
        bpy.ops.render.render(animation=True, write_still=True)
        #ccc.a = a
        area = []
    if opt.is_motion_vector == True:
        scene.node_tree.links.remove(vector_node.inputs['Image'].links[0])
    v2s.get_spike(opt.image_outpath + str(cnt) + "\\dt=1\\", opt.image_outpath + str(cnt) + "\\dt=1\\", opt.spike_w, opt.spike_h, opt.thres, opt.frame_start, opt.frame_end)