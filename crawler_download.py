import requests
from bs4 import BeautifulSoup
import csv
import re
import urllib.request
from multiprocessing import Pool
from datetime import datetime

def get_html(url):
    r = requests.get(url)
    return r.text


def get_all_links(html):
    soup = BeautifulSoup(html, 'lxml')
    divs = soup.find('div', id="catalog_category").find_all('div', class_='col-md-3 col-xs-6')
    links = []
    for div in divs:
        a = div.find('a').get('href')
        link = 'http://..' + a
        links.append(link)
    return links

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
#    Наименование товара
    try:
        name = soup.find('h1').text.strip()
        name = name + ''
    except:
        name = ''  
#    Артикул товара
    try:
#       article = soup.find('div', class_='clearfix hidden-xs hidden-sm').find('p').text.strip()
        art_1 = soup.find('div', class_='clearfix hidden-xs hidden-sm').find('p').text.strip()
        length_1 = len(art_1)	# Длина строки
        index_1 = art_1.find(" ",0,length_1)	#Поиск подстроки в строке. Возвращает номер первого вхождения или -1
        length_1 = int(length_1)
        index_1 = int(index_1)+1
#        print('length_1 = ',length_1)
#        print('index_1 = ',index_1)
        index_2 = length_1 - index_1
        index_2 = int(index_2)
#        print('index_2 = ',index_2)
        split_1 = art_1[index_1:]
        article = split_1 + ''
    except:
        article = ''
#    Категория
    try:
#        category = soup.find('a', href = url_2).text.strip()
#        print(category)
        category ='Средства защиты ...'
    except:
        category = 'Средства защиты ...'        
#    Розничная цена товара  
    try:
        price = soup.find('div', class_='primary-color').find('span').text.strip()
#        print('price = ', price)
        price.replace(" ", "")
        pr_1 = float(price)
        pr_2 = pr_1 * 0.18
        pr_3 = pr_1 + pr_2
        price = int(pr_3)
        price = str(price) + ''
#        print('Новая цена = ', price)
    except:
        price = ''
#    Оптовая цена товара    
    try:
        sale_price = soup.find('div', class_='price-opt').find('span').text.strip()
        sale_price.replace(" ", "")
        spr_1 = float(sale_price)
        spr_2 = spr_1 * 0.18
        spr_3 = spr_1 + spr_2
        sale_price = int(spr_3)
        sale_price = str(sale_price) + ''
#        print('Новая цена = ', sale_price)
    except:
        sale_price = '' 
#    Описание товара    
    try:
        description = soup.find('div', class_='product_description').text.strip()
        description = description + ''
    except:
        description = ''
    # Характеристика товара
    # Вид изделия
    try:
        vid_prod_value = soup.find('span', class_='osmb', text=re.compile('Вид изделия:')).next_element.next_element.next_element.next_element
        vid_prod_value = vid_prod_value.replace("\t", "")
        vid_prod_value = vid_prod_value.replace("\n", "")
        vid_prod_value = vid_prod_value + ''
#        vid_prod_value = 'Вид изделия: ' + vid_prod_value
    except:
        vid_prod_value = ''
   # Упаковка
    try:
        vid_prod_pack = soup.find('span', class_='osmb', text=re.compile('Упаковка:')).next_element.next_element.next_element.next_element
        vid_prod_pack = vid_prod_pack.replace("\t", "")
        vid_prod_pack = vid_prod_pack.replace("\n", "")
        vid_prod_pack = vid_prod_pack + ''
#        vid_prod_pack = 'Упаковка: ' + vid_prod_pack
    except:
        vid_prod_pack = ''
   # Пол
    try:
        vid_prod_gender = soup.find('span', class_='osmb', text=re.compile('Пол:')).next_element.next_element.next_element.next_element
        vid_prod_gender = vid_prod_gender.replace("\t", "")
        vid_prod_gender = vid_prod_gender.replace("\n", "")
        vid_prod_gender = vid_prod_gender + ''
#        vid_prod_gender = 'Пол: ' + vid_prod_gender
    except:
        vid_prod_gender = ''
   # Состав
    try:
        vid_prod_composition = soup.find('span', class_='osmb', text=re.compile('Состав:')).next_element.next_element.next_element.next_element
        vid_prod_composition = vid_prod_composition.replace("\t", "")
        vid_prod_composition = vid_prod_composition.replace("\n", "")
#        vid_prod_composition = 'Состав: ' + vid_prod_composition
        vid_prod_composition = vid_prod_composition + ''
    except:
        vid_prod_composition = '' 
   # Ткань/Материал верха
    try:
        vid_prod_upper_material = soup.find('span', class_='osmb', text=re.compile('Ткань/Материал верха:')).next_element.next_element.next_element.next_element
        vid_prod_upper_material = vid_prod_upper_material.replace("\t", "")
        vid_prod_upper_material = vid_prod_upper_material.replace("\n", "")
