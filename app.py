import os
import shutil
import pathlib
import os.path as path


input_dir = r'input'
output_dir = r'output'


def deal_file(file_path, output_dir):
    with open(file_path, "rb") as f:
        if file_path.find(r'1.2.840') > 0:
            f.seek(0xFC)
            data = bytearray()
            while True:
                byte = f.read(1)
                i = int.from_bytes(byte, byteorder="little")
                if not (i >= 0x30 and i <= 0x39):
                    break
                data += byte
            # 将字节数组转换为UTF-8字符串
            utf8_str = data.decode("utf-8")
        else:
            start_offset = 0x000008d0
            end_offset = 0x000008e0

            f.seek(start_offset)
            data = f.read(end_offset - start_offset)

            result = ""
            for byte in data:
                if (byte >= 0x30 and byte <= 0x39):
                    result += chr(byte)

            # 将字节数组转换为UTF-8字符串
            utf8_str = result

        # 构造新文件名
        new_file_name = utf8_str + ".dcm"

        # 更改文件名并复制到指定目录
        new_file_path = path.join(output_dir, new_file_name)

        print(file_path)
        print(new_file_path)
        print()
        os.makedirs(output_dir, exist_ok=True)
        shutil.copy(file_path, new_file_path)

if __name__ == '__main__':
        # 遍历文件夹中的所有子文件夹和文件
    for subdir, dirs, files in os.walk(input_dir):
        for file in files:
            # 只处理.dcm文件
            if file.endswith(".dcm"):
                # 读取.dcm文件
                file_path = os.path.join(subdir, file)
                deal_file(file_path, subdir.replace(input_dir, output_dir))