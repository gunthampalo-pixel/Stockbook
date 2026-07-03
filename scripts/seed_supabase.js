const fs = require('fs');
const path = require('path');
const { createClient } = require('@supabase/supabase-js');

// Load environment variables from .env
require('dotenv').config();

const supabaseUrl = process.env.SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.SUPABASE_KEY;

if (!supabaseUrl || !supabaseKey) {
  console.error('❌ Error: Please specify SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY in your .env file');
  process.exit(1);
}

// Create Supabase client
const supabase = createClient(supabaseUrl, supabaseKey);

async function main() {
  try {
    const dashboardPath = path.join(__dirname, '../dashboard.html');
    if (!fs.existsSync(dashboardPath)) {
      console.error(`❌ Error: dashboard.html not found at: ${dashboardPath}`);
      process.exit(1);
    }

    console.log('📖 Reading dashboard.html to extract STOCKS data...');
    const content = fs.readFileSync(dashboardPath, 'utf8');

    // Find the STOCKS array block
    const arrayStartPattern = 'let STOCKS = [';
    const startIndex = content.indexOf(arrayStartPattern);
    if (startIndex === -1) {
      console.error('❌ Error: Could not find "let STOCKS = [" array in dashboard.html');
      process.exit(1);
    }

    // Locate the closing bracket of the STOCKS array
    const startOfArray = startIndex + arrayStartPattern.length - 1; // Index of '['
    let openBrackets = 1;
    let endOfArray = -1;

    for (let i = startOfArray + 1; i < content.length; i++) {
      if (content[i] === '[') {
        openBrackets++;
      } else if (content[i] === ']') {
        openBrackets--;
        if (openBrackets === 0) {
          endOfArray = i;
          break;
        }
      }
    }

    if (endOfArray === -1) {
      console.error('❌ Error: Could not find closing bracket "]" for STOCKS array.');
      process.exit(1);
    }

    const arrayText = content.substring(startOfArray, endOfArray + 1);
    
    // Parse the JS array content safely
    let stocks = [];
    try {
      stocks = new Function(`return ${arrayText}`)();
    } catch (parseError) {
      console.error('❌ Error parsing STOCKS array text:', parseError.message);
      process.exit(1);
    }

    console.log(`✅ Extracted ${stocks.length} stocks successfully.`);

    console.log('🚀 Seeding data to Supabase (upserting into "stocks" table)...');
    
    // Format records for Postgres table mapping
    const records = stocks.map(s => ({
      ticker: s.ticker,
      name: s.name,
      logo_url: s.logoUrl || null,
      group: s.group || null,
      style: s.style || null,
      market: s.market || 'US',
      target_price: s.targetPrice || null,
      what_it_does: s.whatItDoes || null,
      how_it_makes_money: s.howItMakesMoney || null,
      deals: s.deals || null,
      moat: s.moat || null,
      risks: s.risks || null,
      financials: s.financials || [],
      image_url: s.imageUrl || null,
      why_interest: s.whyInterest || null,
      financials_snapshot: s.financialsSnapshot || null,
      summary: s.summary || null
    }));

    // Upsert batch to Supabase stocks table
    const { data, error } = await supabase
      .from('stocks')
      .upsert(records, { onConflict: 'ticker' });

    if (error) {
      throw error;
    }

    console.log('🎉 Database seeding completed successfully! All stocks have been uploaded to Supabase.');
  } catch (err) {
    console.error('❌ An error occurred during seeding:', err.message);
    process.exit(1);
  }
}

main();
