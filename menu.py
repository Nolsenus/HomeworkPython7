from user_output import send_output
from user_input import get_input
from calculator import calculate


def console_calc_menu():
    entry = ''
    while entry != 'назад':
        entry = get_input('Введите выражение, которое нужно посчитать, для выхода введите "назад": ', str)
        if entry == 'назад':
            return
        result = calculate(entry)
        if result is not False:
            if isinstance(result, str) and result.startswith('Д'):
                send_output(result)
            else:
                send_output(f'Результат вычислений: {result}')
        else:
            send_output('Полученная строка не является подсчитываемым выражением.')


def console_menu():
    command = ''
    commands = ['выход', 'посчитать', 'помощь']
    while command != 'выход':
        command = get_input('Введите команду, чтобы увидеть список команд введите "помощь": ', str).lower()
        if command in commands:
            if command == 'посчитать':
                console_calc_menu()
            elif command == 'помощь':
                send_output('"выход" - завершение работы программы.\n'
                            '"посчитать" - переход в режим калькулятора.\n'
                            '"помощь" - вывод списка команд.')
            else:
                send_output('Завершеие работы.')
        else:
            send_output(f'Неизвестная команда: {command}')


def open_menu(mode='console'):
    match mode:
        case 'console':
            console_menu()
            return True
        case _:
            send_output(f'Неизвестный режим меню: {mode}')
            return False
