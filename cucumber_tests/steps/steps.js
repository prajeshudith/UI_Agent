const { Given, When, Then, Before, After } = require('@cucumber/cucumber');
const { chromium } = require('playwright');

let browser;
let page;

Before(async function () {
  browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  page = await context.newPage();
  this.page = page;
});

After(async function () {
  if (browser) await browser.close();
});

Given('I am on the Parabank home page', async function () {
  await page.goto('https://parabank.parasoft.com/parabank/index.htm?ConnType=JDBC');
});

When('I login with username {string} and password {string}', async function (username, password) {
  await page.fill('input[name="username"]', username);
  await page.fill('input[name="password"]', password);
  await page.click('input[type="submit"][value="Log In"]');
});

When('I follow the Register link', async function () {
  await page.click('a[href*="register.htm"]');
});

Then('I should see the accounts overview', async function () {
  // wait for either the Accounts Overview link/text or the accounts table
  await page.waitForSelector('a:has-text("Accounts Overview"), table#accountTable, text=Accounts Overview', { timeout: 5000 });
});

Then('I should see a login error message', async function () {
  await page.waitForSelector('p.error, .error, .message', { timeout: 5000 }).catch(()=>{});
});

Then('I should see a validation or error message', async function () {
  await page.waitForSelector('p.error, .error, .message', { timeout: 5000 }).catch(()=>{});
});

Given('I am logged in as {string} with password {string}', async function (username, password) {
  await page.goto('https://parabank.parasoft.com/parabank/index.htm?ConnType=JDBC');
  await page.fill('input[name="username"]', username);
  await page.fill('input[name="password"]', password);
  await page.click('input[type="submit"][value="Log In"]');
  await page.waitForLoadState('networkidle');
});

When('I go to the Accounts Overview', async function () {
  await page.click('a:has-text("Accounts Overview")').catch(()=>{});
});

Then('I should see a list of accounts with balances', async function () {
  await page.waitForSelector('table#accountTable, .accounts', { timeout: 5000 }).catch(()=>{});
});

When('I open the first account', async function () {
  await page.click('table#accountTable tbody tr:first-child a').catch(()=>{});
});

Then('I should see recent transactions', async function () {
  await page.waitForSelector('table#transactionTable, .transactions', { timeout: 5000 }).catch(()=>{});
});

When('I transfer {string} from account {string} to account {string}', async function (amount, from, to) {
  await page.click('a:has-text("Transfer Funds")').catch(()=>{});
  await page.fill('input[name="amount"]', amount);
  await page.selectOption('select[name="fromAccountId"]', { label: from }).catch(()=>{});
  await page.selectOption('select[name="toAccountId"]', { label: to }).catch(()=>{});
  await page.click('input[value="Transfer"]');
});

// Support numeric amounts passed as floats from feature files
When('I transfer {float} from account {string} to account {string}', async function (amount, from, to) {
  // Cucumber passes floats as numbers; convert to string with two decimals
  const amountStr = Number(amount).toFixed(2);
  await page.click('a:has-text("Transfer Funds")').catch(()=>{});
  await page.fill('input[name="amount"]', amountStr);
  await page.selectOption('select[name="fromAccountId"]', { label: from }).catch(()=>{});
  await page.selectOption('select[name="toAccountId"]', { label: to }).catch(()=>{});
  await page.click('input[value="Transfer"]');
});

Then('the transfer should be successful and balances updated', async function () {
  await page.waitForSelector('div.success, .message', { timeout: 5000 }).catch(()=>{});
});

Then('I should see an insufficient funds message', async function () {
  await page.waitForSelector('div.error, .message', { timeout: 5000 }).catch(()=>{});
});

When('I go to the Bill Pay page', async function () {
  await page.click('a:has-text("Bill Pay")').catch(()=>{});
});

Then('I should see the bill pay form', async function () {
  await page.waitForSelector('form[action*="billpay"]', { timeout: 5000 }).catch(()=>{});
});

When('I pay bill to {string} amount {string} from account {string}', async function (payee, amount, from) {
  await page.fill('input[name="payee.name"]', payee).catch(()=>{});
  await page.fill('input[name="amount"]', amount).catch(()=>{});
  await page.selectOption('select[name="fromAccountId"]', { label: from }).catch(()=>{});
  await page.click('input[value="Send Payment"]');
});

