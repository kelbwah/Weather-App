import requests, customtkinter as ctk, time, os
from PIL import Image, ImageTk
global location, text_box, relx, rely, count, widgets_drop_count, text_drop_count, temperature_label_size, weather_code_label_size
relx = 0
rely = 0
location = None
text_box = None
count = 0
widgets_drop_count = 0
text_drop_count = 0
temperature_label_size = 0
weather_code_label_size = 0

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')

# cwd = os.getcwd()
# image_path = "WEATHER_BACKGROUNDS"
# full_path = os.path.join(cwd, image_path)
# full_path = full_path.replace('\\', '/')
# cloudy_image = ctk.CTkImage(Image.open(full_path+'/CLOUDY_BACKGROUND.gif'))
# foggy_image = ctk.CTkImage(Image.open(full_path+'/FOG_WEATHER.gif'))
# raining_image = ctk.CTkImage(Image.open(full_path+'/RAINING_WEATHER.gif'))
# sunny_image = ctk.CTkImage(Image.open(full_path+'/SUNNY_WEATHER.gif'), size=(2560,1440))
# thunder_image = ctk.CTkImage(Image.open(full_path+'/THUNDER_BACKGROUND.gif'))
# snow_image = ctk.CTkImage(Image.open(full_path+'/SNOW_WEATHER.gif'))
#Might use these later

weatherCodes = {
      "0": "Unknown",
      "1000": "Clear",
      "1001": "Cloudy",
      "1100": "Mostly Clear",
      "1101": "Partly Cloudy",
      "1102": "Mostly Cloudy",
      "2000": "Fog",
      "2100": "Light Fog",
      "3000": "Light Wind",
      "3001": "Wind",
      "3002": "Strong Wind",
      "4000": "Drizzle",
      "4001": "Rain",
      "4200": "Light Rain",
      "4201": "Heavy Rain",
      "5000": "Snow",
      "5001": "Flurries",
      "5100": "Light Snow",
      "5101": "Heavy Snow",
      "6000": "Freezing Drizzle",
      "6001": "Freezing Rain",
      "6200": "Light Freezing Rain",
      "6201": "Heavy Freezing Rain",
      "7000": "Ice Pellets",
      "7101": "Heavy Ice Pellets",
      "7102": "Light Ice Pellets",
      "8000": "Thunderstorm"
}
    
def update_screen_first_time():
    global relx, rely, weather_information, text_box, widgets_drop_count, root, frame, text_drop_count, temperature_label_size, weather_code_label_size, temperature_label, weather_code_label, count
    if widgets_drop_count < 30:
            rely+=0.0115
            weather_information.place(relx = relx+0.5, rely = rely+0.3)
            text_box.place(relx = relx+0.5, rely = rely+0.2)
            widgets_drop_count+=1
            root.after(21, update_screen_first_time)
    else:
            if text_drop_count == 0:
                temperature_label.place(relx = relx + 0.5, rely = rely-0.1, anchor='center')
                weather_code_label.place(relx = relx + 0.5, rely = rely+0.03, anchor='center') 
                text_drop_count+=1
                root.after(10, update_screen_first_time)
            elif text_drop_count < 80 and text_drop_count > 0:
                temperature_label.configure(font=('Roboto', temperature_label_size))
                weather_code_label.configure(font=('Roboto', weather_code_label_size))            
                temperature_label_size+=1
                weather_code_label_size+=0.25
                text_drop_count+=1
                root.after(10, update_screen_first_time)
            elif text_drop_count == 80:
                    count+=1
        

def update_screen():
    global relx, rely, root, temperature_label, temperature_label_size, weather_code_label, weather_code_label_size, text_drop_count
    if text_drop_count == 0:
        temperature_label.place(relx = relx + 0.5, rely = rely-0.1, anchor='center')
        weather_code_label.place(relx = relx + 0.5, rely = rely+0.03, anchor='center') 
        text_drop_count+=1
        root.after(10, update_screen_first_time)
    elif text_drop_count < 80 and text_drop_count > 0:
        temperature_label.configure(font=('Roboto', temperature_label_size))
        weather_code_label.configure(font=('Roboto', weather_code_label_size))            
        temperature_label_size+=1
        weather_code_label_size+=0.25
        text_drop_count+=1
        root.after(10, update_screen_first_time)         

def retrieve_weather(event=None):
    global count, frame, temperature_label_size, weather_code_label_size, temperature_label, weather_code_label, text_drop_count, temperature, humidity, weatherCode, error_label
    error_label = None
    user_location = get_location_box()
    url = "https://api.tomorrow.io/v4/weather/realtime"
    api_key = "MDO7cymd27naoVgRsJWYNNXPTlCldIxv"

    querystring = {
    "location":user_location,
    "fields":["temperature"],
    "units":"imperial",
    "apikey":api_key}
    try:
        response = requests.request("GET", url, params=querystring)
        temperature = round(response.json()['data']['values']['temperature'])
        humidity = round(response.json()['data']['values']['humidity'])
        weatherCode = response.json()['data']['values']['weatherCode']

        temperature=str(temperature) + '°'
        weatherCode = weatherCodes[str(weatherCode)]

        if count == 0:
            temperature_label_size = 0
            weather_code_label_size = 0
            temperature_label = ctk.CTkLabel(master = frame, text = temperature, font=('Roboto', temperature_label_size))
            weather_code_label = ctk.CTkLabel(master = frame, text = weatherCode, font=('Roboto', weather_code_label_size))
            update_screen_first_time()
        else:
            temperature_label.destroy()
            weather_code_label.destroy()
            text_drop_count = 0
            temperature_label_size = 0
            weather_code_label_size = 0
            temperature_label = ctk.CTkLabel(master = frame, text = temperature, font=('Roboto', temperature_label_size))
            weather_code_label = ctk.CTkLabel(master = frame, text = weatherCode, font=('Roboto', weather_code_label_size))
            update_screen()
    except requests.exceptions.HTTPError as err:
        if err.response.status_code == 429:
            error_message = "Error 429: Too Many Requests, You must wait again until amount of requests is reset"
            print(error_message)
        else:
            error_message = (f"HTTP error occurred: {err}")
            print(error_message)

def get_location_box():
    global location, text_box
    location = text_box.get()
    return location

def create_app():
    global location, relx, rely, weather_information, text_box, root, count, frame
    
    location = None
    root = ctk.CTk()
    root.title('Weather App')
    root.geometry("800x600")
    
    frame = ctk.CTkFrame(master = root)
    frame.pack(pady=10, padx = 10, fill='both', expand = True)

    label = ctk.CTkLabel(master = frame, text = 'Weather App', font=('Roboto', 24))
    label.place(relx = relx + 0.5, rely = rely + 0.05, anchor='center')

    text_box = ctk.CTkEntry(master = frame, placeholder_text = 'Location', font=('Roboto', 14)) #Relx = 0.5
    text_box.place(relx = relx + 0.5, rely = rely+ 0.2, anchor='center')


    weather_information = ctk.CTkButton(master = frame, text = "Check Weather", font = ('Roboto', 14), command=retrieve_weather) #Relx = 0.5
    weather_information.place(relx = relx + 0.5, rely = rely + 0.3, anchor='center')

    text_box.bind('<Return>', retrieve_weather)
    root.mainloop()

if __name__ == '__main__':
    create_app()
