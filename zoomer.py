from PIL import Image
import matplotlib.pyplot as plt
import pathlib, os
import numpy as np
from matplotlib.patches import Rectangle

dataPath = pathlib.Path(r"C:\Users\z0048drc\Desktop\temp\Retreat_figure\mrcp")


def zoom_at(img, x, y, width, height, path=None):
    img_crop = img.crop((x, y, x + width, y + height))

    plt.imshow(img, cmap='gray')
    # Get the current reference
    ax = plt.gca()
    ax.axis('off')

    # Create a Rectangle patch
    rect = Rectangle((x, y), width=width, height=height, linewidth=2, edgecolor='r', facecolor='none')

    # Add the patch to the Axes
    ax.add_patch(rect)
    if path is None:
        plt.show()
    else:
        figure = plt.gcf()  # get current figure
        figure.set_size_inches(28, 14)
        plt.savefig(path.with_stem(f"{path.stem}_redbox"), bbox_inches='tight', pad_inches=0)
        plt.close()

    plt.close()
    plt.imshow(img_crop, cmap='gray')
    ax = plt.gca()
    ax.axis('off')
    if path is None:
        plt.show()
    else:
        figure = plt.gcf()  # get current figure
        figure.set_size_inches(28, 14)
        plt.savefig(path.with_stem(f"{path.stem}_zoomed"), bbox_inches='tight', pad_inches=0)
        plt.close()


if __name__ == "__main__":
    datalist = os.listdir(dataPath)

    for i in datalist:
        data_dir = dataPath / i
        if data_dir.suffix == ".png":
            image = Image.open(data_dir).convert('L')
            zoom_at(image, 300, 320, 500, 330, data_dir)
