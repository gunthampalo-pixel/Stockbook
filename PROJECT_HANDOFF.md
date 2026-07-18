# Project Stock Handoff

อ่านไฟล์นี้ก่อนทำงานทุกครั้ง และอัปเดตไฟล์นี้ทุกครั้งหลังแก้โปรเจกต์ เพื่อให้คนหรือ AI ตัวอื่นรับงานต่อได้ไม่หลงทาง

## ลิงก์หลัก

- เว็บใช้งานหลัก: https://gunthampalo-pixel.github.io/Stockbook/
- GitHub repo: https://github.com/gunthampalo-pixel/Stockbook
- Sites deployment สำรอง: https://stock-research-kan.commercial166737.chatgpt.site
- Supabase project: Project stock
- Supabase URL: https://tymguuajdnkowvvuiijv.supabase.co

## ภาพรวมโปรเจกต์

Project stock คือเว็บคลังวิจัยหุ้นส่วนตัว ใช้สำหรับ:

- เก็บข้อมูลหุ้นและ thesis การลงทุน
- เพิ่มหุ้นใหม่และแก้ข้อมูลหุ้นจากหน้าเว็บ
- จดโน้ตพอร์ตและ watchlist
- คุยกับ AI ในระบบ โดยให้ AI ใช้ฐานข้อมูลหุ้นและคลังความรู้ประกอบคำตอบ
- อ่านและแก้คลังความรู้กลางจาก Supabase ผ่านแท็บ `คลังความรู้กลาง`

เป้าหมายระยะยาวคือทำให้เป็นผู้ช่วยลงทุนส่วนตัวที่ค่อย ๆ โตต่อได้ เช่น อ่านงบการเงิน, สรุปงบ, ช่วยเทียบหุ้น, ทำ backtest จากข้อมูลจริง และให้ AI อธิบายผล

## เป้าหมายของไฟล์นี้

ไฟล์นี้ไม่ใช่แค่ changelog แต่เป็นไฟล์ส่งต่อความคิดของผู้สร้าง

คนหรือ AI ที่เข้ามาทำงานต่อควรใช้ไฟล์นี้เพื่อเข้าใจว่า:

- ผู้สร้างกำลังพยายามสร้างระบบอะไร
- ตอนนี้ระบบมีอะไรแล้ว
- อะไรที่ยังขาดหรือยังไม่ควรทำแบบลวก ๆ
- ควรตัดสินใจอย่างไรเมื่อจะเพิ่มฟีเจอร์ใหม่
- หลังทำงานเสร็จ ต้องบันทึกอะไรไว้ให้คนถัดไป

ถ้า AI ตัวอื่นจะทำงานต่อ ให้เริ่มจากการอ่านไฟล์นี้ แล้วค่อยอ่านโค้ด

## เจตนาของผู้สร้าง

ผู้สร้างไม่ได้ต้องการเว็บจดหุ้นธรรมดา แต่ต้องการระบบคิดร่วมกับ AI สำหรับการลงทุนระยะยาว

แนวคิดหลักคือ:

- ใช้ AI เป็น research partner ไม่ใช่ oracle ที่เดาสุ่ม
- ให้ข้อมูลทุกอย่างมีฐานอ้างอิง เช่น หุ้น งบ thesis watchlist และคลังความรู้
- สร้างระบบที่เปิดจากเครื่องไหนก็เห็นข้อมูลชุดเดียวกัน
- เพิ่มหุ้นใหม่และปรับ thesis ได้เรื่อย ๆ ไม่ใช่เว็บที่ทำเสร็จแล้วหยุด
- ให้ AI จำสไตล์การลงทุนของผู้ใช้ได้ผ่าน knowledge base และ rules
- ทำให้การลงทุนเป็น process ที่ตรวจสอบย้อนหลังได้ ไม่ใช่แค่ถามตอบเป็นครั้ง ๆ

น้ำเสียงของระบบควรเป็นผู้ช่วยลงทุนส่วนตัวที่พูดตรง ช่วยคิด และไม่อวยหุ้นง่าย ๆ

## หลักคิดเวลาเพิ่มฟีเจอร์

