import pandas as pd
import sys
import re
import os
import glob
import openpyxl
import time


# --- 1. ХЕЛПЕР (для имен, работает с ОТКРЫТОЙ книгой) ---
def get_named_range_value_from_wb(workbook, range_name):
    """
    Извлекает значение из именованного диапазона УЖЕ ОТКРЫТОЙ книги.
    """
    try:
        if range_name in workbook.defined_names:
            named_range = workbook.defined_names[range_name]
            destinations = named_range.destinations
            if destinations:
                sheet_name, cell_coord = list(destinations)[0]
                if '!' in cell_coord:
                    cell_coord = cell_coord.split('!')[-1]
                cell_coord = cell_coord.replace('$', '')
                if ':' in cell_coord:
                    cell_coord = cell_coord.split(':')[0]

                sheet = workbook[sheet_name]
                cell_value = sheet[cell_coord].value
                return str(cell_value).strip() if cell_value is not None else ""
        return ""  # Не найдено
    except Exception as e:
        print(f"      - ОШИБКА (имя): при чтении '{range_name}'. Ошибка: {e}")
        return ""


# --- 1.5. ХЕЛПЕР (для ячеек, работает с ОТКРЫТЫМ листом) ---
def get_cell_value_from_sheet(sheet, cell_coord):
    """
    Извлекает значение из КОНКРЕТНОЙ ЯЧЕЙКИ УЖЕ ОТКРЫТОГО листа.
    """
    try:
        cell_value = sheet[cell_coord].value
        return str(cell_value).strip() if cell_value is not None else ""
    except Exception as e:
        print(f"      - ОШИБКА (ячейка): при чтении '{cell_coord}'. Ошибка: {e}")
        return ""


# --- 2. ЗАГРУЗКА, ПАРСИНГ И ОЧИСТКА (ОПТИМИЗИРОВАННАЯ) ---

def load_and_process_all_files(folder_path="excel_files"):
    """
    Находит все .xlsm, ОТКРЫВАЕТ КАЖДЫЙ 1 РАЗ, парсит,
    собирает в DataFrame и СОХРАНЯЕТ В CSV.
    """

    search_pattern = os.path.join(folder_path, "*.xlsm")
    file_list = glob.glob(search_pattern)

    if not file_list:
        print(f"ОШИБКА: Не найдено ни одного .xlsm файла в папке: {os.path.abspath(folder_path)}")
        return None

    print(f"Найдено {len(file_list)} файлов. Начинаю импорт...")

    all_people_data = []
    workbook = None
    start_time = time.time()

    for i, file in enumerate(file_list):
        try:
            print(f"  ({i + 1}/{len(file_list)}) Обрабатываю: {os.path.basename(file)}...")
            person_data = {}

            # 1. ОТКРЫВАЕМ ФАЙЛ ТОЛЬКО ОДИН РАЗ
            workbook = openpyxl.load_workbook(file, data_only=True)

            # 2. ПОЛУЧАЕМ НУЖНЫЙ ЛИСТ
            sheet = workbook['Кредитна заявка']

            # --- 3. СОБИРАЕМ ВСЕ ДАННЫЕ СРАЗУ ---

            # --- Имена ---
            person_data[
                'ПІБ'] = f"{get_named_range_value_from_wb(workbook, 'lastName')} {get_named_range_value_from_wb(workbook, 'firstName')} {get_named_range_value_from_wb(workbook, 'middleName')}".replace(
                "  ", " ").strip()
            person_data['Телефон'] = get_named_range_value_from_wb(workbook, 'phoneNumber')
            person_data['ІПН'] = get_named_range_value_from_wb(workbook, 'taxNumber')
            person_data['Дата_народження'] = get_named_range_value_from_wb(workbook, 'birthDate')
            person_data['Громадянство'] = get_named_range_value_from_wb(workbook, 'Nationality')
            person_data['Сімейний_стан'] = get_named_range_value_from_wb(workbook, 'maritalStatus')

            # !!! ИСПРАВЛЕНИЕ ЗДЕСЬ !!!
            person_data['Електронна пошта'] = get_named_range_value_from_wb(workbook, 'email')  # Был '_'

            person_data['Освіта'] = ""

            # --- Ячейки (Паспорт и Адрес) ---

            # --- Паспорт ---
            person_data['Серія_паспорта'] = get_cell_value_from_sheet(sheet, 'L32')

            passport_raw = get_cell_value_from_sheet(sheet, 'M32')  # Читаем '123456' или '123456.0'
            if passport_raw:
                try:
                    passport_clean_str = str(int(float(passport_raw)))
                except ValueError:
                    passport_clean_str = re.sub(r'\D', '', passport_raw)

                person_data['Номер_паспорта'] = passport_clean_str.zfill(9)  # '123456' -> '000123456'
            else:
                person_data['Номер_паспорта'] = ""  # Оставляем пустым

            person_data['Дата_видачі'] = get_cell_value_from_sheet(sheet, 'N32')
            person_data['Видано'] = get_cell_value_from_sheet(sheet, 'O32')

            # --- Адрес ---
            person_data['Адреса'] = get_cell_value_from_sheet(sheet, 'O41')  # Читаем 'УКРАЇНА ПОЛТАВСЬКА...'

            # 4. ЗАКРЫВАЕМ ФАЙЛ
            workbook.close()
            workbook = None

            # --- Проверка ---
            if not person_data['ПІБ'] and not person_data['Телефон'] and not person_data['ІПН']:
                print(f"  [!] ПРЕДУПРЕЖДЕНИЕ: Файл {os.path.basename(file)} пропущен (пустые поля).")
                continue

            person_data['Источник_Файл'] = os.path.basename(file)
            all_people_data.append(person_data)

        except Exception as e_file:
            if workbook:
                workbook.close()
                workbook = None
            print(f"  [!] КРИТИЧЕСКАЯ ОШИБКА при обработке файла {os.path.basename(file)}: {e_file}")

    if not all_people_data:
        print("\nОбработка завершена. Не удалось собрать ни одной записи.")
        return

    end_time = time.time()
    print(f"\nОбработка завершена. Собрано {len(all_people_data)} записей за {end_time - start_time:.2f} сек.")
    print("Создаю DataFrame...")

    final_df = pd.DataFrame(all_people_data)

    print("Сохраняю данные в 'database.csv'...")

    # --- ЭТО ГЛАВНАЯ ЦЕЛЬ ---
    final_df.to_csv("database.csv", index=False)

    print("=" * 40)
    print("ГОТОВО. База данных 'database.csv' создана.")
    print("Теперь вы можете запускать bot.py")
    print("=" * 40)


# --- 3. ЗАПУСК СКРИПТА ---
if __name__ == "__main__":
    # Убедитесь, что ваши .xlsm файлы лежат в папке "excel_files"
    load_and_process_all_files(folder_path="excel_files")