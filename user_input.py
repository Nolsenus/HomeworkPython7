from user_output import send_output


def console_input(prompt, req_type, feedback_mode='console'):
    entered = ''
    try:
        entered = input(prompt)
        return req_type(entered)
    except ValueError:
        send_output(f'Несовместимые типы: {entered} и {req_type}', feedback_mode)
        return False


def get_input(prompt, req_type, mode='console'):
    match mode:
        case 'console': return console_input(prompt, req_type)
        case _:
            send_output(f'Неизвстный способ ввода данных: {mode}')
            return False
