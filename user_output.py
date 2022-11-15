def console_output(message):
    print(message)


def send_output(message, mode='console'):
    match mode:
        case 'console':
            console_output(message)
            return True
        case _:
            console_output(f'Неизвестный способ вывода данных: {mode}')
            return False
