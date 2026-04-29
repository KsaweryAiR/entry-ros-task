#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
import math

class PoseVerifier(Node):
    def __init__(self):
        super().__init__('pose_verifier')
        self.subscription = self.create_subscription(
            PoseStamped, '/end_effector_pose', self.listener_callback, 10)
        
        self.prev_pose = None
        self.moves_detected = 0
        self.total_samples = 0
        self.get_logger().info('Verify_run')

    def listener_callback(self, msg):
        self.total_samples += 1
        current_pos = msg.pose.position

        if self.prev_pose is not None:
            dist = math.sqrt(
                (current_pos.x - self.prev_pose.x)**2 +
                (current_pos.y - self.prev_pose.y)**2
            )
            if dist > 0.001:
                self.moves_detected += 1

        self.prev_pose = current_pos
        if self.total_samples % 10 == 0:
            ratio = (self.moves_detected / self.total_samples) * 100
            if ratio > 80:
                self.get_logger().info(f'STATUS: OK - smooth animation({ratio:.1f}%)')
            else:
                self.get_logger().error(f'STATUS: ERROR - too slow ({ratio:.1f}%)')

def main(args=None):
    rclpy.init(args=args)
    node = PoseVerifier()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()