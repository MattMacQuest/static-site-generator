import os, shutil


def copy_files_recursive(src: str, dst: str):
    """Recursively copies all files from source directory to a destination directory

    Args:
        src (str): Source directory
        dst (str): Destination directory
    """
    if not os.path.exists(dst):
        os.mkdir(dst)
    
    for filename in os.listdir(src):
        src_path = os.path.join(src, filename)
        dst_path = os.path.join(dst, filename)
        
        print(f" * {src_path} -> {dst_path}")
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
        else:
            copy_files_recursive(src_path, dst_path)