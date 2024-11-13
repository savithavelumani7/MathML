from xml.etree import ElementTree as ET

def apply_line_breaks(mathml):
    root = ET.fromstring(mathml)

    brace_chars = {"(", ")", "{", "}", "[", "]"}
    skip_chars = {",", ".", "|"}
    
    element_stack = []
    equal_count = 0 

    for elem in root.iter():
        element_stack.append(elem)

        if elem.tag.endswith("mo"):  
            operator = elem.text.strip() if elem.text else ""

            if operator == "∑" or operator in brace_chars or operator in skip_chars:
                continue 

            inside_braces = False
            for ancestor in reversed(element_stack[:-1]): 
                if ancestor.tag.endswith("mrow"):
                    has_braces = any(child.tag.endswith("mo") and child.text in brace_chars for child in ancestor)
                    if has_braces:
                        inside_braces = True
                        break
            
            is_near_summation = False
            for ancestor in reversed(element_stack[:-1]):
                if ancestor.tag.endswith("mrow"):
                    for sibling in ancestor:
                        if sibling.tag.endswith("mo") and sibling.text == "∑":
                            is_near_summation = True
                            break
                if is_near_summation:
                    break
            
            if is_near_summation:
                continue 
            
            if inside_braces:
                elem.set("linebreak", "badbreak") 
                if operator in {"+", "-"} and len(list(ancestor)) > 3:  
                    elem.set("linebreak", "goodbreak")
            else:
                if operator in {"−", "+"}:
                    elem.set("linebreak", "badbreak")
                else:
                    elem.set("linebreak", "goodbreak")
        
        # Handle the '=' operator with the custom logic (first '=' should not have line break)
        if elem.tag.endswith("mo") and elem.text.strip() == "=":
            equal_count += 1
            if equal_count > 1:  # Only set line break for subsequent '=' operators
                elem.set("linebreak", "goodbreak")
        
        element_stack.pop()

    return ET.tostring(root, encoding="unicode")


mathml_input="""
<ce:display xmlns:ce="http://www.w3.org/1998/Math/MathML" xmlns:mml="http://www.w3.org/1998/Math/MathML">
<mml:math altimg="si89.svg">
<mml:mrow>
<mml:mo>{</mml:mo>
<mml:mtable columnalign="left" columnspacing="1em" rowspacing="4pt">
<mml:mtr>
<mml:mtd>
<mml:mi>g</mml:mi>
<mml:mo stretchy="false">(</mml:mo>
<mml:mn>0</mml:mn>
<mml:mo stretchy="false">)</mml:mo>
<mml:mo linebreak="goodbreak">&#x003E;</mml:mo>
<mml:mn>0</mml:mn>
<mml:mstyle displaystyle="false" scriptlevel="0">
<mml:mtext> and </mml:mtext>
</mml:mstyle>
<mml:mi>g</mml:mi>
<mml:mo stretchy="false">(</mml:mo>
<mml:mn>0</mml:mn>
<mml:mo stretchy="false">)</mml:mo>
<mml:mo>⩾</mml:mo>
<mml:mn>2</mml:mn>
<mml:mi>λ</mml:mi>
<mml:mi>g</mml:mi>
<mml:mo stretchy="false">(</mml:mo>
<mml:mn>1</mml:mn>
<mml:mo stretchy="false">)</mml:mo>
</mml:mtd>
</mml:mtr>
<mml:mtr>
<mml:mtd>
<mml:mi>g</mml:mi>
<mml:mo stretchy="false">(</mml:mo>
<mml:mn>1</mml:mn>
<mml:mo stretchy="false">)</mml:mo>
<mml:mo>⩾</mml:mo>
<mml:mo movablelimits="true">max</mml:mo>
<mml:mo fence="false" stretchy="false">{</mml:mo>
<mml:mi>λ</mml:mi>
<mml:mo>+</mml:mo>
<mml:mfrac>
<mml:mn>1</mml:mn>
<mml:mn>2</mml:mn>
</mml:mfrac>
<mml:mo>,</mml:mo>
<mml:mn>2</mml:mn>
<mml:mi>λ</mml:mi>
<mml:mo fence="false" stretchy="false">}</mml:mo>
<mml:mi>g</mml:mi>
<mml:mo stretchy="false">(</mml:mo>
<mml:mn>2</mml:mn>
<mml:mo stretchy="false">)</mml:mo>
</mml:mtd>
</mml:mtr>
<mml:mtr>
<mml:mtd>
<mml:mfrac>
<mml:mrow>
<mml:mi>n</mml:mi>
<mml:mo>+</mml:mo>
<mml:mn>1</mml:mn>
</mml:mrow>
<mml:mrow>
<mml:mi>n</mml:mi>
<mml:mo>+</mml:mo>
<mml:mn>2</mml:mn>
<mml:mi>λ</mml:mi>
<mml:mo>+</mml:mo>
<mml:mn>4</mml:mn>
</mml:mrow>
</mml:mfrac>
<mml:mi>g</mml:mi>
<mml:mo stretchy="false">(</mml:mo>
<mml:mi>n</mml:mi>
<mml:mo>+</mml:mo>
<mml:mn>2</mml:mn>
<mml:mo stretchy="false">)</mml:mo>
<mml:mo>⩾</mml:mo>
<mml:mi>g</mml:mi>
<mml:mo stretchy="false">(</mml:mo>
<mml:mi>n</mml:mi>
<mml:mo>+</mml:mo>
<mml:mn>3</mml:mn>
<mml:mo stretchy="false">)</mml:mo>
</mml:mtd>
<mml:mtd>
<mml:mo stretchy="false">(</mml:mo>
<mml:mi>n</mml:mi>
<mml:mo>⩾</mml:mo>
<mml:mn>0</mml:mn>
<mml:mo stretchy="false">)</mml:mo>
</mml:mtd>
</mml:mtr>
</mml:mtable>
</mml:mrow>
</mml:math>
</ce:display>
"""
output = apply_line_breaks(mathml_input)
print(output)

