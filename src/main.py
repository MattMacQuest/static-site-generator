import os, shutil, sys
from copystatic import copy_files_recursive
from generate_content import generate_page, generate_page_recursive

dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
template_path = "./template.html"

def main():
    basepath = sys.argv[0] or '/'
    print(basepath)
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    print("Generating pages...")
    generate_page_recursive(
        os.path.join(dir_path_content),
        template_path,
        os.path.join(dir_path_public),
        basepath
    )

if __name__ == "__main__":
    main()