#        vid_prod_upper_material = 'Ткань/Материал верха: ' + vid_prod_upper_material
        vid_prod_upper_material = vid_prod_upper_material +''
    except:
        vid_prod_upper_material = ''
   # Сезон
    try:
        vid_prod_season = soup.find('span', class_='osmb', text=re.compile('Сезон:')).next_element.next_element.next_element.next_element
        vid_prod_season = vid_prod_season.replace("\t", "")
        vid_prod_season = vid_prod_season.replace("\n", "")
        vid_prod_season = vid_prod_season + ''
#        vid_prod_season = 'Сезон: ' + vid_prod_season
    except:
        vid_prod_season = ''    
   # Плотность/Толщина материала
    try:
        vid_prod_thickness_material = soup.find('span', class_='osmb', text=re.compile('Плотность/Толщина материала:')).next_element.next_element.next_element.next_element
        vid_prod_thickness_material = vid_prod_thickness_material.replace("\t", "")
        vid_prod_thickness_material = vid_prod_thickness_material.replace("\n", "")
        vid_prod_thickness_material = vid_prod_thickness_material + ''
#        vid_prod_thickness_material = 'Плотность/Толщина материала: ' + vid_prod_thickness_material
    except:
        vid_prod_thickness_material = '' 
   # Защита
    try:
        vid_prod_protection = soup.find('span', class_='osmb', text=re.compile('Защита:')).next_element.next_element.next_element.next_element
        vid_prod_protection = vid_prod_protection.replace("\t", "")
        vid_prod_protection = vid_prod_protection.replace("\n", "")
        vid_prod_protection = vid_prod_protection + ''
#        vid_prod_protection = 'Защита: ' + vid_prod_protection
    except:
        vid_prod_protection = ''
    # Цвет
    try:
        vid_prod_colour = soup.find('span', class_='osmb', text=re.compile('Цвет:')).next_element.next_element.next_element.next_element
        vid_prod_colour = vid_prod_colour.replace("\t", "")
        vid_prod_colour = vid_prod_colour.replace("\n", "")
        vid_prod_colour = vid_prod_colour + ''
#        vid_prod_colour = 'Цвет: ' + vid_prod_colour
    except:
        vid_prod_colour = ''     
   # Комплектность
    try:
        vid_prod_completeness = soup.find('span', class_='osmb', text=re.compile('Комплектность:')).next_element.next_element.next_element.next_element
        vid_prod_completeness = vid_prod_completeness.replace("\t", "")
        vid_prod_completeness = vid_prod_completeness.replace("\n", "")
        vid_prod_completeness =vid_prod_completeness + ''
#        vid_prod_completeness = 'Комплектность: ' + vid_prod_completeness
    except:
        vid_prod_completeness = '' 
   # Размерный ряд
    try:
        vid_prod_size_range = soup.find('span', class_='osmb', text=re.compile('Размерный ряд:')).next_element.next_element.next_element.next_element
        vid_prod_size_range = vid_prod_size_range.replace("\t", "")
        vid_prod_size_range = vid_prod_size_range.replace("\n", "")
        vid_prod_size_range = vid_prod_size_range + ''
#        vid_prod_size_range = 'Размерный ряд: ' + vid_prod_size_range
    except:
        vid_prod_size_range = '' 
   # Ростовка
    try:
        vid_prod_size = soup.find('span', class_='osmb', text=re.compile('Ростовка:')).next_element.next_element.next_element.next_element
        vid_prod_size = vid_prod_size.replace("\t", "")
        vid_prod_size = vid_prod_size.replace("\n", "")
        vid_prod_size = vid_prod_size +''
#        vid_prod_size = 'Ростовка: ' + vid_prod_size
    except:
        vid_prod_size = ''  
   # Световозвращающий материа
    try:
        vid_prod_retroreflective_material = soup.find('span', class_='osmb', text=re.compile('Световозвращающий материа:')).next_element.next_element.next_element.next_element
        vid_prod_retroreflective_material = vid_prod_retroreflective_material.replace("\t", "")
        vid_prod_retroreflective_material = vid_prod_retroreflective_material.replace("\n", "")
        vid_prod_retroreflective_material = vid_prod_retroreflective_material + ''
#        vid_prod_retroreflective_material = 'Световозвращающий материа: ' + vid_prod_retroreflective_material
    except:
        vid_prod_retroreflective_material = ''     
   # Утеплитель
    try:
        vid_prod_heater = soup.find('span', class_='osmb', text=re.compile('Утеплитель:')).next_element.next_element.next_element.next_element
        vid_prod_heater = vid_prod_heater.replace("\t", "")
        vid_prod_heater = vid_prod_heater.replace("\n", "")
        vid_prod_heater = vid_prod_heater + ''
