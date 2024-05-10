import re
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image,
)

def split_nodes_delimiter(old_nodes, delimiter, text_type):
     new_nodes = []
     for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        split = old_node.text.split(delimiter)
        if len(split) % 2 == 0:
            raise ValueError("Invalid markdown")
        for i in range(len(split)):
            if split[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(split[i], text_type_text))
            else:
                new_nodes.append(TextNode(split[i], text_type))
     return new_nodes

def extract_markdown_images(text):
    reg_pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(reg_pattern, text)
    return matches

def extract_markdown_links(text):
    reg_pattern = r"(?<!\!)\[(.*?)\]\((.*?)\)"
    matches = re.findall(reg_pattern, text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        extract_image = extract_markdown_images(original_text) 
        if len(extract_image) == 0:
            new_nodes.append(old_node)
            continue
        for pre , suff in extract_image:
            text = original_text.split(f"![{pre}]({suff})", 1)
            if len(text) != 2:
                raise Exception("Error")
            if text[0] != "":
                new_nodes.append(TextNode(text[0],text_type_text))
            original_text = text[1]
            new_nodes.append(TextNode(pre,text_type_image,suff))
        if original_text != "":
            new_nodes.append(TextNode(original_text, text_type_text))
    return new_nodes     

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        extract_links = extract_markdown_links(original_text) 
        if len(extract_links) == 0:
            new_nodes.append(old_node)
            continue
        for pre , suff in extract_links:
            text = original_text.split(f"[{pre}]({suff})", 1)
            if len(text) != 2:
                raise Exception("Error link ")
            if text[0] != "":
                new_nodes.append(TextNode(text[0],text_type_text))
            original_text = text[1]
            new_nodes.append(TextNode(pre,text_type_link,suff))
        if original_text != "":
            new_nodes.append(TextNode(original_text, text_type_text))
    return new_nodes

def text_to_textnodes(text):
    text_nodes = [TextNode(text,text_type_text)]
    text_nodes = split_nodes_delimiter(text_nodes,"**",text_type_bold)
    text_nodes = split_nodes_delimiter(text_nodes,"*", text_type_italic)
    text_nodes = split_nodes_delimiter(text_nodes,"`", text_type_code)
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)
    return text_nodes








