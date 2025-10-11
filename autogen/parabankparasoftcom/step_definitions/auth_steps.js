// AUTO-GENERATED review and verify selector's

const { Given, When, Then } = require('@cucumber/cucumber');
const { expect } = require('@playwright/test');

Given('I am on the login page', async function() {
    await page.goto('https://parabank.parasoft.com/parabank/index.htm');
});

When('I enter valid credentials', async function(dataTable) {
    const data = dataTable.rowsHash();
    await page.fill('input[name="username"]', data.username);
    await page.fill('input[name="password"]', data.password);
});

When('I enter invalid credentials', async function(dataTable) {
    const data = dataTable.rowsHash();
    await page.fill('input[name="username"]', data.username);
    await page.fill('input[name="password"]', data.password);
});

When('I enter empty credentials', async function(dataTable) {
    const data = dataTable.rowsHash();
    await page.fill('input[name="username"]', data.username);
    await page.fill('input[name="password"]', data.password);
});

When('I click the login button', async function() {
    await page.click('input[type="submit"]'); // Button to log in
});

Then('I should be redirected to the account management page', async function() {
    await page.waitForURL('**/account.htm'); // Adjust the URL as necessary
});

Then('I should see an error message', async function() {
    const errorMessage = await page.locator('.error'); // Adjust selector based on actual error message element
    expect(await errorMessage.isVisible()).toBeTruthy();
});

When('I click on the register link', async function() {
    await page.click('a:has-text("Register")'); // Link to registration page
});

Then('I should be redirected to the registration page', async function() {
    await page.waitForURL('**/register.htm'); // Adjust the URL as necessary
});