#        vid_prod_heater = 'Утеплитель: ' + vid_prod_heater
    except:
        vid_prod_heater = '' 
   # Подкладка
    try:
        vid_prod_lining = soup.find('span', class_='osmb', text=re.compile('Подкладка:')).next_element.next_element.next_element.next_element
        vid_prod_lining = vid_prod_lining.replace("\t", "")
        vid_prod_lining = vid_prod_lining.replace("\n", "")
        vid_prod_lining = vid_prod_lining + ''
#        vid_prod_lining = 'Подкладка: ' + vid_prod_lining
    except:
        vid_prod_lining = ''        
   # Пакет утеплителя
    try:
        vid_prod_insulation_package = soup.find('span', class_='osmb', text=re.compile('Пакет утеплителя:')).next_element.next_element.next_element.next_element
        vid_prod_insulation_package = vid_prod_insulation_package.replace("\t", "")
        vid_prod_insulation_package = vid_prod_insulation_package.replace("\n", "")
        vid_prod_insulation_package = vid_prod_insulation_package + ''
#        vid_prod_insulation_package = 'Пакет утеплителя: ' + vid_prod_insulation_package
    except:
        vid_prod_insulation_package = ''     
   # Объем
    try:
        vid_prod_volume = soup.find('span', class_='osmb', text=re.compile('Объем:')).next_element.next_element.next_element.next_element
        vid_prod_volume = vid_prod_volume.replace("\t", "")
        vid_prod_volume = vid_prod_volume.replace("\n", "")
        vid_prod_volume = vid_prod_volume +''
#        vid_prod_volume = 'Объем: ' + vid_prod_volume
    except:
        vid_prod_volume = ''         
   # Вес изделия
    try:
        vid_prod_product_weight = soup.find('span', class_='osmb', text=re.compile('Вес изделия:')).next_element.next_element.next_element.next_element
        vid_prod_product_weight = vid_prod_product_weight.replace("\t", "")
        vid_prod_product_weight = vid_prod_product_weight.replace("\n", "")
        vid_prod_product_weight = vid_prod_product_weight + ''
#        vid_prod_product_weight = 'Вес изделия: ' + vid_prod_product_weight
    except:
        vid_prod_product_weight = '' 
    # Изоражение товара
    try:
        art_1 = soup.find('div', class_='clearfix hidden-xs hidden-sm').find('p').text.strip()
        length_1 = len(art_1)	# Длина строки
        index_1 = art_1.find(" ",0,length_1)	#Поиск подстроки в строке. Возвращает номер первого вхождения или -1
        length_1 = int(length_1)
        index_1 = int(index_1)+1
#        print('length_1 = ',length_1)
#        print('index_1 = ',index_1)
        index_2 = length_1 - index_1
        index_2 = int(index_2)
#        print('index_2 = ',index_2)
        split_1 = art_1[index_1:]
#        print('split_1 = ', split_1)
        imgs = soup.find_all('a',attrs={"data-lightbox": "product"})
        dir_1 = '/Users/user/Desktop/shop/'
        links_1 = []
        i = 1
        for img in imgs:
#            print('art_1 = ',art_1)
            a = img.get('href')
            link_1 = 'http://...' + a
#            print ('link_1 = ', link_1)
#            print ('i = ', i)
#            print ('dir_1 = ', dir_1)
            photo_1 = dir_1 + split_1 + '(' + str(i) + ').jpg'
            i = i+1
