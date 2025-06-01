import sys
import cv2
import glob
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


class ImageStitcher:
    def __init__(self, nfeatures=2000, min_matches=5, distance_threshold=0.6):
        self.orb = cv2.ORB_create(nfeatures=nfeatures)
        self.min_matches = min_matches
        self.distance_threshold = distance_threshold
        self.result = None

    def load_images(self, folder_path, max_size=2000):
        """Load and resize images from specified folder"""
        path = sorted(Path(folder_path).glob("*.jpg"))
        img_list = []
        
        print("Loading and resizing images...")
        for img_path in path:
            img = cv2.imread(str(img_path))
            if img is not None:
                # Resize image while maintaining aspect ratio
                height, width = img.shape[:2]
                if height > max_size or width > max_size:
                    scale = max_size / max(height, width)
                    new_size = (int(width * scale), int(height * scale))
                    img = cv2.resize(img, new_size, interpolation=cv2.INTER_AREA)
                img_list.append(img)
                print(f"Loaded and processed: {img_path.name}")
            
        if len(img_list) < 2:
            raise ValueError("At least 2 images required for stitching")
        return img_list

    def stitch_images(self, folder_path):
        """Main stitching process"""
        img_list = self.load_images(folder_path)
        print(f"Processing {len(img_list)} images...")

        while len(img_list) > 1:
            img1 = img_list.pop(0)
            img2 = img_list.pop(0)

            # Extract features
            kp1, des1 = self.orb.detectAndCompute(img1, None)
            kp2, des2 = self.orb.detectAndCompute(img2, None)

            if des1 is None or des2 is None:
                print("Warning: No features detected in one or both images")
                continue

            # Match features
            bf = cv2.BFMatcher_create(cv2.NORM_HAMMING)
            matches = bf.knnMatch(des1, des2, k=2)

            # Filter good matches
            good = []
            for m, n in matches:
                if m.distance < self.distance_threshold * n.distance:
                    good.append(m)

            if len(good) > self.min_matches:
                # Get matching points
                src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
                dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

                # Calculate homography
                M, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
                
                # Warp and combine images
                result = self.warp_images(img2, img1, M)
                img_list.insert(0, result)

            if len(img_list) == 1:
                self.result = cv2.cvtColor(img_list[0], cv2.COLOR_BGR2RGB)
                break

    def warp_images(self, img1, img2, H):
        """Warp and blend two images using homography matrix with size checking"""
        rows1, cols1 = img1.shape[:2]
        rows2, cols2 = img2.shape[:2]

        # Check if output dimensions would be too large
        list_of_points_1 = np.float32([[0,0], [0,rows1], [cols1,rows1], [cols1,0]]).reshape(-1,1,2)
        temp_points = np.float32([[0,0], [0,rows2], [cols2,rows2], [cols2,0]]).reshape(-1,1,2)
        
        list_of_points_2 = cv2.perspectiveTransform(temp_points, H)
        list_of_points = np.concatenate((list_of_points_1, list_of_points_2), axis=0)
        
        [x_min, y_min] = np.int32(list_of_points.min(axis=0).ravel() - 0.5)
        [x_max, y_max] = np.int32(list_of_points.max(axis=0).ravel() + 0.5)
        
        # Check output dimensions
        output_width = x_max - x_min
        output_height = y_max - y_min
        
        if output_width >= 32767 or output_height >= 32767:  # OpenCV limit (SHRT_MAX)
            scale = min(32000/output_width, 32000/output_height)
            print(f"Warning: Output too large, rescaling by factor {scale:.2f}")
            
            # Resize input images
            img1 = cv2.resize(img1, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
            img2 = cv2.resize(img2, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
            
            # Adjust homography for new scale
            H_scale = np.array([[scale, 0, 0], [0, scale, 0], [0, 0, 1]])
            H = H_scale.dot(H).dot(np.linalg.inv(H_scale))
            
            # Recalculate dimensions
            rows1, cols1 = img1.shape[:2]
            rows2, cols2 = img2.shape[:2]
            
            # Recalculate points
            list_of_points_1 = np.float32([[0,0], [0,rows1], [cols1,rows1], [cols1,0]]).reshape(-1,1,2)
            temp_points = np.float32([[0,0], [0,rows2], [cols2,rows2], [cols2,0]]).reshape(-1,1,2)
            list_of_points_2 = cv2.perspectiveTransform(temp_points, H)
            list_of_points = np.concatenate((list_of_points_1, list_of_points_2), axis=0)
            
            [x_min, y_min] = np.int32(list_of_points.min(axis=0).ravel() - 0.5)
            [x_max, y_max] = np.int32(list_of_points.max(axis=0).ravel() + 0.5)

        translation_dist = [-x_min, -y_min]
        H_translation = np.array([[1, 0, translation_dist[0]], [0, 1, translation_dist[1]], [0, 0, 1]])
        
        output_img = cv2.warpPerspective(img2, H_translation.dot(H), (x_max-x_min, y_max-y_min))
        output_img[translation_dist[1]:rows1+translation_dist[1], translation_dist[0]:cols1+translation_dist[0]] = img1
        
        return output_img

    def show_result(self):
        """Display the stitched result"""
        if self.result is not None:
            plt.figure(figsize=(15, 10))
            plt.imshow(self.result)
            plt.axis('off')
            plt.show()
        else:
            print("No result available. Run stitch_images first.")

    def save_result(self, output_path):
        """Save the stitched result"""
        if self.result is not None:
            cv2.imwrite(output_path, cv2.cvtColor(self.result, cv2.COLOR_RGB2BGR))
            print(f"Result saved to {output_path}")

if __name__ == "__main__":
    # Initialize stitcher with optional parameters
    stitcher = ImageStitcher(
        nfeatures=2000,        # Number of ORB features to detect
        min_matches=5,         # Minimum matches required
        distance_threshold=0.7  # Distance threshold for matching
    )

    # Process images
    try:
        # Specify your image folder path
        image_folder = r'C:\Users\valde\Desktop\CS classes\senior_projects\ODLC_Machine_Inferencing_System_2024-2025\images'
        
        # Stitch images
        stitcher.stitch_images(image_folder)
        
        # Save with timestamp and size indication
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        stitcher.save_result(f"stitched_output_{timestamp}.jpg")
        
        stitcher.show_result()
        
    except Exception as e:
        print(f"Error during stitching: {e}")