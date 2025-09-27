from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from sqlalchemy import Extract
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from collections import defaultdict

class WebPageAutomation:
    def __init__(self, url=None, headless=False):
        """
        Initialize the automation class
        Args:
        url (str, optional): The URL to navigate to
        headless (bool): Run browser in headless mode
        """

        # Setup Chrome options
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')

        # Initialize the Chrome driver
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.element_cache = {}  # Cache to store the actual WebElement objects.

        if url:
            self.navigate_to(url)

    def navigate_to(self, url):
        """
        Navigate to a specific URL
        Args:
        url (str): The URL to navigate to
        """
        self.driver.get(url)
        time.sleep(2)  # Wait for the page to load

    def extract_page_elements(self):
        """
        Extracts various types of elements from the current page and stores them for later use

        Returns:
            dict: Dictionary containing all extracted elements categorized by type
        """
        print(f"Extracting elements from current page...")

        # Clear previous cache
        self.element_cache = defaultdict(list)
        elements_info = defaultdict(list)

        # Extract text elements
        print("Extracting text elements...")
        for tag in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span', 'div', 'label']:
            elements = self.driver.find_elements(By.TAG_NAME, tag)
            for idx, element in enumerate(elements):
                try:
                    text = element.text.strip()
                    if text:  # Only include elements with text
                        element_id = f"{tag}_{idx}"
                        self.element_cache['text'].append({'id': element_id, 'element': element})

                        # Get XPath
                        xpath = self._generate_xpath(element)
                        elements_info['text'].append({
                            'tag': tag,
                            'id': element_id,
                            'text': text,
                            'xpath': xpath,
                            'location': element.location,
                            'size': element.size
                        })
                except:
                    continue

        # Extract buttons
        print("Extracting buttons...")
        buttons = self.driver.find_elements(By.TAG_NAME, 'button')

        for idx, button in enumerate(buttons):
            try:
                element_id = f"button_{idx}"
                self.element_cache['buttons'].append({'id': element_id, 'element': button})
                xpath = self._generate_xpath(button)
                elements_info['buttons'].append({
                    'id': element_id,
                    'text': button.text.strip(),
                    'xpath': xpath,
                    'location': button.location,
                    'size': button.size,
                    'is_enabled': button.is_enabled()
                })
            except:
                continue

        # Also look for elements with button roles
        role_buttons = self.driver.find_elements(By.XPATH, '//*[@role="button"]')
        for idx, button in enumerate(role_buttons):
            try:
                element_id = f"role_button_{idx}"
                self.element_cache['buttons'].append({'id': element_id, 'element': button})
                xpath = self._generate_xpath(button)
                elements_info['buttons'].append({
                    'id': element_id,
                    'text': button.text.strip(),
                    'xpath': xpath,
                    'location': button.location,
                    'size': button.size,
                    'is_enabled': button.is_enabled()
                })
            except:
                continue

        # Extract input fields
        print("Extracting input fields...")
        inputs = self.driver.find_elements(By.TAG_NAME, 'input')

        for idx, input_field in enumerate(inputs):
            try:
                element_id = f"input_{idx}"
                field_type = input_field.get_attribute('type')
                self.element_cache['input_fields'].append({'id': element_id, 'element': input_field})
                xpath = self._generate_xpath(input_field)
                elements_info['input_fields'].append({
                    "id": element_id,
                    'type': field_type,
                    "name": input_field.get_attribute('name'),
                    "xpath": xpath,
                    "html_id": input_field.get_attribute('id'),
                    'placeholder': input_field.get_attribute('placeholder'),
                    'location': input_field.location,
                    'size': input_field.size,
                    "is_enabled": input_field.is_enabled()
                })
            except:
                continue

        # Extract text areas
        print("Extracting text areas...")
        textareas = self.driver.find_elements(By.TAG_NAME, 'textarea')

        for idx, textarea in enumerate(textareas):
            try:
                element_id = f'textarea_{idx}'
                self.element_cache['textareas'].append({'id': element_id, 'element': textarea})
                xpath = self.generate_xpath(textarea)
                elements_info['textareas'].append({
                    "id": element_id,
                    "name": textarea.get_attribute('name'),
                    "xpath": xpath,
                    "html_id": textarea.get_attribute('id'),
                    'placeholder': textarea.get_attribute('placeholder'),
                    'location': textarea.location,
                    'size': textarea.size,
                    "is_enabled": textarea.is_enabled()
                })
            except:
                continue

        # Extract dropdowns (select elements)
        print("Extracting dropdowns...")
        dropdowns = self.driver.find_elements(By.TAG_NAME, 'select')

        for idx, dropdown in enumerate(dropdowns):
            try:
                element_id = f"select_{idx}"
                self.element_cache["dropdowns"].append({'id': element_id, 'element': dropdown})
                options = []

                for option_idx, option in enumerate(dropdown.find_elements(By.TAG_NAME, 'option')):
                    option_id = f"{element_id}_option_{option_idx}"
                    self.element_cache["options"].append({'id': option_id, 'element': option})
                    options.append({
                        "text": option.text,
                        "id": option_id,
                        "value": option.get_attribute("value")
                    })

                xpath = self._generate_xpath(dropdown)
                elements_info["dropdowns"].append({
                    "id": element_id,
                    "name": dropdown.get_attribute('name'),
                    "html_id": dropdown.get_attribute("id"),
                    "xpath": xpath,
                    "options": options,
                    "location": dropdown.location,
                    "size": dropdown.size
                })
            except:
                continue

        # Extract links
        print("Extracting links...")
        links = self.driver.find_elements(By.TAG_NAME, 'a')

        for idx, link in enumerate(links):
            try:
                href = link.get_attribute('href')
                if href:  # Only include links with actual hrefs
                    element_id = f"link_{idx}"
                    self.element_cache['links'].append({'id': element_id, 'element': link})
                    xpath = self._generate_xpath(link)
                    elements_info['links'].append({
                        'id': element_id,
                        'text': link.text.strip(),
                        'href': href,
                        'xpath': xpath,
                        'location': link.location,
                        'size': link.size
                    })
            except:
                continue

        print("Element extraction completed. Found:")
        for element_type, items in elements_info.items():
            print(f"{len(items)} {element_type}")
        
        return dict(elements_info)

    def _generate_xpath(self, element):
        """Generate an XPath for an element (fallback for interaction)"""

        try:
            return self.driver.execute_script("""
            function getElementXPath(element) {
            if (element && element.id)
                return '//*[@id="' + element.id + '"]';

            var paths = [];
            for (; element && element.nodeType === Node.ELEMENT_NODE; element = element.parentNode) {
                var index = 0;
                var hasFollowingSiblings = false;

                for (var sibling = element.previousSibling; sibling; sibling = sibling.previousSibling) {
                    if (sibling.nodeType === Node.DOCUMENT_TYPE_NODE) continue;
                    if (sibling.nodeName === element.nodeName) {
                        ++index;
                    }
                var tagName = element.nodeName.toLowerCase();
                var pathIndex = (index ? "[" + (index + 1) + "]" : "");
                paths.unshift(tagName + pathIndex);
            }

            return "/" + paths.join("/");
            return getElementXPath(arguments[0]);
            """,
            element)

        except:
            return None

    def interact_with_element(self, element_type, element_id, action="click", value=None):
        """
        Interact with a specific element

        Args:
            element_type (str): Type of element (buttons, input fields, etc.)
            element_id (str): ID of the element as returned from extract_page_elements
            action (str): Action to perform ('click', 'type', 'select', etc.)
            value (str, optional): Value to use for typing or selecting

        Returns:
            bool: Appropriate message indicating success or failure
        """
        # Find the element in cache
        element_obj = None
        for item in self.element_cache.get(element_type, []):
            if item['id'] == element_id:
                element_obj = item['element']
                break

        if not element_obj:
            print(f"Element ({element_id}) not found in cache")
            return f"Element ({element_id}) not found in cache", False

        try:
            # Scroll element into View
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element_obj)
            time.sleep(0.5)

            # Perform the requested action
            if action == "click":
                # Try direct click first
                try:
                    element_obj.click()
                    return f"Clicked on {element_type} ({element_id})", True
                except:
                    # If direct click fails, try using JavaScript
                    print(f"Direct click failed for {element_type} ({element_id}), trying JavaScript click...")
                    self.driver.execute_script("arguments[0].click();", element_obj)
                    return f"Clicked on {element_type} ({element_id}) using JavaScript", True

            elif action == "type":
                if value is None:
                    return "Error 'value' parameter is required for 'type' action", False
                try:
                    element_obj.clear()
                    element_obj.send_keys(value)
                    return f"Typed '{value}' into {element_type} ({element_id})", True
                except Exception as e:
                    return f"Failed to type into {element_type} ({element_id}): {str(e)}", False

            elif action == "select":
                if value is None:
                    return "Error 'value' parameter is required for 'select' action", False
                try:
                    from selenium.webdriver.support.ui import Select
                    select = Select(element_obj)
                    select.select_by_visible_text(value)
                    return f"Selected option '{value}' in {element_type} ({element_id})", True
                except Exception as e:
                    return f"Failed to select option in {element_type} ({element_id}): {str(e)}", False

            elif action == "get_text":
                try:
                    text = element_obj.text.strip()
                    return f"Text of {element_type} ({element_id}): {text}", True
                except Exception as e:
                    return f"Failed to get text from {element_type} ({element_id}): {str(e)}", False
                
            elif action == "get_attribute":
                if value is None:
                    return "Error 'value' parameter is required for 'get_attribute' action", False
                try:
                    attr_value = element_obj.get_attribute(value)
                    return f"Attribute '{value}' of {element_type} ({element_id}): {attr_value}", True
                except Exception as e:
                    return f"Failed to get attribute from {element_type} ({element_id}): {str(e)}", False
                
            else:
                return "Didn't find a valid action from the provided options (click, type, select, get_text, get_attribute)", False
            
        except Exception as e:
            return f"Error interacting with {element_type} ({element_id}): {str(e)}", False

    def interact_by_xpath(self, xpath, action, value=None):
        """
        Interact with an element using XPath (useful when element cache is stale)

        Args:
            xpath (str): XPath of the element
            action (str): Action to perform
            value (str, optional): Value to use for typing or selecting

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Wait for element to be present and visible
            wait = WebDriverWait(self.driver, 10)
            element = wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))

            # Scroll element into view
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.5)

            # Perform the requested action
            if action == 'click':
                element.click()
            elif action == 'type':
                if value is None:
                    print("Error: 'value' parameter is required for 'type' action")
                    return False
                element.clear()
                element.send_keys(value)
            elif action == 'select':
                if value is None:
                    print("Error: 'value' parameter is required for 'select' action")
                    return False
                from selenium.webdriver.support.ui import Select
                Select(element).select_by_visible_text(value)
            elif action == 'get_text':
                return element.text
            elif action == 'get_attribute':
                if value is None:
                    print("Error: 'value' parameter is required for 'get_attribute' action")
                    return False
                return element.get_attribute(value)
            else:
                print("Didn't find a valid action from the provided options (click, type, select, get_text, get_attribute)")
                return False

            return True

        except Exception as e:
            print(f"Error interacting with element by XPath ({xpath}): {str(e)}")
            return False

    def close(self):
        """Close the browser and cleanup"""
        if self.driver:
            self.driver.quit()
            print("Browser closed.")