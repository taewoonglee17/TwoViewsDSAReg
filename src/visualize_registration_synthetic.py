import pyvista as pv
import numpy as np
import visualization_utils as ut
from PIL import Image

# **** INPUTS ****
MESH_PATH = '../data/input/dsa_mesh_yaxis_up.obj'
TARGET_PATH = '../data/output/synthetic/synthetic_image_ref.png'
TARGET_PATH2 = '../data/output/synthetic/synthetic_image_ref2.png'

# open file with registration data
file = open('../data/output/synthetic/RT_data_synthetic.txt','r')
RT_data = []
for line in file:
    float_values = list(map(float, line.strip().strip('[]').split(',')))
    RT_data.append(float_values)

# get image size to create the scene
im = Image.open(TARGET_PATH)
w, h = im.size

plotter = pv.Plotter(off_screen=False, window_size = [1500, 1500])
plotter.camera_position = [(-452.04814588672184, 137.03482836330625, 529.3297257511393),
 (-34.99439930843491, 0.01377875541741247, 34.99705913562692),
 (0.13962097090056574, 0.9782565149436557, -0.15336288812837512)]

# add mesh to scene
mesh = pv.read(MESH_PATH)
plotter.add_mesh(mesh, style='wireframe', color='#059fb0', lighting=False, diffuse=1)

plane = pv.Plane(center=(0,-100,0),direction=(0,1,0),i_size=280,j_size=280)
plotter.add_mesh(plane, show_edges=True, color=[255,255,255], render=False)

# GROUND TRUTH CAMERA
#set ground truth camera
gt_position = np.array(RT_data[-3])
gt_at = np.array(RT_data[-2])
gt_up = np.array(RT_data[-1])
gt_position2 = (gt_at - np.linalg.cross(gt_up,gt_at-gt_position))/np.linalg.norm(gt_at - np.linalg.cross(gt_up,gt_at-gt_position)) * np.linalg.norm(gt_at-gt_position)

# draw gt camera
a = pv.Cone(center=gt_position, direction=gt_position-gt_at, radius=15, height=40, resolution=4)
plotter.add_mesh(a, color='green', style='wireframe', line_width=4)
plotter.add_point_labels(points=gt_position+(gt_position-gt_at)/np.linalg.norm((gt_position-gt_at))*55-gt_up/np.linalg.norm(gt_up)*5,
                         show_points=False,
                         labels=['Ground Truth AP'],
                         shape=None,
                         text_color='green',
                         font_size=30
                         )

# draw a line from the camera looking "at"
ln= pv.Line(gt_position, gt_at)
plotter.add_mesh(ln, color='green', line_width=5, render_lines_as_tubes=True)

# draw image as quad
focal_length = 4.5
distance_from_origin_sillouette = -100
quad = ut.convert_image_to_quad(position=gt_position, distance_from_origin=distance_from_origin_sillouette, view_dir = gt_position-gt_at, view_up=gt_up, focal_length=focal_length, w=w, h=h)
tex = pv.read_texture(TARGET_PATH)
plotter.add_mesh(quad, texture=tex, show_edges=True, line_width=5, opacity=0.99)

# Draw ground truth Camera 2
# draw gt camera2
a = pv.Cone(center=gt_position2, direction=gt_position2-gt_at, radius=15, height=40, resolution=4)
plotter.add_mesh(a, color='green', style='wireframe', line_width=5)
plotter.add_point_labels(points=gt_position2+(gt_position2-gt_at)/np.linalg.norm((gt_position2-gt_at))*5-gt_up/np.linalg.norm(gt_up)*13,
                         show_points=False,
                         labels=['Ground Truth LAT'],
                         shape=None,
                         text_color='green',
                         font_size=30
                         )

# draw a line from the camera looking "at"
ln= pv.Line(gt_position2, gt_at)
plotter.add_mesh(ln, color='green', line_width=5, render_lines_as_tubes=True)

quad2 = ut.convert_image_to_quad(position=gt_position2, distance_from_origin=distance_from_origin_sillouette, view_dir = gt_position2-gt_at, view_up=gt_up, focal_length=focal_length, w=w, h=h)
tex = pv.read_texture(TARGET_PATH2)
plotter.add_mesh(quad2, texture=tex, show_edges=True, line_width=5, opacity=0.99)

