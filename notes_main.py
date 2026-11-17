from PyQt5.QtWidgets import (QWidget, QPushButton, QLabel, QTextEdit, QApplication, QLineEdit
                             , QFileDialog, QShortcut)
from PyQt5.QtGui import QTextCharFormat, QFont, QTextCursor, QKeySequence, QIcon
from PyQt5.QtCore import Qt
import sys, os
from pathlib import Path

class mainNotes(QWidget):
    def __init__(self):
        super().__init__()
        self.textarea = TextEdit(parent=self)
        self.textsize = QLineEdit(self)
        self.bold = QPushButton("B", self)
        self.italic = QPushButton("I", self)
        self.underline = QPushButton("U", self)
        self.fileoptions = QPushButton("File", self)

        self.exportfile = QPushButton("Export", self)
        self.openfile = QPushButton("Open", self)
        self.save = QPushButton("Save", self)
        self.new = QPushButton("New", self)

        self.characterCount = QLabel("Character count (without spaces): 0", self)
        self.characterCountWhite = QLabel("Character count (with spaces): 0", self)
        self.wordCount = QLabel("Word count: 0", self)

        self.filenow = None

        self.ctrls = QShortcut(QKeySequence("Ctrl+S"), self)
        self.ctrlo = QShortcut(QKeySequence("Ctrl+O"), self)
        self.ctrln = QShortcut(QKeySequence("Ctrl+N"), self)

        self.fontsize = QFont("Roboto")
        self.darkmode = False
        self.darkswitch = QPushButton("Dark Mode", self)

        self.setWindowTitle("Cryston Notes")
        self.initUI()
    def initUI(self):
        windowIcon = QIcon()
        windowIcon.addFile("images/CrystonNotes2.png")
        self.setWindowIcon(windowIcon)

        self.setGeometry(0, 30, 1800, 1000)
        self.textarea.setGeometry(20, 75, 1750, 900)
        self.textsize.setGeometry(420, 20, 50, 30)
        self.textsize.setText("40")

        self.characterCount.setGeometry(1200, 20, 400, 30)
        self.characterCountWhite.setGeometry(800, 20, 400, 30)
        self.wordCount.setGeometry(1600, 20, 500, 30)

        self.ctrls.activated.connect(self.saveFile)
        self.ctrlo.activated.connect(self.chooseOpen)
        self.ctrln.activated.connect(self.newFile)

        self.fileoptions.setGeometry(20, 5, 50, 30)

        self.exportfile.setGeometry(20, 35, 100, 30)
        self.exportfile.setVisible(False)
        self.exportfile.setDisabled(True)

        self.openfile.setGeometry(20, 65, 100, 30)
        self.openfile.setVisible(False)
        self.openfile.setDisabled(True)

        self.save.setGeometry(20, 95, 100, 30)
        self.save.setVisible(False)
        self.save.setDisabled(True)

        self.new.setGeometry(20, 125, 100, 30)
        self.new.setVisible(False)
        self.new.setDisabled(True)

        self.fontsize.setPixelSize(40)

        tformat = QTextCharFormat()
        tformat.setFont(self.fontsize)
        self.textarea.mergeCurrentCharFormat(tformat)

        self.bold.setGeometry(250, 20, 40, 40)
        self.italic.setGeometry(290, 20, 40, 40)
        self.underline.setGeometry(330, 20, 40, 40)
        self.darkswitch.setGeometry(630, 20, 100, 40)
        #--------------STYLE----------------

        self.setObjectName("window")
        
        self.setStyleSheet("""
            QPushButton{
                font-size: 20px;
                border: 2px solid;
                background-color: #9a9aff;
                font-family: Roboto;
            }
            QPushButton:hover{
                font-size: 20px;
                border: 2px solid;
                background-color: #ababff;
            }
            QLabel{
                font-size: 20px;
                font-family: roboto;
            }
            QTextEdit{
                border: 2px solid #444444;
                border-radius: 5px;
                font-family: Roboto;
            }
            QLineEdit{
                font-size: 20px;
                border: 2px solid #444444;
                font-family: Roboto;
            }
        """)

        #--------------STYLE----------------

        #--------------CONNECT----------------
        self.textsize.editingFinished.connect(self.changeTextSize)
        self.bold.clicked.connect(self.setbold)
        self.italic.clicked.connect(self.setitalic)
        self.underline.clicked.connect(self.setunderline)

        self.fileoptions.clicked.connect(self.fileoptionsdrop)
        self.exportfile.clicked.connect(self.exportFile)
        self.openfile.clicked.connect(self.chooseOpen)
        self.save.clicked.connect(self.saveFile)
        self.new.clicked.connect(self.newFile)

        self.darkswitch.clicked.connect(self.switchMode)

        self.textarea.textChanged.connect(self.check)
        #--------------CONNECT----------------
    def newFile(self):
        self.filenow = None
        self.textarea.setPlainText("")
        self.textsize.setText("40")
    def saveFile(self):
        print("saved")
        if self.filenow != None:
            with open(self.filenow, "w") as file:
                file.write(self.textarea.toHtml())
        else:
            return None
    def chooseOpen(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Open Cryston File", "",
                                                  "Cryston Files (*.fr)")

        if filepath:
            with open(filepath, "r") as file:
                content = file.read()
                self.filenow = filepath

                self.textarea.setHtml(content)
                self.textsize.setText("40")
    def switchMode(self):
        self.darkmode = not self.darkmode
        self.darkswitch.setText("Light Mode" if self.darkmode else "Dark Mode")

        #toPlainText

        if self.darkmode:
            self.setStyleSheet("""
                QPushButton{
                    font-size: 20px;
                    border: 2px solid;
                    background-color: #9a9aff;
                    font-family: Roboto;
                }
                QPushButton:hover{
                    font-size: 20px;
                    border: 2px solid;
                    background-color: #ababff;
                }
                QTextEdit{
                    border: 2px solid #444444;
                    border-radius: 5px;
                    font-family: Roboto;
                    background-color: #AAAAAA;
                }
                QLabel{
                    font-size: 20px;
                    font-family: roboto;
                    background-color: #bbbbbb;
                }
                QLineEdit{
                    font-size: 20px;
                    border: 2px solid #444444;
                    font-family: Roboto;
                }
                QWidget#window{
                    background-color: #343434;
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton{
                    font-size: 20px;
                    border: 2px solid;
                    background-color: #9a9aff;
                    font-family: Roboto;
                }
                QPushButton:hover{
                    font-size: 20px;
                    border: 2px solid;
                    background-color: #ababff;
                }
                QLabel{
                    font-size: 20px;
                    font-family: roboto;
                }
                QTextEdit{
                    border: 2px solid #444444;
                    border-radius: 5px;
                    font-family: Roboto;
                    background-color: #DDDDDD;
                }
                QLineEdit{
                    font-size: 20px;
                    border: 2px solid #444444;
                    font-family: Roboto;
                }
                QWidget#window{
                    background-color: #EEEEEE;
                }
            """)
    def changeTextSize(self):
        text = self.textsize.text()
        if text.isalnum():
            self.fontsize.setPixelSize(int(text))
     
            tformat = QTextCharFormat()
            tformat.setFont(self.fontsize)
            self.textarea.mergeCurrentCharFormat(tformat)
        else:
            self.textsize.setText("40")
            return None
    def exportFile(self):
        text = self.textarea.toHtml()
        filepath, _ = QFileDialog.getSaveFileName(self, "Export Cryston File", "text.fr"
                                               , "Cryston Files (*.fr)")

        if filepath:
            with open(filepath, "w") as file:
                file.write(text)
    def fileoptionsdrop(self):
        if not self.exportfile.isVisible():
            self.exportfile.setVisible(True)
            self.exportfile.setDisabled(False)

            self.openfile.setVisible(True)
            self.openfile.setDisabled(False)

            self.save.setVisible(True)
            self.save.setDisabled(False)

            self.new.setVisible(True)
            self.new.setDisabled(False)
        else:
            self.exportfile.setVisible(False)
            self.exportfile.setDisabled(True)

            self.openfile.setVisible(False)
            self.openfile.setDisabled(True)

            self.save.setVisible(False)
            self.save.setDisabled(True)

            self.new.setVisible(False)
            self.new.setDisabled(True)
    def check(self):
        text = self.textarea.toPlainText()

        tlen = len(text)

        whitespace_removed = len("".join(text.split()))

        words = len(text.split())

        self.wordCount.setText(f"Word count: {words}")
        self.characterCountWhite.setText(f"Character count (with spaces): {tlen}")
        self.characterCount.setText(f"Character count (without spaces): {whitespace_removed}")

        if tlen == 0:
            self.resetFont()
        else:
            return None
    def resetFont(self):
        text = self.textsize.text()
        
        self.fontsize.setPixelSize(int(text))
    
        tformat = QTextCharFormat()
        tformat.setFont(self.fontsize)
        self.textarea.setCurrentCharFormat(tformat)
    def setbold(self):
        cursor = self.textarea.textCursor()

        if cursor.hasSelection():
            text = cursor.selectedText()

            start = cursor.selectionStart()
            end = cursor.selectionEnd()

            newCursor = QTextCursor(cursor)

            for letter in range(start, end):
                newCursor.setPosition(letter)
                newCursor.setPosition(letter + 1, QTextCursor.MoveMode.KeepAnchor)

                textformat = newCursor.charFormat()
                isbold = True if textformat.fontWeight() == QFont.Weight.Bold else False

                if isbold:
                    textformat.setFontWeight(QFont.Weight.Normal)
                else:
                    textformat.setFontWeight(QFont.Weight.Bold)

                newCursor.mergeCharFormat(textformat)
            cursor.setPosition(end)
            self.textarea.setTextCursor(cursor)
            tformat = QTextCharFormat()
            tformat.setFont(self.fontsize)
            
        
            self.textarea.setCurrentCharFormat(tformat)
    def setitalic(self):
        cursor = self.textarea.textCursor()

        if cursor.hasSelection():
            text = cursor.selectedText()

            start = cursor.selectionStart()
            end = cursor.selectionEnd()

            newCursor = QTextCursor(cursor)

            for letter in range(start, end):
                newCursor.setPosition(letter)
                newCursor.setPosition(letter + 1, QTextCursor.MoveMode.KeepAnchor)

                textformat = newCursor.charFormat()
                isitalic = textformat.fontItalic()

                textformat.setFontItalic(not isitalic)

                newCursor.mergeCharFormat(textformat)
            cursor.setPosition(end)
            
            self.textarea.setTextCursor(cursor)
            tformat = QTextCharFormat()
            tformat.setFont(self.fontsize)
            
            self.textarea.setCurrentCharFormat(tformat)
    def setunderline(self):
        cursor = self.textarea.textCursor()

        if cursor.hasSelection():
            text = cursor.selectedText()

            start = cursor.selectionStart()
            end = cursor.selectionEnd()

            newCursor = QTextCursor(cursor)

            for letter in range(start, end):
                newCursor.setPosition(letter)
                newCursor.setPosition(letter + 1, QTextCursor.MoveMode.KeepAnchor)

                textformat = newCursor.charFormat()
                isunderlined = textformat.fontUnderline()

                textformat.setFontUnderline(not isunderlined)

                newCursor.mergeCharFormat(textformat)
            cursor.setPosition(end)
            self.textarea.setTextCursor(cursor)
            tformat = QTextCharFormat()
            tformat.setFont(self.fontsize)
            self.textarea.setCurrentCharFormat(tformat)

class TextEdit(QTextEdit):
    def __init__(self, text="", parent = ...):
        super().__init__(text, parent)
    def keyPressEvent(self, a0):
        condition = a0.text() and a0.key() not in (Qt.Key.Key_Backspace, Qt.Key.Key_Delete)
        if condition:
            super().keyPressEvent(a0)

            cursor = self.textCursor()
            end = cursor.position()
            start = end - len(a0.text())

            if start >= 0 and end <= self.document().characterCount() - 1:
                cursor.setPosition(start)
                cursor.setPosition(end, QTextCursor.MoveMode.KeepAnchor)

                tformat = QTextCharFormat()
                tformat.setFontWeight(QFont.Weight.Normal)
                tformat.setFontItalic(False)
                tformat.setFontUnderline(False)

                cursor.mergeCharFormat(tformat)
                cursor.setPosition(end)
                self.setTextCursor(cursor)
        if not condition:
            return super().keyPressEvent(a0)
        else:
            return
        

def main():
    app = QApplication(sys.argv)
    notes = mainNotes()
    notes.show()
    sys.exit(app.exec_())

if __name__ ==  "__main__":
    main()