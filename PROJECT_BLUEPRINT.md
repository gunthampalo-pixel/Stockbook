# Project Stock Blueprint

ไฟล์นี้คือ source of truth ของระบบ Project stock

อ่านไฟล์นี้ก่อน `PROJECT_HANDOFF.md` และ `AI_WORK_LOG.md` เมื่อจะทำงานต่อ ห้ามตีความเพิ่มเองโดยไม่ยึด blueprint นี้

## หลักของระบบ

Project stock คือเว็บวิจัยหุ้นส่วนตัวที่เปิดผ่านเว็บได้จากทุกเครื่อง โดยข้อมูลจริงทั้งหมดอยู่ที่ Supabase

- Supabase = ฐานข้อมูลกลางและ source of truth
- GitHub = เก็บโค้ดเว็บ เอกสาร fallback scripts และ schema
- เว็บ = หน้าจอสำหรับอ่าน แก้ คำนวณ และคุยกับ AI
- Safari/browser = ทางผ่านเท่านั้น ไม่ใช่ที่เก็บข้อมูลหลัก
- งานนี้เป็นงานหุ้นเท่านั้น ห้ามเอางาน segment/Power BI หรืองานอื่นมาปน

## 1. เว็บ Project stock

ต้องเปิดผ่านเว็บ ไม่ใช่เปิดไฟล์จากเครื่องใดเครื่องหนึ่ง

เป้าหมาย:

- เปิดจากคอมเครื่องไหนก็เห็นข้อมูลเดียวกัน
- หน้าเว็บต้องอ่าน/แก้/คำนวณได้จริง
- ข้อมูลต้องไม่ค้างเป็น source หลักใน Safari หรือเครื่องเดียว

## 2. Supabase เป็นฐานข้อมูลกลาง

ข้อมูลที่ต้องผูกลง Supabase:

- หุ้น
- notes
- knowledge
- fair value notes
- สรุปจากลิงก์/คลิป/บทความ
- watchlist / target / จุดเข้า / จุดออก
- ข้อมูลที่ AI ต้องอ่านเพื่อตอบ

ตารางที่มีตอนนี้:

- `stocks`
- `portfolio_notes`
- `stock_research_knowledge_documents`

หลักสำคัญ:

- ถ้าผู้ใช้แก้ข้อมูลจากเว็บ ข้อมูลควรกลับไป Supabase
- ถ้าเปิดเครื่องใหม่ เว็บควร reload จาก Supabase
- sessionStorage/localStorage/cache ใช้ได้แค่ชั่วคราว ไม่ใช่ข้อมูลจริง

## 3. GitHub เก็บโค้ดเว็บ

GitHub ใช้เก็บ:

- เว็บ
- README
- blueprint/handoff/work log
- schema
- scripts
- docs fallback

Repo ต้องไม่รกโดยไม่มีเหตุผล และต้องมีเอกสารให้ AI ตัวอื่นอ่านต่อ

ไฟล์ส่งต่องาน:

- `PROJECT_BLUEPRINT.md` - ระบบควรเป็นอะไร
- `PROJECT_HANDOFF.md` - ภาพรวม สถานะ สถาปัตยกรรม
- `AI_WORK_LOG.md` - log รายครั้งว่าใครทำอะไร

ทุกครั้งที่แก้ ต้องอัปเดต `AI_WORK_LOG.md`

## 4. หน้าอ่าน/วิจัยหุ้น

### Styles Guide / E-Book

หน้าที่:

- อ่านคัมภีร์หาไอเดียลงทุน
- อ่านเกณฑ์/โลจิกหุ้น 6 สไตล์หลัก
- ดึงจาก Supabase เป็นหลัก

ข้อมูล:

- `stock_research_knowledge_documents`

### Stock Reader

หน้าที่:

- ค้นหุ้น
- อ่านว่าบริษัททำอะไร
- ได้เงินยังไง
- โมเดลธุรกิจ
- moat
- risks
- deals
- งบการเงินย้อนหลัง
- thesis / notes

ข้อมูล:

- `stocks`
- `portfolio_notes`

### Categorization Grid

หน้าที่:

- จัดกลุ่มหุ้นตาม style
- จัดกลุ่มหุ้นตาม group/theme
- ช่วยสแกนเปรียบเทียบหุ้นในหมวดเดียวกัน

ข้อมูล:

- `stocks.style`
- `stocks.group`
- `stocks.market`

## 5. หน้า Watchlist

### Watchlist Targets & TradingView

หน้าที่:

- แสดงหุ้นที่เฝ้าดู
- target price
- จุดเข้า
- จุดออก / stop
- มี TradingView ดูกราฟ
- คลิกหุ้นแล้วกราฟเปลี่ยนเป็นหุ้นนั้น

ข้อมูล:

- `stocks.target_price`
- `stocks.entry_price`
- `stocks.exit_price`

API/เว็บ:

- Supabase สำหรับข้อมูล watchlist/targets
- TradingView widget สำหรับกราฟ

## 6. หน้า Fair Value

### Fair Value Lab

หน้าที่:

- คิดราคาเหมาะสม
- ใส่สมมติฐาน
- ได้ fair value
- ได้ margin of safety
- บันทึกผลเข้าคลังความรู้

