"""
Small sphinx extension to show PyScript code and corresponding JS.
"""

import os
import hashlib

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

from sphinx.util.compat import Directive
from docutils import nodes

from flexx.pyscript import py2js

pythonLexer, javaScriptLexer = get_lexer_by_name('py'), get_lexer_by_name('js')
htmlFormatter = HtmlFormatter()

# 
# THIS_DIR = os.path.abspath(os.path.dirname(__file__))
# HTML_DIR = os.path.abspath(os.path.join(THIS_DIR, '..', '_build', 'html'))
# 
# if not os.path.isdir(HTML_DIR + '/ui'):
#     os.mkdir(HTML_DIR + '/ui')
#     
# if not os.path.isdir(HTML_DIR + '/ui/examples'):
#     os.mkdir(HTML_DIR + '/ui/examples')


def my_highlight(code):
    return highlight(code, PythonLexer(), HtmlFormatter())

class pyscript_example(nodes.raw): pass

def visit_pyscript_example_html(self, node):
    
    # Get code
    code = node.code.strip() + '\n'
    
    # Split in parts (blocks between two newlines)
    lines = [line.rstrip() for line in code.splitlines()]
    code = '\n'.join(lines)
    parts = code.split('\n\n')
    
    td_style = "style='vertical-align:top;'"  # width:50%;
    pre_style = "style='margin:2px; padding: 2px; border:0px;'"
    
    
    self.body.append("<style> div.hiddenjs {height: 1.2em; width: 2em; overflow:hidden; } div.hiddenjs:hover {height: initial; width: initial;}</style>\n")
    
    self.body.append("<table>")
    #self.body.append("<tr><td style='text-align:right;'> <i>PyScript</i>&nbsp;&nbsp; </td><td>&nbsp;&nbsp; <i>JS</i> </td></tr>")
    
    for py in parts:
        
        if py.strip().startswith('##'):
            text = py.lstrip(' \n#\t')
            self.body.append('<tr><td %s><b>%s</b></td><td %s></td></tr>' % 
                             (td_style, text, td_style))
            continue
        
        js = py2js(py)
        
        py_html = highlight(py, pythonLexer, htmlFormatter)
        js_html = highlight(js, javaScriptLexer, htmlFormatter)
        py_html = py_html.replace("<pre>", '<pre %s>' % pre_style)
        js_html = js_html.replace("<pre>", '<pre %s>' % pre_style)
        js_html = "<div class='hiddenjs'>JS %s</div>" % js_html
        
        #self.body.append("%s <div class='hiddenjs'><a>&nbsp;</a> %s</div>" % (py_html, js_html))
        self.body.append("<tr><td %s>%s</td><td %s>%s</td></tr>" % 
                         (td_style, py_html, td_style, js_html))
        
    self.body.append("</table>")
    
def depart_pyscript_example_html(self, node):
    pass

class PyscriptExampleDirective(Directive):
        has_content = True
        def run(self):
            # Get code and extact height
            code = '\n'.join(self.content)
            try:
                height = int(self.content[0])
            except Exception:
                height = 300
            else:
                 code = code.split('\n', 1)[1].strip()
            
            # iframe
            table = pyscript_example('')
            table.code = code
            
            return[table]


def setup(Sphynx):
    
    #Sphynx.add_javascript('js-image-slider.js')
    #Sphynx.add_stylesheet('js-image-slider.css')
    
    Sphynx.add_node(pyscript_example, html=(visit_pyscript_example_html, depart_pyscript_example_html))
    Sphynx.add_directive('pyscript_example', PyscriptExampleDirective)
