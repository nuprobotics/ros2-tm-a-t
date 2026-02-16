import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger


class TriggerNode(Node):

    def __init__(self):
        super().__init__('trigger_node')

        self.declare_parameter('service_name', '/trigger_service')
        self.declare_parameter('default_string', 'No service available')

        service_name = self.get_parameter('service_name').get_parameter_value().string_value
        self.default_string = self.get_parameter('default_string').get_parameter_value().string_value

        self.stored_message = self.default_string

        self.client = self.create_client(Trigger, '/spgc/trigger')
        self.service = self.create_service(Trigger, service_name, self.service_callback)
        self.call_trigger_service()

    def call_trigger_service(self):
        if not self.client.wait_for_service(timeout_sec=5.0):
            self.get_logger().warn('/spgc/trigger service not available, using default string')
            return

        request = Trigger.Request()
        future = self.client.call_async(request)
        future.add_done_callback(self.trigger_response_callback)

    def trigger_response_callback(self, future):
        try:
            response = future.result()
            if response.success:
                self.stored_message = response.message
                self.get_logger().info('Received from /spgc/trigger: "%s"' % self.stored_message)
            else:
                self.get_logger().warn('/spgc/trigger returned failure, using default string')
        except Exception as e:
            self.get_logger().error('Service call failed: %s' % str(e))

    def service_callback(self, request, response):
        response.success = True
        response.message = self.stored_message
        self.get_logger().info('Responding with: "%s"' % self.stored_message)
        return response


def main(args=None):
    rclpy.init(args=args)
    node = TriggerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
