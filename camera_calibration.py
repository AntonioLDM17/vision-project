import cv2
import glob
import copy
import numpy as np
import imageio
import matplotlib.pyplot as plt
import os

def load_images(filenames):
    return [imageio.v3.imread(filename) for filename in filenames]

def get_chessboard_points(chessboard_shape, dx, dy):
    points = [[i * dx, j * dy, 0] for i in range(chessboard_shape[0]) for j in range(chessboard_shape[1])]
    return np.array(points, dtype=np.float32)

def draw_chessboard_corners(gray_images, corners):
    painted_images = []
    for gray_img, corner in zip(gray_images, corners):
        if corner is not None and corner.any():
            cv2.drawChessboardCorners(gray_img, (11, 10), corner, True)
            painted_images.append(gray_img)
    return painted_images
def calibration_camera():
    # Load images
    current_directory = os.getcwd()
    image_path = os.path.join(current_directory, "calibration_images")
    image_files = [i for i in glob.glob(os.path.join(image_path, '*.jpg'))]
    loaded_images = load_images(image_files)
    images_to_process = load_images(image_files)

    print(f"Total number of images: {len(loaded_images)}\n")

    # Extract corners
    corners = []
    updated_images = []

    for i, img in enumerate(images_to_process):
        success, corner = cv2.findChessboardCorners(img, (11, 10))
        print(f"Processing Image {i}: {success}")
        print(corner)
        if success:
            corners.append(corner)
            updated_images.append(img)

    loaded_images = updated_images

    # Optional: Creating a deep copy to avoid data loss during cornerSubPix
    corners_copy = copy.deepcopy(corners)

    # Criteria for termination
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.01)

    # Convert images to grayscale
    gray_images = [cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) for img in loaded_images]

    # Refine corners using cornerSubPix
    refined_corners = [cv2.cornerSubPix(gray_img, corner, (11, 10), (-1, -1), criteria) if corner is not None and corner.any() else [] for gray_img, corner in zip(gray_images, corners_copy)]

    copied_images = copy.deepcopy(loaded_images)
    painted_images = draw_chessboard_corners(copied_images[:], refined_corners)

    # Display images with painted corners
    plt.figure(figsize=(10,10))
    for i in range(4):
        plt.subplot(2, 2, i+1)
        plt.imshow(painted_images[i])
    plt.show()

    # Get chessboard points
    chessboard_points = get_chessboard_points((11, 10), 16.5, 16.5)

    valid_corners = [corner for corner in refined_corners if corner is not None and corner.any()]
    num_valid_images = len(valid_corners)

    # Create a matrix with the coordinates of the corners
    real_world_points = get_chessboard_points((11, 10), 16.5, 16.5)

    # Convert the coordinates list to a numpy array in the reference system
    object_points = np.asarray([real_world_points for i in range(num_valid_images)], dtype=np.float32)

    # Convert the corners list to an array
    image_points = np.asarray(valid_corners, dtype=np.float32)

    # Calibrate the camera
    rms_error, intrinsic_matrix, distortion_coefficients, rotation_vectors, translation_vectors = cv2.calibrateCamera(object_points, image_points, gray_images[0].shape[::-1], None, None)

    # Calculate extrinsics matrix using Rodrigues on each rotation vector and its translation vector
    extrinsics_matrix = list(map(lambda rvec, tvec: np.hstack((cv2.Rodrigues(rvec)[0], tvec)), rotation_vectors, translation_vectors))

    # Save the calibration file
    np.savez('calibration_results', intrinsic=intrinsic_matrix, extrinsic=extrinsics_matrix)

    # Print some calibration results
    print("Intrinsic Matrix:\n", intrinsic_matrix)
    print("Distortion Coefficients:\n", distortion_coefficients)
    print("Root Mean Square Reprojection Error:\n", rms_error)

    # Calculate the extrinsics with Rodrigues given the translation and rotation matrices
    extrinsics_matrix = list(map(lambda rvec, tvec: np.hstack((cv2.Rodrigues(rvec)[0], tvec)), rotation_vectors, translation_vectors))
    print("Extrinsics Matrix:\n", extrinsics_matrix)

if __name__ == '__main__':
    calibration_camera()




