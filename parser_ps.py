import  subprocess
import datetime


def create_output_text():
    text_ = \
    f"""Отчет о состоянии системы:
    Пользователи системы: {users}
    Процессов запущено: {counter} 

    Пользовательских процессов:
    {users_processes_string}

    Всего памяти используется: {mem}%
    Всего ЦПУ используется: {cpu}%

    Больше всего памяти использует: {most_memory[0][0:20]} - {most_memory[1]}%
    Больше всего ЦПУ использует: {most_cpu[0][0:20]} - {most_cpu[1]}%
    """
    return text_

if __name__=='__main__':
    with open('ps_orig.txt', 'w') as out:
        result = subprocess.run(['ps', '-aux'], stdout=out, check=True)
    with open('ps_orig.txt', 'r') as read_file:
        line = read_file.readline()
        users_set = set()
        users_processes = dict()
        most_memory = ['', 0]   # Процесс больше всего использующий память
        most_cpu = ['', 0]      # Процесс больше всего использующий ЦПУ
        counter = 0             # Общий счетчик процессов
        cpu = 0                 # Общее использование ЦПУ
        mem = 0                 # Общее количество используемой памяти
        for line in read_file:
            counter += 1
            list_lines = line.split()
            users_set.add(list_lines[0])
            users_processes.setdefault(list_lines[0],0)
            users_processes[list_lines[0]] += 1
            cpu += float(list_lines[2])
            mem += float(list_lines[3])
            if float(list_lines[2]) > most_cpu[1]:
                most_cpu[0] = list_lines[10]
                most_cpu[1] = float(list_lines[2])
            if float(list_lines[3]) > most_memory[1]:
                most_memory[0] = list_lines[10]
                most_memory[1] = float(list_lines[3])
    users = ', '.join(map(str, users_set))
    users_processes = sorted(users_processes.items(), key=lambda item_: item_[1], reverse=True)
    users_processes_string = ''
    for key,item in users_processes:
        users_processes_string += f'{key}: {item}\n'
    current_time = datetime.datetime.now()
    output_file_name = current_time.strftime('%d-%m-%y_')+current_time.strftime('%H:%M:%S') +'-scan.txt'
    final_text = create_output_text()
    print(final_text)
    with open(output_file_name, 'w') as result_file:
        result_file.write(final_text)
