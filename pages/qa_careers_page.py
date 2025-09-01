# pages/qa_careers_page.py
from selenium.common import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement  # Import WebElement for type hinting
import time

from pages.base_page import BasePage


class QACareersPage(BasePage):
    URL = "https://useinsider.com/careers/quality-assurance/"

    # --- Locators ---
    SEE_ALL_QA_JOBS_BUTTON = (By.XPATH, '//a[contains(text(), "See all QA jobs")]')
    LOCATION_FILTER_CONTAINER = (By.ID, "select2-filter-by-location-container")
    DEPARTMENT_FILTER_CONTAINER = (By.ID, "select2-filter-by-department-container")
    JOB_LIST_SECTION = (By.ID, "jobs-list")

    # --- New Locators for Job Cards ---
    JOB_CARDS = (By.CSS_SELECTOR, 'div.position-list-item')
    JOB_TITLES = (By.CSS_SELECTOR, "div.job-card .position-title.font-weight-bold")
    JOB_DEPARTMENTS = (By.CSS_SELECTOR, "div.job-card .position-department.text-large.font-weight-600.text-primary")
    JOB_LOCATIONS = (By.CSS_SELECTOR, "div.job-card .position-location.text-large")
    APPLY_NOW_BUTTON = (By.CLASS_NAME, "btn-apply")

    def load(self):
        """Loads the page."""
        self.driver.get(self.URL)

    def click_see_all_qa_jobs(self):
        """Clicks the 'See all QA jobs' button and waits for the new page to load."""
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.SEE_ALL_QA_JOBS_BUTTON)
        ).click()

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.LOCATION_FILTER_CONTAINER)
        )

    def apply_filters(self, location: str, department: str):
        """Applies the specified location and department filters."""
        self._select_option_from_custom_dropdown(self.LOCATION_FILTER_CONTAINER, location)
        self._select_option_from_custom_dropdown(self.DEPARTMENT_FILTER_CONTAINER, department)

        # Wait to ensure the job list has reloaded after filtering
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.JOB_LIST_SECTION)
        )
        time.sleep(3)  # A small static wait can sometimes help ensure all JS rendering is complete

    def _select_option_from_custom_dropdown(self, container_locator: tuple, option_text: str, timeout: int = 10):
        """Helper function for custom dropdown menus. Keeps searching until the option is found."""
        option_locator = (By.XPATH, f"//li[normalize-space(text())='{option_text}']")

        end_time = time.time() + timeout
        while time.time() < end_time:
            try:
                container = self.find(container_locator)
                container.click()

                option_to_click = WebDriverWait(self.driver, 2).until(
                    EC.element_to_be_clickable(option_locator)
                )
                option_to_click.click()
                return
            except Exception:
                continue

        raise TimeoutException(f"Option '{option_text}' not found in dropdown within {timeout} seconds")

    def wait_for_job_cards(self, timeout: int = 10):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(self.JOB_CARDS)
            )
            return len(self.find_all(self.JOB_CARDS)) > 0
        except TimeoutException:
            return False

    def all_positions_contain(self, text_options: list) -> bool:
        """
        Returns True if at least one of the text_options is in every job title.
        """
        job_titles = self.find_all(self.JOB_TITLES)
        for title in job_titles:
            title_text = title.text.lower()
            if not any(opt.lower() in title_text for opt in text_options):
                return False
        return True

    def all_departments_contain(self, text_options: list) -> bool:
        """
        Returns True if at least one of the text_options is in every department element.
        """
        departments = self.find_all(self.JOB_DEPARTMENTS)
        for dept in departments:
            dept_text = dept.text.lower()
            if not any(opt.lower() in dept_text for opt in text_options):
                return False
        return True

    def all_locations_contain(self, locations: list) -> bool:
        locs = self.find_all(self.JOB_LOCATIONS)
        for loc in locs:
            loc_text = loc.text.lower()
            if not any(opt.lower() in loc_text for opt in locations):
                return False
        return True

    def click_view_role_button(self, timeout: int = 10):
        get_card = self.find_all(self.JOB_CARDS)[0]

        """  use ActionChains for hover over the card """
        ActionChains(self.driver).move_to_element(get_card).perform()

        """ Wait until 'View Role' button is visible inside the card """
        try:
            button = WebDriverWait(get_card, timeout).until(
                lambda c: c.find_element(By.XPATH, './/a[contains(text(), "View Role")]')
            )
        except TimeoutException:
            raise Exception("'View Role' button not found in the first job card.")

        """ Scroll to the button and click via JS to avoid interception issues """
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", button
        )
        self.driver.execute_script("arguments[0].click();", button)

