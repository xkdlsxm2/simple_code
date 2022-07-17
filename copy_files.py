import os
import pathlib, pickle
import numpy as np
import shutil

DATA_CACHE_PATH = pathlib.Path(r"C:\Users\z0048drc\Desktop\CS_recon\Results\MRCP\New folder")

if __name__ == "__main__":
    for i in range(1, 44):
        src = DATA_CACHE_PATH/f"MRCP_{i}"/'Recon'/'png'/ 'mrcp_CS-SENSE.png'
        dest = DATA_CACHE_PATH/f"MRCP"/f'mrcp_CS-SENSE_{i}.png'
        shutil.copyfile(src, dest)
