"""
SIAPS - GUI Main Application
Main window and application entry point
"""
import customtkinter as ctk
from typing import Optional
import sys
from pathlib import Path

# Add project root to Python path
ROOT_DIR = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from config.settings import APP_NAME, APP_VERSION, THEME, WINDOW_WIDTH, WINDOW_HEIGHT
from src.utils import setup_logger

logger = setup_logger(__name__)


class MainApplication(ctk.CTk):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        # Window configuration
        self.title(f"{APP_NAME} v{APP_VERSION}")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        
        # Set theme
        ctk.set_appearance_mode(THEME)
        ctk.set_default_color_theme("blue")
        
        # Create UI
        self.create_widgets()
        
        logger.info("Main application initialized")
    
    def create_widgets(self):
        """Create main UI widgets"""
        
        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Sidebar
        self.create_sidebar()
        
        # Main content area
        self.create_main_content()
    
    def create_sidebar(self):
        """Create sidebar with navigation"""
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(10, weight=1)
        
        # Logo/Title
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame,
            text=APP_NAME,
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Navigation buttons
        self.prediction_button = ctk.CTkButton(
            self.sidebar_frame,
            text="股票预测",
            command=self.show_prediction_view
        )
        self.prediction_button.grid(row=1, column=0, padx=20, pady=10)
        
        self.watchlist_button = ctk.CTkButton(
            self.sidebar_frame,
            text="观测池",
            command=self.show_watchlist_view
        )
        self.watchlist_button.grid(row=2, column=0, padx=20, pady=10)
        
        self.history_button = ctk.CTkButton(
            self.sidebar_frame,
            text="历史记录",
            command=self.show_history_view
        )
        self.history_button.grid(row=3, column=0, padx=20, pady=10)
        
        self.settings_button = ctk.CTkButton(
            self.sidebar_frame,
            text="设置",
            command=self.show_settings_view
        )
        self.settings_button.grid(row=4, column=0, padx=20, pady=10)
        
        # Theme switch
        self.theme_label = ctk.CTkLabel(self.sidebar_frame, text="主题:", anchor="w")
        self.theme_label.grid(row=11, column=0, padx=20, pady=(10, 0))
        
        self.theme_switch = ctk.CTkSwitch(
            self.sidebar_frame,
            text="深色模式",
            command=self.toggle_theme,
            onvalue="dark",
            offvalue="light"
        )
        self.theme_switch.grid(row=12, column=0, padx=20, pady=10)
        if THEME == "dark":
            self.theme_switch.select()
    
    def create_main_content(self):
        """Create main content area"""
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # Welcome screen
        self.create_welcome_screen()
    
    def create_welcome_screen(self):
        """Create welcome screen"""
        welcome_frame = ctk.CTkFrame(self.main_frame)
        welcome_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        welcome_frame.grid_columnconfigure(0, weight=1)
        welcome_frame.grid_rowconfigure(0, weight=1)
        
        welcome_label = ctk.CTkLabel(
            welcome_frame,
            text=f"欢迎使用 {APP_NAME}",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        welcome_label.grid(row=0, column=0, pady=(50, 10))
        
        subtitle_label = ctk.CTkLabel(
            welcome_frame,
            text="股票智能分析预测系统",
            font=ctk.CTkFont(size=16)
        )
        subtitle_label.grid(row=1, column=0, pady=10)
        
        version_label = ctk.CTkLabel(
            welcome_frame,
            text=f"版本: {APP_VERSION}",
            font=ctk.CTkFont(size=12)
        )
        version_label.grid(row=2, column=0, pady=10)
        
        start_button = ctk.CTkButton(
            welcome_frame,
            text="开始使用",
            command=self.show_prediction_view,
            width=200,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        start_button.grid(row=3, column=0, pady=30)
    
    def clear_main_frame(self):
        """Clear all widgets from main frame"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def show_prediction_view(self):
        """Show prediction view"""
        self.clear_main_frame()
        
        prediction_frame = ctk.CTkFrame(self.main_frame)
        prediction_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        title = ctk.CTkLabel(
            prediction_frame,
            text="股票预测",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=10)
        
        # Stock input
        input_frame = ctk.CTkFrame(prediction_frame)
        input_frame.pack(pady=20, padx=20, fill="x")
        
        stock_label = ctk.CTkLabel(input_frame, text="股票代码:")
        stock_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.stock_entry = ctk.CTkEntry(input_frame, placeholder_text="例如: 000001")
        self.stock_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        input_frame.grid_columnconfigure(1, weight=1)
        
        predict_button = ctk.CTkButton(
            input_frame,
            text="开始预测",
            command=self.run_prediction
        )
        predict_button.grid(row=0, column=2, padx=10, pady=10)
        
        # Result area
        self.result_textbox = ctk.CTkTextbox(prediction_frame, height=400)
        self.result_textbox.pack(pady=10, padx=20, fill="both", expand=True)
        self.result_textbox.insert("1.0", "请输入股票代码并点击\"开始预测\"按钮...")
        
        logger.info("Switched to prediction view")
    
    def show_watchlist_view(self):
        """Show watchlist view"""
        self.clear_main_frame()
        
        label = ctk.CTkLabel(
            self.main_frame,
            text="观测池功能开发中...",
            font=ctk.CTkFont(size=20)
        )
        label.grid(row=0, column=0, padx=20, pady=20)
        
        logger.info("Switched to watchlist view")
    
    def show_history_view(self):
        """Show history view"""
        self.clear_main_frame()
        
        label = ctk.CTkLabel(
            self.main_frame,
            text="历史记录功能开发中...",
            font=ctk.CTkFont(size=20)
        )
        label.grid(row=0, column=0, padx=20, pady=20)
        
        logger.info("Switched to history view")
    
    def show_settings_view(self):
        """Show settings view"""
        self.clear_main_frame()
        
        label = ctk.CTkLabel(
            self.main_frame,
            text="设置功能开发中...",
            font=ctk.CTkFont(size=20)
        )
        label.grid(row=0, column=0, padx=20, pady=20)
        
        logger.info("Switched to settings view")
    
    def toggle_theme(self):
        """Toggle between light and dark theme"""
        current_mode = ctk.get_appearance_mode()
        new_mode = "Light" if current_mode == "Dark" else "Dark"
        ctk.set_appearance_mode(new_mode)
        logger.info(f"Theme changed to {new_mode}")
    
    def run_prediction(self):
        """Run prediction for entered stock code"""
        stock_code = self.stock_entry.get().strip()
        
        if not stock_code:
            self.result_textbox.delete("1.0", "end")
            self.result_textbox.insert("1.0", "错误: 请输入股票代码")
            return
        
        self.result_textbox.delete("1.0", "end")
        self.result_textbox.insert("1.0", f"正在分析股票: {stock_code}...\n\n")
        self.result_textbox.insert("end", "这是一个示例输出。\n")
        self.result_textbox.insert("end", "完整的预测功能将在后续版本中实现。\n\n")
        self.result_textbox.insert("end", f"股票代码: {stock_code}\n")
        self.result_textbox.insert("end", "预测类型: 短期预测\n")
        self.result_textbox.insert("end", "预测趋势: 待开发\n")
        self.result_textbox.insert("end", "建议操作: 待开发\n")
        
        logger.info(f"Prediction requested for {stock_code}")


def run_app():
    """Run the application"""
    app = MainApplication()
    app.mainloop()


if __name__ == "__main__":
    run_app()
