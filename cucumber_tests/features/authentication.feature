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
