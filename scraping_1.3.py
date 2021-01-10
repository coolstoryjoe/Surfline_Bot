from bs4 import BeautifulSoup as soup 
from urllib.request import urlopen as uReq 
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# sheet_convert = {
#     'BS':['BALANCE','Balance Sheet','SHEETS','Fina'],
#     'IS':['Earn','Inco','Oper','OPER','INCOME','COMP','Comp'],
#     'CF':['Cash','CASH'],
#     'GI':['Entity','Cover','Registrant','REGISTRANT','entity','registrant','Document','ENTITY'],
#     }   

# IS_line_item_convert = {
#     'Sales':['Net sales', 'Net Sales', 'Total revenues','Revenues', 'REVENUE', 'Net revenues', 
#     'Revenue', 'Total net sales', 'Total revenues', 'Net Revenue', 'Revenue, net','Net revenues before provision for doubtful accounts', 
#     'Revenues, Net', 'Revenues:', 'Net Revenues', 'REVENUES', 'Revenue:', 'REVENUE:',  'Sales', 
#     'Net revenues:', 'REVENUES:', 'Revenues, net', 'NET SALES',   'Net sales and revenue', 'Net Revenue:', 
#     'Sales and service revenues',   'REVENUES AND OTHER INCOME', 'Revenue from operations', 'Net revenue','Total operating revenues']
#     }

# line_item_convert = {
#     'NR':['sales','Sales','Revenues','REVENUE', 
#              'revenues','Revenue','Revenues','Total net sales',
#              'Total revenue','Total revenues','Operating revenues',
#              'Revenues, Net','Revenues:', 'Revenue', 'Net sales', 'OPERATING REVENUE', 'Net Revenues'],
    
#     'COGS':['Cost of sales','Cost of Goods and Services Sold',
#                           'Cost of products sold','Cost of Goods and Services Sold'],
    
#     'SG&A':['administrative','Selling','general','selling', 'General', 'Adminstrative','GENERAL'],
    
#     'NI':['Net Income','Net income','Net Earnings',
#                  'Net earnings','income','NET INCOME',
#                  'NET EARNINGS','earnings'],

#     'D&A':['depreciation','amortization','Depreciation','Amortization'],
#      }
# IS_Conversion = {
#     'NR': ['Sales', 'Total operating revenues', 'Total operating revenues', 'Total operating revenues', 
#     'Total operating revenues', 'Total operating revenues', 'Total operating revenues', 'Total operating revenues'], 
#     'COGS': [], 
#     'SG&A': ['Selling expenses', 'Selling expenses'], 
#     'NI': [ 'Net income', 'Net income'], 
#     'D&A': ['Depreciation and amortization', 'Depreciation and amortization']}


page_url1 = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK="
page_url2 = "&type=10-k&dateb=&owner=exclude&count=10"
sec_url = "https://www.sec.gov/"
wiki_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

def parse(url):
    uClient = uReq(url)
    url_soup = soup(uClient.read(), "html.parser")
    uClient.close()
    return(url_soup)


def pull_tickers(a,b):
    wiki_soup = parse(wiki_url)
    cik_containers = wiki_soup.find_all('tr')
    cik_list = []
    company_name = []
    ticker = []
    sector = []
    info_dict = {}
    for i in range(a,b):
        cik = cik_containers[i+1].select('td')[7].string.rstrip()
        cik_list.append(cik)
        try:
            company_name = (cik_containers[i+1].select('td')[1].string.rstrip())
            ticker = cik_containers[i+1].select('td')[0].select('a')[0]['href']
            sector = (cik_containers[i+1].select('td')[3].string.rstrip())
            info_dict[cik]  = [company_name, ticker, sector]
        except:
            pass
    return(info_dict)

