"""
Download SARDet-100K from Kaggle and verify the expected folder structure.

Requirements:
    pip install kaggle
    Place ~/.kaggle/kaggle.json with your API credentials before running.

Usage:
    python scripts/download_dataset.py
"""

import subprocess
import sys
import zipfile
from pathlib import Path

DATASET_ROOT = Path("C:/Users/h/Documents/SARDet_100K")
DOWNLOAD_DIR = Path("C:/Users/h/Documents")
KAGGLE_DATASET = "greatbird/sardet-100k"

REQUIRED_PATHS = [
    DATASET_ROOT / "JPEGImages" / "train",
    DATASET_ROOT / "JPEGImages" / "val",
    DATASET_ROOT / "Annotations" / "train.json",
    DATASET_ROOT / "Annotations" / "val.json",
]


def download():
    print(f"Downloading {KAGGLE_DATASET} to {DOWNLOAD_DIR} ...")
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

    result = subprocess.run(
        ["kaggle", "datasets", "download", "-d", KAGGLE_DATASET, "-p", str(DOWNLOAD_DIR)],
        check=False,
    )
    if result.returncode != 0:
        print(
            "ERROR: kaggle download failed.\n"
            "Make sure the kaggle package is installed (`pip install kaggle`) and\n"
            "~/.kaggle/kaggle.json exists with valid credentials."
        )
        sys.exit(1)


def unzip():
    # Kaggle names the zip after the dataset slug
    zip_name = KAGGLE_DATASET.split("/")[-1] + ".zip"
    zip_path = DOWNLOAD_DIR / zip_name

    if not zip_path.exists():
        # Fall back: look for any .zip in the download directory
        zips = list(DOWNLOAD_DIR.glob("*.zip"))
        if not zips:
            print(f"ERROR: No zip file found in {DOWNLOAD_DIR} after download.")
            sys.exit(1)
        zip_path = zips[0]

    print(f"Unzipping {zip_path} -> {DATASET_ROOT} ...")
    DATASET_ROOT.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(DATASET_ROOT)

    zip_path.unlink()
    print("Zip file removed after extraction.")


def verify():
    missing = [p for p in REQUIRED_PATHS if not p.exists()]
    if missing:
        print("ERROR: The following expected paths are missing after extraction:")
        for p in missing:
            print(f"  {p}")
        print(
            "\nThe zip contents may use a different internal layout. "
            "Check the extracted files under:\n"
            f"  {DATASET_ROOT}"
        )
        sys.exit(1)


def main():
    if DATASET_ROOT.exists():
        print("Dataset already exists, skipping download.")
        sys.exit(0)

    download()
    unzip()
    verify()

    print("\nDataset ready.")
    print(f"  Location : {DATASET_ROOT}")
    print("  Next step: python coco_to_yolo.py")


if __name__ == "__main__":
    main()
