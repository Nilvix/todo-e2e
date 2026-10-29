from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class TodoPage:
    INPUT = (By.ID, "todo-input")
    ADD = (By.ID, "add-btn")
    ITEMS = (By.CSS_SELECTOR, "#todo-list li")
    COUNTER = (By.ID, "counter")
    ERROR = (By.ID, "error")
    CLEAR_DONE = (By.ID, "clear-done")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)

    def add(self, text):
        before = len(self.items())
        field = self.driver.find_element(*self.INPUT)
        field.clear()
        field.send_keys(text)
        self.driver.find_element(*self.ADD).click()
        if text.strip():
            self.wait.until(lambda d: len(self.items()) == before + 1)

    def items(self):
        return self.driver.find_elements(*self.ITEMS)

    def texts(self):
        return [li.find_element(By.CLASS_NAME, "text").text
                for li in self.items()]

    def item(self, text):
        for li in self.items():
            if li.find_element(By.CLASS_NAME, "text").text == text:
                return li
        raise AssertionError(f"Задача '{text}' не найдена")

    def toggle(self, text):
        self.item(text).find_element(By.CLASS_NAME, "toggle").click()

    def delete(self, text):
        self.item(text).find_element(By.CLASS_NAME, "delete").click()

    def filter(self, name):
        self.driver.find_element(
            By.CSS_SELECTOR, f".filters [data-filter='{name}']").click()

    def counter(self):
        return self.driver.find_element(*self.COUNTER).text

    def error(self):
        el = self.driver.find_element(*self.ERROR)
        return el.text if el.is_displayed() else ""
