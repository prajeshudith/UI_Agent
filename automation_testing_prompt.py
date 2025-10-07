task = """ You are provided with the following JSON structure that contains information about a web page and a set of test cases to be performed on various elements of that page. Your task is to go through each test case and execute the specified actions on the web page using browser automation. After executing each action, verify that the expected result is achieved.
        
        1. Start by navigating to the URL provided in the "test_suite_info" section.
        2. For each test case in the "test_cases" array, perform the following steps:
            a. Locate the element on the web page using the provided "id", "xpath", or "css_selector".
            b. Perform the action specified in the "action" field (e.g., click, input_text).
            c. If the action involves inputting text, use the "test_data" field as the input value.
            d. After performing the action, verify that the outcome matches the "expected_result".
            e. Log the result of each test case, indicating whether it passed or failed based on the verification step.
        3. After all test cases have been executed, provide a summary of the results, including the total number of test cases, how many passed, and how many failed.

        # Here is the JSON structure:
        {
            "test_suite_info": {
                "url": "https://www.saucedemo.com/",
                "page_title": "Swag Labs",
                "total_elements": 3,
                "total_test_cases": 6,
                "generated_on": "2025-09-28T21:40:21.627022"
            },
            "test_cases": [
                {
                "element_info": {
                    "id": "login-button",
                    "xpath": "//*[@id='login-button']",
                    "css_selector": "#login-button",
                    "text": "",
                    "element_type": "buttons"
                },
                "test_id": "TC_001",
                "test_name": "Click ",
                "action": "click",
                "test_data": "",
                "expected_result": "Button should be clickable and trigger appropriate action",
                "priority": "High",
                "test_type": "Functional"
                },
                {
                "element_info": {
                    "id": "login-button",
                    "xpath": "//*[@id='login-button']",
                    "css_selector": "#login-button",
                    "text": "",
                    "element_type": "buttons"
                },
                "test_id": "TC_002",
                "test_name": "Hover over ",
                "action": "hover",
                "test_data": "",
                "expected_result": "Button should respond to hover with visual feedback",
                "priority": "Medium",
                "test_type": "UI"
                },
                {
                "element_info": {
                    "id": "user-name",
                    "xpath": "//*[@id='user-name']",
                    "css_selector": "#user-name",
                    "text": "",
                    "element_type": "inputs"
                },
                "test_id": "TC_003",
                "test_name": "Input valid data in user-name",
                "action": "input_text",
                "test_data": "Test Data 123",
                "expected_result": "Field should accept valid input",
                "priority": "High",
                "test_type": "Functional"
                },
                {
                "element_info": {
                    "id": "user-name",
                    "xpath": "//*[@id='user-name']",
                    "css_selector": "#user-name",
                    "text": "",
                    "element_type": "inputs"
                },
                "test_id": "TC_004",
                "test_name": "Input special characters in user-name",
                "action": "input_text",
                "test_data": "!@#$%^&*()",
                "expected_result": "Field should handle special characters appropriately",
                "priority": "Medium",
                "test_type": "Negative"
                },
                {
                "element_info": {
                    "id": "password",
                    "xpath": "//*[@id='password']",
                    "css_selector": "#password",
                    "text": "",
                    "element_type": "inputs"
                },
                "test_id": "TC_005",
                "test_name": "Input valid data in password",
                "action": "input_text",
                "test_data": "Test Data 123",
                "expected_result": "Field should accept valid input",
                "priority": "High",
                "test_type": "Functional"
                },
                {
                "element_info": {
                    "id": "password",
                    "xpath": "//*[@id='password']",
                    "css_selector": "#password",
                    "text": "",
                    "element_type": "inputs"
                },
                "test_id": "TC_006",
                "test_name": "Input special characters in password",
                "action": "input_text",
                "test_data": "!@#$%^&*()",
                "expected_result": "Field should handle special characters appropriately",
                "priority": "Medium",
                "test_type": "Negative"
                }
            ],
            "automation_framework_code": "\n# Generated Selenium Test Code\nfrom selenium import webdriver\nfrom selenium.webdriver.common.by import By\nfrom selenium.webdriver.support.ui import WebDriverWait\nfrom selenium.webdriver.support import expected_conditions as EC\nfrom selenium.webdriver.support.ui import Select\nfrom selenium.webdriver.chrome.service import Service\nfrom selenium.webdriver.chrome.options import Options\nimport unittest\n\nclass GeneratedAutomationTests(unittest.TestCase):\n    \n    def setUp(self):\n        options = Options()\n        options.add_argument(\"--start-maximized\")\n        self.driver = webdriver.Chrome(options=options)\n        self.driver.implicitly_wait(10)\n    \n    def tearDown(self):\n        self.driver.quit()\n    \n\n    def test_tc_001(self):\n        \"\"\"\n        Test: Click \n        Expected: Button should be clickable and trigger appropriate action\n        \"\"\"\n        driver = self.driver\n        \n        # Find element\n        element = None\n        try:\n            if \"login-button\":\n                element = driver.find_element(By.ID, \"login-button\")\n            elif \"//*[@id='login-button']\":\n                element = driver.find_element(By.XPATH, \"//*[@id='login-button']\")\n        except:\n            self.fail(\"Element not found\")\n        \n        # Perform action\n        try:\n            if \"click\" == \"click\":\n                element.click()\n            elif \"click\" == \"input_text\":\n                element.clear()\n                element.send_keys(\"\")\n            elif \"click\" == \"select_dropdown\":\n                select = Select(element)\n                select.select_by_index(1)\n            \n            # Add assertions based on expected results\n            self.assertTrue(True)  # Replace with actual assertion\n        except Exception as e:\n            self.fail(f\"Action failed: {str(e)}\")\n\n    def test_tc_002(self):\n        \"\"\"\n        Test: Hover over \n        Expected: Button should respond to hover with visual feedback\n        \"\"\"\n        driver = self.driver\n        \n        # Find element\n        element = None\n        try:\n            if \"login-button\":\n                element = driver.find_element(By.ID, \"login-button\")\n            elif \"//*[@id='login-button']\":\n                element = driver.find_element(By.XPATH, \"//*[@id='login-button']\")\n        except:\n            self.fail(\"Element not found\")\n        \n        # Perform action\n        try:\n            if \"hover\" == \"click\":\n                element.click()\n            elif \"hover\" == \"input_text\":\n                element.clear()\n                element.send_keys(\"\")\n            elif \"hover\" == \"select_dropdown\":\n                select = Select(element)\n                select.select_by_index(1)\n            \n            # Add assertions based on expected results\n            self.assertTrue(True)  # Replace with actual assertion\n        except Exception as e:\n            self.fail(f\"Action failed: {str(e)}\")\n\n    def test_tc_003(self):\n        \"\"\"\n        Test: Input valid data in user-name\n        Expected: Field should accept valid input\n        \"\"\"\n        driver = self.driver\n        \n        # Find element\n        element = None\n        try:\n            if \"user-name\":\n                element = driver.find_element(By.ID, \"user-name\")\n            elif \"//*[@id='user-name']\":\n                element = driver.find_element(By.XPATH, \"//*[@id='user-name']\")\n        except:\n            self.fail(\"Element not found\")\n        \n        # Perform action\n        try:\n            if \"input_text\" == \"click\":\n                element.click()\n            elif \"input_text\" == \"input_text\":\n                element.clear()\n                element.send_keys(\"Test Data 123\")\n            elif \"input_text\" == \"select_dropdown\":\n                select = Select(element)\n                select.select_by_index(1)\n            \n            # Add assertions based on expected results\n            self.assertTrue(True)  # Replace with actual assertion\n        except Exception as e:\n            self.fail(f\"Action failed: {str(e)}\")\n\n    def test_tc_004(self):\n        \"\"\"\n        Test: Input special characters in user-name\n        Expected: Field should handle special characters appropriately\n        \"\"\"\n        driver = self.driver\n        \n        # Find element\n        element = None\n        try:\n            if \"user-name\":\n                element = driver.find_element(By.ID, \"user-name\")\n            elif \"//*[@id='user-name']\":\n                element = driver.find_element(By.XPATH, \"//*[@id='user-name']\")\n        except:\n            self.fail(\"Element not found\")\n        \n        # Perform action\n        try:\n            if \"input_text\" == \"click\":\n                element.click()\n            elif \"input_text\" == \"input_text\":\n                element.clear()\n                element.send_keys(\"!@#$%^&*()\")\n            elif \"input_text\" == \"select_dropdown\":\n                select = Select(element)\n                select.select_by_index(1)\n            \n            # Add assertions based on expected results\n            self.assertTrue(True)  # Replace with actual assertion\n        except Exception as e:\n            self.fail(f\"Action failed: {str(e)}\")\n\n    def test_tc_005(self):\n        \"\"\"\n        Test: Input valid data in password\n        Expected: Field should accept valid input\n        \"\"\"\n        driver = self.driver\n        \n        # Find element\n        element = None\n        try:\n            if \"password\":\n                element = driver.find_element(By.ID, \"password\")\n            elif \"//*[@id='password']\":\n                element = driver.find_element(By.XPATH, \"//*[@id='password']\")\n        except:\n            self.fail(\"Element not found\")\n        \n        # Perform action\n        try:\n            if \"input_text\" == \"click\":\n                element.click()\n            elif \"input_text\" == \"input_text\":\n                element.clear()\n                element.send_keys(\"Test Data 123\")\n            elif \"input_text\" == \"select_dropdown\":\n                select = Select(element)\n                select.select_by_index(1)\n            \n            # Add assertions based on expected results\n            self.assertTrue(True)  # Replace with actual assertion\n        except Exception as e:\n            self.fail(f\"Action failed: {str(e)}\")\n\n    def test_tc_006(self):\n        \"\"\"\n        Test: Input special characters in password\n        Expected: Field should handle special characters appropriately\n        \"\"\"\n        driver = self.driver\n        \n        # Find element\n        element = None\n        try:\n            if \"password\":\n                element = driver.find_element(By.ID, \"password\")\n            elif \"//*[@id='password']\":\n                element = driver.find_element(By.XPATH, \"//*[@id='password']\")\n        except:\n            self.fail(\"Element not found\")\n        \n        # Perform action\n        try:\n            if \"input_text\" == \"click\":\n                element.click()\n            elif \"input_text\" == \"input_text\":\n                element.clear()\n                element.send_keys(\"!@#$%^&*()\")\n            elif \"input_text\" == \"select_dropdown\":\n                select = Select(element)\n                select.select_by_index(1)\n            \n            # Add assertions based on expected results\n            self.assertTrue(True)  # Replace with actual assertion\n        except Exception as e:\n            self.fail(f\"Action failed: {str(e)}\")\n\n\nif __name__ == '__main__':\n    unittest.main()\n"
            }
        """

