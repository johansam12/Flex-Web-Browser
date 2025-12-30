import sys, os
# --- 1. FORCE TASKBAR ICON & NAME FIX ---
import ctypes
try:
    # This ID tells Windows: "I am a real app named Flex, not just Python"
    myappid = 'flex.browser.ai.v7' 
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass
# -----------------------------------------

import markdown # pip install markdown
from PyQt6.QtWidgets import *
from PyQt6.QtWebEngineWidgets import *
from PyQt6.QtWebEngineCore import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from AI_engine import get_ai_research

# --- FLEX HOME PAGE ---
HOME_PAGE_HTML = """
<!DOCTYPE html>
<html>
<head>
<style>
    body { background-color: #121212; color: #e0e0e0; font-family: 'Segoe UI', sans-serif; margin: 0; display: flex; flex-direction: column; height: 100vh; overflow: hidden; }
    .content { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding-bottom: 100px; }
    h1 { font-size: 80px; margin: 0; letter-spacing: -2px; background: linear-gradient(135deg, #00d2ff, #3a7bd5); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    p { font-size: 18px; color: #666; margin-top: 10px; margin-bottom: 40px; }
    .search-box { 
        width: 600px; padding: 20px 30px; border-radius: 40px; border: none; 
        background: #1e1e1e; color: white; font-size: 18px; outline: none; 
        box-shadow: 0 4px 20px rgba(0,0,0,0.5); transition: 0.3s; 
    }
    .search-box:focus { box-shadow: 0 0 25px rgba(0, 210, 255, 0.3); background: #252525; }
    .speed-dial { display: flex; gap: 20px; margin-top: 50px; }
    .card { 
        background: #1e1e1e; padding: 20px; border-radius: 18px; width: 100px; 
        text-align: center; text-decoration: none; color: #ccc; font-weight: 500; 
        transition: 0.3s; box-shadow: 0 4px 10px rgba(0,0,0,0.2); 
    }
    .card:hover { transform: translateY(-5px); background: #2d2d2d; color: #00d2ff; }
</style>
</head>
<body>
    <div class="content">
        <h1>Flex</h1>
        <p>Browse smarter.</p>
        <form action="https://www.google.com/search" method="get">
            <input type="text" name="q" class="search-box" placeholder="Search or enter web address" autofocus>
        </form>
        <div class="speed-dial">
            <a href="https://google.com" class="card">Google</a>
            <a href="https://youtube.com" class="card">YouTube</a>
            <a href="https://github.com" class="card">GitHub</a>
            <a href="https://chatgpt.com" class="card">ChatGPT</a>
        </div>
    </div>
</body>
</html>
"""

# --- HELPER: GENERATE PRO LOGO ---
def create_app_icon():
    size = 64
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    # Background Gradient
    gradient = QLinearGradient(0, 0, size, size)
    gradient.setColorAt(0.0, QColor("#00d2ff")) 
    gradient.setColorAt(1.0, QColor("#3a7bd5")) 
    painter.setBrush(gradient)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawRoundedRect(0, 0, size, size, 15, 15)
    
    # "Flex" Symbol (Arrow)
    path = QPainterPath()
    path.moveTo(size*0.3, size*0.3)
    path.lineTo(size*0.7, size*0.3)
    path.lineTo(size*0.4, size*0.5)
    path.lineTo(size*0.7, size*0.7)
    path.lineTo(size*0.3, size*0.7)
    path.closeSubpath()
    
    painter.setBrush(QColor("white"))
    painter.drawPath(path)
    painter.end()
    return QIcon(pixmap)

# --- CUSTOM TITLE BAR ---
class FlexTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setFixedHeight(40)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(15, 0, 10, 0)
        self.layout.setSpacing(15)

        # 1. LOGO ON TITLE BAR
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(24, 24)
        self.icon_label.setPixmap(create_app_icon().pixmap(24, 24))
        
        self.title_label = QLabel("Flex")
        self.title_label.setStyleSheet("color: #ccc; font-weight: 600; font-family: 'Segoe UI'; font-size: 13px;")

        # Window Controls
        self.min_btn = self.create_win_btn("─", self.parent.showMinimized)
        self.max_btn = self.create_win_btn("⬜", self.toggle_maximize)
        self.close_btn = self.create_win_btn("✕", self.parent.close, is_close=True)

        self.layout.addWidget(self.icon_label)
        self.layout.addWidget(self.title_label)
        self.layout.addStretch()
        self.layout.addWidget(self.min_btn)
        self.layout.addWidget(self.max_btn)
        self.layout.addWidget(self.close_btn)

    def create_win_btn(self, text, func, is_close=False):
        btn = QPushButton(text)
        btn.setFixedSize(30, 30)
        btn.clicked.connect(func)
        bg_hover = "#e81123" if is_close else "#333"
        btn.setStyleSheet(f"""
            QPushButton {{ background: transparent; color: #888; border: none; border-radius: 15px; font-weight: bold; }}
            QPushButton:hover {{ background: {bg_hover}; color: white; }}
        """)
        return btn

    def toggle_maximize(self):
        if self.parent.isMaximized(): self.parent.showNormal()
        else: self.parent.showMaximized()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.parent.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self.parent.old_pos:
            delta = event.globalPosition().toPoint() - self.parent.old_pos
            self.parent.move(self.parent.pos() + delta)
            self.parent.old_pos = event.globalPosition().toPoint()

