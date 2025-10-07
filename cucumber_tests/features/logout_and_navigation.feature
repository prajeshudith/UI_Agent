Feature: Logout and navigation

  Background:
    Given I am logged in as "prajus" with password "123456789"

  Scenario: Logout returns to home page
    When I logout
    Then I should be on the home page and not see account info

  Scenario: Access account page without login redirects to login
    When I navigate directly to the account activity page without login
    Then I should be redirected to the login page

  Scenario: Session times out and requires re-login
    When my session expires
    Then I should be prompted to login again when navigating protected pages
