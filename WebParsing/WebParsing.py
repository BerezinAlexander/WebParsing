import urllib.request
from bs4 import BeautifulSoup

def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()

def parse(html):
    soup = BeautifulSoup(html, "html.parser");
    #print(soup.prettify())

    table = soup.find('table', class_='b-pr_t')
    all_tr = table.find_all('tr')
    
    dict_hotels = {}
    cur_hotel_name = ""

    for tr in all_tr:
        
        tr_c_hl = tr.find_all('th', class_='c_hl')
        if tr_c_hl:
            #print(tr_c_hl)
            #print(tr_c_hl[0].find_all('a')[0].text)
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
        pr = tr.find_all('div', class_='pe')
        if pr:
            price = pr[0].find_all('b', class_='r')[0].text   
            price = price + " руб"
            if not cur_hotel_name in dict_hotels:
                dict_hotels[cur_hotel_name] = [ [room_name, price] ]
            else:
                dict_hotels[cur_hotel_name].append([room_name, price])


        #if tr_c_hl != None:
        #    hl_a = tr_c_hl.find_all('a')
        #    hotels_name.append({
        #        'tittle': hl_a.text
        #    })

    for hotel in dict_hotels:
        print()        
        print(hotel);
        for hl_room in dict_hotels[hotel]:
            print(hl_room)

    #print(table)

    #table = soup.find('div', class_='b_pr')
    #print(table)

def main():
    #parse(get_html('http://weblanser.net/jobs/'))
    
    # one Shale
    #parse(get_html('https://www.bgoperator.ru/price.shtml?action=price&tid=211&idt=&flt2=100510000863&id_price=121116106101&data=03.02.2018&d2=03.02.2018&f7=8&f3=4*&f3=3*&f8=BB&ho=0&f1=100520751057&F4=102616319233&ins=0-250000-RUR&flt=100410000050&p=0030119820.0030119820.0030119820'))
    
    parse(get_html('https://www.bgoperator.ru/price.shtml?action=price&tid=211&idt=&flt2=100510000863&id_price=121116106101&data=03.02.2018&d2=03.02.2018&f7=8&f3=4*&f3=3*&f8=BB&ho=0&f1=100520751057&ins=0-250000-RUR&flt=100410000050&p=0030119820.0030119820.0030119820'))

if __name__ == '__main__':
    main()