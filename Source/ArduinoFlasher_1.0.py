# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ArduinoFlasher.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!

import subprocess
import os
import sys
import glob
import serial
import os.path
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QComboBox
from PyQt5.QtGui import QIcon

#Below definitions
program_path = '/'

def get_cli_path():
    """ Get absolute path to arduino-cli, works for dev and for PyInstaller """
    
    # Determine executable name based on OS
    if sys.platform.startswith('win'):
        cli_name = 'arduino-cli.exe'
    else:
        cli_name = 'arduino-cli' # Assumes Linux/macOS executable

    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        # This is the path to the bundled executable
        base_path = sys._MEIPASS
        return os.path.join(base_path, cli_name)
    except Exception:
        # Not running in a PyInstaller bundle (e.g., running as a script)
        # Check if 'arduino-cli' is in the same folder as the script
        script_path = os.path.abspath(".")
        local_cli_path = os.path.join(script_path, cli_name)
        if os.path.isfile(local_cli_path):
            print(f"Using local CLI: {local_cli_path}")
            return local_cli_path
        
        # Fallback to assuming 'arduino-cli' is in the system's PATH for development
        print("Using system PATH for arduino-cli")
        return 'arduino-cli'

# Get the path to the arduino-cli executable
compiler = get_cli_path()

flag1_compile = 'compile'
flag2_boardname1 = '-b'
flag5_verbose = '-v'

flag1_upload = 'upload'
flag2_portname1 = '-p'
# Add new flag for hex input
flag_input_file = '--input-file'


#testComPort = 'COM6'

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
            #numberOfPortsFound = numberOfPortsFound + 1
        except (OSError, serial.SerialException):
            #print("ERRORS")
            pass
    return result

