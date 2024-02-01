import os

"""
Summary:

计算该脚本所在目录，所占用的存储空间大小
使用方法:
python3 calc_current_dir_size.py 
"""

def get_current_directory_size():
    # Get the current working directory
    current_directory = os.getcwd()

    # Initialize storage space size
    total_size = 0

    # Traverse the current directory and its subdirectories, accumulate file sizes
    for dirpath, dirnames, filenames in os.walk(current_directory):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            total_size += os.path.getsize(file_path)

    return total_size

def convert_bytes(size):
    # Convert bytes to a human-readable format
    units = ['B', 'KB', 'MB', 'GB', 'TB']

    unit_index = 0
    while size > 1024 and unit_index < len(units) - 1:
        size /= 1024.0
        unit_index += 1

    return "{:.2f} {}".format(size, units[unit_index])

def main():
    total_size_bytes = get_current_directory_size()
    total_size_readable = convert_bytes(total_size_bytes)

    print "Total size of the current directory: {}".format(total_size_readable)

if __name__ == "__main__":
    main()

