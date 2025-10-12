// step_definitions/authentication_steps.js
// AUTO-GENERATED review and verify selector's

const { Given, When, Then } = require('@cucumber/cucumber');
const { expect } = require('chai');

Given('I navigate to {string}', async function (url) {
    await page.goto(url);
});

When('I enter {string} as username', async function (username) {
    await page.fill('input[name="username"]', username); // Using name attribute for stability
});

When('I enter {string} as password', async function (password) {
    await page.fill('input[name="password"]', password); // Using name attribute for stability
});

When('I click on {string}', async function (buttonText) {
    await page.click(`button:has-text("${buttonText}")`); // Using text selector for button
});

Then('I should see the account management page', async function () {
    const title = await page.title();
    expect(title).to.include('Account Management'); // Adjust based on actual title
});

Then('I should see an error message', async function () {
    const errorMessage = await page.locator('.error-message').innerText(); // Adjust selector based on actual error message element
    expect(errorMessage).to.not.be.empty;
});
