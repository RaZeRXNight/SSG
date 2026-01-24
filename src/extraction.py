from re import findall

def extract_markdown_images(text):
    """
    Returns a Tuple (Image Alt, Image Link)
    """
    return findall(r'\!\[(.*?)\]\((.*?)\)', text)

def extract_markdown_links(text):
    """
    Returns a Tuple (Image Alt, Image Link)
    """
    return findall(r'(?<!\!)\[(.*?)\]\((.*?)\)', text)