cucumber_task = """
    You are provided with the following cucumber test cases content from a .feature file. Your task is to implement the step definitions for these test cases. Each step definition should be tested and verified to ensure it correctly performs the actions described in the feature file. Use appropriate browser automation techniques to interact with web elements, input data, and validate outcomes as specified in the scenarios.
    
    Here is the content of the .feature file:

    URL: https://parabank.parasoft.com/parabank/index.htm
    Feature: Authentication and navigation

    Background:
        Given I am on the Parabank home page

    Scenario: Successful login with valid credentials
        When I login with username "prajus" and password "123456789"
        Then I should see the accounts overview

    Scenario: Login fails with incorrect password
        When I login with username "prajus" and password "wrongpass"
        Then I should see a login error message

    Scenario: Login fails with empty credentials
        When I login with username "" and password ""
        Then I should see a validation or error message

    Scenario: Navigate to Register page from home
        When I follow the Register link
        Then I should be on the registration page

        
    1. Start by navigating to the URL provided.
    2. For each scenario, perform the following steps:
        a. Perform the action specified in the "action" field (e.g., click, input_text).
        b. Log the result of each scenario, indicating whether it passed or failed based on the verification step.
    3. After all scenarios have been executed, provide a summary of the results, including the total number of scenarios, how many passed, and how many failed.

    """
