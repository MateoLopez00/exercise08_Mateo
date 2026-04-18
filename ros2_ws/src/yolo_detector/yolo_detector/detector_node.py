import time
from collections import deque
import cv2
import numpy as np
import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import Float32, Header
from perception_msgs.msg import Detection, DetectionArray
from ultralytics import YOLO
class YoloDetector(Node):
    def __init__(self):
        super().__init__("yolo_detector")
        self.declare_parameter("model", "yolov8n.pt")
        self.declare_parameter("conf", 0.25)
        self.declare_parameter("image_topic", "/camera/color/image")
        model_name = self.get_parameter("model").get_parameter_value().string_value
        self.conf = self.get_parameter("conf").get_parameter_value().double_value
        image_topic = self.get_parameter("image_topic").get_parameter_value().string_value
        self.get_logger().info(f"Loading YOLO model: {model_name}")
        self.model = YOLO(model_name)
        self.bridge = CvBridge()
        self.latencies = deque(maxlen=30)
        self.frame_times = deque(maxlen=30)
        self.sub = self.create_subscription(Image, image_topic, self.cb, 10)
        self.pub_det = self.create_publisher(DetectionArray, "/perception/detections", 10)
        self.pub_img = self.create_publisher(Image, "/perception/image_annotated", 10)
        self.pub_lat = self.create_publisher(Float32, "/perception/latency_ms", 10)
        self.pub_fps = self.create_publisher(Float32, "/perception/fps", 10)
    def cb(self, msg: Image):
        try:
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
        except Exception as exc:
            self.get_logger().warn(f"cv_bridge failed: {exc}")
            return
        t0 = time.perf_counter()
        results = self.model.predict(frame, conf=self.conf, verbose=False)
        dt_ms = (time.perf_counter() - t0) * 1000.0
        self.latencies.append(dt_ms)
        self.frame_times.append(time.perf_counter())
        det_array = DetectionArray()
        det_array.header = Header(stamp=msg.header.stamp, frame_id=msg.header.frame_id or "camera")
        annotated = frame.copy()
        for r in results:
            names = r.names
            for b in r.boxes:
                xyxy = b.xyxy[0].cpu().numpy().astype(int)
                cls_id = int(b.cls[0].item())
                conf = float(b.conf[0].item())
                x1, y1, x2, y2 = xyxy
                d = Detection()
                d.class_name = names[cls_id]
                d.confidence = conf
                d.x = int(x1)
                d.y = int(y1)
                d.width = int(x2 - x1)
                d.height = int(y2 - y1)
                det_array.detections.append(d)
                cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(
                    annotated,
                    f"{d.class_name} {conf:.2f}",
                    (x1, max(0, y1 - 5)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    1,
                )
        self.pub_det.publish(det_array)
        out_msg = self.bridge.cv2_to_imgmsg(annotated, encoding="bgr8")
        out_msg.header = det_array.header
        self.pub_img.publish(out_msg)
        self.pub_lat.publish(Float32(data=float(np.mean(self.latencies))))
        if len(self.frame_times) >= 2:
            span = self.frame_times[-1] - self.frame_times[0]
            fps = (len(self.frame_times) - 1) / span if span > 0 else 0.0
            self.pub_fps.publish(Float32(data=float(fps)))
def main(args=None):
    rclpy.init(args=args)
    node = YoloDetector()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()
if __name__ == "__main__":
    main()
