import aiohttp
import pytest
from seleniumwire import webdriver


@pytest.fixture(scope="session")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("no-sandbox")
    options.add_argument("disable-extensions")
    options.add_argument("incognito")
    driver = webdriver.Chrome(options=options)
    try:
        yield driver
    finally:
        driver.quit()


@pytest.fixture
async def session():
    async with aiohttp.ClientSession() as session:
        yield session


@pytest.mark.asyncio
async def test_selenium(driver, session) -> None:
    driver.get("https://www.google.com/")
