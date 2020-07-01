# Pepper recognition QiBullet
[![license](https://img.shields.io/github/license/mashape/apistatus.svg)](LICENSE)

Simulation in QiBullet of a paper robot capable of object recognition using YOLO v3



### Prerequisites
* Tensorflow 2.1.0
* tensorflow_addons 0.9.1 (required for mish activation)

### Instllation
We recommend an isolated eviroment (you can use conda).

Download yolov3.weights file: https://drive.google.com/open?id=1cewMfusmPjYWbrnuJRuKhPMwRe_b9PaT
For CPU:
```
pip install -r requeriments
```
For GPU
```
pip install -r requeriments-gpu
```

### Usage
Run in two different terminals the following commands. You got to wait until image_processor fully starts
```
# Neural Net
python image_processor.py --weights /path/to/yolov3.weights --framework tf --size 320 --model yolov3

# Simulator
python simulatio.py
```

### References

  * YOLOv4: Optimal Speed and Accuracy of Object Detection [YOLOv4](https://arxiv.org/abs/2004.10934).
  * [darknet](https://github.com/AlexeyAB/darknet)
  
   My project is inspired by these previous fantastic YOLOv3 implementations:
  * [Yolov3 tensorflow](https://github.com/YunYang1994/tensorflow-yolov3)
  * [Yolov3 tf2](https://github.com/zzh8829/yolov3-tf2)
  * [tensorflow-yolov4-tflite](https://github.com/hunglc007/tensorflow-yolov4-tflite)