ก่อนเพิ่มอะไร ให้ถาม 5 ข้อนี้:

1. ฟีเจอร์นี้ช่วยให้ผู้ใช้ตัดสินใจลงทุนดีขึ้นไหม
2. ข้อมูลถูกเก็บในฐานกลางหรือยัง หรือยังติดอยู่ในเครื่องเดียว
3. AI กำลังตอบจากข้อมูลจริง หรือกำลังเดา
4. ผลลัพธ์ตรวจสอบย้อนหลังได้ไหม
5. มีความเสี่ยงเรื่อง API key ข้อมูลลับ หรือการเปิด public ไหม

ถ้าฟีเจอร์ไหนทำให้ AI ดูฉลาดขึ้นแต่ไม่มีข้อมูลรองรับ ให้ชะลอไว้ก่อน แล้วสร้าง data pipeline ให้แน่นขึ้นก่อน

## สิ่งที่ระบบยังขาด

### 1. Data model ที่เป็นระบบกว่านี้

ตอนนี้ข้อมูลหุ้นและ knowledge base ใช้ได้แล้ว แต่ยังควรแยก data model ให้ชัดขึ้น เช่น:

- stock master
- thesis history
- financial statements
- price history
- watchlist snapshots
- backtest runs
- AI conversations / research sessions

เป้าหมายคือไม่ให้ทุกอย่างกองอยู่ใน field เดียวจน AI อ่านได้แต่ระบบคำนวณต่อไม่ได้

### 2. ระบบอ่านงบการเงินจริง

สิ่งที่ควรมี:

- import งบจากไฟล์ PDF/Excel/CSV หรือ API
- normalize งบเป็นรายปี/รายไตรมาส
- เก็บ revenue, gross profit, operating income, net income, EPS, cash flow, debt, margin
- ให้ AI สรุปจากตัวเลขที่ระบบ parse แล้ว ไม่ใช่อ่านมั่วจากข้อความยาว ๆ
- ทำ red flag checklist เช่น debt สูง, margin หด, dilution, cash burn

AI ควรเป็นคนอธิบาย ตัวเลขควรให้โค้ดคำนวณ

### 3. ระบบ backtest ที่คำนวณจริง

Backtest ไม่ควรให้ AI เดา

ควรมี:

- price history
- rule engine เช่น EMA 10M, MACD, RSI, breakout, monthly close
- trade simulation
- portfolio sizing
- fee/slippage assumption
- metrics เช่น CAGR, max drawdown, win rate, avg gain/loss, exposure, trade list

AI ใช้หน้าที่อธิบายผล เช่น strategy แพ้ช่วงไหน จุดอ่อนคืออะไร และควรทดลอง parameter ไหนต่อ

### 4. AI backend ที่ปลอดภัย

ตอนนี้ Gemini API key ใส่ใน browser settings รายเครื่อง ซึ่งพอใช้ส่วนตัวได้ แต่ยังไม่ใช่ architecture ที่ดีที่สุด

อนาคตควรทำ:

- server-side proxy ผ่าน Vercel, Supabase Edge Function หรือ Cloudflare Worker
- เก็บ API key เป็น secret ฝั่ง server
- จำกัด rate limit
- log usage
- แยก prompt template และ context retrieval ออกจากหน้า HTML

### 5. Auth / private mode

GitHub Pages เป็น public แม้จะใช้ส่วนตัว

ถ้าระบบเริ่มเก็บข้อมูลสำคัญ ควรเพิ่ม:

- login
- passcode
- Supabase Auth
- RLS ที่แยก user/owner
- จำกัดสิทธิ์เขียนข้อมูล

### 6. AI memory ที่เป็น versioned knowledge

ตอนนี้มีคลังความรู้กลางแล้ว แต่ควรเพิ่ม:

- version history ของเอกสารความรู้
- changelog ของ thesis
- วันที่ AI ใช้ context ชุดไหนตอบ
- rule ว่า AI ต้องอ้างอิงเอกสาร/หุ้นที่ใช้ตอบ

เป้าหมายคือเวลาคำตอบผิด จะย้อนดูได้ว่าผิดเพราะ data, prompt, หรือ reasoning

## แนวทางออกแบบ AI ในระบบนี้

