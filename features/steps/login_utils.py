import time
def login(ctx, username='admin', password='admin'):
    ctx.browser.get(ctx.server_address + "/login")
    uname = ctx.browser.find_element_by_name('username')
    passwd = ctx.browser.find_element_by_name('password')
    login_button = ctx.browser.find_element_by_id('btn_login')
    uname.clear();
    passwd.clear();
    time.sleep(1)
    uname.send_keys(username)
    passwd.send_keys(password)
    time.sleep(1)
    login_button.click()

def logout(ctx):
    pass