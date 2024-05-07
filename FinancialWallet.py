from datetime import datetime
import os

class FinancialWallet:
    #Объявляем аттрибуты и параметры класса
    def __init__(self, data_new_record, record_choise, new_record_sum, new_record_description) -> None:
        self.data_new_record = data_new_record # дата новой записи
        self.record_choise = record_choise # переменная хранящая категорию (доходы/расходы)
        self.new_record_sum = new_record_sum # сумма
        self.new_record_description = new_record_description #описание
 

    def change_record(): #функция изменения записи
        with open('operations.txt', 'r', encoding='utf-8') as file: #открываем файл на чтение
            lines = file.readlines() #разбиваем file на строки
            record_number = int(input('Введите номер записи: ')) #храним номер интересующей записи для редактирования
            #создаём словарь
            new_items = {
                'Дата': input('Введите новую дату: '),
                'Категория': input('Введите вид операции: '),
                'Сумма': int(input('Введите сумму: ')),
                'Описание': input('Введите новое описание: ')
            }
            for i in range(0, len(lines), 2): #перебираем строки с шагом 2
                if lines[i].strip() == f'Номер записи: {record_number}': #проверяем условие что эта та самая нужная запись
                    for key, value in new_items.items(): #проходим пословарю
                        lines[i+1] = f'{key}: {value}\n'#забираем значения которые мы установили словарю
                        i += 1 #проверяем следующую запись (спорный момент ибо номер записи уникален, однако гарантировать не может ибо "защиты от дурака - нет")
        with open('operations.txt', 'w', encoding='utf-8') as file: #открываем на запись
            file.writelines(lines)#записываем


    def check_balance():#проверка на запись
        with open('operations.txt', 'r', encoding='utf-8') as file:#открываем файл на чтение
            lines = file.readlines()#разбиваем file на строки
        income = 0 #инициализируем переменную доходов
        expense = 0#инициализируем переменную расходов
        for i in range(0, len(lines), 2):  # Перебираем строки с шагом 2
            if 'Доход' in lines[i]: #проверяем на слово
                income += int(lines[i+1].split(':')[1])  # Сумма находится в следующей строке
            elif 'Расход' in lines[i]:#проверяем на слово
                expense += int(lines[i+1].split(':')[1])  # Сумма находится в следующей строке
        return print(f'Доход: {income}, Расход: {expense}')#скармливаем значение обратно в функцию для вывода (да вот тут так захотелось)

    #функция записи, здесь я сделал проверку на наличие файла, его пустоту и заполненость (ни один файл не пострадал, наверное)
    def add_record(self):
            try:
                if os.stat('operations.txt').st_size == 0:
                    with open('operations.txt', 'a+', encoding='utf-8') as text_file:
                        #переменная отвечающая за добавление к записи её "уникального" номера (ха-хы в .txt - уникальный номер, хорошая шутка)
                        record_number = 1
                        #определяем словарь
                        operation_dict = {
                            "Номер записи":f'{record_number}',
                            "Дата":f'{self.data_new_record}',
                            "Категория":f'{self.record_choise}',
                            "Сумма":f'{self.new_record_sum}',
                            "Описание":f'{self.new_record_description}\n',
                        }
                        #записываем
                        for key in operation_dict:
                                print(f'{key}: {operation_dict[key]}', file=text_file)

                elif os.stat('operations.txt').st_size != 0:
                        with open('operations.txt', 'r+', encoding='utf-8') as file_check:
                            #увеличиваем на 1 нашу "уникальную переменную"
                            self.record_number = file_check.read().split()[-9]
                        with open('operations.txt', 'a+', encoding='utf-8') as text_file:
                            self.record_number = int(self.record_number) + 1
                            operation_dict = {
                                "Номер записи":f'{self.record_number}',
                                "Дата":f'{self.data_new_record}',
                                "Категория":f'{self.record_choise}',
                                "Сумма":f'{self.new_record_sum}',
                                "Описание":f'{self.new_record_description}\n',
                                }
                            for key in operation_dict:
                                print(f'{key}: {operation_dict[key]}', file=text_file)
            #вдруг файла нет
            except FileNotFoundError:
                with open('operations.txt', 'a+', encoding='utf-8') as text_file:
                    self.record_number = 1
                    operation_dict = {
                        "Номер записи":f'{self.record_number}',
                        "Дата":f'{self.data_new_record}',
                        "Категория":f'{self.record_choise}',
                        "Сумма":f'{self.new_record_sum}',
                        "Описание":f'{self.new_record_description}\n',
                    }
                    for key in operation_dict:
                        print(f'{key}: {operation_dict[key]}', file=text_file)

    #функция поиска
    def search_records(filename, operation=None, sum=None, description=None):
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        results = [] #создаем список
        i = 0 #счётчик
        while i < len(lines):
            if lines[i].strip() == '':
                i += 1
                continue
            # это прям жесть что тут происходит (ну потому что структурированный .txt. - это конечно весело, вы ребята клёвые)
            record = {lines[i+j].split(':')[0]: lines[i+j].split(':')[1].strip() for j in range(5)} #проходимся по каждой строке каждой записи с шагом 5 (у нас же 5 строк в каждой записи)
            #сразу сверяемся
            if ((operation is None or record['Категория'] == category) and
                (sum is None or int(record['Сумма']) == int(sum)) and
                (description is None or record['Описание'] == description)):
                results.append(record)
            i += 6
        #вдруг пустой 
        if not results:
            print("Не найдено записей, соответствующих вашим критериям поиска.")
        else:
            return results
#когда уже конеееец хоспаде...извинити, создаём "разговор" с пользователем
choise = input("Выберете необходимую операцию: \
                1 - Добавление записи\
                2 - Проверка баланса\
                3 - Редактирование\
                4 - Поиск") 
if choise == '1':
    addRecord = FinancialWallet(datetime.now().strftime('%Y-%m-%d'),\
                                input("Доходы или расходы?\n"),\
                                int(input("Введите сумму: ")),\
                                input("Введите описание: ")).add_record()
if choise == '2':
    checkBalance = FinancialWallet.check_balance()
    checkBalance
if choise == '3':
    changeRecord = FinancialWallet.change_record()
if choise == '4':
    search_choise = int(input('Выберите критерий поиска:\
                            1 - Поиск по категории доход/расход\
                            2 - Поиск по сумме\
                            3 - Поиск по описанию\n'))
    if search_choise == 1:
        filename = 'operations.txt'
        category = input('Введите Доход или Расход: ')
        sum = None
        description = None
        records = FinancialWallet.search_records(filename, category, sum, description)
        if records:
            for record in records:
                print(record)
    if search_choise == 2:
        filename = 'operations.txt'
        category = None
        sum = int(input('Введите стоимость: '))
        description = None
        records = FinancialWallet.search_records(filename, category, sum, description)
        if records:
            for record in records:
                print(record)
    if search_choise == 3:
        filename = 'operations.txt'
        category = None
        sum = None
        description = input('Введите описание: ')
        records = FinancialWallet.search_records(filename, category, sum, description)
        if records:
            for record in records:
                print(record)
        
#P.S. Задание, конечно, весьма интересное хоть и на практике не приминимо
#Можно было бахнуть кучу регулярок, зашить всё это в генераторы и веселиться до утра
#Не стал над собой издеваться сделал "как 7ми классник"
#Не судите строго, всего Вам наилучшего.
#За авторство шуток - не ручаюсь.