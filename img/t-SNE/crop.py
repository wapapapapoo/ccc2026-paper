import os
import numpy as np
from PIL import Image

# 判定白色阈值（可调）
WHITE_THRESHOLD = 250

def find_content_bbox(img):
    """
    返回非白区域的 bounding box: (top, bottom, left, right)
    """
    img_np = np.array(img.convert("RGB"))

    # 判断是否接近白色
    non_white = np.any(img_np < WHITE_THRESHOLD, axis=2)

    coords = np.argwhere(non_white)
    if coords.size == 0:
        return None

    top, left = coords.min(axis=0)
    bottom, right = coords.max(axis=0)

    return top, bottom, left, right


def main():
    folder = os.getcwd()
    png_files = [f for f in os.listdir(folder) if f.lower().endswith(".png")]

    if not png_files:
        print("No PNG files found.")
        return

    global_top = 1e9
    global_left = 1e9
    global_bottom = 0
    global_right = 0

    # 第一步：统计全局裁剪范围
    for filename in png_files:
        path = os.path.join(folder, filename)
        with Image.open(path) as img:
            bbox = find_content_bbox(img)

            if bbox is None:
                continue

            top, bottom, left, right = bbox

            global_top = min(global_top, top)
            global_left = min(global_left, left)
            global_bottom = max(global_bottom, bottom)
            global_right = max(global_right, right)

    global_top = int(global_top)
    global_left = int(global_left)
    global_bottom = int(global_bottom)
    global_right = int(global_right)

    print("Global crop box:")
    print(global_top, global_bottom, global_left, global_right)

    # 第二步：裁剪并转换
    for filename in png_files:
        png_path = os.path.join(folder, filename)
        jpg_name = os.path.splitext(filename)[0] + ".jpg"
        jpg_path = os.path.join(folder, jpg_name)

        with Image.open(png_path) as img:
            cropped = img.crop(
                (global_left, global_top, global_right + 1, global_bottom + 1)
            )

            # 处理透明通道
            if cropped.mode in ("RGBA", "LA"):
                background = Image.new("RGB", cropped.size, (255, 255, 255))
                background.paste(cropped, mask=cropped.split()[-1])
                cropped = background
            else:
                cropped = cropped.convert("RGB")

            cropped.save(jpg_path, "JPEG", quality=90)

        print(f"Processed: {filename} -> {jpg_name}")

    print("Done.")


if __name__ == "__main__":
    main()