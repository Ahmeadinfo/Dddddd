import telebot
import requests

# إدخل توكن البوت الخاص بك
BOT_TOKEN = "7739546596:AAEpp7l5unfsFpTZ_XYN8sHRAbHJe4scBjg"
bot = telebot.TeleBot(BOT_TOKEN)

# الرسالة الترحيبية
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        f"🇩🇿 أهلا بك في بوت تفعيل عرض جيزي! أرسل رقم هاتفك لتفعيل العرض."
    )

# التعامل مع أرقام الهواتف
@bot.message_handler(func=lambda message: True)
def handle_number(message):
    num = message.text.strip()
    
    # التحقق من رقم الهاتف
    if not num.startswith("07") or len(num) != 10 or not num.isdigit():
        bot.send_message(
            message.chat.id,
            "❌ الرجاء إدخال رقم صحيح من 10 أرقام يبدأ بـ 07."
        )
        return
    
    bot.send_message(message.chat.id, "💬 جارٍ إرسال OTP...")
    
    # إرسال طلب OTP
    data = f'msisdn=213{num[1:]}&client_id=6E6CwTkp8H1CyQxraPmcEJPQ7xka&scope=smsotp'
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Djezzy/2.6.6"
    }
    
    try:
        res = requests.post(
            'https://apim.djezzy.dz/oauth2/registration', 
            data=data, 
            headers=headers
        ).text
        
        if 'the confirmation code has been sent successfully' in res:
            bot.send_message(
                message.chat.id,
                "✅ تم إرسال OTP. أرسل الكود الآن."
            )
            bot.register_next_step_handler(message, verify_otp, num)
        else:
            bot.send_message(
                message.chat.id,
                "❌ حدث خطأ أثناء إرسال OTP. حاول مرة أخرى لاحقاً."
            )
    except Exception as e:
        bot.send_message(
            message.chat.id,
            f"❌ خطأ في الاتصال بالخادم: {str(e)}"
        )

# التحقق من OTP
def verify_otp(message, num):
    otp = message.text.strip()
    data2 = f'otp={otp}&mobileNumber=213{num[1:]}&scope=openid&client_id=6E6CwTkp8H1CyQxraPmcEJPQ7xka&client_secret=MVpXHW_ImuMsxKIwrJpoVVMHjRsa&grant_type=mobile'
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Djezzy/2.6.6"
    }
    
    try:
        res = requests.post(
            'https://apim.djezzy.dz/oauth2/token', 
            data=data2, 
            headers=headers
        ).json()
        
        token = res.get('access_token')
        if token:
            bot.send_message(
                message.chat.id,
                "✅ تم التحقق من OTP. جارٍ تفعيل العرض..."
            )
            activate_offer(message, num, token)
        else:
            bot.send_message(
                message.chat.id,
                "❌ كود OTP غير صحيح. حاول مرة أخرى."
            )
    except Exception as e:
        bot.send_message(
            message.chat.id,
            f"❌ خطأ في الاتصال بالخادم: {str(e)}"
        )

# تفعيل العرض
def activate_offer(message, num, token):
    json_data = {
        "data": {
            "id": "GIFTWALKWIN",
            "type": "products",
            "meta": {
                "services": {
                    "steps": 10666,
                    "code": "GIFTWALKWIN2GO",
                    "id": "WALKWIN"
                }
            }
        }
    }
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=utf-8",
        "User-Agent": "Djezzy/2.6.6"
    }
    
    try:
        res = requests.post(
            f'https://apim.djezzy.dz/djezzy-api/api/v1/subscribers/213{num[1:]}/subscription-product?include=',
            json=json_data,
            headers=headers
        ).text
        
        if 'successfully done' in res:
            bot.send_message(
                message.chat.id,
                "🎉✅ تم تفعيل عرض جيزي بنجاح!"
            )
        elif '"UNAUTHORIZED"' in res:
            bot.send_message(
                message.chat.id,
                "❌ انتهت صلاحية الجلسة. أعد المحاولة."
            )
        else:
            bot.send_message(
                message.chat.id,
                "❌ حدث خطأ أثناء تفعيل العرض. حاول مرة أخرى."
            )
    except Exception as e:
        bot.send_message(
            message.chat.id,
            f"❌ خطأ في الاتصال بالخادم: {str(e)}"
        )

# تشغيل البوت
print("💬 البوت راهو خدام...")
bot.polling(none_stop=True)
