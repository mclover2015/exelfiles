# import pandas as pd
# import sys
# import re
#
#
# # --- 1. ЗАГРУЗКА БАЗЫ ДАННЫХ (МГНОВЕННО) ---
# def load_database(filepath="database.csv"):
#     """
#     Загружает ОДИН файл CSV и готовит его к поиску.
#     """
#     try:
#         # !!! ИСПРАВЛЕНИЕ ЗДЕСЬ: dtype=str !!!
#         # Заставляем Pandas читать ВСЕ как текст.
#         # Это не даст ему превратить "" в NaN.
#         df = pd.read_csv(filepath, dtype=str)
#
#     except FileNotFoundError:
#         print(f"ОШИБКА: Файл базы данных '{filepath}' не найден.")
#         print("Пожалуйста, сначала запустите 'import_data.py' для его создания.")
#         return None
#     except Exception as e:
#         print(f"ОШИБКА при чтении '{filepath}': {e}")
#         return None
#
#     print(f"База данных успешно загружена. {len(df)} записей.")
#
#     # --- ОЧИСТКА КЛЮЧЕВЫХ ПОЛЕЙ (для поиска) ---
#
#     # fillna('') - теперь заменяет 'nan' (если вдруг просочился) на ''
#     df['ІПН_clean'] = df['ІПН'].fillna('').astype(str).str.strip()
#     df['Телефон_clean'] = df['Телефон'].fillna('').astype(str).str.replace(r'[+\-()\s]', '', regex=True)
#     df['ПІБ_clean'] = df['ПІБ'].fillna('').astype(str).str.lower().str.strip()
#
#     # --- НОВОЕ: Очищаем остальные поля от NaN ---
#     # Мы просто заменяем все NaN на '' во всем DataFrame
#     df = df.fillna('')
#
#     print("Данные готовы к поиску.")
#     return df
#
#
# # --- 2. ФУНКЦИИ ПОИСКА (Без изменений) ---
#
# def search_by_ipn(df, ipn):
#     ipn_clean = str(ipn).strip()
#     result = df[df['ІПН_clean'] == ipn_clean]
#     return result
#
#
# def search_by_phone(df, phone):
#     phone_clean = re.sub(r'[+\-()\s]', '', str(phone))
#     result = df[df['Телефон_clean'] == phone_clean]
#     return result
#
#
# def search_by_name(df, name):
#     name_clean = str(name).lower().strip()
#     result = df[df['ПІБ_clean'].str.contains(name_clean, case=False, na=False)]
#     return result
#
#
# # --- 3. ОТОБРАЖЕНИЕ РЕЗУЛЬТАТОВ (Без изменений) ---
#
# def format_and_print(result_df):
#     """
#     Красиво выводит ПОЛНУЮ АНКЕТУ найденного человека.
#     """
#     if result_df.empty:
#         print("\n---------------------------------")
#         print(">> Ничего не найдено.")
#         print("---------------------------------\n")
#         return
#
#     print(f"\n---------------------------------")
#     print(f">> Найдено записей: {len(result_df)}")
#     print("---------------------------------")
#
#     for index, row in result_df.iterrows():
#         print(f"**Человек {index + 1}**")
#
#         # --- Основные поля ---
#         print(f"  ПІБ:              {row.get('ПІБ', 'N/A')}")
#         print(f"  Телефон:          {row.get('Телефон', 'N/A')}")
#         print(f"  ІНН (ІПН):        {row.get('ІПН', 'N/A')}")
#         print(f"  Дата народження:  {row.get('Дата_народження', 'N/A')}")
#         print(f"  Громадянство:     {row.get('Громадянство', 'N/A')}")
#         print(f"  Серія паспорта:   {row.get('Серія_паспорта', 'N/A')}")
#         print(f"  Номер паспорта:   {row.get('Номер_паспорта', 'N/A')}")
#         print(f"  Дата видачі:      {row.get('Дата_видачі', 'N/A')}")
#         print(f"  Видано:           {row.get('Видано', 'N/A')}")
#         print(f"  Адреса:           {row.get('Адреса', 'N/A')}")
#
#         # --- ИСПРАВЛЕНИЕ ЗДЕСЬ ---
#         # Теперь .get() будет видеть пустую строку '' и печатать '' (а не 'N/A')
#         # print(f"  Освіта:           {row.get('Освіта', 'N/A')}")
#         print(f"  Сімейний стан:    {row.get('Сімейний_стан', 'N/A')}")
#         print(f"  Електронна пошта: {row.get('Електронна пошта', 'N/A')}")  # Теперь ключ правильный
#
#         print(f"  (Источник:       {row.get('Источник_Файл', 'N/A')})")
#         print("---------------------------------")
#     print("\n")
#
#
# # --- 4. ГЛАВНЫЙ ЦИКЛ (Это будет ваш Telegram-бот) ---
#
# def main_loop(df):
#     while True:
#         print("\n--- Консольный Поиск (Тест Бота) ---")
#         print("Выберите опцию:")
#         print("  1. Поиск по ІПН")
#         print("  2. Поиск по Телефону")
#         print("  3. Поиск по ФИО (частичное совпадение)")
#         print("  4. Выход")
#         choice = input("Ваш выбор (1-4): ").strip()
#
#         if choice == '1':
#             term = input("Введите ІПН для поиска: ")
#             results = search_by_ipn(df, term)
#             format_and_print(results)
#
#         elif choice == '2':
#             term = input("Введите Телефон для поиска: ")
#             results = search_by_phone(df, term)
#             format_and_print(results)
#
#         elif choice == '3':
#             term = input("Введите Имя или Фамилию для поиска: ")
#             results = search_by_name(df, term)
#             format_and_print(results)
#
#         elif choice == '4':
#             print("Выход...")
#             sys.exit()
#
#         else:
#             print("! Неверный ввод. Пожалуйста, выберите от 1 до 4.")
#
#
# # --- 5. ЗАПУСК БОТА ---
# if __name__ == "__main__":
#     # Загружаем данные ОДИН РАЗ при старте
#     GLOBAL_DATA_FRAME = load_database()
#
#     if GLOBAL_DATA_FRAME is not None:
#         # Запускаем основной цикл (здесь будет ваш Telegram polling)
#         main_loop(GLOBAL_DATA_FRAME)
#     else:
#         print("Не удалось загрузить данные. Бот не может запуститься.")
ALLOWED_USER_IDS = [973147838,110759463] # Замените на ID свой и тех, кому доверяете