AI ควรทำงานแบบนี้:

1. รับคำถามผู้ใช้
2. ค้น stock data และ knowledge base ที่เกี่ยวข้อง
3. ถ้าต้องใช้ตัวเลข ให้ดึงจากตารางที่ normalize แล้ว
4. ถ้าข้อมูลไม่พอ ให้บอกว่าข้อมูลไม่พอ ไม่แต่งคำตอบ
5. แยกคำตอบเป็น:
   - สิ่งที่รู้จากข้อมูล
   - สิ่งที่เป็น inference
   - สิ่งที่ต้องเช็กต่อ
   - action ถัดไป

AI ไม่ควร:

- ฟันธงซื้อขาย
- อวยหุ้นเพราะ story ดี
- สรุปงบโดยไม่มีตัวเลข
- สร้าง backtest จากความรู้สึก
- แก้ข้อมูลฐานกลางโดยไม่บอกผู้ใช้

## นิยามความสำเร็จ

โปรเจกต์นี้สำเร็จเมื่อผู้ใช้สามารถ:

- เปิดเว็บจากเครื่องไหนก็ได้และเห็นข้อมูลเดียวกัน
- เพิ่มหุ้นใหม่ได้เร็ว
- คุยกับ AI แล้ว AI เข้าใจสไตล์การลงทุนของผู้ใช้
- ให้ AI ช่วยอ่านงบและชี้ red flags ได้
- ทดลอง strategy และดู backtest จากข้อมูลจริงได้
- ย้อนดูได้ว่าทำไมเคยสนใจหุ้นตัวหนึ่ง และ thesis เปลี่ยนไปอย่างไร

ระบบนี้ควรโตเป็น investment operating system ส่วนตัว ไม่ใช่ dashboard สวย ๆ อย่างเดียว

## ไฟล์สำคัญ

- `dashboard.html`  
  หน้าเว็บหลักของ Project stock สำหรับ GitHub Pages

- `public/dashboard.html`  
  สำเนาหน้าเว็บสำหรับ deployment ผ่าน Sites/Vinext ต้อง sync กับ `dashboard.html` เมื่อแก้หน้าเว็บหลัก

- `index.html`  
  หน้า redirect/root entry สำหรับ GitHub Pages

- `README.md`  
  หน้าแสดงผลบน GitHub repo มีลิงก์เปิดเว็บและคำอธิบายสั้น ๆ

- `supabase_schema.sql`  
  schema ที่ใช้สร้างตาราง Supabase

- `scripts/seed_supabase.js`  
  script seed ข้อมูลหุ้นและคลังความรู้เข้า Supabase

- `00_ai_context/`, `01_playbooks/`, `02_templates/`, `03_memos/`, `04_themes/`, `05_watchlists/`, `06_reviews/`  
  คลังความรู้ markdown ที่ใช้เป็นฐานความรู้ของ AI และ seed เข้า Supabase

## Supabase

ตารางหลักที่มีอยู่:

- `stocks`  
  เก็บข้อมูลหุ้น เช่น ticker, name, group, style, market, target price, business model, deals, moat, risks, financials, summary

- `portfolio_notes`  
  เก็บโน้ตพอร์ตแยกตาม ticker

- `stock_research_knowledge_documents`  
  เก็บเอกสารคลังความรู้ markdown ให้เว็บอ่าน/แก้จากแท็บ `คลังความรู้กลาง` และให้ AI ใช้เป็น context

หมายเหตุด้านความปลอดภัย:

- ใช้ publishable key ในหน้าเว็บได้สำหรับ client-side Supabase
- ห้ามฝัง service role key หรือ secret key ใน `dashboard.html`
- Gemini API key ตอนนี้ใส่ใน Settings เป็นรายเครื่องผ่าน browser storage ไม่ควรฝังคีย์กลางลงเว็บสาธารณะ

## สิ่งที่ทำไปแล้ว

### 2026-07-14

