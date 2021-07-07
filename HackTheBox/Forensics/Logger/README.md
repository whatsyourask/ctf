# Logger

Completed: Yes
Platform: HackTheBox

This challenge was not easy at all. I tried to research manually the entire USB protocol, but then I thought that this is too much for an easy challenge. So, when I was researching, I discovered these actions (I  don't understand the entire USB protocol, so it is my guesses).

1. Firstly, the host requests the device descriptor, its configuration.

    ```bash
    4	0.000000	1.16.0	host	USB	87	GET DESCRIPTOR Response CONFIGURATION
    1	0.000000	host	1.16.0	USB	36	GET DESCRIPTOR Request DEVICE
    2	0.000000	1.16.0	host	USB	46	GET DESCRIPTOR Response DEVICE
    3	0.000000	host	1.16.0	USB	36	GET DESCRIPTOR Request CONFIGURATION
    5	0.000000	host	1.16.0	USB	36	SET CONFIGURATION Request
    6	0.000000	1.16.0	host	USB	28	SET CONFIGURATION Response
    ```

2. After the first stage, it is ready to talk. And the data will be sent in URB_INTERRUPT packets(?). It is an HID field. But what device we should look at? With this, the first step will help. In `DESCRIPTOR Response DEVICE`:

    ```bash
    Frame 2: 46 bytes on wire (368 bits), 46 bytes captured (368 bits) on interface wireshark_extcap2640, id 0
    USB URB
        [Source: 1.16.0]
        [Destination: host]
        USBPcap pseudoheader length: 28
        IRP ID: 0x0000000000000000
        IRP USBD_STATUS: USBD_STATUS_SUCCESS (0x00000000)
        URB Function: URB_FUNCTION_CONTROL_TRANSFER (0x0008)
        IRP information: 0x01, Direction: PDO -> FDO
        URB bus id: 1
        Device address: 16
        Endpoint: 0x80, Direction: IN
        URB transfer type: URB_CONTROL (0x02)
        Packet Data Length: 18
        [Request in: 1]
        [Time from request: 0.000000000 seconds]
        Control transfer stage: Complete (3)
    DEVICE DESCRIPTOR
        bLength: 18
        bDescriptorType: 0x01 (DEVICE)
        bcdUSB: 0x0110
        bDeviceClass: Device (0x00)
        bDeviceSubClass: 0
        bDeviceProtocol: 0 (Use class code info from Interface Descriptors)
        bMaxPacketSize0: 8
        idVendor: Holtek Semiconductor, Inc. (0x04d9)
        idProduct: Keyboard LKS02 (0x1702)
        bcdDevice: 0x0406
        iManufacturer: 1
        iProduct: 2
        iSerialNumber: 0
        bNumConfigurations: 1
    ```

    You see the idProduct, which indicated the keyboard. So, source 1.16.1 is a keyboard, and the traffic with this source is definitely the flag. HackTricks helps as always: [https://book.hacktricks.xyz/forensics/basic-forensic-methodology/pcap-inspection/usb-keyboard-pcap-analysis](https://book.hacktricks.xyz/forensics/basic-forensic-methodology/pcap-inspection/usb-keyboard-pcap-analysis). I used this filter: `usb.src == "1.16.1" && usb.transfer_type == 0x1`. So, in the HackTricks article, you can see the solutions to similar challenges, which I used too. I didn't want to spoiler HTB machine, so, I used the first one - [https://abawazeeer.medium.com/kaizen-ctf-2018-reverse-engineer-usb-keystrok-from-pcap-file-2412351679f4](https://abawazeeer.medium.com/kaizen-ctf-2018-reverse-engineer-usb-keystrok-from-pcap-file-2412351679f4). The script from there. With the applied filter export all packets in txt or CSV or whatever.

    Then, in bash grep from there HID Data: `cat wireshark_exported.txt | grep "HID Data:" | cut -d' ' -f3 > hexoutput.txt`.

    Use a little bit of modified script: 

    ```bash
    python3 usbhid_decode.py   
    CapsLockhtb33[3CapsLocki33-3CapsLockc4n33-353333-3CapsLockyCapsLockouCapsLockr33-3CapsLockk3y2CapsLock33]3
    ```

    Now, remains a simple work. 33-3 is something confused here. I replaced them with `_`. So, the final output is:

    ```bash
    CapsLockhtb33[3CapsLocki_CapsLockc4n_533_CapsLockyCapsLockouCapsLockr_CapsLockk3y2CapsLock33]3
    ```

    Which is `HTB{i_C4N_533_yOUr_K3Y2}`