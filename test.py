import asyncio
from pyppeteer import launch

async def openBrowser(url):
    print(1)
    browser = await launch(headless=False)
    page = await browser.newPage()
    await page.goto(url)

asyncio.get_event_loop().run_until_complete(openBrowser('http://www.google.com'))