#            print ('photo_1 = ', photo_1)
            urllib.request.urlretrieve(link_1, photo_1)
        return links
    except:
        imgs = ''
    # Пустые поля
    try:
        vendor = 'Группа ..."'
    except:    
        vendor = 'Группа ..."'
    try:
        supplier = ''
    except:    
        supplier = ''
    try:
        image = ''
    except:    
        image = ''    
    try:
        pre_order = ''
    except:    
        pre_order = ''
    try:
        code_1c = ''
    except:    
        code_1c = ''
    try:
        tags = ''
    except:    
        tags = '' 
    try:
        hidden = '0'
    except:    
        hidden = '0'
    try:
        kind_id = ''
    except:    
        kind_id = '' 
    try:
        is_kind = ''
    except:    
        is_kind = ''
    try:
        discounted = ''
    except:    
        discounted = ''
    try:
        note = ''
    except:    
        note = ''
    try:
        unit = ''
    except:    
        unit = ''
    try:
        weight_unit = 'kg'
    except:    
        weight_unit = 'kg'
    try:
        dimensions = ''
    except:    
        dimensions = ''
    try:
        new = '0'
    except:    
        new = '0'
    try:
        special = '0'
    except:    
        special = '0'
    try:
        yml = '1'
    except:    
        yml = '1'
    try:
        price_old = ''
    except:    
        price_old = ''
    try:
        price2 = ''
    except:    
        price2 = ''
    try:
        price3 = ''
    except:    
        price3 = ''
    try:
        currency = 'RUB'
    except:    
        currency = 'RUB'
    try:
        seo_noindex = ''
    except:    
        seo_noindex = ''
    try:
        sef_url = ''
    except:    
        sef_url = ''
    try:
        uuid = ''
    except:    
        uuid = ''
    try:
        uuid_mod = ''
    except:    
        uuid_mod = ''
    try:
        body_1 = ''
    except:    
        body_1 = ''       
        
        
        
        
    data = {'name':name, 
            'vendor':vendor,
            'supplier':supplier,
            'image':image,
            'pre_order':pre_order,
            'article':article,
            'code_1c':code_1c,
            'category':category,
            'tags':tags,
            'hidden':'0',
            'kind_id':kind_id,
            'is_kind':is_kind,
            'discounted':discounted,
            'note':note,
            'body_1':body_1,
            'description': description,
            'amount':'1000',
            'unit':unit,
            'vid_prod_product_weight':vid_prod_product_weight,
            'weight_unit':weight_unit,
            'dimensions':dimensions,
            'new':new,
            'special':special,
            'yml':yml,
            'price': price,
            'price_old':price_old,
            'price2':price2,
            'price3':price3,
            'currency':currency,
            'seo_noindex':seo_noindex,
            'name':name,
            'name':name,
            'name':name,
            'name':name,
            'sef_url':sef_url,
            'uuid':uuid,
            'uuid_mod':uuid_mod,
            'sale_price': sale_price,
            'vid_prod_value':vid_prod_value,
            'vid_prod_pack':vid_prod_pack,
            'vid_prod_gender':vid_prod_gender,
            'vid_prod_composition':vid_prod_composition,
            'vid_prod_upper_material':vid_prod_upper_material,
            'vid_prod_season':vid_prod_season,
            'vid_prod_thickness_material':vid_prod_thickness_material,
            'vid_prod_protection':vid_prod_protection,
            'vid_prod_colour':vid_prod_colour,
            'vid_prod_completeness':vid_prod_completeness,
            'vid_prod_size_range':vid_prod_size_range,
            'vid_prod_size':vid_prod_size,
            'vid_prod_retroreflective_material':vid_prod_retroreflective_material,
            'vid_prod_heater':vid_prod_heater,
            'vid_prod_lining':vid_prod_lining,
            'vid_prod_insulation_package':vid_prod_insulation_package,
            'vid_prod_volume':vid_prod_volume,
            'vid_prod_product_weight':vid_prod_product_weight
           }
    return data


def write_csv(data):
    with open('export.csv', 'a') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow((data['is_kind'],
                         data['kind_id'],
                         data['new'],
                         data['special'],
                         data['note'],
                         data['description'],
                         data['weight_unit'],
                         data['discounted'],
                         data['yml'],
                         data['name'],
                         data['vid_prod_product_weight'],
                         data['article'],
                         data['code_1c'],
                         data['amount'],
                         data['hidden'],
                         data['pre_order'],
                         data['price'],
                         data['price2'],
                         data['price3'],
                         data['price_old'],
                         data['currency'],
                         data['vendor'],
                         data['supplier'],
                         data['category'],
                         data['image'],
                         data['unit'],
                         data['sef_url'],
                         data['tags'],
                         data['dimensions'],
                         data['uuid'],
                         data['uuid_mod'],
                         data['name'],
                         data['name'],
                         data['name'],
                         data['name'],
                         data['seo_noindex'],
                         data['sale_price'],
                         data['vid_prod_value'],
                         data['vid_prod_pack'],
                         data['vid_prod_gender'],
                         data['vid_prod_composition'],
                         data['vid_prod_upper_material'],
                         data['vid_prod_season'],
                         data['vid_prod_thickness_material'],
                         data['vid_prod_protection'],
                         data['vid_prod_colour'],
                         data['vid_prod_completeness'],
                         data['vid_prod_size_range'],
                         data['vid_prod_size'],
                         data['vid_prod_retroreflective_material'],
                         data['vid_prod_heater'],
                         data['vid_prod_lining'],
                         data['vid_prod_insulation_package'],
                         data['vid_prod_volume'],
                         data['vid_prod_product_weight']
                         ))
        print(data['name'], '->Ok')   
        
        
def make_all(url):
    html = get_html(url)
    data = get_page_data(html)
    write_csv(data)
        

def main():
    start = datetime.now()
    url_1 = 'http://...'
    url_2 = '/katalog/specodezhda/rabochaya-letnyaya/'
    url = url_1+url_2
    all_links = get_all_links(get_html(url))
    with Pool(40) as p:
        p.map(make_all,all_links)
    end = datetime.now()
    total = end - start
    print(str(total))


if __name__ == '__main__':
     main()
