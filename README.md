# Project stock

เว็บคลังวิจัยหุ้นส่วนตัว + AI Chat + Supabase knowledge base

## เปิดเว็บ

- GitHub Pages: https://gunthampalo-pixel.github.io/Stockbook/
- Sites สำรอง: https://stock-research-kan.commercial166737.chatgpt.site

## ใช้ทำอะไร

- หน้า `Home` สรุปภาพรวมระบบ แหล่งข้อมูล และสถานะ Supabase/Gemini
- เพิ่ม/แก้ข้อมูลหุ้น แล้ว sync กับ Supabase
- คุยกับ AI โดยให้ AI อ่านฐานข้อมูลหุ้นและคลังความรู้
- อ่านคู่มือหุ้นจาก `Styles Guide`
- ค้นและอ่านข้อมูลหุ้นจาก `Stock Reader`
- จัดกลุ่มหุ้นจาก `Categorization`
- ดู watchlist พร้อมกราฟ TradingView จาก `Watchlist`
- คิด fair value จากแท็บ `Fair Value`
- วางลิงก์/ข้อความจากคลิป โพสต์ หรือบทความใน `Link to Knowledge`
- ทดลอง payoff หุ้น option จาก `Options Lab`
- เช็กหลังบ้านและล้าง cache เครื่องจาก `Admin`

## โครง repo

- `dashboard.html` - เว็บหลักสำหรับ GitHub Pages
- `public/dashboard.html` - สำเนาเว็บหลักสำหรับ Sites deployment
- `index.html` - หน้าเปิดเว็บและ redirect เข้า dashboard
- `docs/knowledge/` - คลัง markdown สำหรับ seed/fallback local
- `supabase/` - schema และ db config
- `scripts/` - เครื่องมือ seed, fetch financials, backtest, monitor
- `app/`, `worker/`, `build/` - wrapper สำหรับ Sites/Vinext hosting
- `images/` - รูปที่ GitHub Pages ใช้
- `public/images/` - รูปที่ Sites ใช้

## กติกาส่งต่องาน

ก่อนทำงานต่อให้อ่าน:

- `PROJECT_BLUEPRINT.md`
- `PROJECT_HANDOFF.md`
- `AI_WORK_LOG.md`

หลังแก้งานต้องอัปเดต `AI_WORK_LOG.md` ทุกครั้ง

## หมายเหตุเรื่องข้อมูล

- ข้อมูลหลักอยู่ Supabase
- Safari/เครื่องผู้ใช้ไม่ควรเป็น source of truth
- เว็บเวอร์ชันนี้มี one-time cache reset เพื่อล้างค่าเก่าที่เคยค้างใน Safari ของ Project stock
