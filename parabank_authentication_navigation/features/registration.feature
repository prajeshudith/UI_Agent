# features/registration.feature
# AUTO-GENERATED review and verify selector's

Feature: User Registration Navigation

  Scenario: Navigate to registration page
    Given I navigate to "https://parabank.parasoft.com/parabank/index.htm"
    When I click on "Register"
    Then I should see the registration page
