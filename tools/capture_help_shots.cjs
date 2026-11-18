/**
 * Capture the screenshots used by the help pages from the real Yaaddi app.
 *
 * 1. In the app folder, start the web build:   npx expo start --web --port 8081
 * 2. From the Website folder, run:             node tools/capture_help_shots.cjs
 * 3. Convert to web images:                    python tools/make_help_images.py
 *
 * Needs the app's Playwright (installed in the app's node_modules) and the python-basics
 * course zip from the yaaddi-courses repo. Output: tools/source/help/*.png (780x1688, light theme).
 * Environment overrides: APP_DIR, COURSE_ZIP, APP_URL.
 */
const path = require('path');
const fs = require('fs');

const ROOT = path.resolve(__dirname, '..', '..');
const APP_DIR = process.env.APP_DIR || path.join(ROOT, 'app');
const COURSE_ZIP = process.env.COURSE_ZIP || path.join(ROOT, 'yaaddi-courses', 'python-basics', 'python-basics.zip');
const APP_URL = process.env.APP_URL || 'http://localhost:8081/';
const OUT = path.join(__dirname, 'source', 'help');
fs.mkdirSync(OUT, { recursive: true });

const { chromium } = require(path.join(APP_DIR, 'node_modules', '@playwright/test'));

const CARD = '[data-testid^="course-card-"]:not([data-testid^="course-card-menu"]):not([data-testid^="course-card-image"])';

(async () => {
  const browser = await chromium.launch();
  const context = await browser.newContext({
    viewport: { width: 390, height: 844 },
    deviceScaleFactor: 2,
    colorScheme: 'light',
  });
  const page = await context.newPage();
  page.setDefaultTimeout(20000);
  const failures = [];

  const snap = async (name) => {
    // The date simulator is a development-only control; keep it out of the pictures.
    await page.addStyleTag({ content: '[data-testid=date-simulator]{display:none!important}' }).catch(() => {});
    await page.waitForTimeout(700);
    await page.screenshot({ path: path.join(OUT, `${name}.png`) });
    console.log('captured', name);
  };
  const step = async (name, fn) => {
    try { await fn(); await snap(name); } catch (e) { failures.push(name); console.log('FAILED', name, String(e).split('\n')[0]); }
  };
  const tab = (name) => page.getByRole('tab', { name }).first().click();
  const home = async () => { await page.goto(APP_URL); await page.getByTestId('learn-more-button').waitFor({ timeout: 60000 }); };
  const goLearn = async () => { await tab('Learn'); await page.waitForTimeout(500); };

  await page.goto(APP_URL);
  await page.getByTestId('learn-more-button').waitFor({ timeout: 60000 });

  await page.getByTestId('learn-more-button').click();
  const chooser = page.waitForEvent('filechooser');
  await page.locator('[data-testid^="action-menu-"]:not([data-testid$="backdrop"])').nth(1).click();
  await (await chooser).setFiles(COURSE_ZIP);
  await page.locator(CARD).first().waitFor({ timeout: 120000 });

  await step('learn-courses', async () => {});
  await step('more-actions-menu', async () => { await page.getByTestId('learn-more-button').click(); });
  await page.keyboard.press('Escape');
  await page.getByTestId('action-menu-cancel').click({ timeout: 2000 }).catch(() => {});
  await step('course-card-menu', async () => { await page.locator('[data-testid^="course-card-menu-"]').first().click(); });
  await page.getByTestId('action-menu-cancel').click({ timeout: 2000 }).catch(() => {});

  await step('course-map', async () => { await page.locator(CARD).first().click(); await page.waitForTimeout(800); });
  await step('placement', async () => { await page.getByTestId('learn-placement').click(); });
  await home();

  await step('streak-info', async () => { await page.getByTestId('streak-info-button').click(); });
  await home();

  await step('settings', async () => { await tab('Settings'); });
  await step('settings-advanced', async () => { await page.getByTestId('settings-advanced-toggle').click(); await page.getByTestId('settings-advanced-toggle').scrollIntoViewIfNeeded(); });
  await step('stats', async () => { await tab('Stats'); });

  await goLearn();
  await step('library', async () => { await goLearn(); await page.getByTestId('course-library-button').click(); await page.waitForTimeout(3500); });
  await home();
  await step('create-course', async () => {
    await goLearn();
    await page.getByTestId('learn-more-button').click();
    await page.locator('[data-testid^="action-menu-"]:not([data-testid$="backdrop"])').nth(0).click();
  });

  await browser.close();
  if (failures.length) { console.log('Failed shots:', failures.join(', ')); process.exitCode = 1; }
})();
