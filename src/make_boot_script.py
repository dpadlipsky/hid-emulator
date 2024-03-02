from dataclasses import dataclass
from typing import List

from models import HIDDevice
import devices

def make_report_string(report: List[int]):
    report_str = ''
    for val in report:
        report_str += f"\\\\x{val:02x}"
    return report_str

def script_for_hid_device(hid_device: HIDDevice) -> str:
    report_byte_string = make_report_string(hid_device.report)
    return f"""#!/bin/bash
cd /sys/kernel/config/usb_gadget/
mkdir -p dev1
cd dev1
echo {hex(hid_device.vendor_id)} > idVendor
echo {hex(hid_device.product_id)} > idProduct
echo 0x0100 > bcdDevice
echo 0x200 > bcdUSB

mkdir -p strings/0x409
echo "fedcba9876543210" > strings/0x409/serialnumber
echo "{hid_device.manufacturer_name}" > strings/0x409/manufacturer
echo "{hid_device.product_name}" > strings/0x409/product

mkdir -p functions/hid.usb0
echo 1 > functions/hid.usb0/protocol
echo 1 > functions/hid.usb0/subclass
echo 8 > functions/hid.usb0/report_length
echo -ne {report_byte_string} > functions/hid.usb0/report_desc

C=1
mkdir -p configs/c.$C/strings/0x409
ln -s functions/hid.usb0 configs/c.$C/

ls /sys/class/udc > UDC
    """

print(script_for_hid_device(devices.mode.ENVOY))

