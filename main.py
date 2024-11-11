from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 配置 Chrome 无痕模式
chrome_options = Options()
chrome_options.add_argument("--headless")  # 如果不需要显示浏览器界面，可以启用 headless 模式
chrome_options.add_argument("--disable-gpu")

# 设置 Chrome 驱动路径
driver_path = 'D:/Develop/chromedriver-win64/chromedriver.exe'

# XPath 常量（以后可以根据实际需求调整）
XPATHS = {
    'name_input': '//*[@id="app"]/main/div[2]/div/form/div[1]/div/div/span/span/input',
    'pwd_input': '//*[@id="app"]/main/div[2]/div/form/div[2]/div/div/span/span/input',
    'submit_btn': '//*[@id="app"]/main/div[2]/div/form/div[3]/div/div/span/button',
    'menu_item': '//*[@id="sider"]/div/ul/li[2]',
    'edit_link': '//*[@id="content-layout"]/main/div/div/div[2]/div[2]/div/div/div/div/div/div/div/table/tbody/tr/td[1]/a',
    'edit_item': '/html/body/div[2]/div/div/ul/li[2]',
    'port_input': '//*[@id="inbound-modal"]/div[2]/div/div[2]/div[2]/form[1]/div[5]/div[2]/div/span/input',
    'confirm_btn': '//*[@id="inbound-modal"]/div[2]/div/div[2]/div[3]/div/button[2]',
    'success_message': '/html/body/div[4]/span/div/div/div/span'
}


def task_to_run(driver):
    """在凌晨4点时执行的任务"""
    # 打开指定网址
    print("开始修改端口")
    driver.get("http://45.43.59.128:54321/yikolemon/xui/")

    # 登录操作
    name = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, XPATHS['name_input']))
    )
    name.clear()
    name.send_keys("yikolemon")

    pwd = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, XPATHS['pwd_input']))
    )
    pwd.clear()
    pwd.send_keys("Iwaitkaisen")

    btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, XPATHS['submit_btn']))
    )
    btn.click()

    # 导航到下一个页面
    menu = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, XPATHS['menu_item']))
    )
    menu.click()

    # 点击编辑
    edit = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, XPATHS['edit_link']))
    )
    edit.click()

    # 选择编辑项
    edit2 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, XPATHS['edit_item']))
    )
    edit2.click()

    # 输入端口信息
    port = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, XPATHS['port_input']))
    )
    now = datetime.now()
    year_last_digit = str(now.year % 10)
    month = str(now.month).zfill(2)
    day = str(now.day).zfill(2)
    result = year_last_digit + month + day
    port.clear()
    port.send_keys(result)

    # 确认按钮点击
    confirm = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, XPATHS['confirm_btn']))
    )
    confirm.click()

    # 输出成功消息
    show = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, XPATHS['success_message']))
    )
    print("成功")


def run_forever():
    """主循环，每天凌晨4点执行任务"""
    while True:
        now = datetime.now()

        # 检查是否是凌晨 4 点
        if now.hour == 20 and now.minute == 51:
            # 启动 Chrome 浏览器
            driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)
            driver.delete_all_cookies()

            try:
                # 执行任务
                task_to_run(driver)

            finally:
                driver.quit()

            # 等待 60 秒，防止任务被重复执行
            time.sleep(10)
        else:
            # 不是凌晨4点，继续等待
            time.sleep(10)  # 每次等待 60 秒


if __name__ == "__main__":
    run_forever()
