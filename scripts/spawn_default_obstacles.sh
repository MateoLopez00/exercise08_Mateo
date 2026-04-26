#!/usr/bin/env bash
set -euo pipefail

WORLD="${1:-default}"
MODEL_DIR="/root/worlds/spawn_models"

spawn_model() {
  local file="$1"
  local name="$2"
  local x="$3"
  local y="$4"
  local z="$5"
  local yaw="${6:-0.0}"

  echo "Spawning ${name} in world ${WORLD}..."
  gz service -s "/world/${WORLD}/create" \
    --reqtype gz.msgs.EntityFactory \
    --reptype gz.msgs.Boolean \
    --timeout 3000 \
    --req "sdf_filename: '${MODEL_DIR}/${file}', name: '${name}', pose: { position: { x: ${x}, y: ${y}, z: ${z} }, orientation: { z: ${yaw} } }"
}

spawn_model building_box.sdf building_box_1 4.5 0.0 1.5 0.0
spawn_model tree_cylinder.sdf tree_left_1 5.4 2.1 1.4 0.0
spawn_model tree_cylinder.sdf tree_right_1 7.2 1.0 1.4 0.0
spawn_model vehicle_box.sdf vehicle_box_1 6.6 -1.5 0.45 0.2
spawn_model human_cylinder.sdf human_cylinder_1 3.0 1.4 0.85 0.0

echo "Done. Check Gazebo for building, trees, vehicle, and human-sized cylinder."
