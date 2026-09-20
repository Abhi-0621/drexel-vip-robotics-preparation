import math

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, DurabilityPolicy, ReliabilityPolicy

from nav_msgs.msg import Path
from geometry_msgs.msg import PoseWithCovarianceStamped, Twist


class PurePursuitController(Node):

    def __init__(self):
        super().__init__('pure_pursuit_controller')

        self.path = None
        self.robot_pose = None

        self.lookahead_distance = 0.45
        self.linear_speed = 0.20
        self.goal_tolerance = 0.15

        pose_qos = QoSProfile(depth=1)
        pose_qos.durability = DurabilityPolicy.TRANSIENT_LOCAL
        pose_qos.reliability = ReliabilityPolicy.RELIABLE

        self.path_subscriber = self.create_subscription(
            Path,
            '/a200_0000/custom_path',
            self.path_callback,
            10
        )

        self.pose_subscriber = self.create_subscription(
            PoseWithCovarianceStamped,
            '/a200_0000/amcl_pose',
            self.pose_callback,
            pose_qos
        )

        self.cmd_publisher = self.create_publisher(
            Twist,
            '/a200_0000/cmd_vel',
            10
        )

        self.timer = self.create_timer(
            0.1,
            self.control_loop
        )

        self.get_logger().info(
            'Pure Pursuit controller started'
        )


    def path_callback(self, msg):
        self.path = msg

        self.get_logger().info(
            f'Path received with {len(msg.poses)} poses'
        )


    def pose_callback(self, msg):
        self.robot_pose = msg.pose.pose


    def quaternion_to_yaw(self, q):
        siny_cosp = 2.0 * (
            q.w * q.z +
            q.x * q.y
        )

        cosy_cosp = 1.0 - 2.0 * (
            q.y * q.y +
            q.z * q.z
        )

        return math.atan2(
            siny_cosp,
            cosy_cosp
        )


    def stop_robot(self):
        cmd = Twist()

        cmd.linear.x = 0.0
        cmd.angular.z = 0.0

        self.cmd_publisher.publish(cmd)


    def control_loop(self):

        if self.path is None:
            return

        if self.robot_pose is None:
            return

        if len(self.path.poses) == 0:
            return

        robot_x = self.robot_pose.position.x
        robot_y = self.robot_pose.position.y

        goal_pose = self.path.poses[-1].pose

        goal_distance = math.hypot(
            goal_pose.position.x - robot_x,
            goal_pose.position.y - robot_y
        )

        if goal_distance < self.goal_tolerance:
            self.stop_robot()

            self.get_logger().info(
                'Goal reached'
            )

            self.path = None
            return

        lookahead_pose = None

        for pose_stamped in self.path.poses:

            path_x = pose_stamped.pose.position.x
            path_y = pose_stamped.pose.position.y

            distance = math.hypot(
                path_x - robot_x,
                path_y - robot_y
            )

            if distance >= self.lookahead_distance:
                lookahead_pose = pose_stamped.pose
                break

        if lookahead_pose is None:
            lookahead_pose = self.path.poses[-1].pose

        yaw = self.quaternion_to_yaw(
            self.robot_pose.orientation
        )

        dx = lookahead_pose.position.x - robot_x
        dy = lookahead_pose.position.y - robot_y

        # Convert target point from map frame
        # into the robot's local coordinate frame.
        local_x = (
            math.cos(yaw) * dx
            + math.sin(yaw) * dy
        )

        local_y = (
            -math.sin(yaw) * dx
            + math.cos(yaw) * dy
        )

        lookahead_squared = (
            local_x * local_x
            + local_y * local_y
        )

        if lookahead_squared < 0.001:
            return

        curvature = (
            2.0 * local_y
            / lookahead_squared
        )

        cmd = Twist()

        cmd.linear.x = self.linear_speed

        cmd.angular.z = (
            self.linear_speed
            * curvature
        )

        # Limit turning speed.
        cmd.angular.z = max(
            -1.0,
            min(1.0, cmd.angular.z)
        )

        self.cmd_publisher.publish(cmd)


def main(args=None):
    rclpy.init(args=args)

    node = PurePursuitController()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.stop_robot()

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
