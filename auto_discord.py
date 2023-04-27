from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
import random
from get_gpt_reply import *

chrome_path='C:\Program Files\Google\Chrome\Application\chromedriver.exe'

user_agent=['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.48',
'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11']

# channel_id_list=['1098950653746872341/1099683521104203816']

mode={'cat':'meow:smiley_cat:','peace':':innocent:','kiss':':kissing_smiling_eyes:','cool':':sunglasses:'}


with open ('./auto_bot_discord/gpt_key.txt','r') as f:
    key = f.read()

chrome_option = webdriver.ChromeOptions()
services = service.Service(executable_path=chrome_path)
# chrome_option.add_argument("--start-maximized")
# chrome_option.add_argument('--incognito')
chrome_option.add_argument('user-agent='+user_agent[random.randint(0,3)])
# chrome_option.add_argument('--headless')
driver = webdriver.Chrome(service=services, options=chrome_option)
driver.maximize_window()


def log_in_discord(url,log_in):
    driver.get(url=url)
    print('Logging in')
    WebDriverWait(driver=driver,timeout=30,poll_frequency=1).until(EC.element_to_be_clickable((By.XPATH,'//button[@class="marginBottom8-emkd0_ button-1cRKG6 button-ejjZWC lookFilled-1H2Jvj colorBrand-2M3O3N sizeLarge-2xP3-w fullWidth-3M-YBR grow-2T4nbg"]')))
    driver.find_element(By.XPATH,'//input[@class="inputDefault-Ciwd-S input-3O04eu inputField-2RZxdl"]').send_keys(log_in[0])
    driver.find_element(By.XPATH,'//input[@class="inputDefault-Ciwd-S input-3O04eu"]').click()
    time.sleep(2)
    driver.find_element(By.XPATH,'//input[@class="inputDefault-Ciwd-S input-3O04eu"]').send_keys(log_in[1])
    driver.find_element(By.XPATH,'//button[@class="marginBottom8-emkd0_ button-1cRKG6 button-ejjZWC lookFilled-1H2Jvj colorBrand-2M3O3N sizeLarge-2xP3-w fullWidth-3M-YBR grow-2T4nbg"]').click()
    time.sleep(5)


def reply_message_generate(n):
    if n:
        a = random.randint(0,3)
        message = 'Hello! '+mode[list(mode.keys())[a]] + '\n--:heart: from autoscript'
        return message

    else:
        message = 'SP: This message comes from an autoscript, plz ignore it lol'
        return message


def reply_in_discord(your_name):
    while True:
        # # scroll to one channel when someone @/reply you or including you
        # button = WebDriverWait(driver=driver,timeout=10000,poll_frequency=3).until(EC.presence_of_element_located((By.XPATH,'//div[@class="bar-wDIGjg mentionsBar-DpLHCy"]')))
        # button.click()
        
        # when you are mentioned in multiple locations
        print('listening:')
        # locate one guild mention in <div>  each iteration
        # only need the first element because guild visit from top to bottom
        element = WebDriverWait(driver=driver,timeout=10000,poll_frequency=3).until(EC.presence_of_element_located((By.XPATH,'//div[contains(@aria-label,"提及")]')))
        # redirect to guild
        # redirect needs relocate element
        guild_id = locate_in_guild_or_channel('guilds',element=element)
        # locate all channel mentioned in <a>
        # reply in each channel
        Flag = True
        while Flag:
            # guild_id ensure not to repeat in one guild
            element = driver.find_element(By.XPATH,'//div[contains(@data-list-item-id,"%s")]' %guild_id)
            if '提及' in element.get_attribute('aria-label'):
                Flag = True
            else:
                Flag = False
            # in case can't locate channel at bottom
            try:
                # locate one each time in iteration
                channel_element = driver.find_element(By.XPATH,'//a[contains(@aria-label,"提及")]')
                locate_in_guild_or_channel('channels',element=channel_element)


                # locate all reply message        
                for each in driver.find_elements(By.XPATH,'//div[contains(@class,"hasReply")]'):
                    replyto_name = get_replyto_name('reply',your_name,each)
                    message = reply_message_generate(1)
                    reply(replyto_name=replyto_name,message=message)
            
                # when someone @you or @group including you
                for each in driver.find_elements(By.XPATH, '//div[contains(@class,"mentioned-Tre-dv")]'):
                    receive_text = each.find_element(By.XPATH,'./div[1]/div').text
                    # only @? no reply
                    if len(receive_text):
                        answer = get_gpt_reply(api_key=key,query=receive_text)
                        replyto_name = get_replyto_name('@',your_name,element=each)
                        reply(replyto_name=replyto_name,message=answer)
                
                try:
                    # mark all as already read after reply
                    driver.find_element(By.XPATH,'//button[@class="barButtonAlt-TQoCdZ barButtonBase-Sk2mdB"]').click()
                    break
                except:
                    # quite loop for replying in one channel
                    break
            
            # if can't locate channel due to channel at bottom
            # scroll                    
            except:
                # click button to scroll
                driver.find_element(By.XPATH,'//div[@class="bar-wDIGjg mentionsBar-DpLHCy"]').click()
                time.sleep(2)
                # # scroll_element = document.getElementByClassName("scroller-1ox3I2 thin-RnSY0a scrollerBase-1Pkza4 fade-27X6bG customTheme-3QAYZq")
                # jscode = "document.getElementsByClassName('scroller-1ox3I2 thin-RnSY0a scrollerBase-1Pkza4 fade-27X6bG customTheme-3QAYZq')[0].scrollBy(0,200)"
                # driver.execute_script(jscode)


