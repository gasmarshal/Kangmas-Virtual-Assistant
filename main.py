from bs4 import BeautifulSoup as bs
import requests
from function.online import find_my_ip, search_on_wikipedia ,play_on_youtube,search_on_google, send_whatsapp_message, send_email
import pyttsx3
import speech_recognition as sr
from decouple import config
from datetime import datetime
from function.offline import open_calculator, open_camera, open_cmd, open_notepad, open_tidur, report_time
from random import choice
from utils import opening_text
from pprint import pprint
 
USERNAME = config('USER')
BOTNAME = config('BOTNAME')


engine = pyttsx3.init('sapi5')

# Set Rate
engine.setProperty('rate', 190)

# Set Volume
engine.setProperty('volume', 3.0)

# Set Voice (Female)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


# Text to Speech Conversion
def speak(text):
     
    engine.say(text)
    engine.runAndWait()


# Greetings
def greet_user():

    
    hour = datetime.now().hour
    if (hour >= 6) and (hour < 12):
        speak(f"Selamat Pagi {USERNAME}")
    elif (hour >= 12) and (hour < 16):
        speak(f"Selamat Sore {USERNAME}")
    elif (hour >= 16) and (hour < 19):
        speak(f"Selamat Malam {USERNAME}")
    speak(f"Halo Saya {BOTNAME}. ada yang bisa dibantu?")


# suara 
def take_user_input():
    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Lagi dengerin....')
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print('Sedang berjalan...')
        query = r.recognize_google(audio, language='id-ID')
        print(f"user said {query}\n")
        if not 'exit' in query or 'stop' in query:
            speak(choice(opening_text))
        else:
            hour = datetime.now().hour
            if hour >= 21 and hour < 6:
                speak("Selamat malam")
            else:
                speak('Semoga harimu menyenangkan')
            exit()
    except Exception:
        speak('Saya tidak paham, tolong diulangi lagi')
        query = 'None'
    return query


if __name__ == '__main__':
    greet_user()
    while True:
        query = take_user_input().lower()

        if 'buka notepad' in query:
            open_notepad()


        elif 'buka command prompt' in query or 'open cmd' in query:
            open_cmd()

        elif 'buka kamera' in query:
            open_camera()

        elif 'buka kalkulator' in query:
            open_calculator()

        elif 'ip address' in query:
            ip_address = find_my_ip()
            speak(f'IP kamu {ip_address}.\n Biar saya tulis dilayar agar bos bisa baca.')
            print(f'IP Address kamu {ip_address}')

        elif 'wikipedia' in query:
            speak('Mau cari apa di Wikipedia, bos?')
            search_query = take_user_input().lower()
            results = search_on_wikipedia(search_query)
            speak(f"menurut Wikipedia, {results}")
            speak("biar saya tampilkan di layar untuk kamu ya bos.")
            print(results)

        elif 'buka youtube' in query:
            speak('mau buka apa di youtube?')
            video = take_user_input().lower()
            play_on_youtube(video)

        elif 'buka google' in query:
            speak('mau cari apa di google?')
            query = take_user_input().lower()
            search_on_google(query)

        elif "kirim pesan whatsapp" in query:
            speak('Mau kirim pesan kesiapa? coba tuliskan dahulu: ')
            number = input("no telepon: ")
            speak("Pesannya apa bos?")
            message = take_user_input().lower()
            send_whatsapp_message(number, message)
            speak("aku sudah kirim ya.")
            
        elif "send an email" in query:
            speak("On what email address do I send sir? Please enter in the console: ")
            receiver_address = input("Enter email address: ")
            speak("What should be the subject sir?")
            subject = take_user_input().capitalize()
            speak("What is the message sir?")
            message = take_user_input().capitalize()
            if send_email(receiver_address, subject, message):
                speak("I've sent the email sir.")
            else:
                speak("Something went wrong while I was sending the mail. Please check the error logs sir.")
 
        elif 'cuaca' in query:
            page = requests.get("https://www.google.com/search?q=cuaca")
            soup = bs(page.content,"html.parser")
            print("WEATHER INFORMATION :")
            des = soup.find("div",attrs={"class":"BNeawe tAd8D AP7Wnd"})
            print("sekarang hari " + des.text)
            speak("sekarang hari" + des.text)
            loc = soup.find("span",attrs={"class":"BNeawe tAd8D AP7Wnd"})
            print(f"Lokasi  : {loc.text}")
            speak(f"Lokasi saat ini : {loc.text}")
            temp = soup.find("div",attrs={"class":"BNeawe iBp4i AP7Wnd"})
            print(f"TEMPREATURE : {temp.text}")
            speak(f"TEMPREATUR : {temp.text}")

        elif "tidur yuk" in query.lower():
            speak("Kangmas siap tidur, selamat malam")
            open_tidur()
        
        elif 'jam berapa' in query.lower():
            current_time = report_time()
            print(f"sekarang jam {current_time}")
            speak(f"sekarang jam {current_time}")
        
        elif "makasih" in query.lower():
            speak("Selamat tinggal")
            exit()