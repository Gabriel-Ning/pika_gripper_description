# Mesh asset sources

| Path | Role |
| --- | --- |
| `meshes/gripper_base_link.STL` | Pika gripper body (AgileX / remapped axes, meter-valued) |
| `meshes/pika_finray_link.STL` | FinRay finger (meter-valued; right mount uses yaw=-π) |

Base geometry originates from
[agilexrobotics/pika_ros](https://github.com/agilexrobotics/pika_ros)
`pika_gripper_description` (BSD), with frame remapped for this package.
FinRay finger mesh is package-local.

Validated model: `urdf/pika_gripper.xacro` (bench: `pika_gripper_standalone.urdf.xacro`).
ROS packaging for this repository remains Apache-2.0.
