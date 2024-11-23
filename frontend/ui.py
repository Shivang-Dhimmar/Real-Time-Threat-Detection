from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox, QProgressBar, QTextEdit
from PyQt5.QtGui import QIcon, QFont, QColor
from PyQt5.QtCore import QTimer, Qt, QPropertyAnimation, QPoint, QEasingCurve
from PyQt5.QtCore import QThread, pyqtSignal
import sys
import os
from backend.scanner import ClamAVScanner

class ScanWorker(QThread):
    result_signal = pyqtSignal(str)  # Signal to send result back to main thread
    progress_signal = pyqtSignal(int)  # Signal to send progress updates

    def __init__(self, directory_path):
        super().__init__()
        self.directory_path = directory_path
        self.scanner = ClamAVScanner()  

    def run(self):
        if not self.scanner.is_clamd_daemon_running():
            self.result_signal.emit("ClamAV daemon is not running.")
            return
        
        self.result_signal.emit("Scanning started...")
        try:
            result = self.scanner.scan_directory(self.directory_path)
            formatted_result = self.scanner.format_result(result)
            self.result_signal.emit(formatted_result)
        except Exception as e:
            self.result_signal.emit(str(e))
        self.result_signal.emit("Scanning complete")

class ClamAVFrontend(QWidget):
    def __init__(self):
        super().__init__()
        # Set up the UI
        self.initUI()
        

    def initUI(self):
        self.setWindowTitle("Malware Scanner")
        self.setGeometry(100, 100, 650, 600)
        self.setStyleSheet("background-color: #2E2E2E;")  # Dark background color

        # Create main layout
        layout = QVBoxLayout()

        # Title label with modern font and bright color for visibility
        title_label = QLabel("Malware Scanner", self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 36, QFont.Bold))
        title_label.setStyleSheet("color: #FF5733;")  # Bright color for title
        layout.addWidget(title_label)

        # Status label with clean contrast color
        self.status_label = QLabel("Select an option below to start the scan.", self)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFont(QFont("Arial", 18))
        self.status_label.setStyleSheet("color: #D0D0D0;")  # Light grey color for status
        layout.addWidget(self.status_label)

        # Create a button to select a directory to scan
        self.scan_button_directory = QPushButton("Select Directory to Scan", self)
        self.scan_button_directory.setFont(QFont("Arial", 18))
        self.scan_button_directory.setStyleSheet("""
            QPushButton {
                background-color: #FF5733;
                color: white;
                padding: 25px 50px;
                border-radius: 30px;
                border: none;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FF7F50;  # Lighter orange on hover
            }
        """)
        self.scan_button_directory.setIcon(QIcon("folder_icon.png"))  # Add folder icon
        self.scan_button_directory.clicked.connect(self.select_directory)
        layout.addWidget(self.scan_button_directory)

        # Create a button to start the scan
        self.scan_button_start = QPushButton("Start Scan", self)
        self.scan_button_start.setFont(QFont("Arial", 18))
        self.scan_button_start.setStyleSheet("""
            QPushButton {
                background-color: #00BFFF;
                color: white;
                padding: 25px 60px;
                border-radius: 30px;
                border: none;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #87CEFA;  # Lighter blue on hover
            }
        """)
        self.scan_button_start.setIcon(QIcon("start_icon.png"))  # Add start icon
        self.scan_button_start.clicked.connect(self.start_scan)
        layout.addWidget(self.scan_button_start)

        # Create a button for "Full Scan"
        self.full_scan_button = QPushButton("Full Scan", self)
        self.full_scan_button.setFont(QFont("Arial", 18))
        self.full_scan_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 25px 60px;
                border-radius: 30px;
                border: none;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #66BB6A;  # Lighter green on hover
            }
        """)
        self.full_scan_button.setIcon(QIcon("full_scan_icon.png"))  # Add icon for full scan
        self.full_scan_button.clicked.connect(self.full_scan)
        layout.addWidget(self.full_scan_button)

        # Create a circular progress bar
        self.circular_progress = QProgressBar(self)
        self.circular_progress.setRange(0, 0)  # Indeterminate range
        self.circular_progress.setValue(0)
        self.circular_progress.setTextVisible(False)
        self.circular_progress.setStyleSheet("""
            QProgressBar {
                border-radius: 50%;
                background-color: #3A3A3A;
                padding: 15px;
                width: 120px;
                height: 10px;
                margin-top: 20px;
            }
            QProgressBar::chunk {
                border-radius: 50%;
                background-color: #00BFFF;
            }
        """)
        layout.addWidget(self.circular_progress)
        self.set_progress_visible(False)

        # Create a result output box (QTextEdit) to show scan results
        self.output_box = QTextEdit(self)
        self.output_box.setPlaceholderText("Scan results will appear here...")
        self.output_box.setReadOnly(True)
        self.output_box.setFont(QFont("Arial", 12))
        self.output_box.setStyleSheet("""
            background-color: #333333;
            color: #D0D0D0;
            border-radius: 10px;
            padding: 15px;
            font-size: 16px;
            margin-top: 20px;
            border: 1px solid #00BFFF;
        """)
        layout.addWidget(self.output_box)

        # Set layout for the main window
        self.setLayout(layout)

    def select_directory(self):
        # Open the file dialog to select a directory
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.directory_path = directory
            self.status_label.setText(f"Selected directory: {directory}")
            self.output_box.clear()  # Clear any previous output

    def start_scan(self):
        # Reset the progress bar to 0 before starting a new scan
        self.circular_progress.setValue(0)
        self.output_box.clear()  # Clear previous results
        self.status_label.setText("Scanning... Please wait.")

        # Check if a directory is selected
        if not hasattr(self, 'directory_path'):
            QMessageBox.warning(self, "Error", "Please select a directory first!")
            return
        if self.directory_path=="":
            QMessageBox.warning(self, "Error", "Please select a directory first!")
            return
        
        self.scan_worker=ScanWorker(self.directory_path)
        # self.result=self.scanner.run_scan(self.directory_path)
        self.scan_worker.result_signal.connect(self.handle_result)
        # self.scan_worker.progress_signal.connect(self.update_progress)
        self.scan_worker.start()
        self.set_progress_visible(True)

        

    def full_scan(self):
        self.output_box.clear()  # Clear any previous output
        self.status_label.setText("Performing Full Scan... Please wait.")
        self.directory_path=os.path.expanduser("~")
        print(self.directory_path)
        self.scan_worker=ScanWorker(self.directory_path)
        self.scan_worker.result_signal.connect(self.handle_result)
        # self.scan_worker.progress_signal.connect(self.update_progress)
        self.scan_worker.start()
        self.set_progress_visible(True)
        

    def handle_result(self,result):
        if "Scanning startes" in result:
            if self.directory_path==os.path.expanduser("~"):
                self.output_box.append("Full scan started...")
            else:
                self.output_box.append("Scanning started...")
            self.set_progress_visible(True)
            return
        
        if "Scanning complete" in result:
            if self.directory_path==os.path.expanduser("~"):
                self.output_box.append("Full scan complete!")
                self.status_label.setText("Full scan complete!")
                self.set_progress_visible(False)
                QMessageBox.information(self, "Full Scan Complete", "The full scan has completed successfully!")
            else:
                self.status_label.setText("Scan Complete!")
                self.output_box.append("Scan Complete!")
                self.set_progress_visible(False)
                QMessageBox.information(self, "Scan Complete", "The scan has completed successfully!")
            
            self.directory_path=""
            self.scan_worker.result_signal.disconnect(self.handle_result)
            return
        self.output_box.append(result)
    
    def set_progress_visible(self, visible: bool):
        """Method to control visibility of the progress bar"""
        self.circular_progress.setVisible(visible)
            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ClamAVFrontend()
    ex.show()
    sys.exit(app.exec_())