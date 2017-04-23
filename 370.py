# -- coding: utf-8 --

import urllib.request
from bs4 import BeautifulSoup
import collections
import time
from subprocess import call
import logging
import re

# Reikalavimai
# python 3.6
# pip install BeautifulSoup4

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


def get_comments(boards):
	temos_ir_postai = collections.OrderedDict()
	postai = []

	for board in boards:
		board = str(board)
		soup_ = make_soup("http://370chan.lt/" + board)

		for tema in soup_.find_all("div", {"class": "thread"}):
			thread_id = tema.get('id').split("_")[1]
			LOGGER.debug("Tema: {}".format(thread_id))
			new_thread = True
			for reply in tema.find_all("div", {"class": "post reply"}):
				if not temos_ir_postai.get(board):
					temos_ir_postai[board] = collections.OrderedDict()
				if new_thread:
					# Gets op message, one time in reply integration
					# TODO: parse op message "<"
					op_id = reply.previous_sibling.get('id').split("_")[-1]
					op_reply = reply.previous_sibling.find("div", {"class": "body"}).get_text()
					postai.append([collections.OrderedDict(
						{"comment": op_reply, "author": "OP",
						 "reply_id": op_id})])
					new_thread = False
				reply_id = reply.get('id').split("_")[1]
				for author in reply.find_all("span", {"class": "name"}):
					LOGGER.debug(author.get_text())
				for comment in reply.find_all("div", {"class": "body"}):
					LOGGER.debug("Before split: %s" % comment.get_text())
					if len(re.split("(>>\d*)", comment.get_text())) == 1:
						comment = ' '.join(re.split("(>>\d*)", comment.get_text()))
					else:
						comment = ' '.join(re.split("(>>\d*)", comment.get_text())[1:])
					LOGGER.debug("After split: %s" % comment)

				postai.append([collections.OrderedDict(
					{"comment": comment, "author": author.get_text(),
					 "reply_id": reply_id})])
				temos_ir_postai[board][thread_id] = postai
			postai = []  # Clear list after putting in dict
	return temos_ir_postai


def dubliu_tikrinimas(No):
	"""

	:param No: temos arba reply id kaip str
	:return: dubliu skaicius
	"""
	No = No[::-1]
	count = 0
	temp_num = ""
	for index, number in enumerate(No):
		if index == 0:
			count = 1
			temp_num = number
		else:
			if temp_num == number:
				count += 1
				temp_num = number
			if temp_num != number:
				return count

	return count


def pranesti_apie_dublius(dubliu_skaicius):
	"""

	:param dubliu_skaicius(int): besikartojanciu skaiciu kiekis
	:return: grazina eilute atitinkacia dubliu skaiciu
	"""
	if dubliu_skaicius == 0 or dubliu_skaicius == 1:
		return ""
	if dubliu_skaicius == 2:
		return "Dubliai"
	if dubliu_skaicius == 3:
		return "Tripliai"
	if dubliu_skaicius == 4:
		return "Kvarkai"
	if dubliu_skaicius == 5:
		return "Penktetai"
	if dubliu_skaicius == 6:
		return "Sextetai"
	if dubliu_skaicius == 7:
		return "Septetai"
	if dubliu_skaicius == 8:
		return "Oktetai"


def temu_tikrinimas(boards_):
	base_commits = get_comments(boards_)
	while True:
		time.sleep(CHECK_INTERVAL)
		new_commits = get_comments(boards_)

		for board_name in base_commits:
			for board_id_, comments in new_commits[board_name].items():
				reply_id = comments[-1][0]["reply_id"]
				dubliai = pranesti_apie_dublius(dubliu_tikrinimas(reply_id))
				LOGGER.info("Checking /%s/, newest: No.%s  %s " % (board_name, reply_id, dubliai))
				break
		if base_commits != new_commits:
			for board_name, board_id in new_commits.items():
				if new_commits[board_name] != base_commits[board_name]:
					# Get latest commit
					for board_id_, comments in new_commits[board_name].items():
						name = comments[-1][0]["author"]
						description = comments[-1][0]["comment"]
						reply_id = comments[-1][0]["reply_id"]
						dubliai = pranesti_apie_dublius(dubliu_tikrinimas(reply_id))

						LOGGER.info(
							"New content detected\n No: %s %s on /%s/\n name: %s \n description: %s" % (
								reply_id, dubliai, board_name, name, description))
						if dubliai:
							call(
								["/usr/bin/notify-send", "{}, on /{}/".format(name, board_name),
								 "! {} !\n{}".format(dubliai, description)])
						else:
							call(
								["/usr/bin/notify-send", "{}, on /{}/".format(name, board_name), description])
						base_commits = get_comments(boards_)
						break

		else:
			LOGGER.info("No changes detected.")


# TODO: cross platform
temu_tikrinimas(["b", "int", "a", "v"])
