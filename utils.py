import os
import pathlib
import matplotlib.pyplot as plt
from argparse import ArgumentParser
import numpy as np
from skimage.metrics import peak_signal_noise_ratio as PSNR
from skimage.metrics import structural_similarity as SSIM
from numpy.fft import fftn, fftshift


def get_diff(targ, src):
    diff = src - targ
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
        plt.text(0.85 * w, 0.94 * h, psnr, color='yellow', size=30)
    if ssim:
        plt.text(0.85 * w, 0.98 * h, ssim, color='yellow', size=30)

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

    parser.add_argument(
        '--gt',
        type=str,
        default=config_json["target_name"],
        help='A target name')

    parser.add_argument(
        '--pattern',
        type=str,
        default=config_json["target_name_pattern"],
        help='A pattern in the target name')

    args = parser.parse_args()
    data_path = args.data_path
    slurm_job_id = os.environ.get('SLURM_JOB_ID')
    slurm_job_id = "." if slurm_job_id == None else f"{slurm_job_id}.tinygpu"

    data_path = data_path.parent / slurm_job_id / data_path.name
    args.data_path = data_path
    return args


def get_filenames(args, is_k=False):
    targets, sources = [], []
    if len(args.data_name) == 0:
        for root, dir, files in os.walk(args.data_path):
            root = pathlib.Path(root)
            distribute_files(root, files, targets, sources, is_k, GT=args.gt)
    else:
        distribute_files(args.data_path, args.data_name, targets, sources, is_k, GT=args.gt)
    return targets, sources


def distribute_files(root, files, targets, sources, is_k, GT="GRAPPA"):
    for file in files:
        if '.npy' in file:
            if is_k and "_k" in file:
                if GT in file:
                    targets.append((root, file))
                else:
                    sources.append((root, file))
            elif not is_k and "_k" not in file:
                if GT in file:
                    targets.append((root, file))
                else:
                    sources.append((root, file))

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


def apply_fft(img, axes=None):
    if axes is None:
        axes = img.shape[-2:]

    return fftshift(fftn(fftshift(img, axes=axes), axes=axes), axes=axes)
