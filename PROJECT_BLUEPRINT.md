# Project Stock Blueprint

ไฟล์นี้คือ source of truth หลังผู้ใช้สั่งให้ดึงงานเก่าก่อนชุด redesign กลับมา

อ่านไฟล์นี้ก่อน `PROJECT_HANDOFF.md` และ `AI_WORK_LOG.md` เมื่อจะทำงานต่อ

## สถานะที่ต้องยึดตอนนี้

โปรเจกต์ถูก restore กลับไปฐาน commit `180258a`

หน้าเว็บหลักควรเป็นโครงเก่า:

- `Book`
- `Research`
- `Watchlist`
- `Portfolio`
- `คลังความรู้กลาง`
- `AI Chat`

ตอนนี้ยังไม่ต้องกลับไปทำหน้าใหม่ชุดนี้:

- `Home / Command Center`
- `Admin / Settings`
- `Styles Guide`
- `Stock Reader`
- `Categorization`
- `Fair Value`
- `Link to Knowledge`
- `Options Lab`

ถ้าจะเพิ่ม UX ใหม่ภายหลัง ต้องเริ่มจาก flow ใช้งานจริงของผู้ใช้ และทำทีละส่วน ไม่ยัด dashboard ระบบกลับเข้ามา

## หลักของระบบ

- เว็บเปิดผ่าน URL ได้
- GitHub เก็บโค้ด
- Supabase เป็นฐานกลางของข้อมูลหุ้น/โน้ต/คลังความรู้เท่าที่ระบบเก่ารองรับ
- Browser ใช้เป็นทางผ่าน ไม่ใช่ฐานข้อมูลถาวร
- Gemini ใช้ผ่าน API key ที่ผู้ใช้ใส่เองใน Settings

## โครงไฟล์ที่ restore กลับมา

- `dashboard.html` - เว็บหลัก
- `public/dashboard.html` - สำเนาสำหรับ deployment
- `00_ai_context/` - บริบท AI
- `01_playbooks/` - คู่มือ/กฎลงทุน
- `02_templates/` - template memo
- `03_memos/` - stock profiles และ business models
- `04_themes/` - theme research
- `05_watchlists/` - watchlist markdown
- `06_reviews/` - review notes
- `db/`, `drizzle.config.ts`, `supabase_schema.sql` - schema/config แบบเก่า
- `AI_WORK_LOG.md` - log งานที่ต้องอัปเดตทุกครั้ง
- `PROJECT_HANDOFF.md` - handoff ภาพรวมปัจจุบัน

## กติกาทำงานต่อ

- อย่าเพิ่มหน้าใหม่ขนาดใหญ่ทันที
- ถ้าจะปรับให้ใช้ง่าย ให้ปรับจากโครงเก่าก่อน เช่น ลดความรกของ Book/Research/Watchlist
- อย่าพูดว่าฟีเจอร์ที่ไม่มีใช้งานจริงแล้ว
- อย่าฝัง secret key ลง repo
- หลังแก้ทุกครั้ง ต้องอัปเดต `AI_WORK_LOG.md`
