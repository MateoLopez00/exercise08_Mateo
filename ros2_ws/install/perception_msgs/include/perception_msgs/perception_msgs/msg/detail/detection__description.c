// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from perception_msgs:msg/Detection.idl
// generated code does not contain a copyright notice

#include "perception_msgs/msg/detail/detection__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_perception_msgs
const rosidl_type_hash_t *
perception_msgs__msg__Detection__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x1c, 0xb0, 0x97, 0x79, 0xd9, 0xc7, 0xb4, 0xed,
      0x6a, 0x69, 0x91, 0x65, 0x3b, 0xc5, 0x96, 0x63,
      0x26, 0xc5, 0xc9, 0x1d, 0x54, 0xbd, 0x36, 0xb5,
      0x79, 0x66, 0x95, 0xc9, 0x4d, 0xc8, 0xdf, 0xe2,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types

// Hashes for external referenced types
#ifndef NDEBUG
#endif

static char perception_msgs__msg__Detection__TYPE_NAME[] = "perception_msgs/msg/Detection";

// Define type names, field names, and default values
static char perception_msgs__msg__Detection__FIELD_NAME__class_name[] = "class_name";
static char perception_msgs__msg__Detection__FIELD_NAME__confidence[] = "confidence";
static char perception_msgs__msg__Detection__FIELD_NAME__x[] = "x";
static char perception_msgs__msg__Detection__FIELD_NAME__y[] = "y";
static char perception_msgs__msg__Detection__FIELD_NAME__width[] = "width";
static char perception_msgs__msg__Detection__FIELD_NAME__height[] = "height";

static rosidl_runtime_c__type_description__Field perception_msgs__msg__Detection__FIELDS[] = {
  {
    {perception_msgs__msg__Detection__FIELD_NAME__class_name, 10, 10},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {perception_msgs__msg__Detection__FIELD_NAME__confidence, 10, 10},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {perception_msgs__msg__Detection__FIELD_NAME__x, 1, 1},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_INT32,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {perception_msgs__msg__Detection__FIELD_NAME__y, 1, 1},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_INT32,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {perception_msgs__msg__Detection__FIELD_NAME__width, 5, 5},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_INT32,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {perception_msgs__msg__Detection__FIELD_NAME__height, 6, 6},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_INT32,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
perception_msgs__msg__Detection__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {perception_msgs__msg__Detection__TYPE_NAME, 29, 29},
      {perception_msgs__msg__Detection__FIELDS, 6, 6},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "string class_name\n"
  "float32 confidence\n"
  "int32 x\n"
  "int32 y\n"
  "int32 width\n"
  "int32 height";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
perception_msgs__msg__Detection__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {perception_msgs__msg__Detection__TYPE_NAME, 29, 29},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 78, 78},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
perception_msgs__msg__Detection__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *perception_msgs__msg__Detection__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}