import pandas as pd
import sys
import re

# --- Код для скрытия ненужных предупреждений ---
import warnings
from telegram.warnings import PTBUserWarning

warnings.filterwarnings("ignore", category=PTBUserWarning)
# -----------------------------------------------

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters
)


# --- 1. ЗАГРУЗКА БАЗЫ ДАННЫХ (Без изменений) ---
def load_database(filepath="database.csv"):
    """
    Загружает ОДИН файл CSV и готовит его к поиску.
    """
    try:
        df = pd.read_csv(filepath, dtype=str)
    except FileNotFoundError:
        print(f"ОШИБКА: Файл базы данных '{filepath}' не найден.")
        print("Пожалуйста, сначала запустите 'import_data.py' для его создания.")
        return None
    except Exception as e:
        print(f"ОШИБКА при чтении '{filepath}': {e}")
        return None

    print(f"База данных успешно загружена. {len(df)} записей.")

    df['ІПН_clean'] = df['ІПН'].fillna('').astype(str).str.strip()
    df['Телефон_clean'] = df['Телефон'].fillna('').astype(str).str.replace(r'[+\-()\s]', '', regex=True)
    df['ПІБ_clean'] = df['ПІБ'].fillna('').astype(str).str.lower().str.strip()

    df = df.fillna('')

    print("Данные готовы к поиску.")
    return df


# --- 2. ФУНКЦИИ ПОИСКА (Без изменений) ---

def search_by_ipn(df, ipn):
    ipn_clean = str(ipn).strip()
    result = df[df['ІПН_clean'] == ipn_clean]
    return result


