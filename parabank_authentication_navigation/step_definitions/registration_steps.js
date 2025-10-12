// step_definitions/registration_steps.js
// AUTO-GENERATED review and verify selector's

const { Given, When, Then } = require('@cucumber/cucumber');
const { expect } = require('chai');

When('I click on {string}', async function (linkText) {
    await page.click(`a:has-text("${linkText}")`); // Using text selector for link
});

Then('I should see the registration page', async function () {
    const title = await page.title();
    expect(title).to.include('Registration'); // Adjust based on actual title
});
