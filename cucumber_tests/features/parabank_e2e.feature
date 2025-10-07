Feature: ParaBank end-to-end flows (written after inspecting live pages)

  This feature contains 20 scenarios that were authored after inspecting the live ParaBank pages
  and exercising the main authenticated flows (login, transfer, bill pay, open account, find
  transactions, update profile, request loan, lookup). The scenarios use the observed form fields
  and behaviors. Run these with your step definitions that map to the described actions.

  Background:
    Given I am on the Parabank home page

  # 1 - Successful login
  Scenario: Successful login with valid credentials
    When I login with username "prajus" and password "123456789"
    Then I should see the "Accounts Overview" heading and an accounts table

  # 2 - Empty credentials validation (observed exact message)
  Scenario: Login validation shows exact message for empty credentials
    When I login with username "" and password ""
    Then I should see an error page with heading "Error!"
    And I should see the text "Please enter a username and password."

  # 3 - Invalid credentials (authentication error)
  Scenario: Login fails with incorrect password
    When I login with username "prajus" and password "wrongpass"
    Then I should see an error indication (error heading or message)

  # 4 - Registration page presence and fields
  Scenario: Navigate to the Register page and check required fields
    When I go to the Register page
    Then I should see registration fields including "First Name", "Last Name", "Username", "Password", and "Confirm"

  # 5 - Registration negative: missing required fields
  Scenario: Registration fails when required fields are missing
    Given I am on the Register page
    When I submit the registration form with missing required fields
    Then I should see validation responses for required fields

  # 6 - Registration positive (happy path)
  Scenario: Successful registration with valid details
    Given I am on the Register page
    When I register with valid and complete details
    Then I should see a registration success confirmation

  # 7 - Open new account (observed note about minimum deposit)
  Scenario: Open a new Savings account with required minimum deposit
    Given I am logged in as "prajus" with password "123456789"
    When I open a new Savings account with an initial deposit of "100.00"
    Then I should see the new account appear in Accounts Overview

  # 8 - Accounts overview displays account rows
  Scenario: Accounts Overview shows account numbers and balances
    Given I am logged in as "prajus" with password "123456789"
    When I go to the Accounts Overview
    Then I should see at least one account number (e.g. "14343") and a balance column

  # 9 - Open account activity page
  Scenario: Open account activity by clicking an account number
    Given I am logged in as "prajus" with password "123456789"
    When I click an account number link from the Accounts Overview
    Then I should be on an account activity page showing transactions

  #10 - Transfer happy path (fields observed: amount input id/name and from/to selects)
  Scenario: Transfer funds between accounts (happy path)
    Given I am logged in as "prajus" with password "123456789"
    When I go to the Transfer Funds page
    And I enter amount "1.00" into the Amount field (input id "amount")
    And I choose a From account and To account from the account selects (ids "fromAccountId" and "toAccountId")
    And I submit the transfer
    Then I should see a transfer confirmation or an error message indicating why the transfer failed

  #11 - Transfer negative: insufficient funds
  Scenario: Transfer fails due to insufficient funds
    Given I am logged in as "prajus" with password "123456789"
    When I attempt to transfer a very large amount "1000000.00" between accounts
    Then I should see a transfer-specific error or rejection message

  #12 - Bill Pay page fields (observed names)
  Scenario: Bill Pay form contains expected payee fields
    Given I am logged in as "prajus" with password "123456789"
    When I go to the Bill Pay page
    Then I should see inputs with names: "payee.name", "payee.address.street", "payee.address.city", "payee.address.state", "payee.address.zipCode", "amount", and a "fromAccountId" select

  #13 - Bill payment happy path
  Scenario: Successful bill payment records a confirmation
    Given I am logged in as "prajus" with password "123456789"
    When I go to Bill Pay and submit a valid payee name, account, and amount (e.g. "75.50")
    Then I should see a bill payment confirmation or a recorded transaction

  #14 - Bill pay validation for invalid amount
  Scenario: Bill Pay validation fails for invalid amount
    Given I am logged in as "prajus" with password "123456789"
    When I try to pay a bill with amount "-10"
    Then I should see a validation error for the amount field

  #15 - Find Transactions (date format observed: MM-DD-YYYY)
  Scenario: Find transactions by date range
    Given I am logged in as "prajus" with password "123456789"
    When I go to Find Transactions and search account "14343" between dates "01-01-2025" and "12-31-2025"
    Then I should see transactions that fall within the specified date range or a message indicating none were found

  #16 - Update profile fields and confirmation
  Scenario: Update contact information successfully
    Given I am logged in as "prajus" with password "123456789"
    When I go to Update Profile and change my phone number and address
    And I submit the Update Profile form
    Then I should see a profile update confirmation and the new details present on the page

  #17 - Request Loan validation
  Scenario: Request Loan shows validation when required fields missing
    Given I am logged in as "prajus" with password "123456789"
    When I go to Request Loan and submit with missing Loan Amount or Down Payment
    Then I should see validation errors for the loan form

  #18 - Request Loan happy path (form observed: loan amount, down payment, from account select)
  Scenario: Apply for a loan using available account
    Given I am logged in as "prajus" with password "123456789"
    When I go to Request Loan and submit Loan Amount "5000" and Down Payment "500"
    Then I should see a loan application confirmation or a result message

  #19 - Logout behaviour
  Scenario: Logout returns to home/login and hides account services
    Given I am logged in as "prajus" with password "123456789"
    When I click "Log Out"
    Then I should be back on the login/home page and not see Account Services links

  #20 - Forgot login info lookup
  Scenario: Use the Forgot login info lookup by name
    When I follow the "Forgot login info?" link and search using a name (e.g. "John")
    Then I should see either matching records or a message that no records were found
