import os
import shutil
import random

def split_dataset(vis_dir, ir_dir, labels_dir, output_dir, train_ratio=0.8):
    # 创建 train 和 val 目录
    train_vis = os.path.join(output_dir, "train", "Vis")
    train_ir = os.path.join(output_dir, "train", "Ir")
    train_labels = os.path.join(output_dir, "train", "labels")
    val_vis = os.path.join(output_dir, "val", "Vis")
    val_ir = os.path.join(output_dir, "val", "Ir")
    val_labels = os.path.join(output_dir, "val", "labels")
    
    for folder in [train_vis, train_ir, train_labels, val_vis, val_ir, val_labels]:
        os.makedirs(folder, exist_ok=True)
    
    # 获取所有文件名（不含扩展名）
    filenames = [f.split(".")[0] for f in os.listdir(vis_dir) if f.endswith(".png")]
    filenames.sort()
    
    # 随机打乱数据，并按比例划分
    random.shuffle(filenames)
    split_index = int(len(filenames) * train_ratio)
    train_files = filenames[:split_index]
    val_files = filenames[split_index:]
    
    def move_files(files, src_dir, dst_dir, ext):
        for file in files:
            src_path = os.path.join(src_dir, file + ext)
            dst_path = os.path.join(dst_dir, file + ext)
            if os.path.exists(src_path):
                shutil.copy2(src_path, dst_path)
    
    # 移动文件
    move_files(train_files, vis_dir, train_vis, ".png")
    move_files(train_files, ir_dir, train_ir, ".png")
    move_files(train_files, labels_dir, train_labels, ".txt")
    
    move_files(val_files, vis_dir, val_vis, ".png")
    move_files(val_files, ir_dir, val_ir, ".png")
    move_files(val_files, labels_dir, val_labels, ".txt")
    
    print("Dataset split completed!")

if __name__ == "__main__":
    vis_dir = "/media/ntu/volume1/home/s124md306_06/dataset/Vis"
    ir_dir = "/media/ntu/volume1/home/s124md306_06/dataset/Ir"
    labels_dir = "/media/ntu/volume1/home/s124md306_06/dataset/labels"
    output_dir = "/media/ntu/volume1/home/s124md306_06/dataset"
    
    split_dataset(vis_dir, ir_dir, labels_dir, output_dir)
