import h5py, pickle, os, pathlib, torch
import numpy as np

PATH = pathlib.Path(r"C:\Users\z0048drc\Desktop\CS_recon\Results\sens_maps_local\TH0\tmp")


def get_files(directory: pathlib.Path):
    file_lists = np.array(os.listdir(directory))
    file_lists.sort()
    idx = 0
    files = []  # each element: (fname, max_slice_num)
    while idx < len(file_lists):
        fname = file_lists[idx].split("_")[0]
        slices = []
        while True:
            if idx < len(file_lists) and fname in file_lists[idx]:
                slices.append(int(file_lists[idx].split("_")[1]))
                idx += 1
            else:
                files.append((fname, np.max(slices)+1))
                break

    return files


def sens_load(fname, slice_num):
    fname = f"{fname}_{slice_num}_sens_map.pkl"
    sens_map = pickle.load(open(PATH / fname, 'rb'))
    sens_map = sens_map[..., 0] + 1j * sens_map[..., 1]
    return torch.permute(sens_map, (1, 2, 0))


if __name__ == "__main__":
    files = get_files(PATH)
    for file, max_slice in files:
        tmp_sens = sens_load(file, 0)
        sens_maps = torch.zeros((max_slice, *tmp_sens.shape), dtype=torch.complex64)
        for i in range(max_slice):
            sens_maps[i] = sens_load(file, i)
        hf = h5py.File(f'{file}_sens_maps.h5', 'w')
        hf.create_dataset('sens_maps', data=sens_maps.numpy())
