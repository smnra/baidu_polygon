from playwright.sync_api import sync_playwright

import sys,os


def  init_path(path):
    print(f"初始化csv文件目录: csv_path: {path}")
    if not os.path.isdir(path):              # 创建目录
        os.mkdir(path)
    else:                                      # 删除目录下保存的旧文件
        for file_name in os.listdir(path):
            # if file_name.endswith('.csv'):
            file_path = os.path.join(path, file_name)
            os.remove(file_path)
            print(f"Deleted: {file_path}")




# [playwright 相关配置]
root_path = os.path.abspath("./")
os.chdir(root_path)
downloads_path = os.path.join(root_path, 'downloads')               # 下载目录
userData_path = os.path.join(root_path, 'userData' )                 # 用户数据目录
chrome_path = 'C:\\Program Files\\GoogleChromePortable\\App\\Chrome-bin\\chrome.exe'    # 浏览器路径

init_path(downloads_path)  # 初始化 downloads_path 文件目录
# init_path(userData_path)  # 初始化 userData_path 文件目录

chrome_size = {"width": 1440, "height": 900}     # 窗口大小
isHeadless = False    # 是否无头模式运行
chrome_jsFile = os.path.join(root_path, 'stealth.min.js')       # 加载的js文件路径  为隐藏selenium特征

ua = {           # 浏览器 User-Agent
    "web": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 "
           "Safari/537.36",
    "app": "com.ss.android.ugc.aweme/110101 (Linux; U; Android 5.1.1; zh_CN; MI 9; Build/NMF26X; "
           "Cronet/TTNetVersion:b4d74d15 2020-04-23 QuicVersion:0144d358 2020-03-24)"
}


headers = {         # 浏览器自定义请求头
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8,zh-CN;q=0.7,zh;q=0.6",
    "Authorization": "Bearer eyJhbGciOiJIUzUxMiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VyX2tleSI6IjU4M2M0Y2RhLTI1YjAtNGNkNS05Y2ZlLWRkNWQzMTk0OTI3NiIsInVzZXJuYW1lIjoiYWRtaW4ifQ.ywr9_14pWzh7qTdESdBRIB1Pga9VSLb4O8I7pU9AVVyzX0vazUKoH4Pftdvc_bfvWyXBdTu-A5xRQVUeNFOdsg",
    "Connection": "keep-alive",
    "Content-Length": "115",
    "Content-Type": "application/json;charset=UTF-8",
    "Cookie": "JSESSIONID=4A4817D1F040BB6FE1989D78C06864FF; Admin-Token=eyJhbGciOiJIUzUxMiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VyX2tleSI6IjU4M2M0Y2RhLTI1YjAtNGNkNS05Y2ZlLWRkNWQzMTk0OTI3NiIsInVzZXJuYW1lIjoiYWRtaW4ifQ.ywr9_14pWzh7qTdESdBRIB1Pga9VSLb4O8I7pU9AVVyzX0vazUKoH4Pftdvc_bfvWyXBdTu-A5xRQVUeNFOdsg",
    "Dnt": "1",
    "Host": "10.93.19.178",
    "Origin": "http://10.93.19.178",
    "Referer": "http://10.93.19.178/sceneNavigation?nokiaToken=6kKZsa8mLd6%20TBZ676JfFSbrk2eosev1EZfhYsPN3raPZoOQSO%2FG0wzI%2FYN83mSHZIIdHoEQ3rZQV0Yp4iGVKQ%3D%3D&type=2&ticket=ST-7653-HdMm2fdPrLB0",
    "User-Agent": ua["web"],
}




def init_playwright(isPersistent=True, isHeadless=False):
    # isPersistent 是否使用持久化浏览器，默认是True,  isHeadless 是否使用无头模式，默认是False
    # 启动 Playwright 实例
    playwright = sync_playwright().start()

    if isPersistent :
        # 设置浏览器属性  launch_persistent_context() 方法启动有痕模式的浏览器
        browser = playwright.chromium.launch_persistent_context(
            user_agent=ua["web"],  # 设置UA
            chromium_sandbox=False,
            user_data_dir=userData_path,  # 指定浏览器用户数据目录，用于保存cookie等信息，默认是None
            executable_path=chrome_path,  # 指定本机google客户端exe的路径
            # headless=True,  # 是否隐藏浏览器界面，默认是False
            headless=isHeadless,  # 是否隐藏浏览器界面，默认是False
            ignore_https_errors=True,  # 可以忽略 SSL 错误
            accept_downloads=True,  # 要想通过这个下载文件这个必然要开  默认是False
            ignore_default_args=["--enable-automation"],
            viewport=chrome_size,  # 指定浏览器窗口大小，默认是1920x1080
            channel="chrome",
            args=[
                "--load-extension={path_to_extension}",  # 加载插件
                # "--disable-extensions-except={path_to_extension}",  # 禁用除指定插件外的所有插件
                "--disable-infobars",  # 禁用信息栏
                "--disable-extensions",  # 禁用插件
                "--disable-notifications",  # 禁用通知
                "--disable-gpu",  # 禁用GPU
                "--no-sandbox",  # 禁用沙盒模式
                "--disable-dev-shm-usage",  # 禁用共享内存
                "--disable-setuid-sandbox",  # 禁用setuid沙盒
                "--disable-webgl",  # 禁用WebGL
                "--disable-popup-blocking",  # 禁用弹窗阻塞
                "--disable-translate",  # 禁用翻译
                "--disable-background-timer-throttling",  # 禁用后台定时器节流
                "--disable-renderer-backgrounding",  # 禁用渲染器后台运行
                "--disable-device-discovery-notifications",  # 禁用设备发现通知
                "--disable-features=site-per-process",  # 禁用站点隔离
                "--disable-features=TranslateUI",  # 禁用翻译界面
                "--disable-features=BlinkGenPropertyTrees",  # 禁用Blink生成属性树
            ]
        )
        page = browser.pages[0]


    else:

        # 设置浏览器属性  launch() 方法启动无痕模式的浏览器  launch_persistent_context() 方法启动有痕模式的浏览器
        # 无痕模式不能使用 page = browser.pages[0] 来获取标签页
        # 需要使用 page = context.pages[0] 来获取标签页
        browser = playwright.chromium.launch(chromium_sandbox=False,
                                             executable_path=chrome_path,  # 指定本机google客户端exe的路径
                                             headless=isHeadless,  # 是否隐藏浏览器界面，默认是False
                                             ignore_default_args=["--enable-automation"],
                                             channel="chrome",
                                             )
        # 设置浏览器上下文    # 设置cookie   # 设置UA   # 接受下载
        context = browser.new_context(
            accept_downloads=True,  # 要想通过这个下载文件这个必然要开  默认是False
            viewport=chrome_size  # 设置窗口大小
        )

        page = context.new_page()
        page = context.pages[0]

    page.goto("https://www.ipuu.net/Home")
    # 返回 playwright 实例和 browser 对象
    return playwright, browser,page


def load_cookies_from_file(file_path):
    # 读取cookies文件
    with open(file_path, 'r') as file:
        cookies = eval(file.read())  # 使用 eval 读取文件内容并转换为列表
    return cookies


if __name__ == '__main__':

    # 获取实例
    playwright, browser,page = init_playwright(isPersistent=True, isHeadless=False)       # 有痕模式
    # playwright, browser,page = init_playwright(isPersistent=False, isHeadless=False)   # 无痕模式
    try:
        page.goto("https://www.ipplus360.com/getIP")
        # 其他操作...
    finally:
        # 确保关闭浏览器和停止 playwright
        # page.close()
        browser.close()
        playwright.stop()
