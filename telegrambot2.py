import telebot 
import instaloader
import os
import glob

api_key = "" 

bot = telebot.TeleBot(api_key)

ig = instaloader.Instaloader()

ig.load_session_from_file('topcortessecos', filename=('session-topcortessecos'))


@bot.message_handler(commands=["downloadstories"]) 
def baixarstories(mensagem):
    
    print(mensagem)
    sent = bot.send_message(mensagem.chat.id, "Type the Instagram user without @")
    
    bot.register_next_step_handler(sent, uservar)
    
def uservar(mensagem):

    user = str(mensagem.text)
    useridcheck = ig.check_profile_id(user)
   # ig.filename_pattern()
    print(useridcheck)
    bot.reply_to(mensagem, "Downloading the stories from user: @"+user)
    ig.download_stories(userids = [useridcheck], filename_target=(user+str(mensagem.from_user.id)))  
    bot.reply_to(mensagem, "_[CHECKING PROFILE...]_", parse_mode= 'Markdown')
    os.getcwd()
    collection = (user+str(mensagem.from_user.id)+'/')   
    bot.set_webhook()
    
    while True:  
        try:
            test = os.listdir(collection)
            bot.send_message(mensagem.chat.id, 'Public profile ✅')
            break
        except FileNotFoundError:
            bot.send_message(mensagem.chat.id, 'Private profile 🔓 or without any available story \nTry another profile')
            break
    for item in test:
        if item.endswith(".json.xz"):
            os.remove(os.path.join(collection, item))  
            
    for n, filename in enumerate(os.listdir(collection)):
        split_tup = os.path.splitext(str(n)+filename[-4:])
        file_name = split_tup[0]
        file_extension = split_tup[1]
        os.rename(collection+filename,collection+file_name+file_extension)
        if (file_extension == '.jpg'):
            bot.send_photo(chat_id = mensagem.chat.id, photo = open(collection+str(n)+file_extension, 'rb'))
        else:
            bot.send_video(chat_id = mensagem.chat.id, video = open(collection+str(n)+file_extension, 'rb'))
    
    bot.send_message(mensagem.chat.id, "Developed: @v1nox1")
    bot.send_animation(mensagem.chat.id, animation ='https://media.tenor.com/F3la7LnCiGAAAAAC/mighty-lancer-games-wink.gif')
    bot.send_message(mensagem.chat.id, "How about trying a new profile? type anything to bring the command again")
    
    postfiles = glob.glob(collection+'*')
    for f in postfiles:
        os.remove(f)
    

def verificar(mensagem):
    return True

@bot.message_handler(func=verificar) 
def responder(mensagem):
    texto = "/downloadstories - To download all available stories, click on the function\n*ONLY PUBLIC PROFILE, IT'S A BOT NOT A MAGE 🧙‍♂️!*\n\n_version: 1.3_"
    bot.reply_to(mensagem, "*Hey!* 🫶 \nSelect one function: \n\n"+texto, parse_mode= 'Markdown')
bot.polling()
