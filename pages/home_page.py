from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class HomePage(BasePage):
    """Page object for the Insider Home Page."""
    URL = "https://useinsider.com/"
    COMPANY_MENU = (By.XPATH, "//a[normalize-space()='Company']")
    CAREERS_SUBMENU = (By.XPATH, "//a[normalize-space()='Careers']")
    ACCEPT_COOKIES_BUTTON = (By.ID, "wt-cli-accept-all-btn")

    def load(self):
        """Loads the home page and accepts cookies."""
        self.go_to_url(self.URL)
        if self.is_visible(self.ACCEPT_COOKIES_BUTTON):
            self.wait_and_click(self.ACCEPT_COOKIES_BUTTON)

    def is_loaded(self):
        """Checks if the home page is loaded by verifying the title."""
        return "Insider" in self.driver.title

    def navigate_to_careers(self):
        """Navigates from the home page to the careers page."""
        self.wait_and_click(self.COMPANY_MENU)
        self.wait_and_click(self.CAREERS_SUBMENU)