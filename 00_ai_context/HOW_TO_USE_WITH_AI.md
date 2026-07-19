# How To Use With AI

คู่มือนี้ใช้เวลาเปิด AI ใหม่ เปลี่ยนเครื่อง หรือเริ่ม thread ใหม่

## Step 1: ให้ AI อ่าน context

ส่ง prompt นี้ก่อน:

```text
คุณคือ research partner ด้านหุ้นของผม

กรุณาอ่านไฟล์ต่อไปนี้ก่อนตอบ:
- 00_ai_context/AI_CONTEXT.md
- 00_ai_context/INVESTOR_PROFILE.md
- 00_ai_context/RESPONSE_RULES.md

หลังอ่านแล้ว ให้สรุปสั้นๆ ว่าคุณเข้าใจสไตล์การลงทุนของผมอย่างไร และคุณจะใช้กฎอะไรเพื่อป้องกันการอวยหุ้น obvious

สำคัญ: นี่เป็น research process ไม่ใช่คำแนะนำการลงทุน
```

## Step 2: เลือกโหมดงาน

### หา theme ใหม่

```text
ใช้ investor profile และ response rules ของผม

ช่วยหา theme/problem/value chain ที่อาจมี "กราฟเริ่มมาแล้ว แต่ข่าวยังไม่มา"

เงื่อนไข:
- ห้ามเริ่มจากชื่อหุ้น
- เริ่มจาก pain point และ bottleneck
- แยก direct beneficiary กับ indirect beneficiary
- บอก customer quality
- บอก crowdedness
- จบด้วย watchlist candidate types และสิ่งที่ต้อง verify
```

### วิเคราะห์หุ้นตัวเดียว

```text
ใช้ AI_CONTEXT.md และ RESPONSE_RULES.md เป็นกรอบ

ช่วยวิเคราะห์หุ้น [TICKER/COMPANY] แบบ deep memo

ต้องตอบ:
- บริษัททำอะไร
- ใครจ่ายเงินให้บริษัทนี้
- money cycle / revenue cycle
- direct หรือ indirect beneficiary
- moat/switching cost
- คู่แข่ง
- จุดแข็ง/จุดอ่อน/โอกาส/ความเสี่ยง
- financial confirmation
- valuation sanity check
- monthly trend
- crowdedness
- bear case
- decision: Pass / Watch / Study / Buy Candidate / Re-entry / Too Hot / Broken

ย้ำ: เป็น research partner ไม่ใช่คำแนะนำการลงทุน
```

### ทำ memo รายหุ้น

```text
ใช้ template 02_templates/deep_memo.md

สร้าง memo สำหรับ [TICKER/COMPANY]
ถ้าข้อมูลส่วนไหนยังไม่มี ให้ใส่เป็น "ต้อง verify"
อย่าเติมแบบเดา
```

### Review watchlist

```text
ใช้ไฟล์ใน 05_watchlists/ และ 02_templates/weekly_review.md

ช่วย review watchlist โดยแยก:
- thesis ยังดีไหม
- monthly trend ดีขึ้นหรือเสีย
- valuation/crowdedness เปลี่ยนไหม
- ตัวไหนควรย้ายสถานะ
- ตัวไหนต้องตัดทิ้ง
```

## Step 3: เก็บผลลัพธ์

- memo หุ้นเก็บที่ `03_memos/`
- theme เก็บที่ `04_themes/`
- watchlist update ที่ `05_watchlists/`
- review รายสัปดาห์/ไตรมาสที่ `06_reviews/`

## Prompt สั้นที่สุดสำหรับเริ่มงาน

```text
อ่าน 00_ai_context/AI_CONTEXT.md และ 00_ai_context/RESPONSE_RULES.md ก่อน
จากนั้นช่วยวิเคราะห์ [TICKER/THEME] ตามสไตล์ Disruptive Compounder + Monthly Trend Confirmation
ห้ามอวยหุ้น obvious ต้องมี bear case, crowdedness, monthly trend และ decision
นี่คือ research ไม่ใช่คำแนะนำการลงทุน
```
