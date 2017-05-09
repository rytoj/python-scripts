from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def initiate():
	"""
	Innitial login to sychtube
	:return:
	"""
	driver = webdriver.Firefox()
	driver.get("https://synchtu.be/r/370")
	return driver


def login_synchtube(driver_, username):
	"""
	Logins to sychtu.be with username
	:param username: Username to login
	:return:
	"""
	guest = driver_.find_element_by_xpath("//*[@id='guestname']")
	guest.send_keys(username)
	guest.send_keys(Keys.RETURN)


def send_to_chat(driver_, msg):
	"""
	Send message to synch tube
	:param msg:
	:return:
	"""
	chat = driver_.find_element_by_xpath('//*[@id="chatline"]')
	chat.send_keys(msg)
	chat.send_keys(Keys.RETURN)


if __name__ == "__main__":
	driver = initiate()
	login_synchtube(driver, "vaidilute2")
	send_to_chat(driver, "labas")

	driver.close()
