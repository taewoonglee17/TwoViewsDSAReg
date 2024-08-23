import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image 
from tqdm.notebook import tqdm
import imageio
import cv2
import random
from scipy.spatial.transform import Rotation
import re
from skimage import filters, morphology

# Define RAW/RAD file to numpy array method
def xray_read_dt(name):
    """
    Python function for loading 2D images in .rad format and corresponding .raw file to a NumPy array.
    
    """
    # Load 2D image header data
    with open(f"{name}.rad", 'r') as file:
        Xhea = file.read().splitlines()
    
    # Number of pixels along x and y axis
    parts = Xhea[0].split() # Xhea[0]에는 "Size[pixels]: 2480 1920" 이렇게 되어 있음. 이거를 읽어서 nx, ny에 넣게끔 한다.
    Nx = int(parts[1])
    Ny = int(parts[2])

    # Initialize X as an empty array
    X = np.array([])
    
    # Read 2D image data in float (32 bit) consisting of Nx*Ny pixels
    with open(f"{name}.raw", 'rb') as fid:
        Xraw = np.fromfile(fid, dtype=np.float32)
    
    # Arrange to obtain 2D matrix
    X = np.reshape(Xraw, (Ny, Nx))
    
    return X

# Define 2D DSA Segmentation Method
def DSA_segmentation(image, sigma=1): # sigma determines blur intensity

    # Blurring with Gaussian filter
    image_filtered = filters.gaussian(image, sigma)

    # Set thresolh value with Otsu's method
    threshold_value = filters.threshold_otsu(image_filtered)
    binary_image = image_filtered > threshold_value

    # remove small objects
    cleaned_image = morphology.remove_small_objects(binary_image, min_size=50)

    # change True/False to 1/0
    return cleaned_image.astype(int)

def resize_image(image, target_number):
    """
    Resizes the input image to the dimensions closest to the target number
    while maintaining the aspect ratio.

    Parameters:
    - image (numpy array): 2D numpy array with pixel values (1 for white, 0 for black).
    - target_number (int): Desired approximate size for the image dimensions.

    Returns:
    - resized_image (numpy array): Resized image with dimensions closest to the target number.
    """
        
    original_height, original_width = image.shape  # Get original dimensions
    
    # Calculate aspect ratio
    aspect_ratio = original_width / original_height
    
    # Calculate new dimensions maintaining aspect ratio
    if original_width >= original_height:
        # Image is wider than tall, scale based on width
        new_width = target_number
        new_height = int(new_width / aspect_ratio)
    else:
        # Image is taller than wide, scale based on height
        new_height = target_number
        new_width = int(new_height * aspect_ratio)
    
    # Resize the image
    resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
    
    return resized_image

def angular_difference_error(matrix_true, matrix_est):
    """
    Calculate the rotational error between two rotation matrices using SciPy.

    :param matrix_true: True rotation matrix (3x3)
    :param matrix_est: Estimated rotation matrix (3x3)
    :return: Rotational error in degrees
    """
    # Create Rotation objects from matrices
    rot_true = Rotation.from_matrix(matrix_true)
    rot_est = Rotation.from_matrix(matrix_est)
    
    # Calculate relative rotation (from estimated to true)
    relative_rotation = rot_true.inv() * rot_est

    # Extract the angle of rotation
    angle_rad = relative_rotation.magnitude()  # Angle in radians
    angle_deg = np.degrees(angle_rad)  # Convert to degrees
    
    return angle_deg

def ADD_Error(objFilename, R_ground_truth, T_ground_truth, R_estimate, T_estimate):
    
    reComp = re.compile("(?<=^)(v |vn |vt |f )(.*)(?=$)", re.MULTILINE)
    with open(objFilename) as f:
        data = [txt.group() for txt in reComp.finditer(f.read())]

    v_arr = []
    for line in data:
        tokens = line.split(' ')
        if tokens[0] == 'v':
            v_arr.append([float(c) for c in tokens[1:]])    
      
    dist = 0
    for pt in v_arr:
        pt1 = np.matmul(R_ground_truth, pt) + T_ground_truth
        pt2 = np.matmul(R_estimate, pt) + T_estimate
            
        dist += np.linalg.norm(pt1 - pt2)
        
    err = dist/len(v_arr)
    
    return err

def add_noise(binary_image, num_spots, spot_size=1):
    """
    Adds random noise to a binary image by adding small spots with random values between 0 and 1.
    
    Parameters:
    - binary_image: numpy array of shape (H, W) with binary values (0 and 1).
    - num_spots: The number of spots to add.
    - spot_size: The size of each spot (default is 1x1 pixel).
    
    Returns:
    - noisy_image: numpy array of shape (H, W) with added noise.
    """
    noisy_image = binary_image.copy()
    height, width = noisy_image.shape

    for _ in range(num_spots):
        # Randomly choose the position of the spot
        x = random.randint(0, width - spot_size)
        y = random.randint(0, height - spot_size)
        
        # Generate a random value between 0.9 and 1
        #noise_value = random.uniform(0.9, 1)
        noise_value = 1
        
        # Add the spot of noise to the image
        noisy_image[y:y+spot_size, x:x+spot_size] = noise_value
    
    return noisy_image