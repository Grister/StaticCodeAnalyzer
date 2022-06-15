import ast
import re
import sys
from pathlib import Path

from style_errors import indentation, semicolon, spaces, class_name, def_name

count_blanks = 0


def style_guide(path, line, num_line):
    global count_blanks
    if len(line) == 0:
        if count_blanks == 2:
            print(f'{path}: Line {num_line + 1}: S006 More than two blank lines preceding a code line')
            count_blanks = 0
        else:
            count_blanks += 1
        return
    else:
        count_blanks = 0

    if len(line) > 79:
        print(f'{path}: Line {num_line}: S001 Too long')
    if line[0] == ' ':
        if indentation(line):
            print(f'{path}: Line {num_line}: S002 Indentation is not a multiple of four')
    if ';' in line:
        if semicolon(line):
            print(f'{path}: Line {num_line}: S003 Unnecessary semicolon')
    if '#' in line:
        if spaces(line):
            print(f'{path}: Line {num_line}: S004 Less than two spaces before inline comments')
        if 'todo' in line[line.index('#')::].lower():
            print(f'{path}: Line {num_line}: S005 TODO found')
    if line.strip().startswith('class'):
        if class_name(line) is not None:
            print(f"{path}: Line {num_line}: {class_name(line)}")
    if line.strip().startswith('def'):
        if def_name(line) is not None:
            print(f"{path}: Line {num_line}: {def_name(line)}")


def parse_in_rexp(path):
    file = open(path, 'r')
    for index, line in enumerate(file.read().splitlines()):
        style_guide(path, line, index + 1)
    file.close()


def parse_in_ast(path):
    file = open(path, 'r')
    tree = ast.parse(file.read())
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for el in [a.arg for a in node.args.args]:
                if re.match(r'[A-Z]', el):
                    print(f'{path}: Line {node.lineno}: S010 Argument name "{el}" should be written in snake_case')
            for item in [a for a in node.args.defaults]:
                if isinstance(item, ast.List):
                    print(f'{path}: Line {node.lineno}: S012 The default argument value is mutable')
        if isinstance(node, ast.Name):
            if isinstance(node.ctx, ast.Store):
                if re.match(r'[A-Z]', node.id):
                    print(f'{path}: Line {node.lineno}: S011 Variable {node.id} should be written in snake_case')
    file.close()


def start_checking(path):
    parse_in_rexp(path)
    parse_in_ast(path)


def get_path():
    path = sys.argv[1]
    if path.endswith('.py'):
        start_checking(path)
    else:
        entries = Path(path)
        for file in entries.iterdir():
            if str(file).endswith('.py'):
                start_checking(file)


if __name__ == '__main__':
    get_path()