- ย้ายโปรเจกต์ขึ้น GitHub repo `gunthampalo-pixel/Stockbook`
- ตั้ง GitHub Pages ให้เปิดเว็บได้ที่ `https://gunthampalo-pixel.github.io/Stockbook/`
- สร้าง root `index.html` เพื่อให้เปิดลิงก์ repo page แล้วเข้า dashboard ได้ง่าย
- เชื่อม default Supabase เป็น project ส่วนตัว `Project stock`
- สร้าง/seed ตาราง Supabase:
  - `stocks`
  - `portfolio_notes`
  - `stock_research_knowledge_documents`
- ทำให้เว็บดึงข้อมูลหุ้นจาก Supabase เมื่อเปิดหน้า
- ทำ autosave ข้อมูลหุ้นกลับ Supabase
- ทำ autosave portfolio note กลับ Supabase
- เพิ่มแท็บ `คลังความรู้กลาง` สำหรับอ่าน/แก้เอกสารความรู้จาก Supabase
- ทำ AI Chat ให้ใช้ข้อมูลหุ้นและเอกสารความรู้หลักจาก Supabase เป็น context
- เพิ่ม badge แสดง AI model ในหน้าต่างแชต
- เพิ่ม Settings สำหรับเลือก Gemini model
- เพิ่มช่อง `Custom AI Model Version` เพื่อใส่ชื่อโมเดลใหม่เองได้ในอนาคต
- ตั้ง GitHub repo description และ homepage URL
- เพิ่มลิงก์เว็บและคำอธิบายใน `README.md`
- Deploy Sites สำรองที่ `https://stock-research-kan.commercial166737.chatgpt.site`

## สถานะล่าสุด

- เว็บหลักพร้อมใช้ผ่าน GitHub Pages
- ข้อมูลหุ้นและคลังความรู้ใช้ Supabase เป็นฐานกลาง
- เปิดหลายเครื่องจะเห็นข้อมูลจากฐานเดียวกัน
- AI Chat มีในระบบแล้ว แต่ยังใช้ Gemini API key ที่ผู้ใช้ใส่เองใน Settings
- ยังไม่มี server-side AI proxy เพราะไม่ควรฝัง API secret ลงเว็บสาธารณะ
- ยังไม่มีระบบ login/auth จริง ถ้าใช้ส่วนตัวและไม่แชร์ลิงก์ ความเสี่ยงต่ำกว่า แต่เว็บ GitHub Pages ยังเป็น public

## แนวทางทำงานต่อ

ถ้าจะให้ AI ตัวอื่นหรือคนอื่นทำต่อ ให้ทำตามนี้:

1. อ่าน `PROJECT_HANDOFF.md` ไฟล์นี้ก่อน
2. อ่าน `README.md`
3. ถ้าแก้หน้าเว็บ ให้แก้ `dashboard.html`
4. คัดลอก `dashboard.html` ไปทับ `public/dashboard.html` ทุกครั้งหลังแก้ UI/logic หน้าเว็บ
5. ทดสอบ build ด้วย `npm run build` ถ้ารันได้
6. commit และ push ขึ้น GitHub
7. ถ้า deployment ผ่าน Sites ยังใช้ต่อ ให้ deploy Sites หลัง push ด้วย
8. อัปเดต section `Update Log` ในไฟล์นี้ทุกครั้งว่าแก้อะไรไป

## งานต่อที่ควรทำ

- เพิ่มระบบอ่านงบการเงิน:
  - upload/import ไฟล์งบ
  - parse ตารางงบ
  - เก็บ financial statement ลง Supabase
  - ให้ AI สรุปการเติบโต margin cash flow debt และ red flags

- เพิ่มระบบ backtest:
  - ดึง/นำเข้าข้อมูลราคา
  - คำนวณผลด้วยโค้ด ไม่ให้ AI เดาผล
  - เก็บผล backtest เช่น CAGR, max drawdown, win rate, trade list
  - ให้ AI อธิบายผลและจุดอ่อนของ strategy

- เพิ่มระบบ options backtest:
  - เริ่มจาก payoff simulator สำหรับ long call, long put, covered call, cash-secured put
  - ต่อ option chain จริง เช่น strike, expiry, bid/ask, volume, open interest, IV, delta
  - ต่อ historical underlying price สำหรับทดสอบกฎเข้าออก
  - เก็บผลเป็น runs/trades เพื่อให้ AI วิเคราะห์จุดแข็งจุดอ่อนของกลยุทธ์
  - ห้ามให้ AI เดา option premium หรือผล backtest เอง ต้องดึงข้อมูลหรือกรอกข้อมูลจริงก่อน

