#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu

class ImuCovarianceHelper(Node):
    def __init__(self):
        super().__init__('imu_covariance_helper')
        self.subscription = self.create_subscription(
            Imu,
            'imu',
            self.listener_callback,
            10)
        self.publisher = self.create_publisher(Imu, 'imu/corrected', 10)

    def listener_callback(self, msg):
        corrected_msg = Imu()
        corrected_msg.header = msg.header
        corrected_msg.orientation = msg.orientation
        corrected_msg.angular_velocity = msg.angular_velocity
        corrected_msg.linear_acceleration = msg.linear_acceleration
        
        # Populate diagonal of covariance matrices with small non-zero values (e.g. 1e-4)
        # to prevent EKF from treating them as absolute certainty (0.0).
        corrected_msg.orientation_covariance = [
            1e-4, 0.0, 0.0,
            0.0, 1e-4, 0.0,
            0.0, 0.0, 1e-4
        ]
        corrected_msg.angular_velocity_covariance = [
            1e-4, 0.0, 0.0,
            0.0, 1e-4, 0.0,
            0.0, 0.0, 1e-4
        ]
        corrected_msg.linear_acceleration_covariance = [
            1e-4, 0.0, 0.0,
            0.0, 1e-4, 0.0,
            0.0, 0.0, 1e-4
        ]
        
        self.publisher.publish(corrected_msg)

def main(args=None):
    rclpy.init(args=args)
    node = ImuCovarianceHelper()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
