import heapq
import math

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, DurabilityPolicy, ReliabilityPolicy

from nav_msgs.msg import OccupancyGrid, Path
from geometry_msgs.msg import PoseWithCovarianceStamped, PoseStamped


class AStarPlanner(Node):

    def __init__(self):
        super().__init__('astar_planner')

        self.map_data = None
        self.robot_pose = None
        self.goal_pose = None

        # The Clearpath map and AMCL pose use transient-local QoS.
        map_qos = QoSProfile(depth=1)
        map_qos.durability = DurabilityPolicy.TRANSIENT_LOCAL
        map_qos.reliability = ReliabilityPolicy.RELIABLE

        self.map_subscriber = self.create_subscription(
            OccupancyGrid,
            '/a200_0000/map',
            self.map_callback,
            map_qos
        )

        self.pose_subscriber = self.create_subscription(
            PoseWithCovarianceStamped,
            '/a200_0000/amcl_pose',
            self.pose_callback,
            map_qos
        )

        self.goal_subscriber = self.create_subscription(
            PoseStamped,
            '/goal_pose',
            self.goal_callback,
            10
        )

        self.path_publisher = self.create_publisher(
            Path,
            '/a200_0000/custom_path',
            10
        )

        self.get_logger().info('A* planner node started')


    def map_callback(self, msg):
        self.map_data = msg

        self.get_logger().info(
            f'Map received: {msg.info.width} x {msg.info.height}, '
            f'resolution = {msg.info.resolution:.3f} m/cell'
        )


    def pose_callback(self, msg):
        self.robot_pose = msg.pose.pose


    def goal_callback(self, msg):
        self.goal_pose = msg.pose

        goal_x = self.goal_pose.position.x
        goal_y = self.goal_pose.position.y

        self.get_logger().info(
            f'Goal received: x={goal_x:.2f}, y={goal_y:.2f}'
        )

        if self.map_data is None:
            self.get_logger().warn('Cannot plan: no map received yet')
            return

        if self.robot_pose is None:
            self.get_logger().warn('Cannot plan: no robot pose received yet')
            return

        start = self.world_to_grid(
            self.robot_pose.position.x,
            self.robot_pose.position.y
        )

        goal = self.world_to_grid(
            goal_x,
            goal_y
        )

        self.get_logger().info(f'Start grid: {start}')
        self.get_logger().info(f'Goal grid: {goal}')
        self.get_logger().info('Running A*...')

        path_cells = self.astar(start, goal)

        if path_cells is None:
            self.get_logger().error('A* could not find a path')
            return

        self.get_logger().info(
            f'A* found a path with {len(path_cells)} cells'
        )

        self.publish_path(path_cells)


    def world_to_grid(self, x, y):
        resolution = self.map_data.info.resolution

        origin_x = self.map_data.info.origin.position.x
        origin_y = self.map_data.info.origin.position.y

        grid_x = math.floor((x - origin_x) / resolution)
        grid_y = math.floor((y - origin_y) / resolution)

        return (grid_x, grid_y)


    def grid_to_world(self, grid_x, grid_y):
        resolution = self.map_data.info.resolution

        origin_x = self.map_data.info.origin.position.x
        origin_y = self.map_data.info.origin.position.y

        world_x = origin_x + (grid_x + 0.5) * resolution
        world_y = origin_y + (grid_y + 0.5) * resolution

        return world_x, world_y


    def is_free(self, cell):
        x, y = cell

        width = self.map_data.info.width
        height = self.map_data.info.height

        if x < 0 or x >= width or y < 0 or y >= height:
            return False

        index = y * width + x
        value = self.map_data.data[index]

        # -1 = unknown
        # 0 = free
        # 100 = occupied
        return 0 <= value < 50


    def get_neighbors(self, current):
        x, y = current

        movements = [
            (1, 0, 1.0),
            (-1, 0, 1.0),
            (0, 1, 1.0),
            (0, -1, 1.0),

            (1, 1, math.sqrt(2)),
            (1, -1, math.sqrt(2)),
            (-1, 1, math.sqrt(2)),
            (-1, -1, math.sqrt(2))
        ]

        neighbors = []

        for dx, dy, cost in movements:
            neighbor = (x + dx, y + dy)

            if not self.is_free(neighbor):
                continue

            # Prevent diagonal movement through obstacle corners.
            if dx != 0 and dy != 0:
                if not self.is_free((x + dx, y)):
                    continue

                if not self.is_free((x, y + dy)):
                    continue

            neighbors.append((neighbor, cost))

        return neighbors


    def heuristic(self, cell, goal):
        dx = goal[0] - cell[0]
        dy = goal[1] - cell[1]

        return math.sqrt(dx * dx + dy * dy)


    def astar(self, start, goal):

        if not self.is_free(start):
            self.get_logger().error('Start cell is occupied or unknown')
            return None

        if not self.is_free(goal):
            self.get_logger().error('Goal cell is occupied or unknown')
            return None

        open_heap = []

        counter = 0

        heapq.heappush(
            open_heap,
            (self.heuristic(start, goal), counter, start)
        )

        came_from = {}

        g_cost = {
            start: 0.0
        }

        closed = set()

        while open_heap:

            _, _, current = heapq.heappop(open_heap)

            if current in closed:
                continue

            if current == goal:
                return self.reconstruct_path(
                    came_from,
                    current
                )

            closed.add(current)

            for neighbor, movement_cost in self.get_neighbors(current):

                if neighbor in closed:
                    continue

                tentative_g = (
                    g_cost[current] + movement_cost
                )

                if (
                    neighbor not in g_cost
                    or tentative_g < g_cost[neighbor]
                ):

                    came_from[neighbor] = current
                    g_cost[neighbor] = tentative_g

                    f_cost = (
                        tentative_g
                        + self.heuristic(neighbor, goal)
                    )

                    counter += 1

                    heapq.heappush(
                        open_heap,
                        (f_cost, counter, neighbor)
                    )

        return None


    def reconstruct_path(self, came_from, current):
        path = [current]

        while current in came_from:
            current = came_from[current]
            path.append(current)

        path.reverse()

        return path


    def publish_path(self, path_cells):

        path_msg = Path()

        path_msg.header.frame_id = 'map'
        path_msg.header.stamp = (
            self.get_clock().now().to_msg()
        )

        for grid_x, grid_y in path_cells:

            world_x, world_y = self.grid_to_world(
                grid_x,
                grid_y
            )

            pose = PoseStamped()

            pose.header.frame_id = 'map'
            pose.header.stamp = path_msg.header.stamp

            pose.pose.position.x = world_x
            pose.pose.position.y = world_y
            pose.pose.position.z = 0.0

            pose.pose.orientation.w = 1.0

            path_msg.poses.append(pose)

        self.path_publisher.publish(path_msg)

        self.get_logger().info(
            'Custom A* path published'
        )


def main(args=None):
    rclpy.init(args=args)

    node = AStarPlanner()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
