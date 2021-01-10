import praw

reddit = praw.Reddit(
	    client_id="TrnQ-yW8RK-RwQ",
	    client_secret="Y7czDtO3_c-6JrvmuztJkDAbSPWpVw",
	    user_agent="BOYZenberry1 (by u/BOYZenberry1)",
	    username="BOYZenberry1",
	    password="JFK was assinantied")

sub_id3 = 'jrtgyl'

def split_and_stack(example):
	y = []
	x = example.lower().split()
	y.append(x)
	return y[0]

# words in common between two lists 
def words_in_common(list1, list2):
	counter = 0
	for item in list1: 
		if item in list2:
			counter += 1
	return counter

# check each authors words against all other authors words 
def best_friend_finder(phrase_lists):
	master_dict = {}
	for author, words in phrase_lists.items(): 
		d = {}
		for sub_author, sub_words in phrase_lists.items():
			if author == sub_author:
				continue
			d[sub_author] = words_in_common(words,sub_words)
		master_dict[author, max(d, key = d.get)] = d[max(d, key = d.get)]
	best_friends = max(master_dict, key = master_dict.get)
	return best_friends

# create dictionary of Author: ['word1','word2', etc]
def create_dict_of_authors(submission_ID):
	phrase_lists = {}
	submission = reddit.submission(id=submission_ID)
	submission.comments.replace_more(limit=0)
	all_comments = submission.comments.list()
	for item in all_comments:
		phrase_lists[str(item.author)] = split_and_stack(item.body)
	bffs = best_friend_finder(phrase_lists)
	for item in all_comments:
		if str(item.author) == bffs[0]:
			reply_text = '/u/' +bffs[0] + ' you should be friends with /u/' + bffs[1] 
			item.reply(reply_text)
			print(reply_text)
		if str(item.author) == bffs[1]:
			reply_text = '/u/' +bffs[1] + ' you should be friends with /u/' + bffs[0] 
			print(reply_text)
			item.reply(reply_text)
	return 

create_dict_of_authors(sub_id3)

