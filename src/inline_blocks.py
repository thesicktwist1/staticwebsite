block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"

from htmlnode import LeafNode,ParentNode,HTMLNode
from inline_markdown import text_to_textnodes
import re
import math


def extract_title(markdown):
    markdown_splitted = markdown.split("\n")
    for markdowns in markdown_splitted:
        if markdowns.startswith("# "):
            return markdowns[2:]
    else:
        raise Exception("All pages need a single h1 header.")

def markdown_to_blocks(markdown):
    blocks_list = []
    markdown_splitted = markdown.split("\n\n")
    for markdowns in markdown_splitted:
        if markdowns == "":
            continue 
        markdowns = markdown.strip()
        blocks_list.append(markdowns)
    return blocks_list

def block_to_block_type(block):
    lines = block.split("\n")
    heading_pattern = r"^(#{1,6} )"
    list_pattern = r"^(\d+\. )"
    if re.findall(heading_pattern, block):
        return block_type_heading
    if len(lines) > 1 and block.startswith("```") and block.endswith("```"):
        return block_type_code
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return block_type_paragraph
        return block_type_quote
    if block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return block_type_paragraph
        return block_type_unordered_list 
    if re.findall(list_pattern,block) and not block.startswith("0"):
        return block_type_ordered_list
    else:
        return block_type_paragraph

def to_child(text):
    text_node = text_to_textnodes(text)
    children = []
    for text in text_node:
        html_node = text.text_node_to_html_node()
        children.append(html_node)
    return children

def ulist_to_html_node(block):
    lines = block.split("\n")
    ulist = []
    for line in lines:
        text = line[2:]
        children = to_child(text)
        ulist.append(ParentNode(tag="li",children=children))
    return ParentNode(tag="ul",children=ulist)


def olist_to_html_node(block):
    lines = block.split("\n")
    olist = []
    for line in lines:
        text = line[3:]
        children = to_child(text)
        olist.append(ParentNode(tag="li",children=children))
    return ParentNode(tag="ol",children=olist)

def quote_to_html_node(block):
    lines = block.split("\n")
    quote_list = []
    for line in lines:   
       quote_list.append(line.lstrip(">").strip())
    list_joined = " ".join(quote_list)
    new_lines = to_child(list_joined)
    return ParentNode(tag="blockquote",children=new_lines)
           
def code_to_html_node(block):
    if block_to_block_type(block) == block_type_code:
        line = block.lstrip("`").rstrip("`")
        new_lines = to_child(line)
        code_html = ParentNode(tag="code",children=new_lines)
        return ParentNode(tag="pre",children=code_html)
    else:
        raise ValueError("Invalide code")
          
def heading_to_html_node(block):
    split = block.split(" ")
    count = split[0].count("#")
    if count > 6:
        raise ValueError("Invalid heading")
    else:
        lines = block.lstrip("# ")
        new_lines = to_child(lines)
        return ParentNode(tag=f"h{count}",children=new_lines)
    
def paragraph_to_html_node(block):
    lines = block.split("\n")
    new_lines = " ".join(lines)
    paragraph = to_child(new_lines)
    return ParentNode(tag="p",children=paragraph)

def markdown_to_html(markdown):
    new_markdown = markdown_to_blocks(markdown)
    nodes = []
    for markdown in new_markdown:
        html_node = block_to_html_node(markdown)
        nodes.append(html_node)
    return ParentNode(tag="div", children=nodes)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == block_type_paragraph:
        return paragraph_to_html_node(block)
    if block_type == block_type_heading:
        return heading_to_html_node(block)
    if block_type == block_type_code:
        return code_to_html_node(block)
    if block_type == block_type_ordered_list:
        return olist_to_html_node(block)
    if block_type == block_type_unordered_list:
        return ulist_to_html_node(block)
    if block_type == block_type_quote:
        return quote_to_html_node(block)
    raise ValueError("Invalid type")



