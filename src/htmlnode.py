class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        cleaned_props = ""
        if self.props is None:
            return ""
        else:
            for k, v in self.props.items():
                    cleaned_props += f' {k}="{v}"'
            return cleaned_props 

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

class LeafNode(HTMLNode): 
   def __init__(self, tag, value, props=None):
       super().__init__(tag, value, None, props)

   def to_html(self):
      if self.value is None:
          raise ValueError("No value")
      if self.tag is None:
          return self.value
      if self.tag == "img":
          return f"<{self.tag}{self.props_to_html()}>{self.value}"
      else:
          return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
      
   def __repr__(self):
       return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag , children , props=None):
       super().__init__(tag , None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("No tag")
        if not self.children:
            raise ValueError("No children")
        html_string = ""
        for child in self.children:
           html_string += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{html_string}</{self.tag}>"
    
    def __repr__(self):
       return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
    
