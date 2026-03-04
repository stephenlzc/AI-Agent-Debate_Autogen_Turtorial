#---------------data.py 代码如下----------------------#
import json 
import re 
import shutil 
import os 
import copy  
input_file_path = 'pixart-sigma-toy-dataset'
input_json = os.path.join(input_file_path, 'InternData', 'data_info.json') 
if not os.path.exists('images_txt_datasets'):    
    os.makedirs('images_txt_datasets') 
with open(input_json, 'r', encoding='utf-8') as file:    
    datas = json.load(file)
for i, data in enumerate(datas):    
    print(f'--{i}')    
    image_name = data['path']    
    image_path = os.path.join(input_file_path, 'InternImgs', image_name)    
    new_image_path = os.path.join('images_txt_datasets', image_name)    
    shutil.copy2(image_path, new_image_path)         
    txt_name = image_name.replace('png', 'txt')    
    txt_path = os.path.join('images_txt_datasets', txt_name)         
    with open(txt_path, 'w') as file:        
        file.write(data['prompt'])