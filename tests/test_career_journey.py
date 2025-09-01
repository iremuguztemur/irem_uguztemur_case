import pytest
from selenium.webdriver.support.wait import WebDriverWait

from pages.home_page import HomePage
from pages.careers_page import CareersPage
from pages.qa_careers_page import QACareersPage
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(), options=options)
    yield driver
    driver.quit()

def test_insider_qa_career_journey(driver):
    """Full test case for verifying the QA career journey on Insider."""

    # Step 1: Navigate Home → Careers
    home_page = HomePage(driver)
    home_page.load()
    home_page.navigate_to_careers()

    # Step 2: Wait for Careers page to load
    careers_page = CareersPage(driver)
    careers_page.wait_for_page_load()
    assert careers_page.are_core_blocks_displayed(), "Careers core blocks are not visible."

    # Step 3: Load QA Careers page and apply filters
    qa_page = QACareersPage(driver)
    qa_page.load()
    qa_page.click_see_all_qa_jobs()
    qa_page.apply_filters(location="Istanbul, Turkiye", department="Quality Assurance")

    # Step 4: Wait until job cards are visible
    assert qa_page.wait_for_job_cards(), "QA job couldnt find after filtering "
    assert qa_page.all_positions_contain(["Quality Assurance", "QA"]), \
        "Some job titles do not contain 'Quality Assurance' or 'QA'"
    assert qa_page.all_departments_contain("Quality Assurance"), "Some jobs are not in 'Quality Assurance' department"
    assert qa_page.all_locations_contain("Istanbul, Turkiye"), "Some job locations are not 'Istanbul, Turkiye'"

    # Step 5: Click first View Role
    qa_page.click_view_role_button()
    assert "lever.co" in driver.current_url, "Job details not opened"