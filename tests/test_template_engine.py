# Factory test suit
from silhouette.template_engine import *

def test_eval_simple_variables():
    input_text = "/home/ubuntu/project/$name$/$module$/readme.md"
    vars = {"name": "flask", "module": "example"}
    te = TemplateEngine(vars)
    
    result = te.eval_str(input_text)
    assert('/home/ubuntu/project/flask/example/readme.md' in result)


def test_eval_complex_expr():
    input_text = "/home/ubuntu/project/$name$/$module;upper$/readme.md"
    vars = {"name": "flask", "module": "example"}
    te = TemplateEngine(vars)
    
    result = te.eval_str(input_text)
    assert('/home/ubuntu/project/flask/EXAMPLE/readme.md' in result)