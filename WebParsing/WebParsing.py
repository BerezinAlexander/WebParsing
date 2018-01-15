import urllib.request
from bs4 import BeautifulSoup
import smtplib

DATE = '03.02.2018'
NIGHTS = '8'
PERSONS = 3

def get_html(url):
    print("> URL connecting...")
    response = urllib.request.urlopen(url)
    print("> URL connect")
    return response.read()

def parse(html):
    print("> Parsing...")
    soup = BeautifulSoup(html, "html.parser");

    table = soup.find('table', class_='b-pr_t')
    all_tr = table.find_all('tr')
    
    dict_hotels = {}
    cur_hotel_name = ""

    for tr in all_tr:
        
        tr_c_hl = tr.find_all('th', class_='c_hl')
        if tr_c_hl:
            cur_hotel_name = tr_c_hl[0].find_all('a')[0].text  

        room_name = ""
        room = tr.find_all('td', class_='c_ns c_ns__bb cgr')
        if room: 
            room_name = room[0].text
        else:
            room = tr.find_all('td', class_='c_ns c_ns__bb')
            if room: 
                room_name = room[0].text 

        price = ""
        int_price = 0
        pr = tr.find_all('div', class_='pe')
        if pr:
            price = pr[0].find_all('b', class_='r')[0].text   
            int_price = int(price)
            if int_price < 110000:
                price = price + " руб"
                if not cur_hotel_name in dict_hotels:
                    dict_hotels[cur_hotel_name] = [ [room_name, price] ]
                else:
                    dict_hotels[cur_hotel_name].append([room_name, price])

    print("> Parse complete")

    for hotel in dict_hotels:
        print()        
        print(hotel);
        for hl_room in dict_hotels[hotel]:
            print(hl_room[0], hl_room[1])

    sendMessage(formationMessage(dict_hotels))

def sendMessage(message):
    try:
        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpObj.starttls()
        print("> Connecting to bot-mail")
        smtpObj.login('bot.mail.mario@gmail.com','Qwerty963963')
        print("> Sending message...")
        smtpObj.sendmail("bot.mail.mario@gmail.com","elmario2pro@gmail.com", message.encode('utf-8'))
        print("> Message send")
        smtpObj.quit()
    except SMTPException:
        print("> Error: unable to send email")

def formationMessage(dict_hl):
    text = "Date = " + DATE + ", nights = " + NIGHTS + ", persons = " + str(PERSONS) + "\n"
    for hotel in dict_hl:
        text += "\n" + '%-50s' % hotel + "\n"        
        for hl_room in dict_hl[hotel]:
            text += '%-50s' % hl_room[0] + " " + '%-10s' % hl_room[1] + "\n"
    print(text)
    return text

def formationURL(date, nights, persons):
    url = "https://www.bgoperator.ru/price.shtml?action=price&tid=211&idt=&flt2=100510000863&id_price=121116106101"
    url += "&data=" + date + "&d2=" + date
    url += "&f7=" + str(nights)
    url += "&f3=" + "4*" + "&f3=" + "3*" 
    url += "&f8=" + "BB" 
    url += "&ho=0&f1=100520751057&ins=0-250000-RUR&flt=100410000050"
    code_pers = "0030119820"
    url += "&p=" + code_pers
    for count in range(persons-1):
        url += "." + "0030119820"
    print(url)
    return url

def main():
    #parse(get_html('http://weblanser.net/jobs/'))
    
    # one Shale
    #parse(get_html('https://www.bgoperator.ru/price.shtml?action=price&tid=211&idt=&flt2=100510000863&id_price=121116106101&data=03.02.2018&d2=03.02.2018&f7=8&f3=4*&f3=3*&f8=BB&ho=0&f1=100520751057&F4=102616319233&ins=0-250000-RUR&flt=100410000050&p=0030119820.0030119820.0030119820'))
    
    #parse(get_html('https://www.bgoperator.ru/price.shtml?action=price&tid=211&idt=&flt2=100510000863&id_price=121116106101&data=03.02.2018&d2=03.02.2018&f7=8&f3=4*&f3=3*&f8=BB&ho=0&f1=100520751057&ins=0-250000-RUR&flt=100410000050&p=0030119820.0030119820.0030119820'))

    parse(get_html(formationURL(DATE, NIGHTS, PERSONS)))

if __name__ == '__main__':
    main()