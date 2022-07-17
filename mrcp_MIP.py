import imageio, os
import numpy as np
import pathlib
import matplotlib.pyplot as plt

PATH = pathlib.Path(
    r"C:\Users\z0048drc\Desktop\CS_recon\Results\DGX\good\MID00146_FID00965\png\CS")
png_num = len([i for i in os.listdir(PATH) if 'mip' not in i])

for i in range(png_num):
    fname = PATH / f"MID00146_FID00965_{i}_CS.png"
    im = imageio.imread(fname)
    if "images" not in locals():
        images = np.zeros((png_num, *im.shape[:-1]))
    images[i] = im[:, :, 0]

save_name = PATH/ f"mip_CS_MID00146_FID00965.png"
plt.imshow(np.max(images, axis=0), cmap='gray')
plt.axis('off')
figure = plt.gcf()  # get current figure
figure.set_size_inches(28, 14)
plt.savefig(save_name, bbox_inches='tight', pad_inches=0)
plt.close()