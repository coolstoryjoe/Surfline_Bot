from urllib.request import urlopen as uReq 
from bs4 import BeautifulSoup as soup 
import pandas as pd

url = 'https://www.espn.com/college-football/schedule/_/week/10'

stub_url = 'https://www.espn.com/college-football/schedule/_/week/'

year_url = '/year/'

def extract_page(url2):
	Uclient = uReq(url2)
	sport_soup = soup(Uclient.read(),'html.parser')
	Uclient.close()
	return sport_soup

def score_parser(example_data):
	score_list = (example_data.split())
	if len(score_list) == 1:
		return
	winner = score_list[0]
	loser = score_list[2]
	winning_score = (score_list[1])
	losing_score = (score_list[3])
	return [winner, loser, winning_score, losing_score]

def extract_data(url2):
	sport_soup = extract_page(url2)

	#FIND THE TABLE WITHIN THE PAGE THAT HAS THE STATISTICS
	#print(sport_soup)
	sub_soup = sport_soup.find_all("table", "schedule has-team-logos align-left")

	winning_teams = []
	losing_teams = []

	#print((sub_soup[0].prettify()))
	for i in range(len(sub_soup)):
		print(sub_soup.prettify())
		even_sub_soup = sub_soup[i].find_all('tr','odd')
		odd_sub_soup = sub_soup[i].find_all('tr','even')
		for j in range(len(even_sub_soup)):
			even_score = even_sub_soup[j].find_all('td')[2].a.text
			game_obj = score_parser(even_score)
			if game_obj == None:
				continue
			winning_teams.append(game_obj[0])
			losing_teams.append(game_obj[1])
		for h in range(len(odd_sub_soup)):
			odd_score = odd_sub_soup[h].find_all('td')[2].a.text
			game_obj = score_parser(odd_score)
			if game_obj == None:
				continue
			winning_teams.append(game_obj[0])
			losing_teams.append(game_obj[1])
	result_obj = []
	for x in range(len(winning_teams)):
		result_obj.append(1)
	game_schedule = { 'winners': winning_teams, 'losers':losing_teams, 'result': result_obj}
	df = pd.DataFrame(game_schedule)

	all_teams = list(set(winning_teams + losing_teams))
	ranking_obj = []
	for x in range(len(all_teams)):
		ranking_obj.append(1500)

	team_ratings = { 'team_name' : all_teams , 'team_rating' : ranking_obj}
	df1 = pd.DataFrame(team_ratings)
	return [df1 , df]

def multi_year_pull():
	master_df = list_of_dfs[1]
	master_df1 = list_of_dfs[0]

	year = 2017
	for i in range(3):
		for j in range(0,16):
			if j == 1:
				b
			new_url = stub_url + str(j) + year_url + str(year)
			list_of_dfs = extract_data(new_url)
			df = list_of_dfs[1]
			df1 = list_of_dfs[0]
			master_df = master_df.append(df)
			master_df1 = master_df1.append(df1)

		#list_of_dfs = extract_data(first_url)
		#master_df = list_of_dfs[1]
			print(new_url)	
		year += 1

	master_df1.drop_duplicates(subset = ['team_name'], inplace = True)
	
	#print(len(master_df1))

	return [master_df , master_df1]

def multi_week_pull():
	first_url = stub_url + str(1)
	list_of_dfs = extract_data(first_url)
	master_df = list_of_dfs[1]
	master_df1 = list_of_dfs[0]

	for i in range(1,11):
		new_url = stub_url + str(i)
		list_of_dfs = extract_data(new_url)
		#print('....THIS BEGINS LIST OF DFS.....','\n', list_of_dfs)
		df = list_of_dfs[1]
		df1 = list_of_dfs[0]
		master_df = master_df.append(df)
		master_df1 = master_df1.append(df1)

	#print(master_df1.sort_values('team_name'))
	
	master_df1.drop_duplicates(subset = ['team_name'], inplace = True)
	
	#print(len(master_df1))

	return [master_df , master_df1]

#master_list = multi_week_pull()

master_list = multi_year_pull()
print(master_list)
# master_list[1].to_csv('team_ratings_v0.csv')

# master_list[0].to_csv('week_10_games_v0.csv')	
	

	
	# label_list = []
	# for label in sub2_soup:
	# 	label_list.append(label.text)

	# #FIND THE DATA TABLE 
	# stat_soup = sport_soup.find_all("table", "Table Table--align-right")

	# #FIND THE DATA ITEMS
	# stat2_soup = stat_soup[0].find_all('td','Table__TD')

	# stats_list =[]
	# for stat in stat2_soup:
	# 	stats_list.append(stat.text)

	# stats_dict = dict(zip(label_list, stats_list))

