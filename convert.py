import cv2
import os

bmp_file_path = "C:/Users/41477613/Desktop/2x_U1_L1.bmp"

image = cv2.imread(bmp_file_path)

height, width, channels = image.shape

image = cv2.resize(image, (1126, 1126))

cv2.imwrite(bmp_file_path, image)
print(f"ไฟล์ถูกบันทึกเป็น: {bmp_file_path}")

