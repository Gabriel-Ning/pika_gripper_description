# pika_gripper_description

ROS 2 description for the AgileX Pika gripper with FinRay fingers.
Validated kinematics: base + left/right prismatic fingers (1 DOF via mimic).

## Layout

```text
pika_gripper_description/
  config/
    cameras.yaml          # fisheye + D405 TF placeholders
    gripper_tcp.yaml      # TCP pose placeholder
    joint_limits.yaml     # gripper_left_joint [0, 0.05]
  docs/MESH_SOURCES.md
  launch/visualize_pika_gripper.launch.py
  meshes/
    gripper_base_link.STL
    pika_finray_link.STL
  rviz/visualize_pika_gripper.rviz
  urdf/
    pika_gripper.xacro                 # mountable macro (+ prefix)
    pika_gripper.ros2_control.xacro
    pika_gripper_standalone.urdf.xacro # world-fixed bench entry
```

## Visualize

```bash
ros2 launch pika_gripper_description visualize_pika_gripper.launch.py
```

Drag `gripper_left_joint`; `gripper_right_joint` follows (mimic ×1).

## Mount on a host

```xml
<xacro:include filename="$(find pika_gripper_description)/urdf/pika_gripper.xacro"/>
<xacro:pika_gripper prefix="left_" parent="flange_L">
  <origin xyz="0 0 0" rpy="0 0 0"/>
</xacro:pika_gripper>
```

Actuated joint: `${prefix}gripper_left_joint`.
