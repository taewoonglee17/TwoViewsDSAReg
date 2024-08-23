import pyvista as pv
import numpy as np

def convert_image_to_quad(position, view_dir, distance_from_origin, view_up, focal_length, w, h):
    # Calculate the view direction
    view_dir /= np.linalg.norm(view_dir)

    # Calculate the right vector
    right = np.cross(view_dir, view_up)
    right /= np.linalg.norm(right)

    # Calculate the new up vector
    new_up = np.cross(right, view_dir)
    new_up /= np.linalg.norm(new_up)
    
    # Calculate the corners of the quad
    top_left = distance_from_origin*view_dir + 0.5 * w * right/focal_length + 0.5 * h * new_up/focal_length
    top_right = distance_from_origin*view_dir - 0.5 * w * right/focal_length + 0.5 * h * new_up/focal_length
    bottom_left = distance_from_origin*view_dir + 0.5 * w * right/focal_length - 0.5 * h * new_up/focal_length
    bottom_right = distance_from_origin*view_dir - 0.5 * w * right/focal_length - 0.5 * h * new_up/focal_length

    # Create the rectangle as a PolyData object
    points = np.vstack([top_left, top_right, bottom_right, bottom_left])
    faces = [4, 0, 1, 2, 3]
    quad = pv.PolyData(points, faces)
    
    # add texture coordinates
    quad.texture_map_to_plane(inplace=True)

    # adjust texture coordinates to prevent rotation
    quad.point_data['Texture Coordinates'][0] = [0, 1]  # bottom-left corner
    quad.point_data['Texture Coordinates'][1] = [1, 1]  # bottom-right corner
    quad.point_data['Texture Coordinates'][2] = [1, 0]  # top-right corner
    quad.point_data['Texture Coordinates'][3] = [0, 0]  # top-left corner

    return quad