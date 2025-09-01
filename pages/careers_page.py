from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CareersPage(BasePage):
    """Page object for the Insider Careers Page."""
    LOCATIONS_BLOCK = (By.CSS_SELECTOR, "section#career-our-location")
    TEAMS_BLOCK = (By.ID, "career-find-our-calling")
    LIFE_AT_INSIDER_BLOCK = (By.XPATH, "//*[contains(text(), 'Life at Insider')]")

    def wait_for_page_load(self):
        """Waits for a key element on the page to be visible."""
        self.is_visible(self.LOCATIONS_BLOCK)

    def are_core_blocks_displayed(self):
        """Checks if the Locations, Teams, and Life at Insider blocks are visible."""
        return (self.is_visible(self.LOCATIONS_BLOCK) and
                self.is_visible(self.TEAMS_BLOCK) and
                self.is_visible(self.LIFE_AT_INSIDER_BLOCK))