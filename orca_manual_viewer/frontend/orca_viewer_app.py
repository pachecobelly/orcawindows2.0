# -*- coding: utf-8 -*-
"""
Created on Mon May 26 17:21:47 2025

@author: Isabelly
"""

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QHBoxLayout, QStackedWidget, QGridLayout, QTextEdit, QHeaderView,
    QTableWidget, QTableWidgetItem, QDialog, QLineEdit, QScrollArea
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import sys
import os

# --- INÍCIO DA CORREÇÃO ROBusta DO CAMINHO ---
# Este bloco GARANTE que o diretório raiz do seu projeto esteja no sys.path
# 'os.path.dirname(__file__)' obtém o diretório do script atual (frontend/)
# 'os.path.join(..., '..')' sobe um nível (para orca_manual_viewer/)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root) # Adiciona no início da lista para ter prioridade
# --- FIM DA CORREÇÃO ROBusta DO CAMINHO ---


# Import backend managers
# AGORA, estas importações devem funcionar, porque 'orca_manual_viewer' (que contém 'backend')
# está no sys.path, e 'backend' é reconhecido como um pacote por causa do __init__.py
from backend.data_manager import DataManager
from backend.keyword_manager import KeywordManager
from backend.basis_set_manager import BasisSetManager
from backend.dft_manager import DFTManager

class KeywordExplanationDialog(QDialog):
    def __init__(self, title_text, data, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"- {title_text}")
        self.setMinimumWidth(500)

        layout = QVBoxLayout()

        explanation = ""
        # Handle different data structures from search results
        if isinstance(data, list) and all(isinstance(item, dict) and "Keyword" in item for item in data): # Keywords
            for item in data:
                explanation += f"<b>Keyword:</b> {item.get('Keyword', 'N/A')}<br>"
                explanation += f"<b>Input Block:</b> {item.get('Input Block', 'N/A')}<br>"
                explanation += f"<b>Variable:</b> {item.get('Variable', 'N/A')}<br>"
                comment = item.get('Comment', 'N/A')
                explanation += f"<b>Comment:</b><br>{comment.replace(chr(10), '<br>')}<br><hr>"
        elif isinstance(data, list) and all(isinstance(item, str) for item in data): # Basis Sets
            for item_text in data:
                explanation += f"{item_text}<br><hr>"
        elif isinstance(data, list) and all(isinstance(item, dict) and "Keyword" in item and "Comment" in item for item in data): # DFT Methods
            for item in data:
                explanation += f"<b>Keyword:</b> {item.get('Keyword', 'N/A')}<br>"
                comment = item.get('Comment', 'N/A')
                explanation += f"<b>Comment:</b><br>{comment.replace(chr(10), '<br>')}<br><hr>"
        else:
            explanation = "No detailed information available."


        label = QLabel(explanation)
        label.setWordWrap(True)
        label.setTextFormat(Qt.RichText)
        layout.addWidget(label)

        close_button = QPushButton("CLOSE")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button, alignment=Qt.AlignRight)

        self.setLayout(layout)

class OrcaViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ORCA Manual Viewer")
        self.setGeometry(300, 150, 850, 600)

        self.data_manager = DataManager()
        self.keyword_manager = KeywordManager()
        self.basis_set_manager = BasisSetManager()
        self.dft_manager = DFTManager()

        self.stacked_widget = QStackedWidget()
        self.start_page = self.create_scrollable_page()
        self.keyword_page = self.create_scrollable_page()
        self.basis_page = self.create_scrollable_page()
        self.density_page = self.create_scrollable_page()

        self.stacked_widget.addWidget(self.start_page)
        self.stacked_widget.addWidget(self.keyword_page)
        self.stacked_widget.addWidget(self.basis_page)
        self.stacked_widget.addWidget(self.density_page)
        self.setCentralWidget(self.stacked_widget)

        self.init_start_page()
        self.init_keyword_page()
        self.init_basis_page()
        self.init_density_page()
        self.stacked_widget.setCurrentWidget(self.start_page)

        self.setStyleSheet("""
            QMainWindow { background-color: #ffe6f0; }
            QWidget { background-color: #ffe6f0; font-family: Arial; font-size: 12pt; }
            QPushButton { background-color: #f8bbd0; border: 1px solid #ad1457; padding: 5px; border-radius: 10px; }
            QPushButton:hover { background-color: #f48fb1; }
            QLineEdit { background-color: #ffffff; border: 1px solid #ad1457; padding: 4px; border-radius: 8px; }
            QLabel { color: #880e4f; }
            QTableWidget { background-color: #ffffff; border: 1px solid #ad1457; }
            QHeaderView::section { background-color: #f8bbd0; color: #880e4f; }
        """)

    def create_scrollable_page(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        scroll.setWidget(container)
        return scroll

    def init_start_page(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        title = QLabel("<h2>ORCA Manual Viewer</h2>")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search")
        self.search_input.textChanged.connect(self.search_all)
        layout.addWidget(self.search_input)

        self.search_results_area = QScrollArea()
        self.search_results_area.setWidgetResizable(True)
        self.search_results_container = QWidget()
        self.search_results_layout = QVBoxLayout()
        self.search_results_container.setLayout(self.search_results_layout)
        self.search_results_area.setWidget(self.search_results_container)
        layout.addWidget(self.search_results_area)

        button_layout = QHBoxLayout()
        keyword_button = QPushButton("Keywords")
        keyword_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.keyword_page))
        basis_button = QPushButton("Basis Sets")
        basis_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.basis_page))
        density_button = QPushButton("Density Functional Methods")
        density_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.density_page))

        button_layout.addWidget(keyword_button)
        button_layout.addWidget(basis_button)
        button_layout.addWidget(density_button)

        layout.addLayout(button_layout)
        self.start_page.widget().setLayout(layout)

    def search_all(self, text):
        # Clear previous search results
        for i in reversed(range(self.search_results_layout.count())):
            widget = self.search_results_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        if not text.strip():
            return

        results = self.data_manager.search_all_data(text)
        found = False

        # Display Keyword results
        for keyword_data in results["keywords"]:
            btn = QPushButton(f"[Keyword] {keyword_data['Keyword']}")
            btn.clicked.connect(lambda _, k=keyword_data['Keyword']: self.show_keyword_dialog_from_search(k))
            self.search_results_layout.addWidget(btn)
            found = True

        # Display Basis Set results
        for basis_set_group in results["basis_sets"]:
            btn = QPushButton(f"[Basis Set] {basis_set_group['group']}")
            btn.clicked.connect(lambda _, g=basis_set_group['group']: self.show_basis_dialog_from_search(g))
            self.search_results_layout.addWidget(btn)
            found = True

        # Display DFT Method results
        for dft_method_group in results["dft_methods"]:
            group_name = dft_method_group['group']
            # Find specific keywords within the group that match for more precise display
            matching_keywords = []
            for item in dft_method_group['entries']:
                if text.lower() in item.get("Keyword", "").lower() or text.lower() in item.get("Comment", "").lower():
                    matching_keywords.append(item["Keyword"])

            if matching_keywords:
                display_text = f"[DFT] {', '.join(matching_keywords)} ({group_name})"
            else:
                display_text = f"[DFT] {group_name}"

            btn = QPushButton(display_text)
            btn.clicked.connect(lambda _, g=group_name: self.show_dft_dialog_from_search(g))
            self.search_results_layout.addWidget(btn)
            found = True

        if not found:
            label = QLabel("Not found")
            self.search_results_layout.addWidget(label)

        clear_btn = QPushButton("Clear Search")
        clear_btn.clicked.connect(lambda: self.search_input.setText(""))
        self.search_results_layout.addWidget(clear_btn, alignment=Qt.AlignRight)

    def show_keyword_dialog_from_search(self, keyword_name):
        data = self.keyword_manager.get_keyword_details(keyword_name)
        dialog = KeywordExplanationDialog(keyword_name, data, self)
        dialog.exec_()

    def show_basis_dialog_from_search(self, group_name):
        data = self.basis_set_manager.get_basis_set_details(group_name)
        dialog = KeywordExplanationDialog(group_name, data, self)
        dialog.exec_()

    def show_dft_dialog_from_search(self, group_name):
        data = self.dft_manager.get_dft_method_details(group_name)
        dialog = KeywordExplanationDialog(group_name, data, self)
        dialog.exec_()


    def init_keyword_page(self):
        layout = QVBoxLayout()
        title = QLabel("Keywords")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #880e4f; margin: 10px;")
        layout.addWidget(title)

        button_grid = QGridLayout()
        keyword_names = self.keyword_manager.get_all_keyword_names()
        for i, name in enumerate(keyword_names):
            btn = QPushButton(name)
            btn.clicked.connect(self.make_keyword_button_callback(name))
            button_grid.addWidget(btn, i // 2, i % 2)
        layout.addLayout(button_grid)

        back_btn = QPushButton("Back")
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.start_page))
        layout.addWidget(back_btn, alignment=Qt.AlignRight)
        self.keyword_page.widget().setLayout(layout)

    def make_keyword_button_callback(self, name):
        def callback():
            data = self.keyword_manager.get_keyword_details(name)
            dialog = KeywordExplanationDialog(name, data, self)
            dialog.exec_()
        return callback

    def init_basis_page(self):
        layout = QVBoxLayout()
        title = QLabel("Basis Sets")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #880e4f; margin: 10px;")
        layout.addWidget(title)

        button_grid = QGridLayout()
        basis_set_groups = self.basis_set_manager.get_all_basis_set_groups()
        for i, name in enumerate(basis_set_groups):
            btn = QPushButton(name)
            btn.clicked.connect(self.make_basis_callback(name))
            button_grid.addWidget(btn, i // 2, i % 2)
        layout.addLayout(button_grid)

        self.basis_table = QTableWidget()
        self.basis_table.setColumnCount(1)
        self.basis_table.setHorizontalHeaderLabels(["Description"])
        self.basis_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.basis_table.verticalHeader().setVisible(False)
        layout.addWidget(self.basis_table)

        back_btn = QPushButton("Back")
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.start_page))
        layout.addWidget(back_btn, alignment=Qt.AlignRight)
        self.basis_page.widget().setLayout(layout)

    def make_basis_callback(self, name):
        def callback():
            items = self.basis_set_manager.get_basis_set_details(name)
            self.basis_table.setRowCount(len(items))
            for row, text in enumerate(items):
                item = QTableWidgetItem(text)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                item.setFont(QFont("Consolas", 10))
                self.basis_table.setItem(row, 0, item)
        return callback

    def init_density_page(self):
        layout = QVBoxLayout()
        title = QLabel("Density Functional Methods")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #880e4f; margin: 10px;")
        layout.addWidget(title)

        button_grid = QGridLayout()
        dft_method_groups = self.dft_manager.get_all_dft_method_groups()
        for i, name in enumerate(dft_method_groups):
            btn = QPushButton(name)
            btn.clicked.connect(self.make_density_callback(name))
            button_grid.addWidget(btn, i // 2, i % 2)
        layout.addLayout(button_grid)

        self.density_table = QTableWidget()
        self.density_table.setColumnCount(2)
        self.density_table.setHorizontalHeaderLabels(["Keyword", "Comment"])
        self.density_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.density_table.verticalHeader().setVisible(False)
        layout.addWidget(self.density_table)

        back_btn = QPushButton("Back")
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.start_page))
        layout.addWidget(back_btn, alignment=Qt.AlignRight)
        self.density_page.widget().setLayout(layout)

    def make_density_callback(self, name):
        def callback():
            data = self.dft_manager.get_dft_method_details(name)
            self.density_table.setRowCount(len(data))
            for row, item in enumerate(data):
                cell_keyword = QTableWidgetItem(item.get("Keyword", "N/A"))
                cell_keyword.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                cell_keyword.setFont(QFont("Consolas", 10))
                self.density_table.setItem(row, 0, cell_keyword)

                cell_comment = QTableWidgetItem(item.get("Comment", "N/A"))
                cell_comment.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                cell_comment.setFont(QFont("Consolas", 10))
                self.density_table.setItem(row, 1, cell_comment)
        return callback

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = OrcaViewer()
    viewer.show()
    sys.exit(app.exec_())