class Ui_MainWindow(QWidget):
    def setupUi(self, MainWindow):
        #begining of QT-designer generated code
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(550, 590)
        MainWindow.setMinimumSize(QtCore.QSize(550, 590))
        MainWindow.setMaximumSize(QtCore.QSize(550, 16777215))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        
        # Removed Install Tool button and spacer
        
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding) # Smaller spacer
        self.verticalLayout.addItem(spacerItem)

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.toolButton_selectFile = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_selectFile.setObjectName("toolButton_selectFile")
        self.verticalLayout.addWidget(self.toolButton_selectFile)
        self.label_fileChosen = QtWidgets.QLabel(self.centralwidget)
        self.label_fileChosen.setText("")
        self.label_fileChosen.setObjectName("label_fileChosen")
        self.verticalLayout.addWidget(self.label_fileChosen)
        spacerItem1 = QtWidgets.QSpacerItem(20, 80, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        
        # --- REMOVED TARGET ID WIDGETS ---
        
        # --- ADDED FQDN WIDGETS (COMBO BOX) ---
        self.label_FQDN = QtWidgets.QLabel(self.centralwidget)
        self.label_FQDN.setObjectName("label_FQDN")
        self.verticalLayout.addWidget(self.label_FQDN)
        
        # CHANGED: QLineEdit -> QComboBox
        self.comboBox_FQDN = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_FQDN.setObjectName("comboBox_FQDN")
        self.comboBox_FQDN.setEditable(True) # User can type their own
        
        # Add Standard Boards
        self.comboBox_FQDN.addItem("arduino:avr:uno")
        self.comboBox_FQDN.addItem("arduino:avr:nano")
        self.comboBox_FQDN.addItem("arduino:avr:mega")
        self.comboBox_FQDN.addItem("arduino:avr:leonardo")
        self.comboBox_FQDN.addItem("arduino:avr:micro")
        self.comboBox_FQDN.addItem("arduino:avr:yun")
        
        # Default to Uno
        self.comboBox_FQDN.setCurrentIndex(0) 
        
        self.verticalLayout.addWidget(self.comboBox_FQDN)
        # --- END OF ADDED WIDGETS ---
        
        spacerItem2 = QtWidgets.QSpacerItem(20, 80, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.pushButton_RefreshCOM = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_RefreshCOM.setObjectName("pushButton_RefreshCOM")
        self.verticalLayout.addWidget(self.pushButton_RefreshCOM)
        self.comboBox_COMPORTS = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_COMPORTS.setCurrentText("")
        self.comboBox_COMPORTS.setObjectName("comboBox_COMPORTS")
        self.verticalLayout.addWidget(self.comboBox_COMPORTS)
        spacerItem3 = QtWidgets.QSpacerItem(20, 80, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.pushButton_Flash = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Flash.setObjectName("pushButton_Flash")
        self.verticalLayout.addWidget(self.pushButton_Flash)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 550, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        #enf of Qt Generated layout


        #begining of my code
        self.pushButton_Flash.clicked.connect(self.FlashButtonPressed)

        self.pushButton_RefreshCOM.clicked.connect(self.refreshComPortPressed)

        self.comboBox_COMPORTS.setCurrentText("")
        self.comboBox_COMPORTS.setObjectName("comboBox_COMPORTS")

        self.refreshComPortPressed()
        
        self.toolButton_selectFile.clicked.connect(self.openFileNameDialog)

        # Removed installTool button click connect
        
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")

        # Removed spinBox_ID valueChanged connect

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 852, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # Removed installTool(self) method

    #Browse button    
    def openFileNameDialog(self):
        print("Opening Window")
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Select Firmware File', QtCore.QDir.rootPath() , 'Firmware Files (*.ino *.hex);;All Files (*)') #works
        if fileName:
            print(fileName)
            self.label_fileChosen.setText(fileName)
            global program_path
            program_path = fileName
            print("Program path: ", program_path)

    # Refresh com ports when hit refresh
    def refreshComPortPressed(self):
        listReturned = serial_ports()   

        # Clear existing items before adding new ones
        self.comboBox_COMPORTS.clear()

        if(len(listReturned) == 0):
            print("No COM port found")
            self.textEdit.setText("No COM port foud!")
        else:
            print("Found", len(listReturned), "COM ports")
            print(listReturned)
            for comPort in range(len(listReturned)):
                print(comPort+1)
                self.comboBox_COMPORTS.addItem(listReturned[comPort])
                
            # No need to remove items, we cleared it first

            
    #Start compilation and flashing process
    def FlashButtonPressed(self):
        print("FLASH button pressed")
        
        # Re-check ports, but don't clear list if user selected one
        listReturned = serial_ports()
        if(len(listReturned) == 0):
            print("No COM port found")
            self.textEdit.setText("No COM port foud!")
            self.comboBox_COMPORTS.clear() # Clear list if no ports found
            return
        
        # Refresh the list content without losing selection if possible
        current_selection = self.comboBox_COMPORTS.currentText()
        self.comboBox_COMPORTS.clear()
        self.comboBox_COMPORTS.addItems(listReturned)
        if current_selection in listReturned:
            self.comboBox_COMPORTS.setCurrentText(current_selection)
        
        if not self.comboBox_COMPORTS.currentText():
            self.textEdit.setText("Please select a COM port.")
            return


        if program_path == '/':
            print("Select .ino or .hex file to flash first")
            self.textEdit.setText("Select .ino or .hex file to flash first")
            return
            
        # --- CHANGED: Get FQDN from ComboBox instead of LineEdit ---
        board_fqdn = self.comboBox_FQDN.currentText()
        if not board_fqdn:
            self.textEdit.setText("Please select or enter a Board FQDN.")
            return
        
        # Prepare to hide console window on Windows
        startupinfo = None
        if sys.platform == 'win32':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            
        
        #compiling process
        try:
            if program_path.endswith('.ino'):
                # --- .INO FILE: Compile then Upload ---
                self.textEdit.setText("Compiling .ino file...")
                QApplication.processEvents() # Allow GUI to update

                print(f"Running command: {[compiler, flag1_compile, flag2_boardname1, board_fqdn, program_path, flag5_verbose]}")
                
                compile_result = subprocess.run([compiler, flag1_compile, flag2_boardname1, board_fqdn, program_path, flag5_verbose], 
                                                capture_output=True, text=True, encoding='utf-8', startupinfo=startupinfo)
                
                self.textEdit.append("--- Compile Output ---")
                self.textEdit.append(compile_result.stdout)
                self.textEdit.append(compile_result.stderr)
                
                if compile_result.returncode != 0:
                    self.textEdit.append("--- COMPILE FAILED! ---")
                    return

                self.textEdit.append("Compiling done. Flashing...")
                QApplication.processEvents() # Allow GUI to update

                #flashign process
                print(f"Running command: {[compiler, flag1_upload, flag2_boardname1, board_fqdn, flag2_portname1, self.comboBox_COMPORTS.currentText(), program_path, flag5_verbose]}")
                
                upload_result = subprocess.run([compiler, flag1_upload, flag2_boardname1, board_fqdn, flag2_portname1, self.comboBox_COMPORTS.currentText(), program_path, flag5_verbose],
                                               capture_output=True, text=True, encoding='utf-8', startupinfo=startupinfo)

                self.textEdit.append("--- Upload Output ---")
                self.textEdit.append(upload_result.stdout)
                self.textEdit.append(upload_result.stderr)

                if upload_result.returncode == 0:
                    self.textEdit.append("--- Flashing done! ---")
                else:
                    self.textEdit.append("--- UPLOAD FAILED! ---")

            elif program_path.endswith('.hex'):
                # --- .HEX FILE: Upload Only ---
                self.textEdit.setText("Uploading .hex file...")
                QApplication.processEvents() # Allow GUI to update

                print(f"Running command: {[compiler, flag1_upload, flag2_boardname1, board_fqdn, flag2_portname1, self.comboBox_COMPORTS.currentText(), flag_input_file, program_path, flag5_verbose]}")
                
                upload_result = subprocess.run([compiler, flag1_upload, flag2_boardname1, board_fqdn, flag2_portname1, self.comboBox_COMPORTS.currentText(), flag_input_file, program_path, flag5_verbose],
                                               capture_output=True, text=True, encoding='utf-8', startupinfo=startupinfo)

                self.textEdit.append("--- Upload Output ---")
                self.textEdit.append(upload_result.stdout)
                self.textEdit.append(upload_result.stderr)

                if upload_result.returncode == 0:
                    self.textEdit.append("--- Flashing done! ---")
                else:
                    self.textEdit.append("--- UPLOAD FAILED! ---")

        except FileNotFoundError:
            self.textEdit.setText(f"Error: '{compiler}' not found.\nMake sure 'arduino-cli.exe' is bundled correctly.")
        except Exception as e:
            self.textEdit.setText(f"An error occurred: {str(e)}")


    # PyQT5 requirement
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Arduino Flasher"))
        self.pushButton_Flash.setText(_translate("MainWindow", "FLASH!"))
        self.label.setText(_translate("MainWindow", "COM port"))
        self.toolButton_selectFile.setText(_translate("MainWindow", "..."))
        self.label_2.setText(_translate("MainWindow", "Select .ino or .hex file"))
        
        # REMOVED: label_3 setText (Target ID)

        self.label_4.setText(_translate("MainWindow", "ATMEGA328p ARDUINO COMPILER AND FLASHER"))
        self.label_5.setText(_translate("MainWindow", "Debug output:"))
        self.pushButton_RefreshCOM.setText(_translate("MainWindow", "Refresh COM ports"))
        
        # --- UPDATED: Label for FQDN ---
        self.label_FQDN.setText(_translate("MainWindow", "Board FQDN"))

    # test function
    def updateLabel(self, textToUpdate):
        self.textEdit.setText(textToUpdate)

if __name__ == "__main__":
    import sys

    #check if COM ports are connected
    listReturned = serial_ports()

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
