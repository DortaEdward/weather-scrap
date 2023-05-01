from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
from random import randint
from supabase import create_client, Client

class Scraper:
  def __init__(self):
    self.options = Options()
    self.options.headless = True
    self.options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36')
    self.driver = webdriver.Chrome()
    # self.driver = webdriver.Chrome(options=self.options)
    self.url = 'https://www.google.com'
    self.states = ['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
              'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
              'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
              'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
              'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']

  def start(self):
    self.driver.get(self.url)

  def close(self):
    self.driver.close()

  def loop_thur_arr(self):
    self.json = [self.getWeather(x) for x in self.states]

  def create_json_file(self):
    for i in range(len(self.json)):
      self.json[i] = {
        "state": self.states[i],
        "weather": self.json[i]
      }

  def printWeather():
    # Make a table with the weather data and print it out
    
    pass

  def getWeather(self, state: str):
    state_url = 'https://www.google.com/search?q={}+weather'.format(state)
    try:
      print('Getting Weather for:', state)
      self.driver.get(state_url)
      sleep(randint(1, 4))
      weekly_weather = self.driver.find_element(By.XPATH, '//*[@id="wob_dp"]')

      weekly_weather = weekly_weather.text.split('\n')
      for i, string in enumerate(weekly_weather):
        if len(string) == 6:
          weekly_weather[i] = string[:3]

      days_in_week = weekly_weather[0::2]
      weather_per_day = weekly_weather[1::2]

      weather_obj = {}

      for i in range(len(days_in_week)):
        weather_obj[days_in_week[i]] = weather_per_day[i]
        print(weather_obj[days_in_week[i]])
      return weather_obj
    except:
      print('error getting weather for:', state)

  def uploadToDB(self):
    url: str = 'https://jwabetvamhrditzxtffd.supabase.co'
    key: str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imp3YWJldHZhbWhyZGl0enh0ZmZkIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY3NzYwOTE5MiwiZXhwIjoxOTkzMTg1MTkyfQ.byTSGL1YqM38KoV27L_zlOa9VgVRDbIipEFQKDNpMww'
    supabase: Client = create_client(url, key)
    print('This is the json getting sent to supa')
    data, count = supabase.table('weather').insert({"weather":self.json}).execute()
    if data:
      return print('Upload Success')
    return print('Error Uploading file to db, contact Developer')

def main(): 
  chromedriver_autoinstaller.install()
  bot = Scraper()
  bot.start()
  bot.loop_thur_arr()
  bot.create_json_file()
  bot.uploadToDB()

if __name__ == "__main__":
  main()
