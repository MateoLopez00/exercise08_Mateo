// generated from rosidl_typesupport_fastrtps_c/resource/idl__rosidl_typesupport_fastrtps_c.h.em
// with input from perception_msgs:msg/DetectionArray.idl
// generated code does not contain a copyright notice
#ifndef PERCEPTION_MSGS__MSG__DETAIL__DETECTION_ARRAY__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_
#define PERCEPTION_MSGS__MSG__DETAIL__DETECTION_ARRAY__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_


#include <stddef.h>
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "perception_msgs/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "perception_msgs/msg/detail/detection_array__struct.h"
#include "fastcdr/Cdr.h"

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_perception_msgs
bool cdr_serialize_perception_msgs__msg__DetectionArray(
  const perception_msgs__msg__DetectionArray * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_perception_msgs
bool cdr_deserialize_perception_msgs__msg__DetectionArray(
  eprosima::fastcdr::Cdr &,
  perception_msgs__msg__DetectionArray * ros_message);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_perception_msgs
size_t get_serialized_size_perception_msgs__msg__DetectionArray(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_perception_msgs
size_t max_serialized_size_perception_msgs__msg__DetectionArray(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_perception_msgs
bool cdr_serialize_key_perception_msgs__msg__DetectionArray(
  const perception_msgs__msg__DetectionArray * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_perception_msgs
size_t get_serialized_size_key_perception_msgs__msg__DetectionArray(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_perception_msgs
size_t max_serialized_size_key_perception_msgs__msg__DetectionArray(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_perception_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, perception_msgs, msg, DetectionArray)();

#ifdef __cplusplus
}
#endif

#endif  // PERCEPTION_MSGS__MSG__DETAIL__DETECTION_ARRAY__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_
