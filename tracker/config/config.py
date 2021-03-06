from ..utils.parser import get_config
import os
from django.conf import settings

class Config(object):
    # arcface cfg
    use_se = False
    arc_model_path = './tracker/weights/arcface_resnet18_110.pth'
    # arc_model_path = './tracker/weights/arcface_resnet18_40_ft.pth'
    sim_threshold = 0.4
    # sim_threshold = 0.5

    # Retinaface cfg
    cfg_mnet = {
    'name': 'mobilenet0.25',
    'min_sizes': [[16, 32], [64, 128], [256, 512]],
    'steps': [8, 16, 32],
    'variance': [0.1, 0.2],
    'clip': False,
    'loc_weight': 2.0,
    'gpu_train': True,
    'batch_size': 32,
    'ngpu': 1,
    'epoch': 250,
    'decay1': 190,
    'decay2': 220,
    'image_size': 640,
    'pretrain': False,
    'return_layers': {'stage1': 1, 'stage2': 2, 'stage3': 3},
    'in_channel': 32,
    'out_channel': 64,
    'weight_path': './tracker/weights/retina_face_mobilenet0.25_Final.pth'
    # 'weight_path': './tracker/weights/retina_face_mobilenet0.25_Final_ft_e500.pth'
    }    
    confidence_threshold = 0.6
    nms_threshold = 0.4
    detect_threshold = 0.6

    # yolov5 (person detection) cfg
    yolo_model_path = './tracker/weights/yolov5/yolov5s.pt'
    yolo_confidence_threshold = 0.4
    yolo_nms_threshold = 0.5
    
    # deepsort cfg
    deepsort_config_path = './tracker/config/deep_sort.yaml'
    deepsort_cfg = get_config()
    deepsort_cfg.merge_from_file(deepsort_config_path)

    # cfg
    features_path = os.path.join(settings.STATIC_ROOT,'registration')

    