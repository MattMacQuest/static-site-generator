import os
from markdown_blocks import markdown_to_html_node

def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("no title found")
        
# Generates the page HTML using the provided 
def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f" * {from_path} {template_path} -> {dest_path}")
    try:
        with open(from_path, "r") as f:
            md = f.read()
    except Exception as e:
        print(f"Unable to open file {from_path}. Reason: {e}")
        
    try:
        with open(template_path, "r") as f:
            template = f.read()
    except Exception as e:
        print(f"Unable to open file {from_path}. Reason: {e}")
    
    html_string = markdown_to_html_node(md).to_html()
    title = extract_title(md)
    
    final_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html_string)
    
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)

    try:
        with open(dest_path, "w") as f:
            f.write(final_html)
    except Exception as e:
                print(f"Unable to write file {from_path}. Reason: {e}")

def generate_page_recursive(dir_path_content: str, template_path: str, dest_dir_path: str):
    pass