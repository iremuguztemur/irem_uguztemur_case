import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    """A base page class to hold common methods and functionalities."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 20)

    def go_to_url(self, url):
        """Navigates to the specified URL."""
        self.driver.get(url)

    def select_hidden_dropdown_by_value(self, locator, value):
        """
        Directly sets the value of a hidden <select> element and fires the
        'change' event to trigger the page's JavaScript. This is the
        guaranteed method for the Insider filters.
        """
        element = self.wait.until(EC.presence_of_element_located(locator))
        self.driver.execute_script(
            "var select = arguments[0];"
            "select.value = arguments[1];"
            "var event = new Event('change', { bubbles: true });"
            "select.dispatchEvent(event);",
            element, value
        )

    def wait_and_click(self, locator):
        """A standard click method."""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def is_visible(self, locator):
        """Checks if an element is visible on the page."""
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    def get_all_elements(self, locator):
        """Returns a list of all elements matching the locator."""
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def switch_to_new_tab(self):
        """Switches driver focus to the newest tab."""
        self.wait.until(EC.number_of_windows_to_be(2))
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def find(self, locator):
        return self.driver.find_element(*locator)

    def find_all(self, locator):
        return self.driver.find_elements(*locator)