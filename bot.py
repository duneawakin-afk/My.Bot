02.28 6:47 PM
import telebot
import socket
import requests

# আপনার দেওয়া টোকেন
API_TOKEN = '8538554837:AAH-55NyRmP1Q6GLLpIyny-cJjpSHJUcMfo'
bot = telebot.TeleBot(API_TOKEN)

# স্টার্ট কমান্ড
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        " স্বাগতম! আমি আপনার IP Helper বট।\n\n"
        " **কিভাবে ব্যবহার করবেন?**\n"
        "১. কোনো ওয়েবসাইটের IP জানতে লিঙ্ক দিন (উদা: google.com)\n"
        "২. কোনো IP-র তথ্য জানতে সরাসরি IP লিখুন (উদা: 8.8.8.8)"
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

# প্রধান ফাংশন
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text.strip().replace("http://", "").replace("https://", "").split('/')[0]
    
    try:
        # চেক করা হচ্ছে এটি কি IP নাকি ডোমেইন
        if any(char.isalpha() for char in text):
            # ডোমেইন থেকে IP বের করা
            ip_address = socket.gethostbyname(text)
            bot.reply_to(message, f" **Website:** {text}\n **IP Address:** `{ip_address}`", parse_mode='Markdown')
            lookup_ip(message, ip_address) # সাথে সাথে ওই IP-র লোকেশনও দেখাবে
        else:
            # সরাসরি IP ইনফো দেখা
            lookup_ip(message, text)
            
    except Exception as e:
        bot.reply_to(message, "❌ দুঃখিত! সঠিক লিঙ্ক বা IP দিতে পারেননি। আবার চেষ্টা করুন।")

# IP লোকেশন বের করার ফাংশন
def lookup_ip(message, ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}").json()
        
        if response['status'] == 'success':
            country = response.get('country', 'N/A')
            city = response.get('city', 'N/A')
            lat = response.get('lat', 0)
            lon = response.get('lon', 0)
            maps_link = f"https://www.google.com/maps?q={lat},{lon}"
            
            info = (
                f" **IP Logger Info:**\n"
                f"️ **Country:** {country}\n"
                f"️ **City:** {city}\n"
                f"️ **Google Map:** [এখানে ক্লিক করুন]({maps_link})"
            )
            bot.send_message(message.chat.id, info, parse_mode='Markdown', disable_web_page_preview=False)
        else:
            bot.send_message(message.chat.id, " এই IP-র কোনো তথ্য পাওয়া যায়নি।")
    except:
        bot.send_message(message.chat.id, "⚠️ লোকেশন বের করতে সমস্যা হয়েছে।")

print("বটটি এখন চালু আছে...")
bot.infinity_polling()

