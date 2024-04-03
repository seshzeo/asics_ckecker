# использовать шаблонизатор jinja для создания своего класса ил фнкции представления
# список функций и сохранение состояния в глобальные переменные очень похоже на работу ООП.
# Переделать!
 
from telegram import Update
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, Updater, JobQueue, CallbackQueryHandler
from api_connect import parse_info, request_asic_info
import logging
from config import URLS, Endpoint, HEADRS_L, min_hash, ADMIN_CHAT_ID, API_TOKEN
 
logging.basicConfig(
    filename= 'log_tel.txt',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

asics_ip = ['https://ml7.l7mh9050.keenetic.link', 'https://l7.l7mh9050.keenetic.link']

menu_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton('Стата', callback_data='state')],
    [InlineKeyboardButton('Перезагрузить первый асик', callback_data='reboot0')],
    [InlineKeyboardButton('Перезагрузить второй асик', callback_data='reboot1')]
    ])

async def check_asic(context: Update):
    global min_hash, asics_ip
    asics_status = parse_info(ip_list= asics_ip, min_hash= min_hash, return_list=True)
    warning_text = ''
    tag = '\n🔴 '

    for asic in asics_status:
        ip = asic['ip']
        if 'error' in asic:
            warning_text += f"{tag} Проблема: {ip} {asic['error']}\n"
        else:
            hash5s = asic['STATS'][0]['rate_5s']
            hash_unit = asic['STATS'][0]['rate_unit'] # 'MH/s'

            if hash5s < min_hash:
                warning_text += f'{tag} Низкий хешрейт: {ip} {hash5s} {hash_unit}\n'

    if warning_text:
        print(warning_text) #debug
        await context.bot.send_message(
                chat_id = ADMIN_CHAT_ID,
                text = warning_text
            )


async def change_min_hash(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer = ''
    global min_hash
    input_value = int(context.args[0])
    if input_value < 1000 and input_value > 9500:
        answer = f'Неверное значение. Текущее значение {min_hash} MH/s'
    else:
        context.bot_data['my_variable'] = input_value
        answer = f'Пороговое значение хеша изменено на {input_value}'
    update.message.reply_text(answer)

        
async def get_buttons(update: Update):
    global menu_keyboard
    # Отправляем клавиатуру пользователю
    await update.message.reply_text('Выберите действие', reply_markup=menu_keyboard)


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    button_data = query.data
    global asics_ip
    # , reboot_headers
    status = ''

    if button_data == 'state':
        await stat(update=update, context=context)
    elif 'reboot' in button_data:
        index = int(button_data[-1])
        status = request_asic_info(URLS[index] + Endpoint().REBOOT, HEADRS_L[index])
        if status.status_code == 200:
            status = f'{URLS[index]} Перезагрузка началась'
        elif status.status_code >= 400 and status.status_code < 500:
            status = f'{URLS[index]} Ошибка на строне клиента. Код {status}'
        elif status.status_code >= 500 and status.status_code < 600:
            status = f'{URLS[index]} Ошибка на строне сервера. Код {status}'
        await query.answer(status)
    else:
        await context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = '🔴 Invalid command'
        )


async def say_hi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global menu_keyboard
    print('Hi from bot') #debug
    await context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = 'Hi from bot'
    )
    await update.message.reply_text('Выберите действие', reply_markup=menu_keyboard)


async def stat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global menu_keyboard
    parsed_info = parse_info(ip_list= asics_ip, min_hash= min_hash, return_list=False)
    print(parsed_info) #debug
    await context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = parsed_info
    )
    await update.message.reply_text('Выберите действие', reply_markup=menu_keyboard)


if __name__ == '__main__':
    print('Start app.')
    job_queue = JobQueue()
    application = ApplicationBuilder().token(API_TOKEN).job_queue(job_queue).build()
    application.add_handlers([
        CommandHandler('stat', stat),
        CommandHandler('hi', say_hi),
        CommandHandler('minhash', change_min_hash),
        CallbackQueryHandler(button_callback)
    ])
    job_queue.run_repeating(check_asic, interval=10, first=0)
    
    application.run_polling()