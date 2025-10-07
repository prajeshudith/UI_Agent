Feature: Bill Pay and Customer Lookup

  Background:
    Given I am logged in as "prajus" with password "123456789"

  Scenario: Navigate to Bill Pay page
    When I go to the Bill Pay page
    Then I should see the bill pay form

  Scenario: Successful bill payment
    When I pay bill to "Electric Co" amount "75.50" from account "1"
    Then the bill pay should be recorded and transaction visible

  Scenario: Bill payment fails with invalid amount
    When I pay bill to "Electric Co" amount "-10" from account "1"
    Then I should see a validation error for amount

  Scenario: Lookup customer by name
    When I go to the "Forgot login info?" page and search for name "John" address "" city ""
    Then I should see matching customer records or no results
