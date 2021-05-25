from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from browser import Browser
from setting import *
import json
import pymysql
from datetime import datetime


class InsCookiesDownloader:
    URL = "https://www.instagram.com"

    def __init__(self):
        self.browser = Browser(has_screen=has_screen)
        self.login_url = "https://www.instagram.com/accounts/login/"
        self.conn = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, port=PORT)
        self.cursor = self.conn.cursor()

    def login(self, username, password):
        status = 1  # 表示该账号的状态: 1-正常, 0-异常
        self.browser.driver.delete_all_cookies()
        self.browser.get(self.login_url)
        u_input = self.browser.find_one('input[name="username"]')
        u_input.send_keys(username)
        p_input = self.browser.find_one('input[name="password"]')
        p_input.send_keys(password)
        self.browser.find_one(".L3NKy").click()
        try:
            WebDriverWait(self.browser.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//img[@class="_6q-tv"]'))
            )
        except:
            status = 0
        cookieStr = self.browser.get_cookies_str()
        return cookieStr, status

    def save_cookie_to_mysql(self, cookie, username, status):
        update_time = datetime.now()
        sql = '''replace into ins_cookie_pool(username, cookie, status, update_time) values('%s', '%s', '%s', '%s')''' % (username, cookie, status, update_time)
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as ex:
            self.conn.rollback()
            print("写入失败!!!", ex)
        if status == 0:
            print(f"账号: {username} 异常, 请确定后删除该账号信息!!")
        elif status == 1:
            print(f"账号: {username} 正常, 写入成功~")

    def get_user_pwds(self):
        with open("ins_account.json", "r") as f:
            accounts = json.load(f)
        return accounts

    def run(self):
        '''入口程序'''
        accounts = self.get_user_pwds()
        for account in accounts:
            username = account['username']
            password = account['password']
            print(f"正在写入账号: {username} 的cookies信息...")
            try:
                cookie, status = self.login(username, password)
            except Exception as ex:
                cookie = ""
                status = 0
                print(f"账号{username}写入失败!!!", "错误信息:", ex)
                self.save_cookie_to_mysql(cookie, username, status)
            self.save_cookie_to_mysql(cookie, username, status)
        self.cursor.close()
        self.conn.close()
        print("程序结束")


if __name__ == '__main__':
    icd = InsCookiesDownloader()
    icd.run()
