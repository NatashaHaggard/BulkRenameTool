# Natasha's Batch Rename Program

import os

from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5 import uic


class MyGUI(QMainWindow):
    try:
        def __init__(self):
            super(MyGUI, self).__init__()
            uic.loadUi('batch_file_rename.ui', self)
            self.show()

            self.directory = "."
            self.listModel = QStandardItemModel()
            self.selectModel = QStandardItemModel()

            self.selectView.setModel(self.selectModel)
            self.selected = []

            self.buttonSelectFolder.clicked.connect(self.load_directory)
            self.buttonSelect.clicked.connect(self.choose_selection)
            self.buttonRemove.clicked.connect(self.remove_selection)
            self.buttonApply.clicked.connect(self.rename_files)

        def load_directory(self):
            self.directory = QFileDialog.getExistingDirectory(self, "Select a Folder")
            self.labelSelectedFolder.setText(self.directory)

            for file in os.listdir(self.directory):
                if os.path.isfile(os.path.join(self.directory, file)):
                    self.listModel.appendRow(QStandardItem(file))
            self.listView.setModel(self.listModel)

        def rename_files(self):
            if self.radioAddPrefix.isChecked():
                self.add_prefix()

            elif self.radioRemovePrefix.isChecked():
                self.remove_prefix()

            elif self.radioAddSuffix.isChecked():
                self.add_suffix()

            elif self.radioRemoveSuffix.isChecked():
                self.remove_suffix()

            elif self.radioNewName.isChecked():
                self.new_name()

            elif self.radioReplacePartOfName.isChecked():
                self.replace_part_of_name()

            elif self.radioConvertToLowercase.isChecked():
                self.convert_to_lowercase()

            else:
                print("Select a radio button")

            self.selected = []
            self.selectModel.clear()
            self.listModel.clear()

            for file in os.listdir(self.directory):
                print("DEBUG: file in os.listdir ", file)
                if os.path.isfile(os.path.join(self.directory, file)):
                    item = QStandardItem(file)
                    self.listModel.appendRow(item)
            self.listView.setModel(self.listModel)

        def choose_selection(self):
            if len(self.listView.selectedIndexes()) != 0:
                for index in self.listView.selectedIndexes():
                    if index.data() not in self.selected:
                        self.selected.append(index.data())
                        self.selectModel.appendRow(QStandardItem(index.data()))

        def remove_selection(self):
            if len(self.selectView.selectedIndexes()) != 0:
                for index in reversed(sorted(self.selectView.selectedIndexes())):
                    self.selected.remove(index.data())
                    self.selectModel.removeRow(index.row())

        def add_prefix(self):
            for filename in self.selected:
                old_path = os.path.join(self.directory, filename)
                new_path = os.path.join(self.directory, self.nameEdit.text() + filename)
                os.rename(old_path, new_path)

        def remove_prefix(self):
            for filename in self.selected:
                old_path = os.path.join(self.directory, filename)
                new_path = os.path.join(self.directory, filename[len(self.nameEdit.text()):])
                if filename.startswith(self.nameEdit.text()):
                    os.rename(old_path, new_path)
                    print("DEBUG remove_prefix: renaming ", old_path, " to ", new_path)

        def add_suffix(self):
            for filename in self.selected:
                file_name_parts = filename.split('.')
                if len(file_name_parts) > 1:
                    new_filename = f"{file_name_parts[0]}_{self.nameEdit.text()}.{file_name_parts[1]}"
                    old_path = os.path.join(self.directory, filename)
                    new_path = os.path.join(self.directory, new_filename)
                    os.rename(old_path, new_path)
                    print("DEBUG add_suffix: renaming ", old_path, " to ", new_path)

        def remove_suffix(self):
            for filename in self.selected:
                suffix_with_dot = f"_{self.nameEdit.text()}"
                if suffix_with_dot in filename:
                    old_path = os.path.join(self.directory, filename)
                    new_path = os.path.join(self.directory, filename.replace(suffix_with_dot, ""))
                    os.rename(old_path, new_path)
                    print("DEBUG remove_suffix: renaming ", old_path, " to ", new_path)

        def convert_to_lowercase(self):
            for filename in self.selected:
                new_filename = filename.lower()
                print("DEBUG convert_to_lowercase: new_filename ", new_filename)
                old_path = os.path.join(self.directory, filename)
                new_path = os.path.join(self.directory, new_filename)
                os.rename(old_path, new_path)
                print("DEBUG convert_to_lowercase: renaming ", old_path, " to ", new_path)

        def new_name(self):
            counter = 1
            for filename in self.selected:
                filetype = filename.split('.')[-1]
                old_path = os.path.join(self.directory, filename)
                new_path = os.path.join(self.directory, self.nameEdit.text() + str(counter) + '.' + filetype)
                os.rename(old_path, new_path)
                print("DEBUG new_name: renaming ", old_path, " to ", new_path)
                counter += 1

        def replace_part_of_name(self):
            for filename in self.selected:
                old_substring = self.partNameEdit.text()
                new_substring = self.replacePartNameEdit.text()
                new_filename = filename.replace(old_substring, new_substring)
                old_path = os.path.join(self.directory, filename)
                new_path = os.path.join(self.directory, new_filename)
                if old_substring in filename:
                    os.rename(old_path, new_path)
                    print("DEBUG replace_part_of_a_name: ", old_path, " to ", new_path)

    except Exception as e:
        print(e)


app = QApplication([])
window = MyGUI()
app.exec_()
