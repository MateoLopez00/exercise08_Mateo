// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from perception_msgs:msg/Detection.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "perception_msgs/msg/detection.h"


#ifndef PERCEPTION_MSGS__MSG__DETAIL__DETECTION__STRUCT_H_
#define PERCEPTION_MSGS__MSG__DETAIL__DETECTION__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

// Include directives for member types
// Member 'class_name'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/Detection in the package perception_msgs.
typedef struct perception_msgs__msg__Detection
{
  rosidl_runtime_c__String class_name;
  float confidence;
  int32_t x;
  int32_t y;
  int32_t width;
  int32_t height;
} perception_msgs__msg__Detection;

// Struct for a sequence of perception_msgs__msg__Detection.
typedef struct perception_msgs__msg__Detection__Sequence
{
  perception_msgs__msg__Detection * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} perception_msgs__msg__Detection__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // PERCEPTION_MSGS__MSG__DETAIL__DETECTION__STRUCT_H_
