import os
import argparse
import xml.etree.ElementTree
import shutil

parser = argparse.ArgumentParser(prog='anotation renamer for Pascal VOC')
parser.add_argument('input_dir')
parser.add_argument('output_dir')
parser.add_argument('sec_from', type=int)
args = parser.parse_args( )

annotations_dir = os.path.join(args.input_dir, 'Annotations')
annotation_file_list = sorted(os.listdir(annotations_dir))

image_dir = os.path.join(args.input_dir, 'JPEGImages')
image_file_list = sorted(os.listdir(image_dir))

assert len(annotation_file_list) == len(image_file_list)

for index, (annotation_file, image_file) in enumerate(zip(annotation_file_list, image_file_list)):
    index += args.sec_from

    tree = xml.etree.ElementTree.parse(os.path.join(annotations_dir, annotation_file))
    root = tree.getroot()

    for folder in root.iter('folder'):
        folder.text = args.output_dir

    new_annotation_file = '{}.xml'.format(str(index).zfill(6))
    _, ext = os.path.splitext(image_file)
    new_image_file = '{}{}'.format(str(index).zfill(6), ext)

    for filename in root.iter('filename'):
        filename.text = new_image_file

    for path in root.iter('path'):
        path.text = os.path.join(os.path.dirname(path.text), new_image_file)

    tree.write(os.path.join(args.output_dir, new_annotation_file))

    shutil.copyfile(os.path.join(image_dir, image_file), os.path.join(args.output_dir, new_image_file))

