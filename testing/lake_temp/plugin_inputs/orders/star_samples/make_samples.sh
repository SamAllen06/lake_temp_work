#!/bin/bash

cat > $1_min_to_max.json << EOF
{
  "samples":11,
  "ranges":{
    "$1": ["r(0)", "r(1)"]
  }
}
EOF
