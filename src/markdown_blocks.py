def markdown_to_blocks(markdown: str):
    blocks = markdown.split("\n\n")
    stripped_blocks = [block.strip() for block in blocks]
    
    stripped_blocks[:] = [block for block in stripped_blocks if block != ""]
    
    return stripped_blocks