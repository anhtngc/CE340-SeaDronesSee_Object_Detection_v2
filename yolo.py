# Chuyển đổi json theo định dạng YOLO
import json
import os

json_path = 'sample/instances_val.json'
images_dir = 'val'
labels_dir = os.path.join(images_dir, 'labels')
os.makedirs(labels_dir, exist_ok=True)

with open(json_path, 'r') as f:
    coco = json.load(f)

images = {img["id"]: (img["file_name"], img["width"], img["height"]) for img in coco["images"]}
annotations = coco["annotations"]

for ann in annotations:
    image_id = ann["image_id"]
    cat_id = ann["category_id"]
    if cat_id == 0:
        continue  # bỏ class 'ignored'

    x, y, w, h = ann["bbox"]
    file_name, img_w, img_h = images[image_id]

    # Chuẩn hóa tọa độ
    x_center = (x + w / 2) / img_w
    y_center = (y + h / 2) / img_h
    norm_w = w / img_w
    norm_h = h / img_h

    line = f"{cat_id - 1} {x_center:.6f} {y_center:.6f} {norm_w:.6f} {norm_h:.6f}\n"
    label_path = os.path.join(labels_dir, file_name.replace('.jpg', '.txt'))
    with open(label_path, 'a') as f:
        f.write(line)