Feature: Registration and account opening

  Scenario: Successful new user registration (happy path)
    Given I am on the Parabank home page
    When I go to the Register page
    And I register with required valid details
    Then I should see a registration success message

  Scenario: Registration fails with missing required fields
    Given I am on the Register page
    When I try to register with missing required fields
    Then I should see validation errors

  Scenario: Open a new account after registration
    Given I am a registered user and logged in
    When I open a new Savings account with initial deposit "100.00"
    Then the new account should be created and visible in the accounts list
