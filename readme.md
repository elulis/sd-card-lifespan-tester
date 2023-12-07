```shell
C:\data>python lifespan.py
Usage: python lifespan.py <folder>

C:\data>python lifespan.py D:
WRITE: 100%|██████████████████████████████| 7.93G/7.93G [09:44<00:00, 13.6MB/s]
READ : 100%|██████████████████████████████| 7.93G/7.93G [06:16<00:00, 21.0MB/s]
Successfully completed 1 write cycles.

WRITE: 100%|██████████████████████████████| 7.93G/7.93G [09:46<00:00, 13.5MB/s]
READ : 100%|██████████████████████████████| 7.93G/7.93G [06:14<00:00, 21.2MB/s]
Successfully completed 2 write cycles.

WRITE:  39%|███████████▌                  | 3.06G/7.93G [03:43<05:54, 13.7MB/s]
```



## English Version

### SD Card Lifespan Tester


This Python script is designed to test the lifespan of an SD card or other flash storage devices. It writes random data to the device until it's full, verifies the written data, and then deletes it. This process is repeated until an error occurs, which could indicate that the device has reached its write endurance limit.

### Warning

This script can cause irreversible damage to the tested device, as it continuously writes data to the device, potentially until the device's write endurance limit is reached. The testing process can take several weeks or even months to complete, depending on the size and speed of the device.

Use this script at your own risk. The author of this script is not responsible for any damage caused by the use of this script.

### Features


* Direct I/O: The script uses the Windows API to bypass the file system cache, ensuring that the data is actually written to the device.
* Write cycle count: The script keeps track of the number of completed write cycles and displays this count when an error occurs.
* Data verification: After writing the data, the script reads it back and verifies it against the MD5 hash of the written data.

### Dependencies


* Window OS
* Python 3.8 or higher
* tqdm (can be installed with `pip install tqdm`)

### Usage

```shell
python lifespan.py <folder>
```

Replace ` <folder>` with the path to the folder on the device you want to test.



## 中文版本

### SD卡寿命测试器


这个Python脚本用于测试SD卡或其他闪存存储设备的寿命。它将随机数据写入设备，直到设备满为止，然后验证写入的数据，并删除它。这个过程重复进行，直到出现错误，这可能表明设备已经达到了其写入耐久限制。

### 警告

这个脚本可能会对被测试的设备造成不可逆的损害，因为它会持续地向设备写入数据，可能直到设备的写入耐久限制。测试过程可能需要几周甚至几个月的时间才能完成，这取决于设备的大小和速度。

使用这个脚本的风险由用户自己承担。脚本的作者对使用此脚本可能造成的任何损害不承担责任。

### 特性


* 直接I/O：脚本使用Windows API绕过文件系统缓存，确保数据实际写入到设备。
* 写入周期计数：脚本跟踪完成的写入周期数，并在出现错误时显示此计数。
* 数据验证：写入数据后，脚本将其读回并根据写入数据的MD5哈希进行验证。

### 依赖项


* Windows 操作系统
* Python 3.8或更高版本
* tqdm（可以通过`pip install tqdm`安装）

### 使用方法

```shell
python lifespan.py <folder>
```

将`<folder>`替换为你想要测试的设备上的文件夹的路径。