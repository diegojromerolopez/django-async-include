const puppeteer = require('puppeteer');

(async () => {
  const url = process.argv[2];
  if (!url) {
    console.error('No target URL provided');
    process.exit(1);
  }

  console.log(`Launching browser and navigating to: ${url}/test-page/`);
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  try {
    // 1. Fetch raw HTML from the server first to verify that the template content is NOT in the initial payload
    const resHtml = await fetch(`${url}/test-page/`);
    const htmlText = await resHtml.text();
    if (htmlText.includes('Hello from Async Include!')) {
      throw new Error('Template content was found in the initial HTML response. It must be loaded asynchronously.');
    }
    console.log('Verified: Template content is not in the initial HTML response.');

    // 2. Open the page in Puppeteer to let Javascript execute and load the template asynchronously
    const page = await browser.newPage();
    await page.goto(`${url}/test-page/`, { waitUntil: 'networkidle0' });
    
    // Wait for the h1 element inside our async-included template to be rendered
    await page.waitForSelector('h1', { timeout: 10000 });
    
    const h1Text = await page.$eval('h1', el => el.textContent);
    console.log(`Found H1 text: ${h1Text}`);
    
    if (h1Text !== 'Hello from Async Include!') {
      throw new Error(`Expected 'Hello from Async Include!', but got '${h1Text}'`);
    }
    
    console.log('E2E test passed successfully!');
    await browser.close();
    process.exit(0);
  } catch (err) {
    console.error('E2E test failed:', err);
    await browser.close();
    process.exit(1);
  }
})();
