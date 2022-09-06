import sys
sys.path.append('./')  # to run '$ python *.py' files in subdirectories
import torch
import torch.nn as nn
import models
from models.experimental import attempt_load
from utils.activations import Hardswish, SiLU

# Load PyTorch model
weights = './temp/yolov7-w6-pose.pt'
device = torch.device('cpu')  # cuda:0
model = attempt_load(weights, map_location=device)  # load FP32 model

# Update model
for k, m in model.named_modules():
    m._non_persistent_buffers_set = set()  # pytorch 1.6.0 compatibility
    if isinstance(m, models.common.Conv):  # assign export-friendly activations
        if isinstance(m.act, nn.Hardswish):
            m.act = Hardswish()
        elif isinstance(m.act, nn.SiLU):
            m.act = SiLU()
model.model[-1].export = True # set Detect() layer grid export
model.eval()

# Input
img = torch.randn(1, 3, 1280, 768).to(device)  # image size(1,3,320,192) iDetection
torch.onnx.export(model, img, './temp/yolov7-w6-poseeeee.onnx', verbose=False, opset_version=13, input_names=['images'])