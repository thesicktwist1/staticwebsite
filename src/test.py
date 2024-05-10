import unittest
from htmlnode import LeafNode, ParentNode, HTMLNode 
from inline_markdown import (split_nodes_delimiter,extract_markdown_links,extract_markdown_images,split_nodes_image,split_nodes_link, text_to_textnodes)
from inline_blocks import(markdown_to_blocks,block_to_block_type,markdown_to_html,block_type_code,block_type_unordered_list)
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image,
)
file_path = "src/markdown_text.md"


class Test(unittest.TestCase):
    def test_first_word(self):
        node = TextNode("*italic* first word ", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        self.assertListEqual(
            [
                TextNode("italic", text_type_italic),
                TextNode(" first word ", text_type_text)
            ],
            new_nodes,
        )
    def test_two_words(self):
        node = TextNode("*italic* first *word*", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        self.assertListEqual(
            [
                TextNode("italic", text_type_italic),
                TextNode(" first ", text_type_text),
                TextNode("word", text_type_italic)
            ],
            new_nodes,
        )
    def test_markdown_links(self):
        pass
    def test_markdown_images(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        text2 = "This is text without a ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        self.assertListEqual(
            [
                ("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), 
                ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")             
            ],
            extract_markdown_images(text2)
        )
        self.assertListEqual(
            [],
            extract_markdown_images(text)
        )
    def test_split_nodes_image(self):
        node = TextNode(
    "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png) and another link again ![third image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
    text_type_text,
)
        new_nodes = split_nodes_image([node])
    def test_text_to_textnodes(self):
       text = r"This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
       result_nodes = [
    TextNode("This is ", text_type_text),
    TextNode("text", text_type_bold),
    TextNode(" with an ", text_type_text),
    TextNode("italic", text_type_italic),
    TextNode(" word and a ", text_type_text),
    TextNode("code block", text_type_code),
    TextNode(" and an ", text_type_text),
    TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
    TextNode(" and a ", text_type_text),
    TextNode("link", text_type_link, "https://boot.dev"),
]
       text_noded = text_to_textnodes(text)
       self.assertEqual(result_nodes , text_noded)

    
    
     
if __name__ == "__main__":
    unittest.main()
   