import smtplib , ssl
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup 
import yagmail

urls = ['https://www.surfline.com/surf-report/county-line/5842041f4e65fad6a7708813',
		'https://www.surfline.com/surf-report/leo-carrillo/5842041f4e65fad6a770893f',
		'https://www.surfline.com/surf-report/county-line-overview/584204214e65fad6a7709cfc',
		'https://www.surfline.com/surf-report/zuma-beach/5afb6566bb6fd9001a250fbb',
		'https://www.surfline.com/surf-report/malibu-surfrider-beach/5a8cacffb0f634001ada08fb',
		'https://www.surfline.com/surf-report/lower-trestles/5842041f4e65fad6a770888a']

def pull_surf_condidtions():
	waves = []
	for url in urls: 
		req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
		Uclient = urlopen(req)
		soups = soup(Uclient.read(),'html.parser')
		Uclient.close()

		beach_name = soups.find_all('h1','sl-forecast-header__main__title')[0].text.replace('Surf Report & Forecast','')
		wave_size = soups.find_all("div", "quiver-spot-forecast-summary__stat-container quiver-spot-forecast-summary__stat-container--surf-height")[0].find_all('span','quiver-surf-height')[0].text
		conditions = soups.find_all('div','quiver-spot-report')[0].contents[0].text
		waves.append(beach_name + ': ' + wave_size + ' ' + conditions +'\n' )
	str1 = ' '
	wave_report = (str1.join(waves))
	return wave_report

def send_email(body):
	yag = yagmail.SMTP('xxxxx@gmail.com', 'xxxxx')

	yag.send(
		to = 'xxxxx@gmail.com',
		subject = 'Gnar Report',
		contents = body, 
		)

waves = send_email(pull_surf_condidtions())