def pull_NYSE_quotes(url):
    #url = 'https://www.nyse.com/quote/XNYS:ABT'
    chrome_driver_path = '/Users/josepholeynik/Python_Practice/Selenium_Demo/chromedriver'
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    webdriverC = webdriver.Chrome(
        executable_path = chrome_driver_path,
        options = chrome_options
        )
    
    with webdriverC as driver:
        wait = WebDriverWait(driver, 10)
        driver.get(url)   
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,'d-dquote-x3')))   
        #results = driver.find_element_by_class_name('d-dquote-x3').text
        quotesoup = soup(driver.page_source, features="lxml")
        driver.close()
    
    redsoup = float(quotesoup.find('span',{'class':'d-dquote-x3'}).text)
    #counnt= (quotesoup.find_all('div',{'class':"landing-section"}))
    return(redsoup)
    # import requests

def pull_NASDAQ_quotes(url):
    #url = 'https://www.nyse.com/quote/XNYS:ABT'
    chrome_driver_path = '/Users/josepholeynik/Python_Practice/Selenium_Demo/chromedriver'
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'    
    chrome_options.add_argument('user-agent={0}'.format(user_agent))
    
    webdriverC = webdriver.Chrome(
        executable_path = chrome_driver_path,
        options = chrome_options
        )
    
    with webdriverC as driver:
        wait = WebDriverWait(driver, 30)
        driver.implicitly_wait(10)
        driver.get(url)   
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,'symbol-page-header__left')))   
        #results = driver.find_element_by_class_name('d-dquote-x3').text
        quotesoup = soup(driver.page_source, features="lxml")
        driver.close()
    #redsoup = float(quotesoup.find('span',{'class':'symbol-page-header__pricing-price'}).text.strip('$'))
    #counnt= (quotesoup.find_all('div',{'class':"landing-section"}))
    red = float((quotesoup.find_all('span',{'class':'symbol-page-header__pricing-price'})[0].text).replace('$',''))
    return(red)

def pull_quotes(list_of_url):
    quote_dict = {}
    for url in list_of_url:
        quote = 0 
        try:
            quote = pull_NYSE_quotes(url)
        except:
            quote = pull_NASDAQ_quotes(url)
        else:
            pass #add CBOE ticker
        quote_dict[url] = quote
        print(url, quote)
    return(quote_dict)

url_list = []


red = pull_tickers(0,10)
for key, item in red.items():
    url_list.append(item[1])

    
for url in red.values():
    url_list.append(url[1])
    print(url_list)
    
Current_Price = pd.DataFrame.from_dict(pull_quotes(url_list))
print(Current_Price)

def sheet_exporting(export_name_dict,xls_doc):
    export_dict = {}
    sheet_names = (xls_doc.sheet_names)
    for y in export_name_dict.keys():
        for name in sheet_names:
            for z in export_name_dict[y]:
                if z in str(name):
                    sheet_ind = sheet_names[sheet_names.index(name)]
                    export_dict[y] = xls_doc.parse(sheet_ind,index_col = 0)
                    break
            else:
                continue
            break
    return export_dict


def scrape_docs(cik_list):
    docs = {}
    for cik in cik_list:
        page_soup = parse(page_url1 + cik + page_url2)
        containers = page_soup.find(id = 'interactiveDataBtn')
        try:
            xls_soup = parse(sec_url + containers.get('href'))
            xls_link = sec_url + xls_soup.select('td > a')[1].get('href')
            xls = pd.ExcelFile(xls_link)
            docs[cik] = sheet_exporting(sheet_convert,xls)
        except:
            pass
    return docs

def changing_line_items(replacement_dict,dict_of_dict_of_statements):
    for MasterKey, dict_of_statements in dict_of_dict_of_statements.items():
        for SetKey in dict_of_statements.keys():
            finance_doc = dict_of_statements[SetKey]
            i=0
            new_index = list(finance_doc.index)
            old_index = list(finance_doc.index)
            for y in replacement_dict.keys():
                for item in old_index:
                    for z in replacement_dict[y]:
                        if z == str(item):
                            new_index[old_index.index(item)] = y
                            finance_doc.index = new_index
                            break
                    else:
                        continue
                    break
                i += 1
            dict_of_statements[SetKey] = finance_doc
        dict_of_dict_of_statements[MasterKey] = dict_of_statements
    return dict_of_dict_of_statements

