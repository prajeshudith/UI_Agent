# features/authentication.feature
# AUTO-GENERATED review and verify selector's

Feature: User Authentication

  Scenario: Successful login with valid credentials
    Given I navigate to "https://parabank.parasoft.com/parabank/index.htm"
    When I enter "prajus" as username
    And I enter "123456789" as password
    And I click on "Log In"
    Then I should see the account management page

  Scenario: Failed login with invalid credentials
    Given I navigate to "https://parabank.parasoft.com/parabank/index.htm"
    When I enter "prajus" as username
    And I enter "wrongpass" as password
    And I click on "Log In"
    Then I should see an error message

  Scenario: Failed login with empty credentials
    Given I navigate to "https://parabank.parasoft.com/parabank/index.htm"
    When I enter "" as username
    And I enter "" as password
    And I click on "Log In"
    Then I should see an error message
