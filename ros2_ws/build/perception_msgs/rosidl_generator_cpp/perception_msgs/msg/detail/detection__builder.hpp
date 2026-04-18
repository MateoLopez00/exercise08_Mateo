// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from perception_msgs:msg/Detection.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "perception_msgs/msg/detection.hpp"


#ifndef PERCEPTION_MSGS__MSG__DETAIL__DETECTION__BUILDER_HPP_
#define PERCEPTION_MSGS__MSG__DETAIL__DETECTION__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "perception_msgs/msg/detail/detection__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace perception_msgs
{

namespace msg
{

namespace builder
{

class Init_Detection_height
{
public:
  explicit Init_Detection_height(::perception_msgs::msg::Detection & msg)
  : msg_(msg)
  {}
  ::perception_msgs::msg::Detection height(::perception_msgs::msg::Detection::_height_type arg)
  {
    msg_.height = std::move(arg);
    return std::move(msg_);
  }

private:
  ::perception_msgs::msg::Detection msg_;
};

class Init_Detection_width
{
public:
  explicit Init_Detection_width(::perception_msgs::msg::Detection & msg)
  : msg_(msg)
  {}
  Init_Detection_height width(::perception_msgs::msg::Detection::_width_type arg)
  {
    msg_.width = std::move(arg);
    return Init_Detection_height(msg_);
  }

private:
  ::perception_msgs::msg::Detection msg_;
};

class Init_Detection_y
{
public:
  explicit Init_Detection_y(::perception_msgs::msg::Detection & msg)
  : msg_(msg)
  {}
  Init_Detection_width y(::perception_msgs::msg::Detection::_y_type arg)
  {
    msg_.y = std::move(arg);
    return Init_Detection_width(msg_);
  }

private:
  ::perception_msgs::msg::Detection msg_;
};

class Init_Detection_x
{
public:
  explicit Init_Detection_x(::perception_msgs::msg::Detection & msg)
  : msg_(msg)
  {}
  Init_Detection_y x(::perception_msgs::msg::Detection::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_Detection_y(msg_);
  }

private:
  ::perception_msgs::msg::Detection msg_;
};

class Init_Detection_confidence
{
public:
  explicit Init_Detection_confidence(::perception_msgs::msg::Detection & msg)
  : msg_(msg)
  {}
  Init_Detection_x confidence(::perception_msgs::msg::Detection::_confidence_type arg)
  {
    msg_.confidence = std::move(arg);
    return Init_Detection_x(msg_);
  }

private:
  ::perception_msgs::msg::Detection msg_;
};

class Init_Detection_class_name
{
public:
  Init_Detection_class_name()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Detection_confidence class_name(::perception_msgs::msg::Detection::_class_name_type arg)
  {
    msg_.class_name = std::move(arg);
    return Init_Detection_confidence(msg_);
  }

private:
  ::perception_msgs::msg::Detection msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::perception_msgs::msg::Detection>()
{
  return perception_msgs::msg::builder::Init_Detection_class_name();
}

}  // namespace perception_msgs

#endif  // PERCEPTION_MSGS__MSG__DETAIL__DETECTION__BUILDER_HPP_
