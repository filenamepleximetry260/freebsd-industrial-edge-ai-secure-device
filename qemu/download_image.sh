#!/usr/bin/env bash
# LICENSE UPL
# Author: Mauro Risonho de Paula Assumpção
# Description: Downloads FreeBSD AArch64 VM image for the Edge AI platform
#
# Downloads FreeBSD AArch64 VM image for the Edge AI platform

set -e

# Change to the script's directory
cd "$(dirname "$0")"

# FreeBSD 14.4-RELEASE aarch64
URL="https://download.freebsd.org/releases/VM-IMAGES/14.4-RELEASE/aarch64/Latest/FreeBSD-14.4-RELEASE-arm64-aarch64-ufs.qcow2.xz"
IMG_XZ="FreeBSD-14.4-RELEASE-arm64-aarch64-ufs.qcow2.xz"
IMG_QCOW2="FreeBSD-14.4-RELEASE-arm64-aarch64-ufs.qcow2"

if [ ! -f "$IMG_QCOW2" ]; then
    echo "Downloading $IMG_XZ..."
    wget -nc "$URL" || true
    if [ -f "$IMG_XZ" ]; then
        echo "Extracting image..."
        unxz -k "$IMG_XZ"
    fi
else
    echo "Image $IMG_QCOW2 already exists."
fi

# Ensure QEMU AArch64 and EFI firmware are installed
echo "Please ensure 'qemu-system-aarch64' and 'qemu-efi-aarch64' are installed on your host system."
echo "For Ubuntu/Debian: sudo apt-get install qemu-system-arm qemu-efi-aarch64"
