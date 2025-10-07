Feature: Accounts and transfers

  Background:
    Given I am logged in as "prajus" with password "123456789"

  Scenario: View account details
    When I go to the Accounts Overview
    Then I should see a list of accounts with balances

  Scenario: View account activity
    When I open the first account
    Then I should see recent transactions

  Scenario: Successful fund transfer between own accounts
    When I transfer 50.00 from account "1" to account "2"
    Then the transfer should be successful and balances updated

  Scenario: Transfer fails with insufficient funds
    When I transfer 1000000.00 from account "1" to account "2"
    Then I should see an insufficient funds message
