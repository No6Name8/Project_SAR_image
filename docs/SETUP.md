# Environment Setup

## Prerequisites

### 1. Kaggle API key

The dataset is hosted on Kaggle. You need a free Kaggle account and an API token:

1. Log in at https://www.kaggle.com → Account → **Create New Token**
2. A `kaggle.json` file is downloaded. Place it at:

   ```
   ~/.kaggle/kaggle.json
   ```

3. Set permissions so only you can read it:

   ```bash
   chmod 600 ~/.kaggle/kaggle.json
   ```

4. Install the Kaggle CLI if you haven't already:

   ```bash
   pip install kaggle
   ```

### 2. Download the dataset

Run the download script from the repository root:

```bash
python scripts/download_dataset.py
```

This will:
- Download SARDet-100K (`greatbird/sardet-100k`) to `/home/user/sar/datasets/`
- Unzip it into `/home/user/sar/datasets/SARDet_100K/`
- Verify that the expected images and annotation files are present

If the dataset folder already exists, the script exits immediately without re-downloading.

### 3. Convert annotations to YOLO format

SARDet-100K ships with COCO-style JSON annotations. Convert them to the YOLO `.txt` format before training:

```bash
python coco_to_yolo.py
```

> `coco_to_yolo.py` will be added to the repo root. See the script's docstring for output paths and class mapping.

## Expected directory layout after setup

```
/home/user/sar/datasets/SARDet_100K/
├── Annotations/
│   ├── train.json
│   └── val.json
└── JPEGImages/
    ├── train/
    └── val/
```
