#!/bin/bash
i=1
for p in $(find /share/motioneye/Camera1 -type f -name "*.jpg" -exec stat -c "%y %n" {} + | sort -r | head -6 | awk '{ print $3}'); do
  from=$p
  to="/config/www/camera1/image_${i}.jpg"
  cp $from $to
  i=$((i+1))
done
