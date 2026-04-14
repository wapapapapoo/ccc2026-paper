import os
import numpy as np
from PIL import Image

def remove_white_pixels_from_png(file_path):
    img = Image.open(file_path).convert("RGBA")
    data = np.array(img)

    # 找到纯白像素
    white = (data[:, :, 0] == 255) & \
            (data[:, :, 1] == 255) & \
            (data[:, :, 2] == 255)

    # 设置 alpha 为 0
    data[white, 3] = 0

    new_img = Image.fromarray(data)
    new_img.save(file_path)
    print(f"Processed: {file_path}")

def main():
    for filename in os.listdir("."):
        if filename.lower().endswith(".png"):
            remove_white_pixels_from_png(filename)

if __name__ == "__main__":
    main()