def search_by_phone(df, phone):
    phone_clean = re.sub(r'[+\-()\s]', '', str(phone))
    result = df[df['Телефон_clean'] == phone_clean]
    return result


def search_by_name(df, name):
    name_clean = str(name).lower().strip()
    result = df[df['ПІБ_clean'].str.contains(name_clean, case=False, na=False)]
    return result


# --- 3. ОТОБРАЖЕНИЕ РЕЗУЛЬТАТОВ (Чистый, ровный формат) ---
def format_results(result_df):
    """
    Форматирует DataFrame в красивую СТРОКУ для отправки в Telegram.
    Использует ``` для моноширинного шрифта и выравнивания.
    """
    if result_df.empty:
        return "```\n>> Ничего не найдено.\n```"

    response_parts = []

    for index, row in result_df.iterrows():
        info_lines = [
            f"ПІБ:              {row.get('ПІБ', '')}",
            f"Телефон:          {row.get('Телефон', '')}",
            f"ІНН (ІПН):        {row.get('ІПН', '')}",
            f"Дата народження:  {row.get('Дата_народження', '')}",
            f"Громадянство:     {row.get('Громадянство', '')}",
            f"Серія паспорта:   {row.get('Серія_паспорта', '')}",
            f"Номер паспорта:   {row.get('Номер_паспорта', '')}",
            f"Дата видачі:      {row.get('Дата_видачі', '')}",
            f"Видано:           {row.get('Видано', '')}",
            f"Адреса:           {row.get('Адреса', '')}",
            f"Освіта:           {row.get('Освіта', '')}",
            f"Сімейний стан:    {row.get('Сімейний_стан', '')}",
            f"Електронна пошта: {row.get('Електронна пошта', '')}",

        ]

        # Оборачиваем в ``` (блок моноширинного кода)
        person_info = "```\n" + "\n".join(info_lines) + "\n```"
        response_parts.append(person_info)

    return "\n\n".join(response_parts)


# --- 4. ЛОГИКА ТЕЛЕГРАМ-БОТА ---

GLOBAL_DATA_FRAME = load_database()
SELECTING_ACTION, AWAITING_IPN, AWAITING_PHONE, AWAITING_NAME = range(4)


