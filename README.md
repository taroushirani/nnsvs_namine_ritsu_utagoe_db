# nnsvs_namine_ritsu_utagoe_db

[NNSVS](https://github.com/r9y9/nnsvs) recipe of Ritsu Namine's singing voice database (60 songs).
Almost all codes are derived from [kiritan_singing](https://github.com/r9y9/kiritan_singing).

## Requirements
- nnsvs
- utaupy
- nnmnkwii
- librosa
- soundfile
- scipy
- numpy
- tqdm
- jaconv
- pyyaml

## How to use
Due to the licensing issue, this recipe does not include data nor helper scripts for downloading automatically. First of all, you need to get 
「波音リツ」歌声データベース.zip from https://drive.google.com/drive/folders/1XA2cm3UyRpAk_BJb1LTytOWrhjsZKbSN . Next, clone this repository and change `db_root` in `svs-mdn-world/config.yaml` according to your environment. Then move to `svs-mdn-world` directory and run:

    run.sh --stage 0 --stop-stage 6

The directory structure made by this recipe is the same as kiritan_singing does.

## Sample code
- 


## Resources
- 「波音リツ」歌声データベース 配布　【※これは生歌です】: https://www.youtube.com/watch?v=K0NuZK0IiGA