def locate_in_guild_or_channel(n,element):
    if n == 'guilds':
        # find guild_url
        guild_id = element.get_attribute("data-list-item-id")[12:]
        guild_name = element.get_attribute('aria-label')
        print('mentioned at %s, navigating to it, please wait' %guild_name)
        # driver.current_url may be different
        # guild_url = 'https://discord.com/channels/' + guild_id
        # driver.get(url=guild_url)
        element.click()
        time.sleep(random.randrange(5,10))
        return guild_id
    
    elif n == 'channels':
        # find channel_url
        channel_id = element.get_attribute('data-list-item-id')[11:]
        # guild_url + channel_id
        index = driver.current_url.rfind('/')
        channel_url = driver.current_url[:index] + '/' + channel_id
        print(channel_url)
        channel_name = element.get_attribute('aria-label')
        driver.get(url=channel_url)
        print('Navigating to channel %s, please wait' %channel_name)
        time.sleep(random.randrange(5,10))
        return channel_id
        # else:
        #     scroll_element = document.getElementByClassName("scroller-1ox3I2 thin-RnSY0a scrollerBase-1Pkza4 fade-27X6bG customTheme-3QAYZq")
        #     jscode = scroll_element.scrollIntoView()
        #     driver.execute_script(jscode,element)



def get_your_name_in_guild():
    print(1)


def get_replyto_name(n,your_name,element):
    # for replyto_you
    if n=='reply':
        # str of 'one name 正在回复 another name'
        label_string = element.find_element(By.XPATH,'./div').get_attribute('aria-label')
        # find messages that others reply to you
        if label_string.endswith(your_name):
            replyto_name = label_string[:label_string.index('正')]
            replyto_name = '@'+replyto_name.replace(' ','')
            return replyto_name
    # for @you
    elif n == '@':
        # reponse only to @you message
        replyto_name = ''
        flag = True
        if your_name in element.find_element(By.XPATH,'./div/div/span').text:
            # when multiple lines of message received
            while flag:
                try:
                    element.find_element(By.XPATH,'./div[1]/h3/span/span')
                    flag = False
                except:
                    # search upward
                    element = element.find_element(By.XPATH,'./../preceding-sibling::li[1]/div')
                    flag = True
            replyto_name = element.find_element(By.XPATH,'./div[1]/h3/span/span').text
            replyto_name = '@'+replyto_name.replace(' ','')
            return replyto_name   

'''
    sleep_time: sleep for each reply
'''
def reply(replyto_name,message,sleep=True):
    # had to do in 4 steps otherwise cannot @someone successfully
    # not None 
    if replyto_name and message:
        driver.find_element(By.XPATH,'//span[@class="emptyText-1o0WH_"]').send_keys(replyto_name)
        driver.find_element(By.XPATH,'//span[@data-slate-string="true"]').send_keys(Keys.TAB)
        driver.find_element(By.XPATH,'//span[@data-slate-string="true"]').send_keys(message)
        driver.find_element(By.XPATH,'//span[@data-slate-string="true"]').send_keys(Keys.ENTER)
        if sleep:
            # frequency control
            sleep_time = len(message)//20+1
            time.sleep(sleep_time)    



if __name__ == '__main__':
    # your account and password here
    log_in=['account','password']
    # or read in txt
    if log_in[0] == 'account':
        with open ('./auto_bot_discord/discord_account.txt','r') as f:
            log_in[0] = f.readline().strip('\n')
            log_in[1] = f.readline().strip('\n')
    # your name in one server
    your_name = 'Pony The Great'

    # change url_list if blocked, provide 3 in case, can add more
    url_list = ['https://discord.com/app','https://discord.com/login','https://discord.com/channels/@me']

    log_in_discord(url=url_list[2],log_in=log_in)
    reply_in_discord(your_name=your_name)
