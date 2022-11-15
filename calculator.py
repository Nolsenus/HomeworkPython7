def split_including_splitter(string, splitters):
    result = []
    left = ''
    for char in string:
        if char in splitters:
            result.append(left)
            result.append(char)
            left = ''
        else:
            left += char
    result.append(left)
    if len(result) > 1:
        return result
    return result[0]


def is_expression(string):
    status = 'begin'
    is_complex = False
    after_point = False
    open_brackets = 0
    signs = ('+', '-', '/', '*')
    for char in string:
        if status == 'begin':
            after_point = False
            if char.isdigit():
                status = 'num'
            elif char == '-':
                status = 'after sign'
            elif char == '(':
                open_brackets += 1
            elif char == 'j':
                status = 'after_j'
                is_complex = True
            else:
                status = 'error'
                break
        elif status == 'num':
            if char.isdigit():
                continue
            if char == ')':
                open_brackets -= 1
                if open_brackets < 0:
                    status = 'error'
                    break
                status = 'after bracket close'
            elif char in signs:
                status = 'after sign'
            elif char == 'j':
                status = 'after_j'
                is_complex = True
            elif char == '.':
                if after_point:
                    status = 'error'
                    break
                status = 'after_point'
                after_point = True
            else:
                status = 'error'
                break
        elif status == 'after sign':
            if char == '(':
                status = 'begin'
                open_brackets += 1
            elif char.isdigit():
                status = 'num'
            elif char == 'j':
                status = 'after_j'
                is_complex = True
            else:
                status = 'error'
                break
        elif status == 'after bracket close':
            if char in signs:
                status = 'after sign'
            elif char == ')':
                open_brackets -= 1
                if open_brackets < 0:
                    status = 'error'
                    break
            else:
                status = 'error'
                break
        elif status == 'after_point':
            if char.isdigit():
                status = 'num'
            else:
                status = 'error'
                break
        else:
            if char == ')':
                open_brackets -= 1
                if open_brackets < 0:
                    status = 'error'
                    break
                status = 'after bracket close'
            elif char in signs:
                status = 'after sign'
            else:
                status = 'error'
                break
    if status == 'error' or open_brackets != 0:
        return False
    return 'complex' if is_complex else 'real'


def is_int_or_float(string: str):
    if string.isdigit():
        return True
    try:
        float(string)
        return True
    except ValueError:
        return False


def multiply_or_divide(string):
    if '*' not in string and '/' not in string:
        try:
            return float(string)
        except ValueError:
            return string
    string = (split_including_splitter(string, ['*', '/']))
    result = 1
    sign = '*'
    for element in string:
        if is_int_or_float(element):
            if sign == '*':
                result *= float(element)
            else:
                try:
                    result /= float(element)
                except ZeroDivisionError:
                    return f'Деление на ноль. {"".join(string)}'
        elif element:
            sign = element
    return result


def calculate_real(expression):
    sum_parts = split_including_splitter(expression, ['+', '-'])
    if isinstance(sum_parts, str):
        return multiply_or_divide(sum_parts)
    for i in range(len(sum_parts)):
        sum_parts[i] = multiply_or_divide(sum_parts[i])
    res = 0
    sign = '+'
    for element in sum_parts:
        if isinstance(element, int) or isinstance(element, float):
            if sign == '+':
                res += element
            else:
                res -= element
        elif is_int_or_float(element):
            if sign == '+':
                res += float(element)
            else:
                res -= float(element)
        elif element.startswith('Д'):
            return element
        elif element == '+':
            sign = '+'
        else:
            sign = '-'
    return res


def transform_complex(entry):
    result = ''
    current = ''
    is_imaginary = False
    replace_minus_with_plus = False
    previous = ''
    for char in entry:
        if char.isdigit() or char == '.':
            current += char
        elif char == 'j':
            if not previous.isdigit():
                current += '1'
            is_imaginary = True
        else:
            if current:
                if replace_minus_with_plus:
                    result += '+'
                if is_imaginary:
                    result += f'0;{current}'
                else:
                    result += f'{current};0'
                current = ''
                replace_minus_with_plus = False
                is_imaginary = False
            if char == '-':
                current = '-'
                if previous.isdigit() or previous == ')' or previous == 'j':
                    replace_minus_with_plus = True
            else:
                result += char
        previous = char
    if current:
        if replace_minus_with_plus:
            result += '+'
        if is_imaginary:
            result += f'0;{current}'
        else:
            result += f'{current};0'
    return result


def multiply_complex(left, right):
    return [left[0] * right[0] - right[1] * left[1], left[0] * right[1] + left[1] * right[0]]


def divide_complex(divisible, divisor):
    mult = [divisor[0], -divisor[1]]
    divisible = multiply_complex(divisible, mult)
    divisor = multiply_complex(divisor, mult)
    try:
        return [divisible[0] / divisor[0], divisible[1] / divisor[0]]
    except ZeroDivisionError:
        return 'Деление на ноль.'


def multiply_or_divide_complex(entry):
    if '*' not in entry and '/' not in entry:
        return get_complex(entry)
    entry = (split_including_splitter(entry, ['*', '/']))
    result = get_complex(entry[0])
    sign = '*'
    for element in entry[1:]:
        if element == '*' or element == '/':
            sign = element
        else:
            element = get_complex(element)
            if sign == '*':
                result = multiply_complex(result, element)
            else:
                result = divide_complex(result, element)
                if result == 'Деление на ноль.':
                    return result
    return result


def get_complex(string):
    res = string.split(';')
    res[0] = float(res[0])
    res[1] = float(res[1])
    return res


def calculate_complex(entry):
    sum_parts = entry.split('+')
    if isinstance(sum_parts, str):
        return multiply_or_divide_complex(sum_parts)
    for i in range(len(sum_parts)):
        sum_parts[i] = multiply_or_divide_complex(sum_parts[i])
        if sum_parts[i] == 'Деление на ноль.':
            return sum_parts[i]
    res = sum_parts[0]
    for element in sum_parts[1:]:
        res[0] += element[0]
        res[1] += element[1]
    return f'{res[0]};{res[1]}'


def calculate_with_brackets(entry, mode):
    calc = calculate_real if mode == 'real' else calculate_complex
    current = ''
    while '(' in entry:
        for char in entry:
            if char == ')':
                equivalent = calc(current)
                if equivalent == 'Деление на ноль.':
                    return equivalent
                entry = entry.replace('(' + current + ')', str(equivalent))
                break
            elif char == '(':
                current = ''
            else:
                current += char
    return calc(entry)


def calculate(entry):
    entry = entry.replace(' ', '')
    is_exp = is_expression(entry)
    if is_exp is False:
        return False
    if is_exp == 'complex':
        entry = transform_complex(entry)
    result = calculate_with_brackets(entry, is_exp)
    if isinstance(result, float) or result.startswith('Деление на ноль.'):
        return result
    result = get_complex(result)
    return f'({result[0]}{"+" if result[1] >= 0 else ""}{result[1]}j)'
