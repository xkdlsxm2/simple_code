from PIL import Image
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import os

DATA_PATH = Path(r"C:\Users\z0048drc\Desktop\CS_recon\Results\MRCP\Results\GRAPPA(PAT3) vs CS, SSDU (PAT6)\PF_x")

if __name__ == "__main__":
    # folders = ["test", "val"]
    files = list(set(["_".join(i.split("_")[2:4]) for i in os.listdir(DATA_PATH)]))
    for file in files:
        print(f"      - {file}...")
        GT_name = [i for i in os.listdir(DATA_PATH) if "GRAPPA" in i and file in i and "diff" not in i][0]
        GT = np.array(Image.open(DATA_PATH / GT_name).convert("L")).astype(float)  # convert "L" => gray scale
        GT /= GT.max()
        targets = [i for i in os.listdir(DATA_PATH) if "GRAPPA" not in i and "diff" not in i and file in i]
        for target in targets:
            target_method = target.split("_")[1]
            recon = np.array(Image.open(DATA_PATH / target).convert("L")).astype(float)
            recon /= recon.max()
            diff = GT - recon

            diff_file_name = DATA_PATH / f"mip_{target_method}_{file}_diff"

            plt.imshow(diff, cmap='gray')
            plt.axis('off')
            figure = plt.gcf()  # get current figure
            figure.set_size_inches(28, 14)
            plt.savefig(diff_file_name, bbox_inches='tight', pad_inches=0)
            plt.close()