# --- MAIN BROWSER ---
class FlexBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(1400, 900)
        self.old_pos = None
        
        # --- 2. THE CRITICAL FIXES ---
        self.setWindowTitle("Flex") # Shows "Flex" on Hover
        self.setWindowIcon(create_app_icon()) # Shows Custom Logo on Taskbar
        # -----------------------------

        self.container = QWidget()
        self.container.setStyleSheet("background-color: #0c0c0c; border-radius: 10px; border: 1px solid #222;")
        self.setCentralWidget(self.container)
        self.layout = QVBoxLayout(self.container)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.title_bar = FlexTitleBar(self)
        self.layout.addWidget(self.title_bar)
        
        self.setup_toolbar()
        
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.tabBarClicked.connect(self.check_plus_click)
        self.layout.addWidget(self.tabs)

        self.setup_ai_sidebar()
        self.apply_style()

        self.add_tab(None, "Home")
        self.add_plus_tab()

    def setup_toolbar(self):
        self.toolbar = QToolBar()
        self.toolbar.setMovable(False)
        self.toolbar.setFixedHeight(55) 
        self.toolbar.setStyleSheet("background: #0c0c0c; border-bottom: 1px solid #1a1a1a; padding: 0 10px; spacing: 10px;")
        self.layout.addWidget(self.toolbar)

        self.add_nav_btn("🡠", self.go_back)
        self.add_nav_btn("🡢", self.go_forward)
        self.add_nav_btn("↻", self.reload_page)

        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Search or enter web address")
        self.url_bar.returnPressed.connect(self.navigate)
        self.toolbar.addWidget(self.url_bar)

        self.ai_btn = QPushButton("✨")
        self.ai_btn.setFixedSize(35, 35)
        self.ai_btn.setCheckable(True)
        self.ai_btn.clicked.connect(self.toggle_ai)
        self.toolbar.addWidget(self.ai_btn)

    def add_nav_btn(self, text, func):
        btn = QPushButton(text)
        btn.setFixedSize(50, 40)
        btn.clicked.connect(func)
        btn.setStyleSheet("""
            QPushButton { 
                background: transparent; color: #ccc; border-radius: 20px; 
                font-size: 24px; font-weight: bold; margin-right: 5px; padding-bottom: 3px;
            }
            QPushButton:hover { background: #333; color: white; }
        """)
        self.toolbar.addWidget(btn)

    # --- PROFESSIONAL AI SIDEBAR ---
    def setup_ai_sidebar(self):
        self.dock = QDockWidget(self)
        self.dock.setTitleBarWidget(QWidget())
        
        container = QWidget()
        container.setStyleSheet("background: #1e1e1e; border-left: 1px solid #333;")
        layout = QVBoxLayout(container)
        
        # Chat Display
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("""
            QTextEdit { border: none; color: #e0e0e0; font-size: 14px; padding: 10px; }
            ul { margin-left: -20px; }
            li { margin-bottom: 8px; }
            strong, b { color: #00d2ff; }
        """)
        self.chat_display.setHtml("""
            <div style='text-align:center; color:#888; margin-top:20px;'>
                <h2 style='color:#00d2ff;'>Flex AI</h2>
                <p>Hi! What can I help you research?</p>
            </div>
        """)
        layout.addWidget(self.chat_display)
        
        # Input Bar
        input_layout = QHBoxLayout()
        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText("Ask Flex AI...")
        self.chat_input.setStyleSheet("background: #2b2b2b; color: white; border: 1px solid #444; border-radius: 15px; padding: 8px;")
        self.chat_input.returnPressed.connect(self.process_ai_query)
        
        send_btn = QPushButton("➤")
        send_btn.setFixedSize(35, 35)
        send_btn.clicked.connect(self.process_ai_query)
        send_btn.setStyleSheet("background: #00d2ff; color: #000; border-radius: 17px; font-weight: bold; border: none;")
        
        input_layout.addWidget(self.chat_input)
        input_layout.addWidget(send_btn)
        
        layout.addLayout(input_layout)
        
        self.dock.setWidget(container)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock)
        self.dock.hide()

    def process_ai_query(self):
        user_text = self.chat_input.text().strip()
        if not user_text: return
        
        self.chat_display.append(f"<div style='text-align:right; margin-bottom:10px;'><span style='background:#00d2ff; color:black; padding:5px 10px; border-radius:10px;'>{user_text}</span></div>")
        self.chat_input.clear()
        QApplication.processEvents() 
        
        try:
            raw_response = get_ai_research(user_text)
            formatted_html = markdown.markdown(raw_response)
            
            html_block = f"""
            <div style='background:#2d2d2d; padding:15px; border-radius:15px; margin-bottom:15px;'>
                <b style='color:#00d2ff; font-size:1.1em;'>Flex AI:</b><br>
                {formatted_html}
            </div>
            """
            self.chat_display.append(html_block)
            
        except Exception as e:
            self.chat_display.append(f"<p style='color:red'>Error: {str(e)}</p>")
            
        sb = self.chat_display.verticalScrollBar()
        sb.setValue(sb.maximum())

    def toggle_ai(self):
        self.dock.setVisible(not self.dock.isVisible())

    def add_tab(self, url=None, label="New Tab"):
        browser = QWebEngineView()
        if url: browser.setUrl(url)
        else: browser.setHtml(HOME_PAGE_HTML)
        
        idx = self.tabs.count() - 1 if self.tabs.count() > 0 else 0
        self.tabs.insertTab(idx, browser, label)
        self.tabs.setCurrentIndex(idx)
        
        browser.urlChanged.connect(lambda u: self.update_url_bar(u))
        browser.titleChanged.connect(lambda t: self.tabs.setTabText(self.tabs.indexOf(browser), t[:15]))
        browser.iconChanged.connect(lambda icon: self.tabs.setTabIcon(self.tabs.indexOf(browser), icon))

    def update_url_bar(self, url):
        url_str = url.toString()
        if url_str.startswith("data:"):
            self.url_bar.setText("")
            self.url_bar.setPlaceholderText("Search or enter web address")
        else:
            self.url_bar.setText(url_str)

    def add_plus_tab(self):
        self.plus_widget = QWidget()
        self.tabs.addTab(self.plus_widget, "+")
        self.tabs.tabBar().setTabButton(self.tabs.count()-1, QTabBar.ButtonPosition.RightSide, None)

    def check_plus_click(self, index):
        if index == self.tabs.count() - 1:
            self.add_tab(None, "New Tab")

    def close_tab(self, index):
        if index == self.tabs.count() - 1: return 
        self.tabs.removeTab(index)
        if self.tabs.currentIndex() == self.tabs.count() - 1:
            self.tabs.setCurrentIndex(self.tabs.count() - 2)
        if self.tabs.count() == 1: self.close()

    def apply_style(self):
        self.setStyleSheet("""
            QTabWidget::pane { border: 0; background: #0c0c0c; }
            QTabBar::tab { 
                background: transparent; color: #888; padding: 8px 15px; 
                border-top-left-radius: 8px; border-top-right-radius: 8px;
                min-width: 120px; max-width: 200px;
            }
            QTabBar::tab:selected { background: #1e1e1e; color: #00d2ff; border-bottom: 2px solid #00d2ff; }
            QTabBar::tab:hover { background: #151515; color: white; }
            QTabBar::tab:last { color: #888; min-width: 30px; font-size: 18px; }
            QTabBar::tab:last:hover { color: #00d2ff; }
            QLineEdit { 
                background: #1a1a1a; color: white; border: 1px solid #333; 
                border-radius: 20px; padding: 8px 20px; font-size: 14px;
                selection-background-color: #00d2ff;
            }
            QLineEdit:focus { border: 1px solid #00d2ff; }
        """)

    def navigate(self):
        u = QUrl(self.url_bar.text())
        if u.scheme() == "": u.setScheme("https")
        self.tabs.currentWidget().setUrl(u)

    def go_back(self): self.tabs.currentWidget().back()
    def go_forward(self): self.tabs.currentWidget().forward()
    def reload_page(self): self.tabs.currentWidget().reload()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FlexBrowser()
    window.show()
    sys.exit(app.exec())