block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"
from textnode import text_node_to_html_node
from htmlnode import LeafNode,ParentNode,HTMLNode
from inline_markdown import text_to_textnodes


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
    if (
        block.startswith("# ")
        or block.startswith("## ")
        or block.startswith("### ")
        or block.startswith("#### ")
        or block.startswith("##### ")
        or block.startswith("###### ")
    ):
        return block_type_heading
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
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
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return block_type_paragraph
        return block_type_unordered_list
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return block_type_paragraph
            i += 1
        return block_type_ordered_list
    return block_type_paragraph

def to_child(text):
    text_node = text_to_textnodes(text)
    children = []
    for text in text_node:
        html_node = text_node_to_html_node(text)
        children.append(html_node)
    return children

def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = to_child(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = to_child(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)

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
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1 :]
    children = to_child(text.strip())
    return ParentNode(f"h{level}", children)
    
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
    return ParentNode("div", nodes, None)

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