# --- Клавиатуры ---
def get_main_keyboard():
    keyboard = [
        [InlineKeyboardButton("🔍 Поиск по ІПН", callback_data='ipn')],
        [InlineKeyboardButton("📞 Поиск по Телефону", callback_data='phone')],
        [InlineKeyboardButton("👤 Поиск по ФІО", callback_data='name')],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_persistent_keyboard():
    keyboard = [['🏠 Главное меню']]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# --- Обработчики этапов ---

# Этап 1: Команда /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начинает диалог и показывает кнопки."""
    user_id = update.message.from_user.id

    # --- !!! ВОТ ПРОВЕРКА !!! ---
    if user_id not in ALLOWED_USER_IDS:
        await update.message.reply_text("⛔️ У вас нет доступа к этому боту.")
        return ConversationHandler.END # Завершаем диалог
    # ---------------------------

    if GLOBAL_DATA_FRAME is None:
        await update.message.reply_text("⛔️ Ошибка: База данных не загружена. Бот не может работать.")
        return ConversationHandler.END

        # 1. Отправляем приветствие И постоянную клавиатуру
    # await update.message.reply_text(
    #     "Привет! Я бот для поиска по базе.\n"
    #     "Нажмите /start или '🏠 Главное меню', чтобы начать/перезапустить поиск.",
    #     reply_markup=get_persistent_keyboard()
    # )

    # 2. Отправляем кнопки выбора
    await update.message.reply_text(
        "По чему хотите сделать поиск?",
        reply_markup=get_main_keyboard()
    )

    return SELECTING_ACTION


# Этап 2: Пользователь нажимает кнопку
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает нажатие кнопок 'ipn', 'phone' или 'name'."""
    query = update.callback_query
    await query.answer()

    choice = query.data
    await query.edit_message_reply_markup(reply_markup=None)

    if choice == 'ipn':
        await query.message.reply_text("Пожалуйста, введите **ІПН**:", parse_mode='MarkdownV2')
        return AWAITING_IPN
    elif choice == 'phone':
        await query.message.reply_text("Пожалуйста, введите **номер телефона**:", parse_mode='MarkdownV2')
        return AWAITING_PHONE
    elif choice == 'name':
        await query.message.reply_text("Пожалуйста, введите **ФІО**:", parse_mode='MarkdownV2')
        return AWAITING_NAME

    # Этап 3 (А): Пользователь прислал текст (ІПН)


async def handle_ipn_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    search_term = update.message.text
    results_df = search_by_ipn(GLOBAL_DATA_FRAME, search_term)
    response_text = format_results(results_df)

    await update.message.reply_text(response_text, parse_mode='MarkdownV2')

    await update.message.reply_text("По чему хотите сделать поиск?", reply_markup=get_main_keyboard())
    return SELECTING_ACTION


# Этап 3 (Б): Пользователь прислал текст (Телефон)
async def handle_phone_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    search_term = update.message.text
    results_df = search_by_phone(GLOBAL_DATA_FRAME, search_term)
    response_text = format_results(results_df)

    await update.message.reply_text(response_text, parse_mode='MarkdownV2')

    await update.message.reply_text("По чему хотите сделать поиск?", reply_markup=get_main_keyboard())
    return SELECTING_ACTION


# Этап 3 (В): Пользователь прислал текст (ФИО)
async def handle_name_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    search_term = update.message.text
    results_df = search_by_name(GLOBAL_DATA_FRAME, search_term)
    response_text = format_results(results_df)

    await update.message.reply_text(response_text, parse_mode='MarkdownV2')

    await update.message.reply_text("По чему хотите сделать поиск?", reply_markup=get_main_keyboard())
    return SELECTING_ACTION


# Команда для отмены
async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отменяет текущий диалог."""
    await update.message.reply_text("Действие отменено. Нажмите '🏠 Главное меню', чтобы начать заново.",
                                    reply_markup=get_persistent_keyboard())
    return ConversationHandler.END


# --- 5. ЗАПУСК БОТА ---
def main():
    """Главная функция запуска бота."""

    TOKEN = "8051459362:AAHCImcZThdFXZpHgcDzW38_TA3hTa5WMU0"

    if TOKEN == "ВАШ_ТОКЕН_ОТ_BOTFATHER_ЗДЕСЬ":
        print("!!! ОШИБКА: Пожалуйста, вставьте ваш токен в переменную TOKEN в файле bot.py")
        return

    if GLOBAL_DATA_FRAME is None:
        print("!!! ОШИБКА: Не удалось загрузить database.csv. Бот не может запуститься.")
        return

    application = Application.builder().token(TOKEN).build()

    # --- !!! ИСПРАВЛЕНИЕ ЗДЕСЬ !!! ---
    # Мы создаем ОДИН обработчик диалога
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start_command),
            MessageHandler(filters.Text("🏠 Главное меню"), start_command)
        ],

        states={
            SELECTING_ACTION: [CallbackQueryHandler(button_handler)],
            AWAITING_IPN: [MessageHandler(filters.Text() & ~filters.COMMAND, handle_ipn_input)],
            AWAITING_PHONE: [MessageHandler(filters.Text() & ~filters.COMMAND, handle_phone_input)],
            AWAITING_NAME: [MessageHandler(filters.Text() & ~filters.COMMAND, handle_name_input)],
        },
        fallbacks=[
            CommandHandler("cancel", cancel_command),
            CommandHandler("start", start_command),
            MessageHandler(filters.Text("🏠 Главное меню"), start_command)
        ],
        per_message=False
    )

    # ...И добавляем ТОЛЬКО ЕГО.
    application.add_handler(conv_handler)
    # ------------------------------------

    print("Бот запущен. Нажмите Ctrl+C для остановки.")

    application.run_polling()


if __name__ == "__main__":
    main()