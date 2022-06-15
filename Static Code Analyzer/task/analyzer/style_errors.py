import re


def indentation(line):  # Indentation is not a multiple of four
    count = 0
    for i in line:
        if i == ' ':
            count += 1
        else:
            break
    return True if count % 4 != 0 else False


def semicolon(line):  # Unnecessary semicolon
    if '#' in line:
        code_string = line[:line.index('#')].strip()
        if len(code_string) != 0:
            if ';' in code_string[-1]:
                return True
            else:
                return False
        else:
            return False
    elif line.strip()[-1] == ';':
        return True


def spaces(line):  # At least two spaces required before inline comments
    code_string = line[:line.index('#')]
    if len(code_string) == 0:
        return False
    else:
        count = 0
        for i in code_string[::-1]:
            if i == ' ':
                count += 1
            else:
                break
        return True if count != 2 else False


def class_name(line):
    if re.match(r'class [A-Z]', line.strip()):
        return None
    elif line.strip().startswith(r'class  '):
        return "S007 Too many spaces after class"
    else:
        new_line = line[:line.index(':')].replace("class", ' ').strip()
        return f"S008 Class name '{new_line}' should be written in CamelCase"


def def_name(line):
    if re.match(r'def [A-Z]', line.strip()):
        new_line = line.replace("():", " ").replace("def", ' ').strip()
        return f"S009 Function name '{new_line}' should be written in snake_case"
    elif line.strip().startswith(r'def  '):
        return "S007 Too many spaces after function"
    else:
        return None


def spaces_after_cons(line):
    pass
