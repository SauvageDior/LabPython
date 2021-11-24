import zipfile
import os
import hashlib
import re
import csv
import requests
#######################################

# Программно разархивировать архив в выбранную директорию.
directory_to_extract_to = r'H:\\Labs\\lab1\\Lab1'
try:
    os.mkdir(directory_to_extract_to)
except Exception:
    print("Файл уже существует")
else:
    arch_file = zipfile.ZipFile('H:\\Labs\\tiff-4.2.0_lab1.zip')
    arch_file.extractall(directory_to_extract_to)
    arch_file.close()
# 2.1 Получить список файлов (полный путь) формата sh. Сохранить полученный список
txt_files = []
for r, d, f in os.walk("."):
    for file in f:
        if file.endswith(".txt"):
            txt_files.append(os.path.join(r, file))
print("Список всех файлов с расширением .txt")
print('\n'.join(txt_files))
# Задание №2.2 Получить значения MD5 хеша для найденных файлов и вывести полученные данные на экран.
result = []
for file in txt_files:
    data = open(file, 'rb')
    a = data.read()
    result.append(hashlib.md5(a).hexdigest())
    data.close()
print("Хэш-функция:")
print('\n'.join(result))
# Задание №3
target_hash = "4636f9ae9fef12ebd56cd39586d33cfb"
target_file = 'H:\\Labs\\tiff-4.2.0_lab1.zip'
target_file_data = ''

for r, d, f in os.walk(directory_to_extract_to):
    for file in f:
        data = os.path.join(r, file)
        data = open(data, 'rb')
        a = data.read()
        if (hashlib.md5(a).hexdigest()) == target_hash:
            target_file_data = a
            target_file += "\\" + file
        data.close()
print(target_file)
print(target_file_data)
# Задание №4
try:
    r = requests.get(target_file_data)
except Exception:
    print('invalid URL')
result_dct = {}

counter = 0

lines = re.findall(r'<div class="Table-module_row__3TH83">.*?</div>.*?</div>.*?</div>.*?</div>.*?</div>', r.text)
for line in lines:
    if counter == 0:
        # Удаление тегов
        headers = re.sub('<.*?>', ' ', line)
        # Извлечение списка заголовков
        headers = re.findall(r'Заболели|Умерли|Вылечились|Активные случаи', headers)
        print(headers)
    else:
#удаление тегов т символов лишних
        temp = re.sub('<.*?>', ';', line)
        temp = re.sub("\(.*?\)", '', temp)
        temp = re.sub(';+', ';', temp)
        temp = temp[1: len(temp) - 1]
        temp = re.sub('\s(?=\d)', '', temp)
        temp = re.sub('(?<=\d)\s', '', temp)
        temp = re.sub('(?<=0)\*', '', temp)
        temp = re.sub('_', '-1', temp)

        # Разбитие строки на подстроки
        tmp_split = temp.split(';')
        if len(tmp_split) == 6:
            tmp_split.pop(0)
#извлечение и удаление лишних символов из первого столбца
        country_name = tmp_split[0]
        country_name = re.sub('.*\s\s', '', country_name)
#извлечение данных из остальных столбцов
        col1_val = tmp_split[1]
        col2_val = tmp_split[2]
        col3_val = tmp_split[3]
        col4_val = tmp_split[4]

        # Запись данных в словарь
        result_dct[country_name] = [0, 0, 0, 0]
        result_dct[country_name][0] = int(col1_val)
        result_dct[country_name][1] = int(col2_val)
        result_dct[country_name][2] = int(col3_val)
        result_dct[country_name][3] = int(col4_val)

    counter += 1

    """
    temp = re.sub('<.*?>', ';', line)
    resultArr = list(filter(None, temp.split(';')))
    for i in range(len(resultArr)):
        if '(+' in resultArr[i]:
            resultArr[i - 1] += resultArr[i]
            resultArr[i] = ''
    resultArr = list(filter(None, resultArr))

    if resultArr[0] == 'Заболели' or resultArr[0] == '📝  ':
        continue

    resultArr[0] = resultArr[0][4::]


    result_dct[resultArr[0]] = 'Заболели: ' + resultArr[1] + '\nУмерли: ' + resultArr[2] + '\nВылечились: ' + resultArr[
        3] + '\nАктивные случаи: ' + resultArr[4] + ';\n'
    """

# Задание №5
output = open('data.csv', 'w')
w = csv.writer(output, delimiter=";")
w.writerow(headers)
for key in result_dct.keys():
    w.writerow([key, result_dct[key][0], result_dct[key][1], result_dct[key][2], result_dct[key][3]])
output.close()

# Задание №6
f_bool = True


try:
    target_country = input("Введите название страны: ")
    print(result_dct[target_country])
except Exception: print("Не верно введено название страны")







