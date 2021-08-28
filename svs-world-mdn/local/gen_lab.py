# coding: utf-8
from utaupy.utils import ust2hts
import os
import sys
from glob import glob
from os.path import join, basename, expanduser, splitext
from nnmnkwii.io import hts
from util import merge_sil, fix_mono_lab_before_align
from tqdm import tqdm
import yaml
import tempfile

if len(sys.argv) != 2:
    print(f"USAGE: {sys.argv[0]} config_path")
    sys.exit(-1)

config = None
with open(sys.argv[1], 'r') as yml:
    config = yaml.load(yml, Loader=yaml.FullLoader)
if config is None:
    print(f"Cannot read config file: {sys.argv[1]}.")
    sys.exit(-1)

table_path = join(expanduser(config["db_root"]), "kana2phonemes_002_oto2lab.table")
    
# generate full/mono labels by utaupy
print("Convert ust to label files.")
files = sorted(glob(join(expanduser(config["db_root"]), "**/*.ust"), recursive=True))
for ust_path in tqdm(files):
    name = splitext(basename(ust_path))[0]
    if name in config["exclude_songs"]:
        continue

    for as_mono in [True, False]:
        n = "utaupy_mono" if as_mono else "utaupy_full"
        f = tempfile.NamedTemporaryFile("w+")
        
        ust2hts(ust_path, f.name, table_path, strict_sinsy_style=False, as_mono=as_mono)    

        lab = hts.HTSLabelFile()
        for l in f.readlines():
            lab.append(l.split(), strict=False)
        lab = merge_sil(lab)
        dst_dir = join(config["out_dir"], f"{n}")
        os.makedirs(dst_dir, exist_ok=True)
        with open(join(dst_dir, name + ".lab"), "w") as f:
            f.write(str(lab))

        f.close()

        
print("Copy original label files.")
files = sorted(glob(join(expanduser(config["db_root"]), "**/*.lab"), recursive=True))
dst_dir = join(config["out_dir"], "mono_label")
os.makedirs(dst_dir, exist_ok=True)
for m in tqdm(files):
    name = splitext(basename(m))[0]
    if name in config["exclude_songs"]:
        continue
    f = hts.load(m)
    with open(join(dst_dir, basename(m)), "w") as of:
        of.write(str(fix_mono_lab_before_align(f, config["spk"])))

# Rounding
print("Round label files.")
for name in ["utaupy_mono", "utaupy_full", "mono_label"]:
    files = sorted(glob(join(config["out_dir"], name, "*.lab")))
    dst_dir = join(config["out_dir"], name + "_round")
    os.makedirs(dst_dir, exist_ok=True)

    for path in tqdm(files):
        lab = hts.load(path)
        name = basename(path)

        for x in range(len(lab)):
            lab.start_times[x] = round(lab.start_times[x] / 50000) * 50000
            lab.end_times[x] = round(lab.end_times[x] / 50000) * 50000

        # Check if rounding is done property
        if name == "mono_label":
            for i in range(len(lab)-1):
                if lab.end_times[i] != lab.start_times[i+1]:
                    print(path)
                    print(i, lab[i])
                    print(i+1, lab[i+1])
                    import ipdb; ipdb.set_trace()

        with open(join(dst_dir, name), "w") as of:
            of.write(str(lab))
