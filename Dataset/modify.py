import os
import xml.etree.ElementTree as ET

# 类别名称，确保它们与训练时的类别顺序一致
classes = ["People", "Car", "Bus", "Motorcycle", "Lamp", "Truck"]

def convert_voc_to_yolo(xml_file, output_dir):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    xml_filename = os.path.basename(xml_file)
    txt_filename = xml_filename.replace(".xml", ".txt")
    
    width = int(root.find("size/width").text)
    height = int(root.find("size/height").text)
    
    output_file = os.path.join(output_dir, txt_filename)
    with open(output_file, "w") as f:
        for obj in root.findall("object"):
            class_name = obj.find("name").text
            if class_name not in classes:
                continue
            class_id = classes.index(class_name)
            
            bbox = obj.find("bndbox")
            xmin = int(bbox.find("xmin").text)
            ymin = int(bbox.find("ymin").text)
            xmax = int(bbox.find("xmax").text)
            ymax = int(bbox.find("ymax").text)
            
            # 归一化 YOLO 格式 (x_center, y_center, width, height)
            x_center = (xmin + xmax) / 2.0 / width
            y_center = (ymin + ymax) / 2.0 / height
            box_width = (xmax - xmin) / width
            box_height = (ymax - ymin) / height
            
            f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {box_width:.6f} {box_height:.6f}\n")

def process_xml_folder(xml_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for i in range(4200):
        xml_file = f"{i:05d}.xml"
        xml_path = os.path.join(xml_folder, xml_file)
        if os.path.exists(xml_path):
            convert_voc_to_yolo(xml_path, output_folder)
            print(f"Converted: {xml_file} -> {xml_file.replace('.xml', '.txt')}")

if __name__ == "__main__":
    xml_folder = "/media/ntu/volume1/home/s124md306_06/dataset/Annotation"
    output_folder = "/media/ntu/volume1/home/s124md306_06/dataset/labels"
    process_xml_folder(xml_folder, output_folder)
    print("Conversion completed!")
