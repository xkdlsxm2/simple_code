from PIL import Image
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import os
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim

DATA_PATH = Path(r"C:\Users\z0048drc\Desktop\CS_recon\Results\MRCP\Results\GRAPPA(PAT3) vs CS, SSDU (PAT6)\PF_x")

if __name__ == "__main__":
    # folders = ["test", "val"]
    files = list(set(["_".join(i.split("_")[2:4]) for i in os.listdir(DATA_PATH)]))
    for file in files:
        print(f"      - {file}...")
        GT_name = [i for i in os.listdir(DATA_PATH) if "GRAPPA" in i and file in i and "diff" not in i][0]
        GT = np.array(Image.open(DATA_PATH / GT_name).convert("L")).astype(float)  # convert "L" => gray scale
        GT /= GT.max()
        targets = [i for i in os.listdir(DATA_PATH) if "GRAPPA" not in i and "diff" not in i and file in i and "metrics" not in i]
        for target in targets:
            target_method = target.split("_")[1]
            recon = np.array(Image.open(DATA_PATH / target).convert("L")).astype(float)
            recon /= recon.max()
            psnr_ = psnr(GT, recon)
            ssim_ = ssim(GT, recon)

            metric_file_path = DATA_PATH / "metrics"
            metric_file_path.mkdir(parents=True, exist_ok=True)
            diff_file_name = metric_file_path / target

            plt.imshow(recon, cmap='gray')
            plt.axis('off')
            plt.text(1265, 50, f'{psnr_:.2f} dB', color='yellow', size=40)
            plt.text(1265, 120, f'{ssim_ * 100:.2f} %', color='yellow', size=40)
            figure = plt.gcf()  # get current figure
            figure.set_size_inches(28, 14)
            plt.savefig(diff_file_name, bbox_inches='tight', pad_inches=0)
            plt.close()
