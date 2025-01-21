import argparse
import cv2 as cv

backends = (cv.dnn.DNN_BACKEND_DEFAULT, cv.dnn.DNN_BACKEND_HALIDE, cv.dnn.DNN_BACKEND_INFERENCE_ENGINE, cv.dnn.DNN_BACKEND_OPENCV,
            cv.dnn.DNN_BACKEND_VKCOM, cv.dnn.DNN_BACKEND_CUDA)
targets = (cv.dnn.DNN_TARGET_CPU, cv.dnn.DNN_TARGET_OPENCL, cv.dnn.DNN_TARGET_OPENCL_FP16, cv.dnn.DNN_TARGET_MYRIAD,
           cv.dnn.DNN_TARGET_VULKAN, cv.dnn.DNN_TARGET_CUDA, cv.dnn.DNN_TARGET_CUDA_FP16)
def parser_fn(parser):
        #parser.add_argument("--input", type=str, default="VIDEO\VIDEO3.1.mp4", help="Path to video source")
        parser.add_argument("--tracker_algo", type=str, default="nanotrack", help="One of available tracking algorithms: mil, goturn, dasiamrpn, nanotrack, vittrack") #default=nanotrack
        parser.add_argument("--goturn", type=str, default="goturn.prototxt", help="Path to GOTURN architecture")
        parser.add_argument("--goturn_model", type=str, default="goturn.caffemodel", help="Path to GOTERN model")
        parser.add_argument("--dasiamrpn_net", type=str, default="dasiamrpn_model.onnx", help="Path to onnx model of DaSiamRPN net")
        parser.add_argument("--dasiamrpn_kernel_r1", type=str, default="dasiamrpn_kernel_r1.onnx", help="Path to onnx model of DaSiamRPN kernel_r1")
        parser.add_argument("--dasiamrpn_kernel_cls1", type=str, default="dasiamrpn_kernel_cls1.onnx", help="Path to onnx model of DaSiamRPN kernel_cls1")
        parser.add_argument("--nanotrack_backbone", type=str, default="nanotrack_backbone_sim.onnx", help="Path to onnx model of NanoTrack backBone")
        parser.add_argument("--nanotrack_headneck", type=str, default="nanotrack_head_sim.onnx", help="Path to onnx model of NanoTrack headNeck")
        parser.add_argument("--vittrack_net", type=str, default="vitTracker.onnx", help="Path to onnx model of  vittrack")
        parser.add_argument('--tracking_score_threshold', type=float,  help="Tracking score threshold. If a bbox of score >= 0.3, it is considered as found ")# I DONT KNPOW IF IT REALLY CHANGES, ORIGINAL WAS 0.3
        parser.add_argument('--backend', choices=backends, default=cv.dnn.DNN_BACKEND_DEFAULT, type=int, # HABRIA K MIRAR K PSTOAS ES ESTO
                        help="Choose one of computation backends: "
                                "%d: automatically (by default), "
                                "%d: Halide language (http://halide-lang.org/), "
                                "%d: Intel's Deep Learning Inference Engine (https://software.intel.com/openvino-toolkit), "
                                "%d: OpenCV implementation, "
                                "%d: VKCOM, "
                                "%d: CUDA"% backends) 
        parser.add_argument("--target", choices=targets, default=cv.dnn.DNN_TARGET_CPU, type=int,
                        help="Choose one of target computation devices: "
                                '%d: CPU target (by default), '
                                '%d: OpenCL, '
                                '%d: OpenCL fp16 (half-float precision), '
                                '%d: VPU, '
                                '%d: VULKAN, '
                                '%d: CUDA, '
                                '%d: CUDA fp16 (half-float preprocess)'% targets)