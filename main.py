import zipfile
from pathlib import Path
import os
import json
import shutil

texture_dir = Path("")

tmp_dir = Path("tmp")
packtexture = Path("packtexture")

if not os.path.exists(tmp_dir):
    os.mkdir(tmp_dir)

if not os.path.exists(packtexture):
    os.mkdir(packtexture)

for file in os.listdir(texture_dir):
    if not os.path.isfile(texture_dir/file):
        continue
    
    if file.endswith(".disabled"):
        continue

    with zipfile.ZipFile(texture_dir/file, 'r') as zip_ref:
        # detect assets folder
        if "assets/" in zip_ref.namelist():
            for name in zip_ref.namelist():
                if name.startswith("assets"):
                    zip_ref.extract(name, tmp_dir)
        else:
            continue

        for path, subdirs, files in os.walk(tmp_dir):
            for name in files:
                file_name = os.path.join(path, name)
                file_name = file_name[4:]

                pth = Path()
                for folder in file_name.split("\\")[:-1]:
                    pth = pth/folder
                    if not os.path.isdir(packtexture/pth):
                        os.mkdir(packtexture/pth)
                
                if os.path.isfile(packtexture/file_name):
                    if file_name.endswith(".png"):
                        os.remove(packtexture/file_name)
                    elif file_name.endswith(".json"):
                        with open(packtexture/file_name, "r") as f:
                            data = json.load(f)
                        with open(tmp_dir/file_name, "r") as f:
                            data2 = json.load(f)
                        data.update(data2)
                        with open(packtexture/file_name, "w") as f:
                            json.dump(data, f)
                        os.remove(tmp_dir/file_name)
                else:
                    os.rename(tmp_dir/file_name, packtexture/file_name)
    shutil.rmtree(tmp_dir/'assets', ignore_errors=True)