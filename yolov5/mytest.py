# YOLO5.ipynb
# Install Dependencies
from google.colab import drive
from IPython.display import Image, display
import glob
from utils.plots import plot_results  # plot results.txt as results.png
from IPython.core.magic import register_line_cell_magic
import yaml
from utils.google_utils import gdrive_download  # to download models/datasets
from IPython.display import Image, clear_output  # to display images
import torch

# clone YOLOv5 repository
# !git clone https: // github.com/ultralytics/yolov5  # clone repo
# %cd yolov5
# !git reset - -hard 886f1c03d839575afecb059accf74296fad395b6

# install dependencies as necessary
# !pip install - qr requirements.txt  # install dependencies (ignore errors)

# clear_output()
print('Setup complete. Using torch %s %s' % (torch.__version__,
      torch.cuda.get_device_properties(0) if torch.cuda.is_available() else 'CPU'))

# Download Correctly Formatted Custom Dataset from roboflow.com
# Export code snippet and paste here
# %cd / content
# !curl - L "https://app.roboflow.com/ds/CHANGE HERE" > roboflow.zip
# unzip roboflow.zip
# rm roboflow.zip
# this is the YAML file Roboflow wrote for us that we're loading into this notebook with our data
# %cat data.yaml

# Model Configuration and Architecture
# define number of classes based on YAML
with open("data.yaml", 'r') as stream:
    num_classes = str(yaml.safe_load(stream)['nc'])

# this is the model configuration we will use for our tutorial
# %cat / content/yolov5/models/yolov5s.yaml

# customize iPython writefile so we can write variables


@register_line_cell_magic
def writetemplate(line, cell):
    with open(line, 'w') as f:
        f.write(cell.format(**globals()))


# % % writetemplate / content/yolov5/models/custom_yolov5s.yaml

# parameters
nc: {num_classes}  # number of classes
depth_multiple: 0.33  # model depth multiple
width_multiple: 0.50  # layer channel multiple

# anchors
anchors:
    - [10, 13, 16, 30, 33, 23]  # P3/8
    - [30, 61, 62, 45, 59, 119]  # P4/16
    - [116, 90, 156, 198, 373, 326]  # P5/32

# YOLOv5 backbone
backbone:
    # [from, number, module, args]
    [[-1, 1, Focus, [64, 3]],  # 0-P1/2
     [-1, 1, Conv, [128, 3, 2]],  # 1-P2/4
     [-1, 3, BottleneckCSP, [128]],
     [-1, 1, Conv, [256, 3, 2]],  # 3-P3/8
     [-1, 9, BottleneckCSP, [256]],
     [-1, 1, Conv, [512, 3, 2]],  # 5-P4/16
     [-1, 9, BottleneckCSP, [512]],
     [-1, 1, Conv, [1024, 3, 2]],  # 7-P5/32
     [-1, 1, SPP, [1024, [5, 9, 13]]],
     [-1, 3, BottleneckCSP, [1024, False]],  # 9
     ]

# YOLOv5 head
head:
    [[-1, 1, Conv, [512, 1, 1]],
     [-1, 1, nn.Upsample, [None, 2, 'nearest']],
     [[-1, 6], 1, Concat, [1]],  # cat backbone P4
     [-1, 3, BottleneckCSP, [512, False]],  # 13

     [-1, 1, Conv, [256, 1, 1]],
     [-1, 1, nn.Upsample, [None, 2, 'nearest']],
     [[-1, 4], 1, Concat, [1]],  # cat backbone P3
     [-1, 3, BottleneckCSP, [256, False]],  # 17 (P3/8-small)

     [-1, 1, Conv, [256, 3, 2]],
     [[-1, 14], 1, Concat, [1]],  # cat head P4
     [-1, 3, BottleneckCSP, [512, False]],  # 20 (P4/16-medium)

     [-1, 1, Conv, [512, 3, 2]],
     [[-1, 10], 1, Concat, [1]],  # cat head P5
     [-1, 3, BottleneckCSP, [1024, False]],  # 23 (P5/32-large)

     [[17, 20, 23], 1, Detect, [nc, anchors]],  # Detect(P3, P4, P5)
     ]

# Train on custom dataset
# Here, we are able to pass a number of arguments:
# - **img:** define input image size
# - **batch:** determine batch size
# - **epochs:** define the number of training epochs. (Note: often, 3000+ are common here!)
# - **data:** set the path to our yaml file
# - **cfg:** specify our model configuration
# - **weights:** specify a custom path to weights. (Note: you can download weights from the Ultralytics Google Drive [folder](https://drive.google.com/open?id=1Drs_Aiu7xx6S-ix95f9kNsA6ueKRpN2J))
# - **name:** result names
# - **nosave:** only save the final checkpoint
# - **cache:** cache images for faster training

# train yolov5s on custom data for 100 epochs
# time its performance
% % time
%cd / content/yolov5/
!python train.py - -img 256 - -batch 16 - -epochs 350 - -data '../data.yaml' - -cfg ./models/custom_yolov5s.yaml - -weights '' - -name yolov5s_results - -cache

# Evaluate Custom YOLOv5 Detector Performance
# Start tensorboard
# Launch after you have started training
# logs save in the folder "runs"
%load_ext tensorboard
%tensorboard - -logdir runs

# we can also output some older school graphs if the tensor board isn't working for whatever reason...
Image(filename='/content/yolov5/runs/train/yolov5s_results/results.png',
      width=1000)  # view results.png

# Visualization
# first, display our ground truth data
print("GROUND TRUTH TRAINING DATA:")
Image(filename='/content/yolov5/runs/train/yolov5s_results/test_batch0_labels.jpg', width=900)

# print out an augmented training example
print("GROUND TRUTH AUGMENTED TRAINING DATA:")
Image(filename='/content/yolov5/runs/train/yolov5s_results/train_batch0.jpg', width=900)

# trained weights are saved by default in our weights folder
%ls runs/
%ls runs/train/yolov5s_results/weights

# use the best weights!
%cd / content/yolov5/
!python detect.py - -weights runs/train/yolov5s_results/weights/best.pt - -img 416 - -conf 0.4 - -source ../test/images

# display inference on ALL test images
# this looks much better with longer training above


for imageName in glob.glob('/content/yolov5/runs/detect/exp/*.jpg'):  # assuming JPG
    display(Image(filename=imageName))
    print("\n")

# Trained Weights for Future Inference
drive.mount('/content/gdrive')
%cp / content/yolov5/runs/train/yolov5s_results/weights/best.pt / content/gdrive/My\ Drive
