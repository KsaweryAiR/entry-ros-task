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
class TFPublisher(Node):

    def __init__(self):
        super().__init__('tf_publisher')
        self.get_logger().info('TFPublisher started.')



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
