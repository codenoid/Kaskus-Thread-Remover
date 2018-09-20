import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()

driver.get("https://m.kaskus.co.id/user/login/home")

user_username = input("Masukkan Username Kakus : ")
user_password = input("Masukkan Password Kakus : ")

input_username = driver.find_elements_by_css_selector("input#username")
input_password = driver.find_elements_by_css_selector('input[name="password"]')

input_submit = driver.find_elements_by_css_selector("input#submit-button")

if len(input_username) > 0 and len(input_password) > 0 and len(input_submit) > 0:
	input_username[0].send_keys(user_username)
	input_password[0].send_keys(user_password)
	input_submit[0].click()
	driver.get("https://m.kaskus.co.id/myforum/mythread/")
	time.sleep(2)
	last_paging = driver.find_elements_by_css_selector('span.text-right a[href*="/myforum/mythread"].arr:last-child')
	if len(last_paging) > 0:
		last_page = int(last_paging[0].get_attribute('href').split("/")[-1])
		for i in range(1,last_page+1):
			driver.get("https://m.kaskus.co.id/myforum/mythread/" + str(i))
			threads = driver.find_elements_by_css_selector('a[href*="/thread"]')
			threads_in_pages = []
			print("Collecting Threads")
			for thread in threads:
				threads_in_pages.append(thread.get_attribute('href'))
			print("Exploring Threads")
			for thread in threads_in_pages:
				driver.get(thread)
				time.sleep(2)
				is_already_deleted = driver.find_elements_by_css_selector("h2.entry-title")
				if len(is_already_deleted) > 0:
					if is_already_deleted[0].text == "Deleted Thread":
						continue
					else:
						print(is_already_deleted[0].text)
						is_editable = driver.find_elements_by_css_selector('div[id*="post"][class=""]')
						if len(is_editable) > 0:
							post_hash = is_editable[0].get_attribute("id").replace("post", "")
							print(post_hash)
							driver.get("https://m.kaskus.co.id/edit_post/"+post_hash)
							# Deleted Thread
							input_title = driver.find_elements_by_css_selector('input[name="title"]')
							input_desc = driver.find_elements_by_css_selector('textarea#message')
							if len(input_title) > 0 and len(input_desc) > 0:
								input_title[0].clear()
								input_desc[0].clear()
								input_title[0].send_keys("Deleted Thread")
								input_desc[0].send_keys("Deleted Thread")
								time.sleep(2)
								try:
									save_btn = driver.find_elements_by_css_selector('input[name="sbutton"]')
									if len(save_btn) > 0:
										save_btn[0].click()
								except:
									print("b")

driver.quit()