plotter.add_axes()

# Make GIF
plotter.open_gif("../data/output/synthetic/3D_Demo_DSA_Registration_synthetic.gif")

number_of_frames = int(len(RT_data)/3)
for i in range(number_of_frames):
    # CAMERA 1
    position = np.array(RT_data[3*i])
    at = np.array(RT_data[3*i+1])
    up = np.array(RT_data[3*i+2])

    # draw camera
    a = pv.Cone(center=position, direction=position-at, radius=15, height=40, resolution=4)
    actor_camera_ap = plotter.add_mesh(a, color='blue', style='wireframe', line_width=5)
    plotter.add_points(position, color='blue', render_points_as_spheres=True, point_size=7)
    actor_label_ap = plotter.add_point_labels(points=position+(position-at)/np.linalg.norm((position-at))*5+(gt_up)/np.linalg.norm(gt_up)*15,
                        show_points=False,
                        labels=['AP'],
                        shape=None,
                        text_color='blue',
                        font_size=30
                        )
 
    # draw a line from the camera looking "at"
    ln= pv.Line(position, at)
    actor_line_ap = plotter.add_mesh(ln, color='blue', line_width=2, render_lines_as_tubes=True)

    SILLOUETTE1_PATH = "./GIF_Visualization/sillouettes/image_sillouette_synthetic_"+str(i)+".png"
    quad_sillouette1 = ut.convert_image_to_quad(position=position, distance_from_origin=distance_from_origin_sillouette, view_dir = position-at, view_up=up, focal_length=focal_length, w=w, h=h)
    tex = pv.read_texture(SILLOUETTE1_PATH)
    actor_sillouette = plotter.add_mesh(quad_sillouette1, texture=tex, show_edges=True, line_width=5, opacity=0.5)

    # CAMERA 2
    position2 = (at - np.linalg.cross(up,at-position))/np.linalg.norm(at - np.linalg.cross(up,at-position)) * np.linalg.norm(at-position)

    SILLOUETTE2_PATH = "./GIF_Visualization/sillouettes/image_sillouette2_synthetic_"+str(i)+".png"
    quad_sillouette2 = ut.convert_image_to_quad(position=position2, distance_from_origin=distance_from_origin_sillouette, view_dir = position2-at, view_up=up, focal_length=focal_length, w=w, h=h)
    tex = pv.read_texture(SILLOUETTE2_PATH)
    actor_sillouette2 = plotter.add_mesh(quad_sillouette2, texture=tex, show_edges=True, line_width=5, opacity=0.5)
    
    # connect dots for camera position
    if(i>=1):
        connect_camera_line = pv.Line(position, position_prev)
        connect_camera_line2 = pv.Line(position2, position2_prev)
        plotter.add_mesh(connect_camera_line, color='blue', line_width=5, render_lines_as_tubes=True)
        plotter.add_mesh(connect_camera_line2, color='red', line_width=5, render_lines_as_tubes=True)
    position_prev = position
    position2_prev = position2
    
    # draw camera
    a2 = pv.Cone(center=position2, direction=position2-at, radius=15, height=40, resolution=4)
    actor_camera_lat = plotter.add_mesh(a2, color='red', style='wireframe', line_width=5)
    plotter.add_points(position2, color='red', render_points_as_spheres=True, point_size=7)
    actor_label_lat = plotter.add_point_labels(points=position2-(gt_up)/np.linalg.norm(gt_up)*15,
                        show_points=False,
                        labels=['LAT'],
                        shape=None,
                        text_color='red',
                        font_size=30
                        )

    # draw a line from the camera looking "at"
    ln= pv.Line(position2, at)
    actor_line_lat = plotter.add_mesh(ln, color='red', line_width=5, render_lines_as_tubes=True)
    
    plotter.write_frame()
    plotter.remove_actor(actor_camera_ap)
    plotter.remove_actor(actor_line_ap)
    plotter.remove_actor(actor_sillouette)
    plotter.remove_actor(actor_label_ap)
    plotter.remove_actor(actor_camera_lat)
    plotter.remove_actor(actor_line_lat)
    plotter.remove_actor(actor_sillouette2)
    plotter.remove_actor(actor_label_lat)
    
plotter.show()
print(plotter.camera_position)
plotter.close()