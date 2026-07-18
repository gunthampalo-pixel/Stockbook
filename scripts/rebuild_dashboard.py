import os
import sys

def rebuild():
    file_path = "/Users/gunthampalo/Library/CloudStorage/OneDrive-CentralGroup/น้องกัณฑ์/ai/MY PROJECT/หุ้นๆๆๆ/stock-research-knowledge-base/dashboard.html"
    
    if not os.path.exists(file_path):
        print(f"❌ Error: {file_path} not found.")
        sys.exit(1)
        
    print(f"📖 Reading {file_path}...")
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Inject custom CSS styles for Book Reader, Watchlist Targets, and Floating Bot
    new_css = """
    /* --- NEW E-BOOK & PREMIUM STYLING --- */
    .book-reader {
      font-family: 'Georgia', 'Merriweather', serif;
      line-height: 1.8;
      font-size: 16px;
      color: #e2e8f0;
      padding: 30px;
      max-width: 800px;
      margin: 0 auto;
    }
    .book-reader h1, .book-reader h2, .book-reader h3 {
      font-family: 'Outfit', 'Inter', sans-serif;
      color: var(--accent-cyan);
      margin-top: 1.5em;
      margin-bottom: 0.5em;
    }
    .book-reader p {
      margin-bottom: 1.5em;
    }
    .book-reader ul, .book-reader ol {
      margin-bottom: 1.5em;
      padding-left: 20px;
    }
    .book-reader li {
      margin-bottom: 0.5em;
    }
    .book-reader table {
      width: 100%;
      border-collapse: collapse;
      margin: 20px 0;
      font-family: 'Inter', sans-serif;
      font-size: 14px;
    }
    .book-reader th, .book-reader td {
      border: 1px solid var(--border-color);
      padding: 10px;
      text-align: left;
    }
    .book-reader th {
      background: rgba(0, 240, 255, 0.1);
      color: var(--accent-cyan);
    }
    
    /* Style filter chips */
    .filter-chips {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      margin-bottom: 15px;
    }
    .chip {
      padding: 6px 12px;
      border-radius: 20px;
      background: rgba(255,255,255,0.05);
      border: 1px solid var(--border-color);
      color: var(--text-secondary);
      font-size: 12px;
      cursor: pointer;
      transition: all 0.2s;
      font-weight: 500;
    }
    .chip.active {
      background: var(--accent-cyan);
      border-color: var(--accent-cyan);
      color: #000;
      box-shadow: 0 0 10px rgba(0,240,255,0.3);
    }
    
    /* Watchlist Target fields styling */
    .target-badge {
      font-family: monospace;
      font-weight: bold;
      padding: 2px 6px;
      border-radius: 4px;
    }
    .target-entry { background: rgba(16, 185, 129, 0.15); color: var(--accent-green); }
    .target-exit { background: rgba(239, 68, 68, 0.15); color: var(--accent-red); }
    .target-sell { background: rgba(168, 85, 247, 0.15); color: #c084fc; }

    /* Floating Bot Styles */
    #floating-bot-trigger {
      position: fixed;
      bottom: 25px;
      right: 25px;
      width: 55px;
      height: 55px;
      background: var(--accent-cyan);
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      box-shadow: 0 4px 20px rgba(0, 240, 255, 0.4);
      z-index: 9999;
      transition: transform 0.2s, background 0.2s;
    }
    #floating-bot-trigger:hover {
      transform: scale(1.1);
      background: #00e6ff;
    }
    #floating-bot-chat {
      position: fixed;
      bottom: 95px;
      right: 25px;
      width: 380px;
      height: 520px;
      display: none;
      flex-direction: column;
      z-index: 9999;
      box-shadow: 0 10px 30px rgba(0,0,0,0.5);
      border-radius: 12px;
      overflow: hidden;
      border: 1px solid var(--border-color);
    }
    .floating-chat-header {
      background: rgba(15, 23, 42, 0.95);
      padding: 12px 16px;
      border-bottom: 1px solid var(--border-color);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .floating-chat-body {
      flex: 1;
      overflow-y: auto;
      padding: 16px;
      background: rgba(15, 23, 42, 0.85);
      display: flex;
      flex-direction: column;
      gap: 12px;
    }
    .floating-chat-footer {
      padding: 12px;
      background: rgba(15, 23, 42, 0.95);
      border-top: 1px solid var(--border-color);
      display: flex;
      gap: 8px;
    }
    .floating-chat-footer input {
      flex: 1;
      background: rgba(255,255,255,0.05);
      border: 1px solid var(--border-color);
      border-radius: 6px;
      padding: 8px 12px;
      color: #fff;
      font-size: 13px;
    }
    .floating-chat-footer input:focus {
      outline: none;
      border-color: var(--accent-cyan);
    }
    .floating-chat-footer button {
      background: var(--accent-cyan);
      color: #000;
      border: none;
      border-radius: 6px;
      padding: 8px 14px;
      font-weight: 600;
      cursor: pointer;
      transition: background 0.2s;
    }
    .floating-chat-footer button:hover {
      background: #00e6ff;
    }
    </style>
    """
    
    # Insert new CSS just before </style>
    content = content.replace("    </style>", new_css + "\n    </style>")

    # 2. Re-define TABS array in Javascript to reflect the 4 new pages
    old_tabs_definition = """      let TABS = JSON.parse(S.get('app_tabs') || 'null');
      if (!TABS) {
        TABS = [
          { id: 'thesis', title: 'My Playbook', icon: 'book-open', type: 'book' },
          { id: 'selection', title: 'วิธีหาหุ้น (คอขวด)', icon: 'search', type: 'book' },
          { id: 'research', title: 'Stock Research', icon: 'database', type: 'system' },
          { id: 'watchlist', title: 'Watchlist', icon: 'star', type: 'system' },
          { id: 'portfolio', title: 'Portfolio', icon: 'briefcase', type: 'system' },
          { id: 'knowledge', title: 'คลังความรู้กลาง', icon: 'library', type: 'system' }
        ];
        S.set('app_tabs', JSON.stringify(TABS));
      } else {
        // Ensure system tabs are present in existing TABS
        if (!TABS.some(t => t.id === 'portfolio')) {
          TABS.push({ id: 'portfolio', title: 'Portfolio', icon: 'briefcase', type: 'system' });
        }
        if (!TABS.some(t => t.id === 'knowledge')) {
          TABS.push({ id: 'knowledge', title: 'คลังความรู้กลาง', icon: 'library', type: 'system' });
        }
        S.set('app_tabs', JSON.stringify(TABS));
      }"""
      
    new_tabs_definition = """      let TABS = [
        { id: 'styles-guide', title: 'สไตล์หุ้น', icon: 'book-open', type: 'system' },
        { id: 'stock-reader', title: 'เสิร์ชอ่านข้อมูลหุ้น', icon: 'search', type: 'system' },
        { id: 'categorization-board', title: 'จัดกลุ่มหุ้น', icon: 'layout-grid', type: 'system' },
        { id: 'watchlist-targets', title: 'Watchlist Targets', icon: 'star', type: 'system' }
      ];
      S.set('app_tabs', JSON.stringify(TABS));"""
      
    content = content.replace(old_tabs_definition, new_tabs_definition)

    # 3. Replace HTML Page Container layout
    # First, let's extract the start of the page-container and find where we can replace it.
    old_pages_start = '      <!-- ===== PAGES ===== -->\n      <div class="page-container">'
    old_pages_end = '      </div><!-- end page-container -->'
    
    # We want to replace everything inside page-container with our 4 new pages
    new_pages_html = """
      <!-- ===== PAGES ===== -->
      <div class="page-container">

        <!-- PAGE 1: STOCK STYLES GUIDE -->
        <div class="page active research-page" id="page-styles-guide" style="padding: 12px; display:flex; gap:12px; height:100%;">
          <div class="stock-sidebar glass-panel" style="padding:12px; display:flex; flex-direction:column; gap:8px;">
            <div style="font-size: 13px; font-weight: 700; color: var(--accent-cyan); display: flex; align-items: center; gap: 6px; padding: 4px;">
              <i data-lucide="book-open" style="width:18px;height:18px;"></i>
              <span>สารบัญสไตล์หุ้น</span>
            </div>
            <div style="font-size: 11px; color: var(--text-muted); padding: 0 4px 6px; border-bottom: 1px solid var(--border-color);">
              เกณฑ์ โโลจิก และคัมภีร์วิเคราะห์
            </div>
            <div class="stock-list" id="styles-guide-list" style="flex:1; overflow-y:auto;">
              <!-- Dynamically populated in JS -->
            </div>
          </div>
          <div class="stock-detail glass-panel" style="padding:0; flex:1; display:flex; flex-direction:column; overflow:hidden;">
            <div id="styles-guide-content" class="book-reader" style="height:100%; overflow-y:auto;">
              <div style="display:flex;align-items:center;justify-content:center;height:100%;color:var(--text-muted);flex-direction:column;gap:10px;">
                <i data-lucide="book-open" style="width:40px;height:40px;opacity:0.3;color:var(--accent-cyan);"></i>
                <p>เลือกสไตล์หุ้นจากด้านซ้ายเพื่อเปิดอ่านคู่มือวิจัย</p>
              </div>
            </div>
          </div>
        </div>

        <!-- PAGE 2: SEARCHABLE STOCK READER -->
        <div class="page research-page" id="page-stock-reader" style="padding: 12px; display:none; gap:12px; height:100%;">
          <div class="stock-sidebar glass-panel" style="padding:12px; display:flex; flex-direction:column; gap:8px;">
            <div style="font-size: 13px; font-weight: 700; color: var(--accent-cyan); display: flex; align-items: center; gap: 6px; padding: 4px;">
              <i data-lucide="search" style="width:18px;height:18px;"></i>
              <span>ค้นข้อมูลหุ้น</span>
            </div>
            <div class="stock-search">
              <input type="text" id="reader-search-input" placeholder="พิมพ์ชื่อหุ้น หรือ Ticker..." style="width:100%;" />
            </div>
            <div class="stock-list" id="reader-stock-list" style="flex:1; overflow-y:auto;">
              <!-- Stocks populated in JS -->
            </div>
          </div>
          <div class="stock-detail glass-panel" style="padding:0; flex:1; display:flex; flex-direction:column; overflow:hidden;">
            <div id="reader-content" style="height:100%; overflow-y:auto; padding:20px;">
              <div style="display:flex;align-items:center;justify-content:center;height:100%;color:var(--text-muted);flex-direction:column;gap:10px;">
                <i data-lucide="search" style="width:40px;height:40px;opacity:0.3;color:var(--accent-cyan);"></i>
                <p>ค้นหาหุ้นหรือคลิกเลือกจากรายการด้านซ้ายเพื่อเปิดอ่านรายละเอียดเชิงลึก</p>
              </div>
            </div>
          </div>
        </div>

        <!-- PAGE 3: CATEGORIZATION BOARD -->
        <div class="page" id="page-categorization-board" style="padding: 12px; display:none; flex-direction:column; gap:12px; height:100%; overflow:hidden;">
          <div style="display:flex; justify-content:space-between; align-items:center; padding:4px;">
            <div style="font-size: 15px; font-weight: 700; color: var(--accent-cyan); display: flex; align-items: center; gap: 6px;">
              <i data-lucide="layout-grid" style="width:20px;height:20px;"></i>
              <span>จัดกลุ่มแยกตามสไตล์หุ้น</span>
            </div>
          </div>
          
          <!-- Category Chips -->
          <div class="filter-chips" id="board-style-chips">
            <!-- Populated dynamically -->
          </div>

          <!-- Cards Grid -->
          <div class="stock-grid" id="board-cards-grid" style="flex:1; overflow-y:auto; padding-bottom:20px;">
            <!-- Classified stock cards will render here -->
          </div>
        </div>

        <!-- PAGE 4: WATCHLIST TARGETS & TRADINGVIEW -->
        <div class="page research-page" id="page-watchlist-targets" style="padding: 12px; display:none; gap:12px; height:100%;">
          <!-- Watchlist Table Section -->
          <div class="glass-panel" style="flex: 1.2; padding:15px; display:flex; flex-direction:column; gap:10px; overflow:hidden;">
            <div style="font-size: 15px; font-weight: 700; color: var(--accent-cyan); display: flex; align-items: center; gap: 6px; border-bottom:1px solid var(--border-color); padding-bottom:8px;">
              <i data-lucide="star" style="width:18px;height:18px;color:var(--accent-orange);"></i>
              <span>รายการหุ้นเฝ้าระวัง (Watchlist Targets)</span>
            </div>
            <div style="overflow-x:auto; flex:1;">
              <table style="width:100%; border-collapse:collapse; font-size:13px;" id="watchlist-targets-table">
                <thead>
                  <tr style="border-bottom: 1px solid var(--border-color); text-align:left;">
                    <th style="padding:10px 8px; color:var(--text-muted);">หุ้น</th>
                    <th style="padding:10px 8px; color:var(--text-muted);">ราคาล่าสุด</th>
                    <th style="padding:10px 8px; color:var(--accent-green);">จุดเข้าซื้อ</th>
                    <th style="padding:10px 8px; color:var(--accent-red);">จุดคัทออก</th>
                    <th style="padding:10px 8px; color: #c084fc;">จุดขายทำกำไร</th>
                    <th style="padding:10px 8px; color:var(--text-muted); text-align:center;">การกระทำ</th>
                  </tr>
                </thead>
                <tbody id="watchlist-targets-tbody">
                  <!-- Watchlist stocks will render here -->
                </tbody>
              </table>
            </div>
          </div>

          <!-- TradingView Live Chart Widget Section -->
          <div class="glass-panel" style="flex: 1; display:flex; flex-direction:column; overflow:hidden; padding: 10px;">
            <div style="font-size: 12px; font-weight: 600; color: var(--text-secondary); margin-bottom: 8px; display:flex; align-items:center; gap:6px;">
              <i data-lucide="line-chart" style="width:14px;height:14px;color:var(--accent-cyan);"></i>
              <span id="tv-chart-title">TradingView Chart (เลือกหุ้นเพื่อเปิดดูกราฟ)</span>
            </div>
            <div id="tv-chart-container" style="flex:1; background: rgba(0,0,0,0.2); border-radius: 6px; overflow:hidden; display:flex; align-items:center; justify-content:center; color:var(--text-muted);">
              <div style="text-align:center; padding:20px;">
                <i data-lucide="line-chart" style="width:36px;height:36px;opacity:0.2;margin-bottom:8px;"></i>
                <p style="font-size:11px;">คลิกเลือกหุ้นจากตาราง Watchlist ด้านซ้าย เพื่อโหลดกราฟสดที่นี่</p>
              </div>
            </div>
          </div>
        </div>

      </div><!-- end page-container -->
    """
    
    # Locate index of page-container start and end, and replace the whole block
    start_idx = content.find(old_pages_start)
    end_idx = content.find(old_pages_end)
    
    if start_idx != -1 and end_idx != -1:
        # Include the end tag in the replacement range
        end_idx += len(old_pages_end)
        content = content[:start_idx] + new_pages_html + content[end_idx:]
        print("✅ Replaced page-container HTML successfully.")
    else:
        print("⚠️ Warning: page-container tags not found for replacement.")

    # 4. Inject Floating Bot HTML in the body (just before </body>)
    floating_bot_html = """
    <!-- ===== FLOATING AI ADVISOR BOT ===== -->
    <div id="floating-bot-trigger" onclick="toggleFloatingBot()" title="คุยกับบอทคู่คิด">
      <i data-lucide="message-square" style="width:24px;height:24px;color:#000;"></i>
    </div>
    
    <div id="floating-bot-chat" class="glass-panel">
      <div class="floating-chat-header">
        <div style="display:flex; align-items:center; gap:8px;">
          <span style="display:inline-block; width:8px; height:8px; background:var(--accent-cyan); border-radius:50%; box-shadow:0 0 8px var(--accent-cyan);"></span>
          <span style="font-weight:600; font-size:14px; color:#fff;">บอทที่ปรึกษา AI</span>
        </div>
        <i data-lucide="x" style="width:16px;height:16px;cursor:pointer;color:var(--text-muted);" onclick="toggleFloatingBot()"></i>
      </div>
      <div class="floating-chat-body" id="floating-chat-messages">
        <div class="chat-msg ai">สวัสดีครับพี่กัณฑ์! ผมคือบอทคู่คิดวิเคราะห์หุ้น เปิดหน้าไหนผมจะดูข้อมูลหน้านั้นมารอเลย มีอะไรอยากปรึกษา หรืออยากให้ช่วยรัน Backtest พิมพ์บอกผมได้เลยครับ!</div>
      </div>
      <div class="floating-chat-footer">
        <input type="text" id="floating-chat-input" placeholder="ถามคำถาม หรือสั่งควบคุมหน้าจอ..." onkeydown="if(event.key==='Enter') sendFloatingChat()" />
        <button onclick="sendFloatingChat()">ส่ง</button>
      </div>
    </div>
    
    </body>
    """
    content = content.replace("</body>", floating_bot_html)

    # 5. Overwrite the navigation logic switchPage and add new rendering functions
    # Let's find the switchPage function to replace it.
    old_switch_page_start = "      function switchPage(tabId) {"
    # We will search for this function and replace it with a brand new implementation of switchPage and the custom page renders
    
    new_js_logic = """
      // ====== NEW WEB APP NAVIGATION & RENDERS ======
      let currentActiveContext = 'Home';

      function switchPage(tabId) {
        currentTab = tabId;
        
        // Update tab buttons active state
        document.querySelectorAll('.tab-bar .tab-btn').forEach(b => {
          if (b.getAttribute('data-tab') === tabId) {
            b.classList.add('active');
          } else {
            b.classList.remove('active');
          }
        });
        
        // Hide all pages
        document.querySelectorAll('.page-container .page').forEach(p => {
          p.classList.remove('active');
          p.style.display = 'none';
        });
        
        const page = $('page-' + tabId);
        if (page) {
          page.classList.add('active');
          page.style.display = 'flex';
        }
        
        // Update context & trigger specific renders
        if (tabId === 'styles-guide') {
          currentActiveContext = 'หน้าสไตล์หุ้น (Investment Playbooks & Guides)';
          renderStylesGuide();
        } else if (tabId === 'stock-reader') {
          currentActiveContext = 'หน้าค้นอ่านข้อมูลหุ้นเจาะลึก (Searchable Stock Reader)';
          renderStockReaderList();
        } else if (tabId === 'categorization-board') {
          currentActiveContext = 'หน้าบอร์ดจัดกลุ่มประเภทสไตล์หุ้น (Categorization Grid)';
          renderCategorizationBoard();
        } else if (tabId === 'watchlist-targets') {
          currentActiveContext = 'หน้าจอรายการเฝ้าสังเกตการณ์เป้าหมาย (Watchlist Targets)';
          renderWatchlistTargets();
        }
        
        lucide.createIcons();
      }

      // 1. PAGE 1: RENDER STOCK STYLES GUIDE
      const STYLE_DOCS = [
        { id: 'bible', title: '💡 วิธีการหาไอเดียลงทุน (Idea Generation)', path: './01_playbooks/00_idea_generation_bible.md' },
        { id: 'growth', title: '📈 1. หุ้นเติบโต (Disruptive Compounder)', path: './01_playbooks/01_disruptive_compounder.md' },
        { id: 'reentry', title: '🔄 2. หุ้นผู้ชนะเดิมรอซื้อใหม่ (Old Winners Re-entry)', path: './01_playbooks/02_old_winners_reentry.md' },
        { id: 'indirect', title: '🧱 3. หุ้นผู้ช่วยพระเอก (Second-Order Beneficiaries)', path: './01_playbooks/03_second_order_beneficiaries.md' },
        { id: 'bottleneck', title: '🔌 4. หุ้นคอขวดที่ห้ามขาด (Infrastructure Bottleneck)', path: './01_playbooks/04_infrastructure_bottleneck.md' },
        { id: 'inflection', title: '💥 5. หุ้นกำไรระเบิด (Earnings Inflection)', path: './01_playbooks/05_earnings_inflection.md' },
        { id: 'turnaround', title: '🧬 6. หุ้นฟื้นไข้ตามเทรนด์เดือน (Turnaround Monthly)', path: './01_playbooks/06_turnaround_monthly_trend.md' }
      ];
      let selectedStyleDocId = 'bible';

      async function renderStylesGuide() {
        const listDiv = $('styles-guide-list');
        if (!listDiv) return;
        
        listDiv.innerHTML = STYLE_DOCS.map(doc => `
          <div class="stock-item ${doc.id === selectedStyleDocId ? 'active' : ''}" onclick="selectStyleDoc('${doc.id}')">
            <div style="font-weight: 500; font-size: 12px;">${doc.title}</div>
          </div>
        `).join('');
        
        const activeDoc = STYLE_DOCS.find(d => d.id === selectedStyleDocId);
        const contentDiv = $('styles-guide-content');
        if (activeDoc && contentDiv) {
          contentDiv.innerHTML = '<p style="color:var(--text-muted); padding:20px;">กำลังเปิดสมุดคู่มือ...</p>';
          const html = await loadLocalMarkdown(activeDoc.path);
          contentDiv.innerHTML = html;
        }
      }

      window.selectStyleDoc = function(docId) {
        selectedStyleDocId = docId;
        renderStylesGuide();
      };

      async function loadLocalMarkdown(path) {
        try {
          const res = await fetch(path);
          if (res.ok) {
            const md = await res.text();
            return marked.parse(md);
          }
          return `<p style="color:var(--accent-red);">ไม่พบไฟล์เอกสาร: ${path}</p>`;
        } catch (e) {
          return `<p style="color:var(--accent-red);">เกิดข้อผิดพลาดในการดึงไฟล์: ${e.message}</p>`;
        }
      }

      // 2. PAGE 2: RENDER SEARCHABLE STOCK READER
      let selectedReaderTicker = '';
      function renderStockReaderList() {
        const listDiv = $('reader-stock-list');
        const query = ($('reader-search-input')?.value || '').toLowerCase().trim();
        if (!listDiv) return;

        const filtered = STOCKS.filter(s => 
          s.ticker.toLowerCase().includes(query) || 
          s.name.toLowerCase().includes(query)
        );

        listDiv.innerHTML = filtered.map(s => `
          <div class="stock-item ${s.ticker === selectedReaderTicker ? 'active' : ''}" onclick="selectReaderStock('${s.ticker}')">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <span style="font-weight:700; color:var(--accent-cyan);">${s.ticker}</span>
              <span style="font-size:10px; color:var(--text-muted);">${s.style || 'ทั่วไป'}</span>
            </div>
            <div style="font-size:11px; color:var(--text-secondary); margin-top:2px;">${s.name}</div>
          </div>
        `).join('');
      }

      window.selectReaderStock = function(ticker) {
        selectedReaderTicker = ticker;
        currentActiveContext = `หน้าข้อมูลวิจัยหุ้นเดี่ยว: ${ticker}`;
        renderStockReaderList();
        renderStockReaderContent(ticker);
      };

      function renderStockReaderContent(ticker) {
        const contentDiv = $('reader-content');
        if (!contentDiv) return;
        const s = STOCKS.find(x => x.ticker === ticker);
        if (!s) return;

        // Render financial statement table
        let finTable = '<p style="color:var(--text-muted); font-size:12px;">ไม่มีข้อมูลตารางงบการเงินสะสม (สามารถสั่งรัน fetch_financials.py ได้)</p>';
        if (s.financials && s.financials.length > 0) {
          finTable = `
            <table class="edit-table">
              <thead>
                <tr>
                  <th>ปี (Year)</th>
                  <th>รายได้ (Total Revenue)</th>
                  <th>กำไรสุทธิ (Net Income)</th>
                  <th>YoY Growth</th>
                </tr>
              </thead>
              <tbody>
                ${s.financials.map(f => `
                  <tr>
                    <td><b>${f.year}</b></td>
                    <td>$${(f.revenue/1e6).toFixed(1)}M</td>
                    <td>$${(f.profit/1e6).toFixed(1)}M</td>
                    <td style="color:${parseFloat(f.growth) >= 15 ? 'var(--accent-green)' : 'inherit'}">${f.growth}</td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          `;
        }

        contentDiv.innerHTML = `
          <div class="book-reader" style="max-width:100%; padding: 10px;">
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid var(--border-color); padding-bottom:15px; margin-bottom:20px;">
              <div>
                <h1 style="margin:0; font-size:28px; color:var(--accent-cyan); font-family:'Outfit';">${s.name} (${s.ticker})</h1>
                <div style="display:flex; gap:10px; margin-top:6px;">
                  <span class="badge" style="background:rgba(0,240,255,0.15); color:var(--accent-cyan); font-size:11px;">${s.style || 'ทั่วไป'}</span>
                  <span class="badge" style="background:rgba(168,85,247,0.15); color:#c084fc; font-size:11px;">${s.group || 'ไม่มีกลุ่ม'}</span>
                </div>
              </div>
              ${s.logoUrl ? `<img src="${s.logoUrl}" style="width:50px; height:50px; border-radius:8px; border:1px solid var(--border-color);" />` : ''}
            </div>

            <h2>💰 1. โมเดลการหาเงินหลัก (Revenue Model)</h2>
            <p><b>ลักษณะธุรกิจ:</b> ${s.whatItDoes || '-'}</p>
            <p><b>กลไกสร้างรายได้:</b> ${s.howItMakesMoney || '-'}</p>

            <h2>🧱 2. ความแข็งแกร่งและคอขวดธุรกิจ (Moat & Advantage)</h2>
            <p>${s.moat ? marked.parse(s.moat) : '-'}</p>

            <h2>⚠️ 3. ข้อเสียและความเสี่ยงสำคัญ (Risks & Bear Case)</h2>
            <p>${s.risks ? marked.parse(s.risks) : '-'}</p>

            <h2>🤝 4. ดีลและตัวเร่งสำคัญ (Deals & Catalysts)</h2>
            <p>${s.deals ? marked.parse(s.deals) : '-'}</p>

            <h2>📊 5. งบการเงินย้อนหลัง (Financial Statements)</h2>
            ${finTable}
          </div>
        `;
      }

      if ($('reader-search-input')) $('reader-search-input').addEventListener('input', renderStockReaderList);

      // 3. PAGE 3: RENDER CATEGORIZATION BOARD
      let selectedFilterStyle = 'ALL';
      const AVAILABLE_STYLES = ['ALL', 'Growth', 'Dividend', 'Core', 'Cyclical', 'ETF', 'Defensive', 'Dark Horse'];

      function renderCategorizationBoard() {
        const chipsDiv = $('board-style-chips');
        const gridDiv = $('board-cards-grid');
        if (!chipsDiv || !gridDiv) return;

        // Render filter chips
        chipsDiv.innerHTML = AVAILABLE_STYLES.map(style => `
          <div class="chip ${style === selectedFilterStyle ? 'active' : ''}" onclick="filterBoardStyle('${style}')">${style === 'ALL' ? '🌎 ทั้งหมด' : style}</div>
        `).join('');

        // Filter stocks
        const filtered = STOCKS.filter(s => {
          if (selectedFilterStyle === 'ALL') return true;
          return (s.style || '').toLowerCase().includes(selectedFilterStyle.toLowerCase());
        });

        if (filtered.length === 0) {
          gridDiv.innerHTML = `<p style="color:var(--text-muted); text-align:center; padding:40px; grid-column: 1/-1;">ไม่มีหุ้นในสไตล์ "${selectedFilterStyle}"</p>`;
          return;
        }

        gridDiv.innerHTML = filtered.map(s => `
          <div class="stock-card glass-panel" onclick="selectReaderStockAndSwitch('${s.ticker}')">
            <div class="card-header">
              <div>
                <h3 class="card-title">${s.name}</h3>
                <span class="card-ticker">${s.ticker}</span>
              </div>
              ${s.logoUrl ? `<img src="${s.logoUrl}" class="card-logo" />` : '<div class="card-logo" style="background:rgba(255,255,255,0.05); display:flex; align-items:center; justify-content:center; font-size:10px;">No Logo</div>'}
            </div>
            <div class="card-body">
              <div class="card-meta">
                <span class="badge" style="background:rgba(0,240,255,0.1); color:var(--accent-cyan); font-size:10px;">${s.style || 'ทั่วไป'}</span>
                <span class="badge" style="background:rgba(255,165,0,0.1); color:var(--accent-orange); font-size:10px;">${s.market || 'US'}</span>
              </div>
              <p style="font-size:11px; line-height:1.4; color:var(--text-secondary); margin-top:8px;">${s.whatItDoes || '-'}</p>
            </div>
          </div>
        `).join('');
      }

      window.filterBoardStyle = function(style) {
        selectedFilterStyle = style;
        renderCategorizationBoard();
      };

      window.selectReaderStockAndSwitch = function(ticker) {
        switchPage('stock-reader');
        selectReaderStock(ticker);
      };

      // 4. PAGE 4: RENDER WATCHLIST TARGETS & TRADINGVIEW
      let selectedWatchlistTicker = '';

      function renderWatchlistTargets() {
        const tbody = $('watchlist-targets-tbody');
        if (!tbody) return;

        // Get watchlisted stocks (e.g. from watchlists files or just the ones tagged as Watchlist)
        // Let's render all stocks in our database that have target/entry prices or let the user watchlist any
        tbody.innerHTML = STOCKS.map(s => {
          const isSelected = s.ticker === selectedWatchlistTicker;
          return `
            <tr style="border-bottom:1px solid var(--border-color); cursor:pointer; background:${isSelected ? 'rgba(0,240,255,0.05)' : 'none'};" onclick="selectWatchlistStock('${s.ticker}')">
              <td style="padding:10px 8px;">
                <div style="font-weight:700; color:var(--accent-cyan);">${s.ticker}</div>
                <div style="font-size:11px; color:var(--text-muted);">${s.name}</div>
              </td>
              <td style="padding:10px 8px; font-weight:500;" id="price-${s.ticker}">-</td>
              <td style="padding:10px 8px;"><span class="target-badge target-entry">${s.entry_price || s.entryPrice || '-'}</span></td>
              <td style="padding:10px 8px;"><span class="target-badge target-exit">${s.exit_price || s.exitPrice || '-'}</span></td>
              <td style="padding:10px 8px;"><span class="target-badge target-sell">${s.targetPrice || s.target_price || '-'}</span></td>
              <td style="padding:10px 8px; text-align:center;">
                <button class="tab-action-btn" onclick="event.stopPropagation(); editWatchlistTargets('${s.ticker}')" style="font-size:11px; padding:3px 8px;">✏️ ตั้งเป้า</button>
              </td>
            </tr>
          `;
        }).join('');

        // Load prices
        const tickers = STOCKS.map(s => s.ticker);
        updateWatchlistPrices(tickers);
      }

      window.selectWatchlistStock = function(ticker) {
        selectedWatchlistTicker = ticker;
        currentActiveContext = `หน้า Watchlist: กำลังดูหุ้น ${ticker}`;
        
        // Re-render table row highlights
        renderWatchlistTargets();

        // Render TradingView Chart
        const chartTitle = $('tv-chart-title');
        const container = $('tv-chart-container');
        if (chartTitle) chartTitle.innerText = `กราฟสด TradingView: ${ticker}`;
        if (container) {
          container.innerHTML = getTradingViewIFrame(ticker);
        }
      };

      function getTradingViewIFrame(symbol) {
        let cleanSymbol = symbol.trim().toUpperCase();
        if (cleanSymbol.includes(':')) {
          cleanSymbol = cleanSymbol.split(':')[1];
        }
        // Embed interactive chart widget
        return `<iframe 
          style="width: 100%; height: 100%; border: none;" 
          src="https://s.tradingview.com/widgetembed/?symbol=${cleanSymbol}&interval=D&theme=dark&style=1&timezone=Asia%2FBangkok&locale=th"
          allowfullscreen>
        </iframe>`;
      }

      window.editWatchlistTargets = function(ticker) {
        const s = STOCKS.find(x => x.ticker === ticker);
        if (!s) return;
        
        const entry = prompt(`ตั้งเป้าหมายจุดเข้าซื้อ (Entry) ของ ${ticker}:`, s.entry_price || s.entryPrice || '');
        const exit = prompt(`ตั้งเป้าหมายจุดคัทขาดทุน (Exit/Cut) ของ ${ticker}:`, s.exit_price || s.exitPrice || '');
        const target = prompt(`ตั้งเป้าหมายราคาขาย (Target/Sell) ของ ${ticker}:`, s.targetPrice || '');
        
        if (entry !== null) s.entry_price = entry;
        if (exit !== null) s.exit_price = exit;
        if (target !== null) s.targetPrice = target;
        
        saveStocks();
        renderWatchlistTargets();
      };

      // 5. FLOATING AI ADVISOR BOT LOGIC
      window.toggleFloatingBot = function() {
        const chat = $('floating-bot-chat');
        if (!chat) return;
        if (chat.style.display === 'flex') {
          chat.style.display = 'none';
        } else {
          chat.style.display = 'flex';
          // Auto-scroll chat body
          const body = $('floating-chat-messages');
          if (body) body.scrollTop = body.scrollHeight;
        }
      };

      window.sendFloatingChat = async function() {
        const input = $('floating-chat-input');
        const body = $('floating-chat-messages');
        if (!input || !body) return;
        
        const text = input.value.trim();
        if (!text) return;
        
        // Add user message
        body.innerHTML += `<div class="chat-msg user">${text}</div>`;
        input.value = '';
        body.scrollTop = body.scrollHeight;

        // Display typing state
        const typingId = 'typing-' + Date.now();
        body.innerHTML += `<div class="chat-msg ai" id="${typingId}">กำลังประมวลผลคำปรึกษา...</div>`;
        body.scrollTop = body.scrollHeight;

        try {
          // Prepare context-aware prompt
          const systemContext = `บริบทหน้าจอที่ผู้ใช้กำลังเปิดดูในปัจจุบัน: ${currentActiveContext}\\n\\n`;
          const finalPrompt = systemContext + text;

          // Call API (Gemini Client in dashboard.html)
          let responseText = '';
          if (config.apiKey) {
            const apiModel = config.model || 'gemini-2.0-flash';
            const endpoint = `https://generativelanguage.googleapis.com/v1beta/models/${apiModel}:generateContent?key=${config.apiKey}`;
            
            const payload = {
              contents: [{ parts: [{ text: finalPrompt }] }],
              generationConfig: { maxOutputTokens: 1200 }
            };
            
            const res = await fetch(endpoint, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(payload)
            });
            
            if (res.ok) {
              const data = await res.json();
              responseText = data.candidates?.[0]?.content?.parts?.[0]?.text || 'ไม่สามารถดึงคำตอบได้';
            } else {
              responseText = `เกิดข้อผิดพลาดในการโทรหา API: ${res.statusText}`;
            }
          } else {
            responseText = '⚠️ บอทยังไม่ได้รับการเชื่อมต่อ API Key กรุณาเปิดไปที่รูปฟันเฟืองมุมบนขวาเพื่อกรอก API Key ก่อนคุยครับ';
          }

          // Replace typing with response
          const typingDiv = $(typingId);
          if (typingDiv) {
            typingDiv.innerHTML = marked.parse(responseText);
          }
          
          // Check for Screen Control commands in AI response
          // e.g. [ACTION: switch_tab(watchlist-targets)] or [ACTION: show_chart(VRT)]
          if (responseText.includes('[ACTION:')) {
            const match = responseText.match(/\\[ACTION:\\s*(\\w+)\\(([^)]*)\\)\\s*\\]/);
            if (match) {
              const action = match[1];
              const arg = match[2].replace(/['"]/g, '').trim();
              executeUIAction(action, arg);
            }
          }
        } catch(e) {
          const typingDiv = $(typingId);
          if (typingDiv) typingDiv.innerText = `Error: ${e.message}`;
        }
        body.scrollTop = body.scrollHeight;
      };

      function executeUIAction(action, arg) {
        console.log('Bot UI Control Triggered:', action, arg);
        if (action === 'switch_tab') {
          switchPage(arg);
        } else if (action === 'show_chart') {
          switchPage('watchlist-targets');
          selectWatchlistStock(arg);
        } else if (action === 'filter_style') {
          switchPage('categorization-board');
          filterBoardStyle(arg);
        }
      }
    """
    
    # Locate switchPage and replace the whole chunk with our new renders
    start_sp = content.find("      function switchPage(tabId) {")
    end_sp = content.find("      // ====== TAB BAR CRUD ======")
    
    if start_sp != -1 and end_sp != -1:
        content = content[:start_sp] + new_js_logic + "\n" + content[end_sp:]
        print("✅ Replaced switchPage and navigation JS successfully.")
    else:
        print("⚠️ Warning: switchPage function not found for replacement.")

    # 6. Finally, update the init() loop to open the default new tab
    old_init_body = """        updateApiDot();
        buildGroupFilter();
        renderStockList();
        renderPlaybook();
        renderSelectionPage();
        renderChat();
        lucide.createIcons();

        // Async sync from Supabase if credentials exist
        initSupabase();
        if (supabaseClient) {
          syncFromSupabase().then(ok => {
            if (ok) {
              console.log('Async sync from Supabase completed.');
              buildGroupFilter();
              renderStockList();
              renderPortfolio();
            }
          });
        }"""
        
    new_init_body = """        updateApiDot();
        switchPage('styles-guide');
        
        // Initialize Supabase and auto-sync
        initSupabase();
        if (supabaseClient) {
          syncFromSupabase().then(ok => {
            if (ok) {
              console.log('Async sync from Supabase completed.');
              renderStylesGuide();
              renderStockReaderList();
              renderCategorizationBoard();
              renderWatchlistTargets();
            }
          });
        }"""
        
    content = content.replace(old_init_body, new_init_body)
    print("✅ Updated init function.")

    # Write the modified content back to dashboard.html
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"🎉 Successfully rebuilt {file_path}! Cleaned, restructured, and updated.")

if __name__ == "__main__":
    rebuild()
