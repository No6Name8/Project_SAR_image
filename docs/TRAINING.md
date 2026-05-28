# Training on Kaggle

All training runs are executed on Kaggle notebooks using the free T4 GPU (16 GB VRAM). No local GPU is required. Local machines are only used for repo management, config edits, and reviewing results that have been committed back to the repository.

## Step-by-step

### 1. Create a new notebook

1. Go to https://www.kaggle.com → **Create** → **New Notebook**
2. In the notebook sidebar: **Session options** → **Accelerator** → select **GPU T4 x2**
3. Set **Persistence** to **Files only** so outputs survive after the session ends

### 2. Attach the dataset

In the notebook sidebar: **Add data** → search for **greatbird/sardet-100k** → **Add**.

The dataset will be mounted read-only at:
```
/kaggle/input/sardet-100k/
```

### 3. Clone the repo

Run this in a notebook cell to pull configs, scripts, and any helper files:

```python
!git clone https://github.com/No6Name8/Project_SAR_image.git /kaggle/working/repo
```

### 4. Install dependencies and run training

```python
%cd /kaggle/working/repo
!pip install -q ultralytics

# Example: train YOLOv12-small for 50 epochs
!yolo detect train \
    model=yolov12s.pt \
    data=configs/sardet.yaml \
    epochs=50 \
    imgsz=640 \
    project=/kaggle/working/runs \
    name=yolov12s_sardet
```

Adjust `model=` to switch between `yolov12n`, `yolov12s`, `yolov12m`, `yolov12l`, `yolov12x`.

### 5. Save results back to the repo

After training, commit metrics and config snapshots so results are tracked:

```python
import subprocess, shutil, os

# Copy the results summary into the repo
shutil.copytree(
    "/kaggle/working/runs/yolov12s_sardet",
    "/kaggle/working/repo/results/yolov12s_sardet",
    dirs_exist_ok=True,
)

os.chdir("/kaggle/working/repo")
subprocess.run(["git", "config", "user.email", "you@example.com"])
subprocess.run(["git", "config", "user.name", "Your Name"])
subprocess.run(["git", "add", "results/"])
subprocess.run(["git", "commit", "-m", "Add yolov12s training results"])
subprocess.run(["git", "push"])
```

> You will need a GitHub personal access token (PAT) with `repo` scope. Either embed it in the remote URL or store it as a Kaggle secret and read it with `os.environ`.

## Kaggle GPU limits

| Plan | GPU hours / week |
|------|-----------------|
| Free | ~30 h (T4 x2)  |

Sessions time out after 12 hours of inactivity. Save checkpoints frequently using the `save_period` YOLO flag (e.g. `save_period=5`).
