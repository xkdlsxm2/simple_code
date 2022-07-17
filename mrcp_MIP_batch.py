import imageio, os
import numpy as np
import pathlib
import matplotlib.pyplot as plt

Folder_path = pathlib.Path(r"C:\Users\z0048drc\Desktop\CS_recon\Results\MRCP\PAT6\PF_o\pngs")
Folders = [i for i in os.listdir(Folder_path) if "MID" in i[:3]]

for folder in Folders:
    print(f"      - {folder}...")
    PATH = Folder_path / folder / "CS"
    png_num = len([i for i in os.listdir(PATH) if 'mip' not in i])

    for i in range(png_num):
        fname = PATH / f"{folder}_{i}_CS.png"
        im = imageio.imread(fname)
        if "images" not in locals():
            images = np.zeros((png_num, *im.shape[:-1]))
        images[i] = im[:, :, 0]

    save_folder = Folder_path / "MIPs"
    save_folder.mkdir(exist_ok=True, parents=True)
    save_name = save_folder / f"mip_CS_{folder}.png"
    plt.imshow(np.max(images, axis=0), cmap='gray')
    plt.axis('off')
    figure = plt.gcf()  # get current figure
    figure.set_size_inches(28, 14)
    plt.savefig(save_name, bbox_inches='tight', pad_inches=0)
    plt.close()