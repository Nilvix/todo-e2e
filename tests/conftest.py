import functools
import http.server
import pathlib
import threading

import pytest
from selenium import webdriver

APP_DIR = pathlib.Path(__file__).parent.parent
SHOTS = APP_DIR / "screenshots"


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


@pytest.fixture(scope="session")
def app_url():
    """Отдаёт приложение через локальный HTTP-сервер.

    По file:// Chrome на macOS получал ERR_ACCESS_DENIED
    для папки на рабочем столе, а по http такой проблемы нет.
    """
    handler = functools.partial(QuietHandler, directory=str(APP_DIR))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{server.server_port}/index.html"
    server.shutdown()


@pytest.fixture
def driver(request, app_url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=900,800")
    # В контейнере GitHub Actions Chrome без этих флагов не стартует
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    drv = webdriver.Chrome(options=options)
    drv.get(app_url)
    yield drv
    SHOTS.mkdir(exist_ok=True)
    drv.save_screenshot(str(SHOTS / f"{request.node.name}.png"))
    drv.quit()


@pytest.fixture
def app(driver):
    from tests.todo_page import TodoPage
    return TodoPage(driver)
