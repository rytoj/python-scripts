import urllib.request
from bs4 import BeautifulSoup
import collections
import time
from subprocess import call
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%M-%d %a %H:%M:%S')
LOGGER = logging.getLogger(__name__)

CHECK_INTERVAL = 10  # seconds


def make_soup(url):
	req = urllib.request.Request(
		url,
		data=None,
		headers={
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
		}
	)
	f = urllib.request.urlopen(req)
	soupdata = BeautifulSoup(f, "html.parser")
	return soupdata


def get_comments(*boards):
	temos_ir_postai = collections.OrderedDict()
	postai = []

	for board in boards:
		soup_ = make_soup("http://370chan.lt/" + board)

		for tema in soup_.find_all("div", {"class": "thread"}):
			thread_id = tema.get('id').split("_")[1]
			LOGGER.debug("Tema: {}".format(thread_id))
			for reply_index, reply in enumerate(tema.find_all("div", {"class": "post reply"})):
				reply_id = reply.get('id').split("_")[1]
				if not temos_ir_postai.get(board):
					temos_ir_postai[board] = collections.OrderedDict()
				for author in reply.find_all("span", {"class": "name"}):
					LOGGER.debug(author.get_text())
				for comment in reply.find_all("div", {"class": "body"}):
					LOGGER.debug(comment.get_text())
				postai.append([collections.OrderedDict(
					{"comment": comment.get_text(), "author": author.get_text(), "reply_id": reply_id})])
				temos_ir_postai[board][thread_id] = postai
			postai = []  # Clear list after putting in dict
	return temos_ir_postai


# TODO: parse 200258išlįsk iš akvariumo, board: b
# TODO: factor to method
# TODO: cross platform
base_commits = get_comments("b", "v", "a")
while True:
	time.sleep(CHECK_INTERVAL)
	new_commits = get_comments("b", "v", "a")

	for boards in base_commits:
		LOGGER.info("Checking boards: " + boards)
	if base_commits != new_commits:
		for board_name, board_id in new_commits.items():
			if new_commits[board_name] != base_commits[board_name]:
				# Get latest commit
				for board_id_, comments in new_commits[board_name].items():
					name = comments[-1][0]["author"]
					description = comments[-1][0]["comment"]
					reply_id = comments[-1][0]["reply_id"]
					LOGGER.info(
						"No now content detected\n No: %s on /%s/\n name: %s \n description: %s" % (
							reply_id, board_name,  name, description))
					call(
						["/usr/bin/notify-send", "{}, on /{}/".format(name, board_name), description])
					base_commits = get_comments("b", "v", "a")
					break

	else:
		LOGGER.info("No commit changes detected.")