# import xml.etree.ElementTree as ET

# # Sample MathML XML
# mathml_content = '''<?xml version="1.0" encoding="UTF-8"?>

# <ce:display xmlns:ce="http://www.w3.org/1998/Math/MathML" xmlns:mml="http://www.w3.org/1998/Math/MathML">
#  <ce:formula id="fd45c">
#  <ce:label>(45c)</ce:label>
#  <mml:math altimg="si125.gif">
#  <mml:mrow>
#  <mml:msub>
#  <mml:mrow>
#  <mml:mi>f</mml:mi>
#  </mml:mrow>
#  <mml:mrow>
#  <mml:mi>N</mml:mi>
#  </mml:mrow>
#  </mml:msub>
#  <mml:mo>=</mml:mo>
#  <mml:mo>−</mml:mo>
#  <mml:msub>
#  <mml:mrow>
#  <mml:mover accent="true">
#  <mml:mi>Q</mml:mi>
#  <mml:mo>ˉ</mml:mo>
#  </mml:mover>
#  </mml:mrow>
#  <mml:mrow>
#  <mml:mi>N</mml:mi>
#  </mml:mrow>
#  </mml:msub>
#  <mml:mo>=</mml:mo>
#  <mml:mo>−</mml:mo>
#  <mml:mfrac>
#  <mml:mrow>
#  <mml:msup>
#  <mml:mrow>
#  <mml:mi>L</mml:mi>
#  </mml:mrow>
#  <mml:mrow>
#  <mml:mn>3</mml:mn>
#  </mml:mrow>
#  </mml:msup>
#  <mml:msub>
#  <mml:mrow>
#  <mml:mi>Q</mml:mi>
#  </mml:mrow>
#  <mml:mrow>
#  <mml:mi>N</mml:mi>
#  </mml:mrow>
#  </mml:msub>
#  </mml:mrow>
#  <mml:mrow>
#  <mml:mi>E</mml:mi>
#  <mml:mi>I</mml:mi>
#  </mml:mrow>
#  </mml:mfrac>
#  <mml:mo>=</mml:mo>
#  <mml:mrow>
#  <mml:mo>(</mml:mo>
#  <mml:mrow>
#  <mml:mo>−</mml:mo>
#  <mml:msup>
#  <mml:mrow>
#  <mml:mi>η</mml:mi>
#  </mml:mrow>
#  <mml:mrow>
#  <mml:mn>2</mml:mn>
#  </mml:mrow>
#  </mml:msup>
#  <mml:munderover>
#  <mml:mo>∑</mml:mo>
#  <mml:mrow>
#  <mml:mi>j</mml:mi>
#  <mml:mo>=</mml:mo>
#  <mml:mn>1</mml:mn>
#  </mml:mrow>
#  <mml:mrow>
#  <mml:mi>N</mml:mi>
#  <mml:mo>+</mml:mo>
#  <mml:mn>4</mml:mn>
#  </mml:mrow>
#  </mml:munderover>
#  <mml:mrow>
#  <mml:msubsup>
#  <mml:mrow>
#  <mml:mi>E</mml:mi>
#  </mml:mrow>
#  <mml:mrow>
#  <mml:mi>N</mml:mi>
#  <mml:mi>j</mml:mi>
#  </mml:mrow>
#  <mml:mrow>
#  <mml:mrow>
#  <mml:mo>[</mml:mo>
#  <mml:mrow>
#  <mml:mn>5</mml:mn>
#  </mml:mrow>
#  <mml:mo>]</mml:mo>
#  </mml:mrow>
#  </mml:mrow>
#  </mml:msubsup>
#  <mml:msub>
#  <mml:mrow>
#  <mml:mi>δ</mml:mi>
#  </mml:mrow>
#  <mml:mrow>
#  <mml:mi>j</mml:mi>
#  </mml:mrow>
#  </mml:msub>
#  <mml:mo>+</mml:mo>
#  <mml:mrow>
#  <mml:mo>(</mml:mo>
#  <mml:mrow>
#  <mml:mn>1</mml:mn>
#  <mml:mo>−</mml:mo>
#  <mml:msup>
#  <mml:mrow>
#  <mml:mi>μ</mml:mi>
#  </mml:mrow>
#  <mml:mrow>
#  <mml:mn>2</mml:mn>
#  </mml:mrow>
#  </mml:msup>
#  <mml:msup>
#  <mml:mrow>
#  <mml:mover accent="true">
#  <mml:mi>r</mml:mi>
#  <mml:mo>ˉ</mml:mo>
#  </mml:mover>
#  </mml:mrow>
#  <mml:mrow>
#  <mml:mn>2</mml:mn>
#  </mml:mrow>
#  </mml:msup>
#  <mml:msup>
#  <mml:mrow>
#  <mml:mtext>Ω</mml:mtext>
#  </mml:mrow>
#  <mml:mrow>
#  <mml:mn>2</mml:mn>
#  </mml:mrow>
#  </mml:msup>
#  <mml:mo>+</mml:mo>
#  <mml:msup>
#  <mml:mrow>
#  <mml:mi>μ</mml:mi>
#  </mml:mrow>
#  <mml:mrow>
#  <mml:mn>2</mml:mn>
#  </mml:mrow>
#  </mml:msup>
#  <mml:msub>
#  <mml:mrow>
#  <mml:mi>K</mml:mi>
#  </mml:mrow>
#  <mml:mrow>
#  <mml:mi>p</mml:mi>
#  </mml:mrow>
#  </mml:msub>
#  </mml:mrow>
#  <mml:mo>)</mml:mo>
#  </mml:mrow>
#  </mml:mrow>
#  <mml:munderover>
#  <mml:mo>∑</mml:mo>
#  <mml:mrow>
#  <mml:mi>j</mml:mi>
#  <mml:mo>=</mml:mo>
#  <mml:mn>1</mml:mn>
#  </mml:mrow>
#  <mml:mrow>
#  <mml:mi>N</mml:mi>
#  <mml:mo>+</mml:mo>
#  <mml:mn>4</mml:mn>
#  </mml:mrow>
#  </mml:munderover>
#  <mml:mrow>
#  <mml:msubsup>
#  <mml:mrow>
#  <mml:mi>E</mml:mi>
#  </mml:mrow>
#  <mml:mrow>
#  <mml:mi>N</mml:mi>
#  <mml:mi>j</mml:mi>
#  </mml:mrow>
#  <mml:mrow>
#  <mml:mrow>
#  <mml:mo>[</mml:mo>
#  <mml:mrow>
#  <mml:mn>3</mml:mn>
#  </mml:mrow>
#  <mml:mo>]</mml:mo>
#  </mml:mrow>
#  </mml:mrow>
#  </mml:msubsup>
#  <mml:msub>
#  <mml:mrow>
#  <mml:mi>δ</mml:mi>
#  </mml:mrow>
#  <mml:mrow>
#  <mml:mi>j</mml:mi>
#  </mml:mrow>
#  </mml:msub>
#  <mml:mo>+</mml:mo>
#  <mml:mrow>
#  <mml:mo>(</mml:mo>
#  <mml:mrow>
#  <mml:msup>
#  <mml:mrow>
#  <mml:mtext>Ω</mml:mtext>
#  </mml:mrow>
#  <mml:mrow>
#  <mml:mn>2</mml:mn>
#  </mml:mrow>
#  </mml:msup>
#  <mml:msup>
#  <mml:mrow>
#  <mml:mi>μ</mml:mi>
#  </mml:mrow>
#  <mml:mrow>
#  <mml:mn>2</mml:mn>
#  </mml:mrow>
#  </mml:msup>
#  <mml:mo>+</mml:mo>
#  <mml:msup>
#  <mml:mrow>
#  <mml:mtext>Ω</mml:mtext>
#  </mml:mrow>
#  <mml:mrow>
#  <mml:mn>2</mml:mn>
#  </mml:mrow>
#  </mml:msup>
#  <mml:msup>
#  <mml:mrow> 
#  <mml:mover accent="true">
#  <mml:mi>r</mml:mi>
#  <mml:mo>ˉ</mml:mo>
#  </mml:mover>
#  </mml:mrow>
#  <mml:mrow>
#  <mml:mn>2</mml:mn>
#  </mml:mrow>
#  </mml:msup>
#  <mml:mo>−</mml:mo>
#  <mml:msup>
#  <mml:mrow>
#  <mml:mi>μ</mml:mi>
#  </mml:mrow>
#  <mml:mrow>
#  <mml:mn>2</mml:mn>
#  </mml:mrow>
#  </mml:msup>
#  <mml:msub>
#  <mml:mrow>
#  <mml:mi>K</mml:mi>
#  </mml:mrow>
#  <mml:mrow>
#  <mml:mi>w</mml:mi>
#  </mml:mrow>
#  </mml:msub>
#  <mml:mo>−</mml:mo>
#  <mml:msub>
#  <mml:mrow>
#  <mml:mi>K</mml:mi>
#  </mml:mrow>
#  <mml:mrow>
#  <mml:mi>p</mml:mi>
#  </mml:mrow>
#  </mml:msub>
#  </mml:mrow>
#  <mml:mo>)</mml:mo>
#  </mml:mrow>
#  </mml:mrow>
#  <mml:munderover>
#  <mml:mo>∑</mml:mo>
#  <mml:mrow>
#  <mml:mi>j</mml:mi>
#  <mml:mo>=</mml:mo>
#  <mml:mn>1</mml:mn>
#  </mml:mrow>
#  <mml:mrow>
#  <mml:mi>N</mml:mi>
#  <mml:mo>+</mml:mo>
#  <mml:mn>4</mml:mn>
#  </mml:mrow>
#  </mml:munderover>
#  <mml:mrow>
#  <mml:msubsup>
#  <mml:mrow>
#  <mml:mi>E</mml:mi>
#  </mml:mrow>
#  <mml:mrow>
#  <mml:mi>N</mml:mi>
#  <mml:mi>j</mml:mi>
#  </mml:mrow>
#  <mml:mrow>
#  <mml:mrow>
#  <mml:mo>[</mml:mo>
#  <mml:mrow>
#  <mml:mn>1</mml:mn>
#  </mml:mrow>
#  <mml:mo>]</mml:mo>
#  </mml:mrow>
#  </mml:mrow>
#  </mml:msubsup>
#  <mml:msub>
#  <mml:mrow>
#  <mml:mi>δ</mml:mi>
#  </mml:mrow>
#  <mml:mrow>
#  <mml:mi>j</mml:mi>
#  </mml:mrow>
#  </mml:msub>
#  </mml:mrow>
#  </mml:mrow>
#  <mml:mo>)</mml:mo>
#  </mml:mrow>
#  <mml:mo>,</mml:mo>
#  </mml:mrow>
#  </mml:math>
#  </ce:formula>
# </ce:display>'''

