#!/usr/bin/env python3
"""
TF Publisher Node
-----------------
Publishes the TF2 transform chain for a 2-DOF robot arm.

Chain layout:
    world
      └── base_link       (static, identity)
            └── link1     (dynamic, rotates around Z over time)
                  └── link2  (static offset: x=0.3m from link1)
                        └── end_effector  (static offset: x=0.2m from link2)

Your task (TODO 1):
    Implement the _broadcast() method so that:
    - 'world' → 'base_link'       is a static identity transform
    - 'base_link' → 'link1'       rotates around Z with amplitude 45° (0.785 rad)
                                  at a frequency of 0.5 Hz
    - 'link1' → 'link2'           is a static transform with x=0.3m offset
    - 'link2' → 'end_effector'    is a static transform with x=0.2m offset

    Use StaticTransformBroadcaster for transforms that never change.
    Use TransformBroadcaster for transforms that change over time.
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster, StaticTransformBroadcaster
import math

class TFPublisher(Node):

    def __init__(self):
        super().__init__('tf_publisher')
        self.get_logger().info('TFPublisher started.')

    
        self.tf_broadcaster = TransformBroadcaster(self)
        self.static_tf_broadcaster = StaticTransformBroadcaster(self)

        self.amplitude = 0.785 
        self.frequency = 0.5

        self.publish_static_transforms()
        self.timer = self.create_timer(1.0 / 30.0, self.dynamic_broadcast)

    def publish_static_transforms(self):
        now = self.get_clock().now().to_msg()

        #1
        t1 = TransformStamped()
        t1.header.stamp = now
        t1.header.frame_id = 'world'
        t1.child_frame_id = 'base_link'
        t1.transform.rotation.w = 1.0 

        #2 
        t2 = TransformStamped()
        t2.header.stamp = now
        t2.header.frame_id = 'link1'
        t2.child_frame_id = 'link2'
        t2.transform.translation.x = 0.3
        t2.transform.rotation.w = 1.0

        #4
        t3 = TransformStamped()
        t3.header.stamp = now
        t3.header.frame_id = 'link2'
        t3.child_frame_id = 'end_effector'
        t3.transform.translation.x = 0.2
        t3.transform.rotation.w = 1.0

        #4 publish
        self.static_tf_broadcaster.sendTransform([t1, t2, t3])

    def dynamic_broadcast(self):
        now = self.get_clock().now()
        t = now.nanoseconds / 1e9

        angle = self.amplitude * math.sin(2 * math.pi * self.frequency * t)

        dynamic_t = TransformStamped()
        dynamic_t.header.stamp = now.to_msg()
        dynamic_t.header.frame_id = 'base_link'
        dynamic_t.child_frame_id = 'link1'
        dynamic_t.transform.translation.z = 0.05

        dynamic_t.transform.rotation.z = math.sin(angle / 2.0)
        dynamic_t.transform.rotation.w = math.cos(angle / 2.0)

        self.tf_broadcaster.sendTransform(dynamic_t)




def main(args=None):
    rclpy.init(args=args)
    node = TFPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
