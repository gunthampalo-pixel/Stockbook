import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { createClient } from "@supabase/supabase-js";
import "dotenv/config";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const supabaseUrl = process.env.SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.SUPABASE_KEY;

if (!supabaseUrl || !supabaseKey) {
  console.error("Error: Please specify SUPABASE_URL and SUPABASE_KEY in your .env file");
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseKey);

function extractStocksFromDashboard(content) {
  const arrayStartPattern = "let STOCKS = [";
  const startIndex = content.indexOf(arrayStartPattern);
  if (startIndex === -1) {
    throw new Error('Could not find "let STOCKS = [" array in dashboard.html');
  }

  const startOfArray = startIndex + arrayStartPattern.length - 1;
  let openBrackets = 1;
  let endOfArray = -1;

  for (let i = startOfArray + 1; i < content.length; i++) {
    if (content[i] === "[") {
      openBrackets++;
    } else if (content[i] === "]") {
      openBrackets--;
      if (openBrackets === 0) {
        endOfArray = i;
        break;
      }
    }
  }

  if (endOfArray === -1) {
    throw new Error('Could not find closing bracket "]" for STOCKS array.');
  }

  return new Function(`return ${content.substring(startOfArray, endOfArray + 1)}`)();
}

async function main() {
  const dashboardPath = path.join(__dirname, "../dashboard.html");
  if (!fs.existsSync(dashboardPath)) {
    throw new Error(`dashboard.html not found at: ${dashboardPath}`);
  }

  console.log("Reading dashboard.html to extract STOCKS data...");
  const stocks = extractStocksFromDashboard(fs.readFileSync(dashboardPath, "utf8"));
  console.log(`Extracted ${stocks.length} stocks successfully.`);

  const records = stocks.map((s) => ({
    ticker: s.ticker,
    name: s.name,
    logo_url: s.logoUrl || null,
    group: s.group || null,
    style: s.style || null,
    market: s.market || "US",
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
    summary: s.summary || null,
  }));

  const { error } = await supabase.from("stocks").upsert(records, { onConflict: "ticker" });
  if (error) throw error;

  console.log("Database seeding completed successfully.");
}

main().catch((error) => {
  console.error("An error occurred during seeding:", error.message);
  process.exit(1);
});
