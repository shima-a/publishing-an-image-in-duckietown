#!/usr/bin/env python3

import os
from platform import node
import rospy
from duckietown.dtros import DTROS, NodeType
from std_msgs.msg import String
import cv2  
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge, CvBridgeError
from duckietown_msgs.msg import Twist2DStamped
import numpy as np

bridge = CvBridge()

class MainNode(DTROS):

    def __init__(self, node_name):
        super(MainNode, self).__init__(node_name=node_name, node_type=NodeType.GENERIC)
        
        self.image_pub = rospy.Publisher("image_topic_pub",CompressedImage)

        image_topic = '/db00/camera_node/image/compressed'
        self.sub = rospy.Subscriber(image_topic, CompressedImage, self.camera_callback , queue_size=1 , buff_size=2**24)
  
    def camera_callback(self , data):
        print ('got an image')
        global bridge

        try:
            cv_image = bridge.compressed_imgmsg_to_cv2(data)
        except CvBridgeError as e:
            print(e)

        try:
            ros_image = bridge.cv2_to_imgmsg(cv_image)
            self.image_pub.publish(ros_image)
        except CvBridgeError as e:
            print(e)

if __name__ == '__main__':  

    node = MainNode(node_name='my_node')
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print ("Shutting Down")
