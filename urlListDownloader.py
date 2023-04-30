import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QProgressBar, QFileDialog

class DownloadWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.url_list = []

        self.initUI()

    def initUI(self):
        # Create GUI Stuff Here
        self.url_label = QLabel('Enter URL:')
        self.url_input = QLineEdit()
        self.add_button = QPushButton('Add URL')
        self.load_button = QPushButton('Load URLs')
        self.download_button = QPushButton('Download')
        self.progress_bar = QProgressBar()

        # Creating Layout for elements
        layout = QVBoxLayout()
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)
        layout.addWidget(self.add_button)
        layout.addWidget(self.load_button)
        layout.addWidget(self.download_button)
        layout.addWidget(self.progress_bar)

        # Connecting the buttons for clicking
        self.add_button.clicked.connect(self.add_url)
        self.load_button.clicked.connect(self.load_urls)
        self.download_button.clicked.connect(self.download_urls)

        # setting main window
        self.setLayout(layout)

    def add_url(self):
        # Adding url to list
        url = self.url_input.text()
        self.url_list.append(url)
        self.url_input.setText('')

    def load_urls(self):
        # prompting user to select file for their list
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'Text Files (*.txt)')

        # read Urls from list
        with open(file_name, 'r') as f:
            urls = f.read().splitlines()
            self.url_list.extend(urls)

    def download_urls(self):
        # disable the download button while downloading

        # loop through list and download with yt-dlp 
        num_urls = len(self.url_list)
        for i, url in enumerate(self.url_list):
            args = ['yt-dlp.exe', '--legacy-server-connect', url]         # possible issue here with --legacy-server-connect and -a parameters
            subprocess.call(args)

            # progress bar
            progress = int((i+1)/num_urls * 100)
            self.progress_bar.setValue(progress)

        # re-enabling the download button
        self.download_button.setEnabled(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DownloadWindow()
    window.show()
    sys.exit(app.exec_())