แนวทาง:

- ต้องคำนวณจากสูตร
- สูตรจะค่อย ๆ ถูกสอน/ปรับตามสไตล์หุ้นแต่ละแบบ
- ตอนนี้ทำเป็น simple DCF ได้ก่อน แต่ห้ามพูดเหมือนเป็นสูตรสุดท้าย

ข้อมูล:

- อ่าน input จากหน้าเว็บ
- บันทึกผลลง `stock_research_knowledge_documents`
- category: `09_valuation_notes`

## 7. หน้า Link to Knowledge

### Link to Knowledge / Extractor

หน้าที่:

- วางลิงก์โพสต์/คลิป/บทความ
- วาง transcript หรือข้อความ
- ให้ AI สรุปเป็นความรู้
- เก็บเข้าคลังความรู้ Supabase
- ใช้เพื่อให้ผู้ใช้และ AI เรียนรู้ต่อจากแหล่งความรู้ที่เจอ

ข้อมูล:

- บันทึกลง `stock_research_knowledge_documents`
- category: `08_extracted_knowledge`

API:

- Gemini สำหรับสรุป
- Supabase สำหรับเก็บผล

หมายเหตุ:

- ตอนนี้ให้วาง transcript/text เองก่อน
- การดึง YouTube/Facebook ตรงควรทำภายหลังผ่าน backend/API ถ้าจำเป็น

## 8. หน้า Options Lab

หน้าที่:

- ใช้กับ stock options
- คำนวณ payoff
- ดู breakeven
- ดู P/L
- ดู risk

จุดประสงค์จริง:

- ถ้าผู้ใช้เข้าตามหลัก technical แล้ว ต้องการรู้ว่าตอนออกจะกำไรไหม
- ตอนนี้เน้นคำนวณกำไร/ขาดทุนตาม input ไม่ใช่ backtest เต็ม

ข้อมูล:

- คำนวณในเว็บได้ก่อน
- ถ้าจะบันทึกภายหลังให้บันทึกลง Supabase

## 9. AI ในระบบ

### Floating AI Advisor Bot

หน้าที่:

- ปุ่มลอยขวาล่าง
- คุยได้ทุกหน้า
- รู้ว่าผู้ใช้อยู่หน้าไหน
- ใช้ข้อมูลจาก Supabase ตอบ
- สั่งเปลี่ยนหน้าได้ เช่น "ไป Options Lab"
- ช่วยคิดหุ้น/fair value/options/ความเสี่ยง

จุดประสงค์จริง:

- คุยก่อนเข้าซื้อ
- คุยก่อนออก
- ออกแบบความรู้ใหม่ ๆ
- หารายละเอียดเพิ่ม
- เพิ่มหุ้นใหม่หรือปรับข้อมูลหุ้น

API:

- Gemini สำหรับแชท
- Supabase สำหรับ context

AI ต้อง:

- อ้างอิงข้อมูลจาก Supabase เท่าที่มี
- ถ้าข้อมูลไม่พอ ต้องบอกว่าต้อง verify
- ไม่ฟันธงซื้อขาย
- ไม่แต่งตัวเลขเอง

## 10. หลังบ้าน / Settings

หน้าที่:

- เช็ก Supabase ต่อไหม
- เช็ก Gemini ใช้ได้ไหม
- เลือก Gemini model
- reload ข้อมูลจาก Supabase
- clear cache เครื่อง/Safari
- จัดหน้า/เมนูได้
- เปิด/ปิด AI controller ได้

เรื่องข้อมูลที่ต้องแยกให้ชัด:

- ราคาหุ้นดึงจากไหน
- งบการเงินดึงจากไหน
- knowledge ดึงจากไหน
- ข้อมูลไหนเขียนกลับ Supabase
- ข้อมูลไหนเป็นแค่ค่าชั่วคราวใน browser

ตอนนี้:

- Supabase เป็นฐานกลาง
- Gemini key/model ใช้สำหรับ AI
- TradingView ใช้สำหรับกราฟ

ต้องไม่ใส่ backup/import/export เป็น requirement ตอนนี้ ถ้าผู้ใช้ไม่ได้ขอ

## 11. ไม่ให้ข้อมูลปน

กติกา:

- งานหุ้นเท่านั้น
- ทุก AI ที่มาทำต่ออ่าน `PROJECT_BLUEPRINT.md`, `PROJECT_HANDOFF.md`, `AI_WORK_LOG.md` ก่อน
- ทุกครั้งที่แก้ต้องอัปเดต log
- log ต้องบอกว่าตอนนี้มีอะไร จะทำอะไร กำลังทำอะไร ทำอะไรไปแล้ว และจะทำอะไรต่อ

## สิ่งที่ห้ามทำ

- ห้ามเพิ่ม feature ใหม่โดยไม่ยึด blueprint นี้
- ห้ามพูดสิ่งที่ยังไม่มีว่าใช้งานจริงแล้ว
- ห้ามเอางานอื่นมาปน
- ห้ามทำให้ Safari/localStorage เป็น source of truth
- ห้ามฝัง secret key ลง repo
