import utils


class multitools:
    def __init__(self, args):
        self.args = args
        self.mode = None
        self.data_path = args.data_path
        self.targets, self.sources = None, None
        self.save_path = None

    def choose_mode(self, mode):
        if mode == "diff":
            self.mode = self.diff
            self.save_path = self.args.save_path / "diff"
        elif mode == "metrics":
            self.mode = self.metrics
            self.save_path = self.args.save_path / "metrics"
        elif mode == 'mip':
            self.mode = self.mip
            self.save_path = self.args.save_path / "mip"
        elif mode == 'slice_imgs':
            self.mode = self.slice_imgs
            self.save_path = self.args.save_path / "slice_imgs"
        elif mode == 'kspace':
            self.mode = self.kspace
            self.save_path = self.args.save_path / "kspace"
        else:
            raise "Mode should be one of 'diff', 'metrics', or 'mip'!"
        print("    - Selected mode:")
        print(self.mode)

    def set_files(self, is_k=False):
        self.targets, self.sources = utils.get_filenames(self.args, is_k)

    def run(self):
        print(f"{self.args.mode} will be processed")
        for mode in self.args.mode:
            self.choose_mode(mode)
            self.mode()

    def diff(self):
        print("\n    - Start diff()\n")
        self.set_files(is_k=False)
        '''
        file name should have the pattern of "mip_METHOD_MIDxxxxx_FIDxxxxx_*"
        '''
        for targ_path, targ in self.targets:
            if self.args.pattern in targ:
                print(f"    {targ}...")
                targ_img = utils.read_image(targ_path/targ)
                for src_path, src in self.sources:
                    print(f"      {src}...")
                    src_img = utils.read_image(src_path/src)
                    diff = utils.get_diff(targ_img, src_img)
                    src_stem = utils.get_stem(src)
                    utils.save_image(diff, self.save_path, f"diff_{src_stem}", vmax=0.1)

    def metrics(self):
        print("\n    - Start metrics()\n")
        self.set_files(is_k=False)
        for targ_path, targ in self.targets:
            if self.args.pattern in targ:
                targ_stem = utils.get_stem(targ)
                print(f"    {targ_stem}...")
                targ_img = utils.read_image(targ_path/targ)
                targ_stem = utils.get_stem(targ)
                utils.save_image(targ_img, self.save_path, f"metrics_{targ_stem}", psnr=f"{'PSNR': >10}", ssim=f"{'SSIM': >10}")
                for src_path, src in self.sources:
                    print(f"      {src}...")
                    src_img = utils.read_image(src_path/src)
                    psnr = utils.get_psnr(targ_img, src_img)
                    ssim = utils.get_ssim(targ_img, src_img)
                    psnr = f"{psnr:.2f} dB"
                    ssim = f'{ssim * 100:.2f} %'
                    src_stem = utils.get_stem(src)
                    utils.save_image(src_img, self.save_path, f"metrics_{src_stem}", psnr=psnr, ssim=ssim)

    def mip(self):
        print("\n    - Start mip()\n")
        self.set_files(is_k=False)
        npy_list = self.targets + self.sources
        for npy_path, npy in npy_list:
            npy_stem = utils.get_stem(npy)
            print(f"   {npy_stem}...")
            npy_img = utils.read_image(npy_path/npy)
            utils.save_image(npy_img, self.save_path, f"mip_{npy_stem}", vmax=0.5)

    def slice_imgs(self):
        print("\n    - Start slice_imgs()\n")
        self.set_files(is_k=False)
        npy_list = self.targets + self.sources
        for npy_path, npy in npy_list:
            npy_stem = utils.get_stem(npy)
            print(f"   {npy_stem}...")
            npy_img = utils.read_image(npy_path/npy)
            utils.save_image(npy_img, self.save_path, f"slice_{npy_stem}", vmin=None, vmax=None)

    def kspace(self):
        print("\n    - Start kspace()\n")
        self.set_files(is_k=True)
        npy_list = self.targets + self.sources
        for npy_path, npy in npy_list:
            if '_k' in npy:
                npy_stem = utils.get_stem(npy, npy)
                print(f"   {npy_stem}...")
                kspace = utils.read_image(npy_path)[0]
                utils.save_image(abs(kspace), self.save_path, f"kspace_{npy_stem}", vmin=None, vmax=None)
