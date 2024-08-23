import pyvista as pv
import numpy as np
from PIL import Image

# **** INPUTS ****
MESH_PATH = '../data/input/dsa_mesh_zaxis_up.obj'
TARGET_PATH = '../data/input/DSA_AP_seg.png'

# get image size to create the scene
im = Image.open(TARGET_PATH)
w, h = im.size

plotter = pv.Plotter(off_screen=False, window_size = [1500, 800])
plotter.camera_position = [(405.50216846299713, -320.7797067181996, 74.76279267926645),
 (-34.99439930843491, 0.01377875541741247, 34.99705913562692),
 (-0.05271180044226161, 0.051244070726894395, 0.9972940946929709)]

# add mesh to scene
mesh = pv.read(MESH_PATH)
plotter.add_mesh(mesh, style='wireframe', color='#059fb0', lighting=False, diffuse=1)

plane = pv.Plane(center=(-5,5,-47),direction=(0,0,1),i_size=200,j_size=200)
plotter.add_mesh(plane, show_edges=True, color=[255,255,255], render=False)

# open file with registration data
file = open('../data/output/real/RT_data_real.txt','r')
RT_data = []
for line in file:
    float_values = list(map(float, line.strip().strip('[]').split(',')))
    RT_data.append(float_values)
    
# GROUND TRUTH CAMERA
#set ground truth camera
gt_position = np.array(RT_data[-3])
gt_at = np.array(RT_data[-2])
gt_up = np.array(RT_data[-1])
gt_position2 = (gt_at - np.linalg.cross(gt_up,gt_at-gt_position))/np.linalg.norm(gt_at - np.linalg.cross(gt_up,gt_at-gt_position)) * np.linalg.norm(gt_at-gt_position)

# draw gt camera
a = pv.Cone(center=gt_position, direction=gt_position-gt_at, radius=15, height=40, resolution=4)
plotter.add_mesh(a, color='green', style='wireframe', line_width=5)

# Draw ground truth Camera 2
a = pv.Cone(center=gt_position2, direction=gt_position2-gt_at, radius=15, height=40, resolution=4)
plotter.add_mesh(a, color='green', style='wireframe', line_width=5)

plotter.add_axes()

# Make GIF
plotter.open_gif("../data/output/real/3D_Demo_DSA_Registration_real.gif")

number_of_frames = int(len(RT_data)/3)
for i in range(number_of_frames):
    # CAMERA 1
    position = np.array(RT_data[3*i])
    at = np.array(RT_data[3*i+1])
    up = np.array(RT_data[3*i+2])

    # draw camera
    a = pv.Cone(center=position, direction=position-at, radius=15, height=40, resolution=4)
    actor_camera_ap = plotter.add_mesh(a, color='blue', style='wireframe', line_width=5)
    plotter.add_points(position, color='blue', render_points_as_spheres=True, point_size=10)
    actor_label_ap = plotter.add_point_labels(points=position+(gt_up)/np.linalg.norm(gt_up)*25,
                         show_points=False,
                         labels=['AP'],
                         shape=None,
                         text_color='blue',
                         font_size=30
                         )

    if(i>=1):
        connect_camera_line = pv.Line(position, position_prev)
        plotter.add_mesh(connect_camera_line, color='blue', line_width=5, render_lines_as_tubes=True)
    position_prev = position


    # CAMERA 2
    position2 = (at - np.linalg.cross(up,at-position))/np.linalg.norm(at - np.linalg.cross(up,at-position)) * np.linalg.norm(at-position)
        
    # draw camera
    a2 = pv.Cone(center=position2, direction=position2-at, radius=15, height=40, resolution=4)
    actor_camera_lat = plotter.add_mesh(a2, color='red', style='wireframe', line_width=5)
    plotter.add_points(position2, color='red', render_points_as_spheres=True, point_size=10)
    actor_label_lat = plotter.add_point_labels(points=position2+(gt_up)/np.linalg.norm(gt_up)*20,
                        show_points=False,
                        labels=['LAT'],
                        shape=None,
                        text_color='red',
                        font_size=30
                        )

    # connect dots for camera position
    if(i>=1):
        connect_camera_line2 = pv.Line(position2, position2_prev)
        plotter.add_mesh(connect_camera_line2, color='red', line_width=5, render_lines_as_tubes=True)
    position2_prev = position2
    
    plotter.write_frame()
    plotter.remove_actor(actor_camera_ap)
    plotter.remove_actor(actor_label_ap)
    plotter.remove_actor(actor_camera_lat)
    plotter.remove_actor(actor_label_lat)
    
plotter.show()
print(plotter.camera_position)
plotter.close()