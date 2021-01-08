# Factory test suit
from silhouette.factory import *

def test_render_file_paths():
    src_paths = ["/home/ubuntu/project/$name$/$module$/readme.md", "/home/ubuntu/project/$name$/$module$/jenkinsfile"]
    vars = {"name": "flask", "module": "example"}
    result = render_file_paths(src_paths, vars)
    assert('/home/ubuntu/project/flask/example/readme.md' in result)
    assert('/home/ubuntu/project/flask/example/jenkinsfile' in result)