# AUTO-GENERATED review and verify selector's

Feature: User Authentication

  Scenario: Successful login with valid credentials
    Given I am on the login page
    When I enter valid credentials
      | username | password     |
      | prajus   | 123456789    |
    And I click the login button
    Then I should be redirected to the account management page

  Scenario: Failed login with invalid credentials
    Given I am on the login page
    When I enter invalid credentials
      | username | password   |
      | prajus   | wrongpass  |
    And I click the login button
    Then I should see an error message

  Scenario: Failed login with empty credentials
    Given I am on the login page
    When I enter empty credentials
      | username | password |
      |          |          |
    And I click the login button
    Then I should see an error message
