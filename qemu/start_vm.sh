#!/usr/bin/env bash
# LICENSE UPL
# Author: Mauro Risonho de Paula Assumpção
# Description: Automatically boots the downloaded FreeBSD 14.1 AArch64 image
#
# Automatically boots the downloaded FreeBSD 14.4 AArch64 image

cd "$(dirname "$0")"

IMG="FreeBSD-14.4-RELEASE-arm64-aarch64-ufs.qcow2"
BIOS="/usr/share/qemu-efi-aarch64/QEMU_EFI.fd"

if [ ! -f "$IMG" ]; then
    echo "Error: Disk image $IMG not found."
    echo "Please run download_image.sh first."
    exit 1
fi

if [ ! -f "$BIOS" ]; then
    echo "Error: UEFI firmware $BIOS not found."
    echo "Please install qemu-efi-aarch64 package: sudo apt install qemu-efi-aarch64"
    exit 1
fi

echo "Starting FreeBSD AArch64 VM..."
echo "Host port 2222 forwards to VM port 22 (SSH)."
echo "Telemetry is sent from the VM to host at 10.0.2.2:8080 via QEMU user networking."
echo "Press Ctrl+A then X to exit QEMU."

qemu-system-aarch64 \
    -m 2048 \
    -cpu cortex-a57 \
    -M virt \
    -nographic \
    -bios "$BIOS" \
    -drive if=none,file="$IMG",id=hd0 \
    -device virtio-blk-device,drive=hd0 \
    -netdev user,id=net0,hostfwd=tcp::2222-:22 \
    -device virtio-net-device,netdev=net0
