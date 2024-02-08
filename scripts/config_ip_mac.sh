#!/bin/sh
# Configure marble_mmc IP and mac addresses based on serial number
# config_ip_mac.sh [-d /dev/ttyUSB3] serial_number
# Set environment variable TTY_MMC to point to whatever /dev/ttyUSBx
# the marble_mmc enumerated as.  Defaults to /dev/ttyUSB3

devnext=0
dev=
snum=
for arg in "$@"; do
  if [ $devnext != 0 ]; then
    dev=$arg
    devnext=0
  elif [ "$arg" = "-d" ]; then
    devnext=1
  else
    snum=$arg
  fi
done

SCRIPT_DIR=$( dirname -- "$0"; )

if [ -z "$snum" ]; then
  if [ -n "$IP" ]; then
    # TODO - This only extracts 2-digit numbers!!! Need to use sed to extract everything after last '.'
    snum=$(printf "%-.2s" "$IP")
    echo "Using serial number from IP: $snum"
  else
    echo "Usage: config_ip_mac.sh [-d /dev/ttyUSB3] serial_number"
    exit 1
  fi
fi

if [ -z "$dev" ]; then
  if [ -n "$TTY_MMC" ]; then
    dev=$TTY_MMC
  else
    dev=/dev/ttyUSB3
  fi
fi

mac=$(printf "12:55:55:0:1f:%x" "$snum")
ip=$(printf "192.168.79.%s" "$snum")

echo "ip = $ip; mac = $mac; dev = $dev"

python3 $SCRIPT_DIR/load.py -d "$dev" "m $ip" "n $mac"

exit 0
