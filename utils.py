import os
import pathlib
import matplotlib.pyplot as plt
from argparse import ArgumentParser
import numpy as np
from PIL import Image
from skimage.metrics import peak_signal_noise_ratio as PSNR
from skimage.metrics import structural_similarity as SSIM


def get_diff(targ, src):
    diff = src - targ
    diff -= diff.min()
    diff /= diff.max()
    return diff


def get_mip(image):
    mip = np.max(image, axis=0)
    mip /= mip.max()
    return mip


def save_image(image, path: pathlib.Path, name, vmin=0, vmax=1, psnr=None, ssim=None):
    h, w = image.shape

    path.mkdir(parents=True, exist_ok=True)
    diff_file_name = path / name

    plt.imshow(image, cmap='gray', vmax=vmax, vmin=vmin)
    plt.axis('off')
    if psnr:
        plt.text(0.85*w, 0.92*h, f'{psnr:.2f} dB', color='yellow', size=25)
    if ssim:
        plt.text(0.85*w, 0.98*h, f'{ssim * 100:.2f} %', color='yellow', size=25)

    figure = plt.gcf()  # get current figure
    figure.set_size_inches(28, 14)
    plt.savefig(diff_file_name, bbox_inches='tight', pad_inches=0)
    plt.close()


def build_args(config_json):
    parser = ArgumentParser()

    config = config_json['path']
    parser.add_argument(
        '--save_path',
        type=str,
        default=pathlib.Path(config["save_path"]),
        help='path to save reconstruction images and pickles')

    parser.add_argument(
        '--data_path',
        type=str,
        default=pathlib.Path(config["data_path"]),
        help='path to data')

    parser.add_argument(
        '--data_name',
        default=config["data_name"],
        help='data name to be reconstructed (None: all data in the path')

    config = config_json['programs']
    parser.add_argument(
        '--mode',
        type=list,
        default=config["mode"],
        help='Multitools mode')

    args = parser.parse_args()
    data_path = args.data_path
    slurm_job_id = os.environ.get('SLURM_JOB_ID')
    slurm_job_id = "." if slurm_job_id == None else f"{slurm_job_id}.tinygpu"

    data_path = data_path.parent / slurm_job_id / data_path.name
    args.data_path = data_path
    return args


def get_filenames(path):
    targets, sources = [], []

    for root, dir, files in os.walk(path):
        for file in files:
            if "GRAPPA" in file:
                targets.append(file)
            else:
                sources.append(file)
    return targets, sources


def read_image(path):
    with open(path, 'rb') as f:
        image = np.load(f)
    return image


def get_psnr(src, targ):
    return PSNR(src, targ)


def get_ssim(src, targ):
    return SSIM(src, targ)


def get_stem(fname):
    return fname.split(".")[0]