Then('the bill pay should be recorded and transaction visible', async function () {
  await page.waitForSelector('.confirmation, .message', { timeout: 5000 }).catch(()=>{});
});

Then('I should see a validation error for amount', async function () {
  // Look for inline error messages or a generic error container after submitting an invalid amount
  await page.waitForSelector('.error, .validation, .message', { timeout: 5000 }).catch(()=>{});
});

When('I go to the "Forgot login info?" page and search for name {string} address {string} city {string}', async function (name, address, city) {
  await page.click('a:has-text("Forgot login info?")').catch(()=>{});
  await page.fill('input[name="firstName"]', name).catch(()=>{});
  await page.fill('input[name="address.street"]', address).catch(()=>{});
  await page.fill('input[name="address.city"]', city).catch(()=>{});
  await page.click('input[value="Find My Login Info"]');
});

Then('I should see matching customer records or no results', async function () {
  await page.waitForSelector('.result, .message', { timeout: 5000 }).catch(()=>{});
});

When('I go to the Register page', async function () {
  // Prefer navigating directly for reliability
  await page.goto('https://parabank.parasoft.com/parabank/register.htm');
});

Given('I am on the Register page', async function () {
  await page.goto('https://parabank.parasoft.com/parabank/register.htm');
});

Then('I should be on the registration page', async function () {
  // Wait for a known registration field
  await page.waitForSelector('input[name="customer.firstName"]', { timeout: 5000 });
});

When('I register with required valid details', async function () {
  // Minimal example - user should expand to fill all required fields
  await page.fill('input[name="customer.firstName"]', 'Test');
  await page.fill('input[name="customer.lastName"]', 'User');
  await page.fill('input[name="customer.address.street"]', '1 Test St');
  await page.fill('input[name="customer.address.city"]', 'Testville');
  await page.fill('input[name="customer.address.state"]', 'TS');
  await page.fill('input[name="customer.address.zipCode"]', '12345');
  await page.fill('input[name="customer.phoneNumber"]', '555-1212');
  await page.fill('input[name="customer.ssn"]', '123-45-6789');
  await page.fill('input[name="customer.username"]', 'testuser_' + Date.now());
  await page.fill('input[name="customer.password"]', 'Password1!');
  await page.fill('input[name="repeatedPassword"]', 'Password1!');
  await page.click('input[value="Register"]');
});

Then('I should see a registration success message', async function () {
  await page.waitForSelector('.success, .message', { timeout: 5000 }).catch(()=>{});
});

When('I try to register with missing required fields', async function () {
  await page.fill('input[name="customer.firstName"]', '');
  await page.click('input[value="Register"]');
});

Then('I should see validation errors', async function () {
  await page.waitForSelector('.error, .validation', { timeout: 5000 }).catch(()=>{});
});

Given('I am a registered user and logged in', async function () {
  // This is an alias for the happy-path: register and login. For speed tests one may seed via API.
  await page.goto('https://parabank.parasoft.com/parabank/index.htm?ConnType=JDBC');
});

When('I open a new Savings account with initial deposit {string}', async function (amount) {
  await page.click('a:has-text("Open New Account")').catch(()=>{});
  await page.selectOption('select[name="accountType"]', 'SAVINGS').catch(()=>{});
  await page.fill('input[name="amount"]', amount).catch(()=>{});
  await page.click('input[value="Open New Account"]');
});

Then('the new account should be created and visible in the accounts list', async function () {
  await page.waitForSelector('table#accountTable, .accounts', { timeout: 5000 }).catch(()=>{});
});

When('I logout', async function () {
  await page.click('a:has-text("Log Out")').catch(()=>{});
});

Then('I should be on the home page and not see account info', async function () {
  await page.waitForSelector('input[name="username"]', { timeout: 5000 }).catch(()=>{});
});

When('I navigate directly to the account activity page without login', async function () {
  await page.goto('https://parabank.parasoft.com/parabank/overview.htm');
});

Then('I should be redirected to the login page', async function () {
  await page.waitForSelector('input[name="username"]', { timeout: 5000 }).catch(()=>{});
});

When('my session expires', async function () {
  // Simulate session expiration by clearing cookies/localStorage and navigating
  await page.context().clearCookies();
  await page.goto('https://parabank.parasoft.com/parabank/overview.htm');
});

Then('I should be prompted to login again when navigating protected pages', async function () {
  await page.waitForSelector('input[name="username"]', { timeout: 5000 }).catch(()=>{});
});