def remove_nonpulled_docs(Bible):
    removal_list = []
    for key , value in Bible.items():
        if len(value.keys()) == 4:
            pass
        else:
            removal_list.append(key)
    for ticker in removal_list:
        Bible.pop(ticker)
    return Bible

def delete_blanks(dict_of_dict_of_pandas):
    for MasterKey , value in dict_of_dict_of_pandas.items():
        for subkey, FS in value.items():
            for col in FS.columns:
                cols = FS[col]
                percent_blank = (pd.isna(cols).sum()/len(cols))
                if percent_blank > .8:
                    FS = FS.drop(columns = col)
            FS = FS.dropna(thresh=2)
            value[subkey] = FS
        dict_of_dict_of_pandas[MasterKey] = value
    return(dict_of_dict_of_pandas)

def finding_IS_line_items(replacement_dict,dict_of_dict_of_statements):
    possible_keywords = {}
    for key, dicts in dict_of_dict_of_statements.items():
        finance_doc = dicts['IS']
        index = list(finance_doc.index)
        for y in replacement_dict.keys():
            for item in index:
                for z in replacement_dict[y]:
                    if z in str(item):
                        #print(z, item, y)
                        if y in possible_keywords: 
                            possible_keywords[y].append(str(item))
                        else:
                            possible_keywords[y] = [str(item)]
                        break
                    else:
                        continue
                    break    
    return possible_keywords

def sales_export(dict_of_dict_pandas):
    export_dict = {}
    for key, doc in dict_of_dict_pandas.items():
        for subkey, subdoc in doc.items():
            if subkey == 'IS':
                target = doc[subkey]
                try:
                    Sales_number = (target.at['Sales',target.columns[0]])
                    print('wassup')
                    #if type(Sales) == float or type(Sales) == int:
                    #elif:
                    export_dict[key] = Sales_number
                except:
                    pass
    return 


#fin_doc = scrape_docs(pull_tickers(10,30))
#fin_doc = changing_line_items(IS_line_item_convert,delete_blanks(remove_nonpulled_docs(fin_doc)))

#items_list = finding_IS_line_items(line_item_convert, fin_doc)

#print(items_list)

# for doc in docs.values():
#     possible_kwargs.append(finding_IS_line_items(find_line_items,doc))
#     flat_list = list(dict.fromkeys([item for sublist in possible_kwargs for item in sublist]))
# Sales.append(flat_list)

# new_list = []
# for item in Sales:
#     if type(item) == str:
#         new_list.append(item)
#     else:
#         for ite in item:
#             new_list.append(ite)
# flat_sales = list(dict.fromkeys(new_list))

# #change line items to based on new conversion method
# for key, doc in docs.items():
#     doc2 = changing_line_items(IS_line_item_convert,doc)
#     docs[key] = doc2 

# #create dataframe of CIK as column and Sales as first row 

# old_testemant = {}
# for key, doc in docs.items():
#     for DOC in doc.keys():
#         if DOC == 'IS':
#             fin = doc[DOC]
#             try:
#                 Sales = (fin.at['Sales',doc3.columns[0]])
#                 if type(Sales) == float or type(Sales) == int:
#                     if math.isnan(Sales):
#                         pass
#                     else:
#                         old_testemant[key] = Sales
#             except:
#                 pass
            
# for documents in new_testament.values():
#     possible_kwargs = finding_IS_line_items(find_line_items,doc)

# def save_bible(testemant_dict):
#     bible = pd.DataFrame(testemant_dict,index=['Sales'])
#     engine = create_engine('sqlite:////Users/josepholeynik/Python_Practice/torah.db', echo=False)
#     bible.to_sql('users', con=engine)
#     return

# def edit_bible(testemant_dict):
#     #bible = pd.DataFrame(testemant_dict,index=['Sales'])
#     #engine = create_engine('sqlite:////Users/josepholeynik/Python_Practice/torah.db', echo=False)
#     #bible.to_sql('users', con=engine)
#     return
    
# def open_bible():    
#     king_james_version = pd.read_sql_table('users',engine,index_col='index')
#     return king_james_version