- เพิ่ม server-side AI proxy:
  - ใช้ Vercel/Supabase Edge Function/Cloudflare Worker
  - เก็บ Gemini API key เป็น secret ฝั่ง server
  - หน้าเว็บเรียก proxy แทนเรียก Gemini ตรง ๆ

- เพิ่ม auth หรือ passcode:
  - ถ้าต้องการให้เว็บแก้ข้อมูลได้แบบปลอดภัยขึ้น
  - ปัจจุบันเว็บ public และ Supabase key เป็น publishable client key

## Update Log

### 2026-07-19 (Antigravity Upgrades)

- **ปรับโครงสร้างเป็น E-Book Dashboard 5 หน้าใหม่:** สไตล์หุ้น (Styles Guide), ค้นอ่านหุ้น (Searchable Reader), จัดกลุ่มหุ้น (Categorization Grid), Watchlist Targets และ Options Lab
- **ฝังกราฟ TradingView สด:** ดึงกราฟเทคนิคัลโต้ตอบได้มาพล็อตเคียงข้างตาราง Watchlist รายหุ้นอัตโนมัติ
- **บอทลอยตัวอัจฉริยะ (Floating AI Advisor):** ไอคอนวงกลมลอยมุมล่างขวาประเมินหน้าจอที่กำลังเปิด (Context-Aware) และสามารถพิมพ์แชทคุมหน้าจอเว็บได้ (UI Screen Controller)
- **สร้างระบบแบคเทสออปชัน (Options LEAPs Backtester):** สร้างสคริปต์ [backtest_options.py](file:///Users/gunthampalo/Library/CloudStorage/OneDrive-CentralGroup/น้องกัณฑ์/ai/MY%20PROJECT/หุ้นๆๆๆ/stock-research-knowledge-base/scripts/backtest_options.py) เพื่อจำลองผลตอบแทนสัญญา LEAPs Call 1 ปี ตามเส้น EMA 10M รายเดือน (รันตรวจสอบหุ้นได้ทุกตัว)
- **ปรับปรุง Database Schema:** เพิ่มคอลัมน์ `entry_price` และ `exit_price` ลงในตาราง `stocks` ในไฟล์ [supabase_schema.sql](file:///Users/gunthampalo/Library/CloudStorage/OneDrive-CentralGroup/น้องกัณฑ์/ai/MY%20PROJECT/หุ้นๆๆๆ/stock-research-knowledge-base/supabase_schema.sql)
- **ทำความสะอาดสิทธิ์ Git:** ลบไฟล์ซ้ำ และกวาดต้อนประวัติขึ้น GitHub คลาวด์สำเร็จ

### 2026-07-19 (Codex Updates)

- เพิ่มแท็บ `Options Lab` ใน `dashboard.html`
- เพิ่ม prototype payoff engine สำหรับ long call, long put, covered call และ cash-secured put
- แสดง P/L at expiry, breakeven, max loss, return on capital และ payoff table
- เพิ่มลิงก์ `PROJECT_HANDOFF.md` ใน `README.md`
- หมายเหตุ: นี่ยังไม่ใช่ options backtest เต็ม ต้องต่อ option chain, IV, bid/ask, expiry calendar และ historical price ภายหลัง

### 2026-07-18

- เพิ่มไฟล์ `PROJECT_HANDOFF.md` เพื่อเป็นไฟล์ส่งต่องานสำหรับ AI/คนอื่น
- ระบุลิงก์หลัก สถานะล่าสุด ไฟล์สำคัญ Supabase และขั้นตอนที่ต้องอัปเดตทุกครั้งหลังทำงาน
- เพิ่มส่วนเป้าหมายของไฟล์ เจตนาผู้สร้าง สิ่งที่ระบบยังขาด แนวทางออกแบบ AI และนิยามความสำเร็จ เพื่อให้ AI/คนอื่นช่วยคิดต่อได้ถูกทิศทาง