# # Parse XML content
# tree = ET.ElementTree(ET.fromstring(mathml_content))
# root = tree.getroot()

# # Define scoring criteria for good breaks
# def calculate_score(element):
#     """Calculate a score for a given 'good break' element."""
#     score = 0
#     if element.text == "=":
#         score += 10  # Assign a high score for equal sign
#     elif element.text in ["+", "−", "-"]:
#         score += 8  # Medium score for additive/subtractive operators
#     else:
#         score += 5  # Default score for other operators
    
#     # Example additional scoring criteria
#     # Consider depth (e.g., operators outside nested elements might score higher)
#     depth = len(list(element.iterancestors()))
#     score += (10 - depth)  # Higher score for breaks at shallower depths
    
#     return score

# # Find all 'good break' elements and assign scores
# good_breaks = []
# for elem in root.findall(".//mml:mo[@linebreak='goodbreak']", namespaces={'mml': 'http://www.w3.org/1998/Math/MathML'}):
#     score = calculate_score(elem)
#     good_breaks.append((elem, score))

# # Sort good breaks by score and set the highest one as 'newline'
# if good_breaks:
#     # Sort by score in descending order and take the highest
#     best_break = max(good_breaks, key=lambda x: x[1])
#     best_break[0].set("linebreak", "newline")

# # Output the modified XML
# ET.dump(root)
