from contextlib import asynccontextmanager
from typing import AsyncIterator, Optional
from nonebot.log import logger
from nonebot import get_driver
from . import save_token
from .. import config
from playwright.async_api import Browser,Page, async_playwright,Error

_browser: Optional[Browser] = None
_playwright = None



async def init(**kwargs) -> Optional[Browser]:
    global _browser
    global _playwright
    _playwright = await async_playwright().start()
    try:
        _browser = await launch_browser(**kwargs)
    except Error:
        await install_browser()
        _browser = await launch_browser(**kwargs)
    return _browser

async def launch_browser(**kwargs) -> Browser:
    return await _playwright.chromium.launch(**kwargs)

async def get_browser(**kwargs) -> Browser:
    return _browser or await init(**kwargs)


async def install_browser():
    """自动安装、更新 Chromium"""
    logger.info("正在检查Chromium更新")
    import sys
    from playwright.__main__ import main

    sys.argv = ["","install","chromium"]
    try:
        main()
    except SystemExit:
        pass
# 增加一个卸载的,然后开启最下面的driver


async def shutdown_browser():
    await _browser.close()
    await _playwright.stop()

@asynccontextmanager
async def get_new_page(**kwargs) -> AsyncIterator[Page]:
    browser = await get_browser()
    page = await browser.new_page(**kwargs)
    try:
        yield page
    finally:
        await page.close()


async def get_new_token():
    browser = await get_browser()
    page = None
    try:
        page = await browser.new_page()
        await page.goto("https://uis.zafu.edu.cn/cas/login?service=http%3A%2F%2Fappui.zafu.edu.cn%2Fsso%2Flogin.jsp%3FtargetUrl%3D%7Bbase64%7DaHR0cDovL2FwcHVpLnphZnUuZWR1LmNuL3Nzby9pbmRleC5qc3A%3D",wait_until='networkidle',timeout=20000)
        await page.click("[placeholder=\"账号\"]")
        await page.fill("[placeholder=\"账号\"]", config.user_id)
        await page.click("[placeholder=\"密码\"]")
        await page.fill("[placeholder=\"密码\"]", config.password)
        await page.click("text=登 录")
        await page.goto("https://appui.zafu.edu.cn/h5app/ssotransfer/trans.htm?app=YqdjIndex",
                        wait_until="networkidle",timeout=20000)
        new_token = await page.evaluate("() => window.localStorage.getItem('token')")
        await page.close()
        save_token(new_token)
        return new_token
    except Exception:
        logger.warning("模拟爬取失败")
        if page:
            await page.close()
        raise



# get_driver().on_startup(delete_browser)
# get_driver().on_startup(install_browser)