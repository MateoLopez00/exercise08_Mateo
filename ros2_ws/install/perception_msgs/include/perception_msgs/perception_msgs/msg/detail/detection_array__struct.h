// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from perception_msgs:msg/DetectionArray.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "perception_msgs/msg/detection_array.h"


#ifndef PERCEPTION_MSGS__MSG__DETAIL__DETECTION_ARRAY__STRUCT_H_
#define PERCEPTION_MSGS__MSG__DETAIL__DETECTION_ARRAY__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"
// Member 'detections'
#include "perception_msgs/msg/detail/detection__struct.h"

/// Struct defined in msg/DetectionArray in the package perception_msgs.
typedef struct perception_msgs__msg__DetectionArray
{
  std_msgs__msg__Header header;
  perception_msgs__msg__Detection__Sequence detections;
} perception_msgs__msg__DetectionArray;

// Struct for a sequence of perception_msgs__msg__DetectionArray.
typedef struct perception_msgs__msg__DetectionArray__Sequence
{
  perception_msgs__msg__DetectionArray * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} perception_msgs__msg__DetectionArray__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // PERCEPTION_MSGS__MSG__DETAIL__DETECTION_ARRAY__STRUCT_H_
