# Project Stock Handoff

อ่าน `PROJECT_BLUEPRINT.md` ก่อน แล้วอ่านไฟล์นี้ จากนั้นอ่าน `AI_WORK_LOG.md`

## สถานะล่าสุด

ผู้ใช้ไม่ต้องการหน้า redesign ล่าสุด จึง restore โปรเจกต์กลับไปฐานเก่า commit `180258a`

เป้าหมายตอนนี้คือให้เว็บกลับมาอยู่ในรูปแบบเดิมก่อน แล้วค่อยคิด UX ใหม่อย่างช้า ๆ

## เว็บหลัก

- GitHub Pages: https://gunthampalo-pixel.github.io/Stockbook/
- Dashboard ตรง: https://gunthampalo-pixel.github.io/Stockbook/dashboard.html
- Sites สำรอง: https://stock-research-kan.commercial166737.chatgpt.site
- GitHub repo: https://github.com/gunthampalo-pixel/Stockbook

## หน้าในเว็บเวอร์ชันเก่า

- `Book` - เปิดอ่านคู่มือ/คลังความรู้จาก playbooks และ context
- `Research` - อ่าน/แก้ข้อมูลหุ้นรายตัว
- `Watchlist` - รายการหุ้นที่เฝ้าดู
- `Portfolio` - โน้ตพอร์ตและ thesis รายตัว
- `คลังความรู้กลาง` - โหลด/แก้ knowledge docs จาก Supabase
- `AI Chat` - แชทกับ Gemini โดยใช้ context ของระบบ

## โครง repo ที่กลับมา

- knowledge markdown อยู่ระดับ root เช่น `00_ai_context/`, `01_playbooks/`, `03_memos/`
- schema เก่าอยู่ที่ `db/`, `drizzle.config.ts`, `supabase_schema.sql`
- `docs/knowledge/` และ `supabase/` จาก cleanup ใหม่ถูกถอดออกในการ restore นี้

## ข้อควรระวัง

- อย่าดึงหน้า `Home/Admin/Fair Value/Options/Link to Knowledge` กลับมาเอง เว้นแต่ผู้ใช้ขออีกครั้ง
- ถ้าจะทำให้ง่ายขึ้น ให้ปรับจากหน้าเก่า ไม่ใช่สร้างระบบใหม่ทับ
- อย่าลบ `AI_WORK_LOG.md`
- หลังแก้ต้องเพิ่ม entry ใหม่ใน `AI_WORK_LOG.md`

## งานต่อที่เหมาะสม

- เปิดหน้าเก่าให้ผู้ใช้ดูก่อน
- ถ้าผู้ใช้บอกว่าส่วนไหนใช้ยาก ค่อยปรับเฉพาะส่วนนั้น
- ถ้าจะเพิ่มฟีเจอร์ใหม่ ให้ทำ prototype เล็กและไม่ทำให้โครงเก่าหาย
