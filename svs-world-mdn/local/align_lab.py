# coding: utf-8
import os
import sys
from glob import glob
from os.path import join, basename, expanduser, splitext
from nnmnkwii.io import hts
from fastdtw import fastdtw
import sys
from util import prep_ph2num, ph2numeric, fix_mono_lab_after_align
from tqdm import tqdm
import yaml

if len(sys.argv) != 2:
    print(f"USAGE: {sys.argv[0]} config_path")
    sys.exit(-1)

config = None
with open(sys.argv[1], 'r') as yml:
    config = yaml.load(yml, Loader=yaml.FullLoader)
if config is None:
    print(f"Cannot read config file: {sys.argv[1]}.")
    sys.exit(-1)

with open(sys.argv[1], 'r') as yml:
    config = yaml.load(yml, Loader=yaml.FullLoader)

# Get rough alignment between
# 1) mono-phone labels of singing voice database and
# 2) generated labels by utaupy

table_path = join(expanduser(config["db_root"]), "kana2phonemes_002_oto2lab.table")
ph2num = prep_ph2num(table_path)

utaupy_files = sorted(glob(join(config["out_dir"], "utaupy_mono_round/*.lab")))
mono_label_files = sorted(glob(join(config["out_dir"], "mono_label_round/*.lab")))

dst_dir = join(config["out_dir"], "mono_dtw")
os.makedirs(dst_dir, exist_ok=True)

excludes = []
for (path1, path2) in tqdm(zip(utaupy_files, mono_label_files)):
    lab_utaupy = hts.load(path1)
    lab_mono_label = hts.load(path2)
    name = basename(path1)
    if name in excludes:
        print("Skip!", name)
        continue

    # align two labels roughly based on the phoneme labels
    d, path = fastdtw(ph2numeric(lab_utaupy.contexts,ph2num),
        ph2numeric(lab_mono_label.contexts, ph2num), radius=len(lab_mono_label))

    # Edit utaupy labels with hand-annontated aligments
    for x, y in path:
        lab_utaupy.start_times[x] = lab_mono_label.start_times[y]
        lab_utaupy.end_times[x] = lab_mono_label.end_times[y]

    lab_utaupy = fix_mono_lab_after_align(lab_utaupy, config["spk"])
    with open(join(dst_dir, name), "w") as of:
        of.write(str(lab_utaupy))
    print(name, d)

sys.exit(0)
