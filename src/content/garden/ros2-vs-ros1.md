---
title: "ROS2 vs ROS1 Nodes"
description: "Key differences in node architecture and messaging."
date: "2023-08-20"
tags: ["ROS", "CPP"]
status: "Seedling"
---

# ROS2 vs ROS1: Node Architecture

Quick comparison of key differences between ROS1 and ROS2.

## Node Initialization

**ROS1:**
```cpp
ros::init(argc, argv, "node_name");
ros::NodeHandle nh;
```

**ROS2:**
```cpp
rclcpp::init(argc, argv);
auto node = rclcpp::Node::make_shared("node_name");
```

## Key Differences

- ROS2 uses DDS for communication
- No roscore required in ROS2
- Better real-time support in ROS2
- Improved security in ROS2

## Migration Tips

1. Start with simple nodes
2. Use ros1_bridge during transition
3. Update CMakeLists.txt and package.xml
