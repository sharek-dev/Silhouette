import re

def fold_left(items, function, default):
    acc = default
    for x in items:
        acc = function(acc,x)
    return acc


BUILT_IN_FUNCTIONS = {
    "upper": str.upper,
    "lower": str.lower,
    "capitalize": str.capitalize,
    "casefold": str.casefold,
    "strip": str.strip,
    "swapcase": str.swapcase,
    "title": str.title
}

class SilhouetteExpression:
    def __init__(self, expr):
        self.expr = expr
        self.variable, self.functions = self.parse(expr)

    def get_variable(self):
        return self.variable

    def get_functions(self):
        return [ BUILT_IN_FUNCTIONS[f_name] for f_name in self.functions]

    def parse(self, expr):
        steps = expr.split(";")
        return steps[0], steps[1:]
    
    def validate(self):
        # Todo! implement
        pass

    def eval(self, value):
        """ 
        Example: "$name;upper$", "sample" -> "SAMPLE"
        """
        applied_functions = self.get_functions()
        return fold_left(applied_functions,lambda acc, x: x(acc) ,value)
        
        

class TemplateEngine:
    def __init__(self, vars):
        self.vars = vars
        self.search_regex = r"\$([^\$]*)\$"

    def get_value(self, var_name):
        if var_name in self.vars:
            return self.vars[var_name]
        else:
            raise Exception("Field {} was not declared in default.properties".format(var_name))

    def get_function(self, f):
        pass
    
    def find_all(self, text):
        matches = re.finditer(self.search_regex, text, re.MULTILINE)
        return [ (match.start(), match.end(), match.group(1) ) for matchNum, match in enumerate(matches, start=1) ]

    def replace_into(self, s, key, value):
        replaced_keys = "${}$".format(key)
        return s.replace(replaced_keys, value)

    def eval_str(self, text):
        expressions = self.find_all(text)

        result = text
        for start, end, expr in expressions:
            silhouette_expr = SilhouetteExpression(expr)
            variable_value = silhouette_expr.get_variable()
            evaluated_expr = silhouette_expr.eval( self.get_value(variable_value) )
            result = self.replace_into(result, expr, evaluated_expr)

        return result