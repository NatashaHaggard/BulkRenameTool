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

            self.checkNewName.stateChanged.connect(self.disable_checkboxes_NewName)
            self.checkAddPrefix.stateChanged.connect(self.disable_checkboxes_AddPrefix)
            self.checkRemovePrefix.stateChanged.connect(self.disable_checkboxes_RemovePrefix)
            self.checkAddSuffix.stateChanged.connect(self.disable_checkboxes_AddSuffix)
            self.checkRemoveSuffix.stateChanged.connect(self.disable_checkboxes_RemoveSuffix)
            self.checkReplacePartOfName.stateChanged.connect(self.disable_checkboxes_Replace)
            self.checkConvertToLowercase.stateChanged.connect(self.disable_checkboxes_ConvertToLowercase)
            self.checkConvertToUppercase.stateChanged.connect(self.disable_checkboxes_ConvertToUppercase)
            self.checkCamelcaseToUnderscore.stateChanged.connect(self.disable_checkboxes_CamelcaseToUnderscore)
            self.checkUnderscoreToCamelcase.stateChanged.connect(self.disable_checkboxes_UnderscoreToCamelcase)

        def load_directory(self):
            self.directory = QFileDialog.getExistingDirectory(self, "Select a Folder")
            if self.directory:
                self.labelSelectedFolder.setText(self.directory)

                for file in os.listdir(self.directory):
                    if os.path.isfile(os.path.join(self.directory, file)):
                        self.listModel.appendRow(QStandardItem(file))
                self.listView.setModel(self.listModel)

        def rename_files(self):
            if self.checkNewName.isChecked():
                self.new_name()

            elif self.checkReplacePartOfName.isChecked():
                self.replace_part_of_name()

            elif self.checkAddPrefix.isChecked():
                self.add_prefix()

            elif self.checkRemovePrefix.isChecked():
                self.remove_prefix()

            elif self.checkAddSuffix.isChecked():
                self.add_suffix()

            elif self.checkRemoveSuffix.isChecked():
                self.remove_suffix()

            elif self.checkConvertToLowercase.isChecked():
                self.convert_to_lowercase()

            elif self.checkConvertToUppercase.isChecked():
                self.convert_to_uppercase()

            elif self.checkCamelcaseToUnderscore.isChecked():
                print("test")
                self.camelcase_to_underscore()

            elif self.checkUnderscoreToCamelcase.isChecked():
                self.underscore_to_camelcase()

            else:
                print("Select a radio button")

            self.selected = []
            self.selectModel.clear()
            self.listModel.clear()

            for file in os.listdir(self.directory):
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

        # Rename Functions

        def new_name(self):
            counter = 1
            for filename in self.selected:
                filetype = filename.split('.')[-1]
                old_path = os.path.join(self.directory, filename)
                new_path = os.path.join(self.directory, self.newNameEdit.text() + str(counter) + '.' + filetype)
                os.rename(old_path, new_path)
                print("DEBUG new_name: renaming ", old_path, " to ", new_path)
                counter += 1

        def replace_part_of_name(self):
            for filename in self.selected:
                old_substring = self.replaceOldSubstringEdit.text()
                new_substring = self.replaceNewSubstringEdit.text()
                new_filename = filename.replace(old_substring, new_substring)
                old_path = os.path.join(self.directory, filename)
                new_path = os.path.join(self.directory, new_filename)
                if old_substring in filename:
                    os.rename(old_path, new_path)
                    print("DEBUG replace_part_of_a_name: ", old_path, " to ", new_path)

        def add_prefix(self):
            for filename in self.selected:
                old_path = os.path.join(self.directory, filename)
                new_path = os.path.join(self.directory, self.addPrefixEdit.text() + filename)
                os.rename(old_path, new_path)

        def remove_prefix(self):
            for filename in self.selected:
                old_path = os.path.join(self.directory, filename)
                new_path = os.path.join(self.directory, filename[len(self.nameEdit.text()):])
                if filename.startswith(self.removePrefixEdit.text()):
                    os.rename(old_path, new_path)
                    print("DEBUG remove_prefix: renaming ", old_path, " to ", new_path)

        def add_suffix(self):
            for filename in self.selected:
                file_name_parts = filename.split('.')
                if len(file_name_parts) > 1:
                    new_filename = f"{file_name_parts[0]}_{self.addSuffixEdit.text()}.{file_name_parts[1]}"
                    old_path = os.path.join(self.directory, filename)
                    new_path = os.path.join(self.directory, new_filename)
                    os.rename(old_path, new_path)
                    print("DEBUG add_suffix: renaming ", old_path, " to ", new_path)

        def remove_suffix(self):
            for filename in self.selected:
                suffix_with_dot = f"_{self.removeSuffixEdit.text()}"
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

        def convert_to_uppercase(self):
            for filename in self.selected:
                new_filename = filename.upper()
                print("DEBUG convert_to_uppercase: new_filename ", new_filename)
                old_path = os.path.join(self.directory, filename)
                new_path = os.path.join(self.directory, new_filename)
                os.rename(old_path, new_path)
                print("DEBUG convert_to_uppercase: renaming ", old_path, " to ", new_path)

        def underscore_to_camelcase(self):
            for filename in self.selected:
                words = filename.split('_')
                # Capitalize the first letter of each word after the first one.
                capitalized_words = [words[0]] + [word.capitalize() for word in words[1:]]
                # Join the words together without underscores.
                new_filename = ''.join(capitalized_words)
                old_path = os.path.join(self.directory, filename)
                new_path = os.path.join(self.directory, new_filename)
                os.rename(old_path, new_path)
                print("DEBUG underscore_to_camelcase: renaming ", old_path, " to ", new_path)

        def camelcase_to_underscore(self):
            for filename in self.selected:
                # Add an underscore before each capital letter except the first one.
                new_filename = ''.join(
                    ['_' + char.lower() if char.isupper() and index > 0 else char for index, char in
                     enumerate(filename)])
                print("DEBUG camelcase_to_underscore: new filename ", new_filename)
                old_path = os.path.join(self.directory, filename)
                new_path = os.path.join(self.directory, new_filename)
                os.rename(old_path, new_path)
                print("DEBUG camelcase_to_underscore: renaming ", old_path, " to ", new_path)

        # Checkbox Rules

        def disable_checkboxes_NewName(self):
            if self.checkNewName.isChecked():
                self.checkReplacePartOfName.setEnabled(False)
                self.replaceOldSubstringEdit.setEnabled(False)
                self.labelWith.setEnabled(False)
                self.replaceNewSubstringEdit.setEnabled(False)

                self.checkAddPrefix.setEnabled(False)
                self.addPrefixEdit.setEnabled(False)

                self.checkRemovePrefix.setEnabled(False)
                self.removePrefixEdit.setEnabled(False)

                self.checkAddSuffix.setEnabled(False)
                self.addSuffixEdit.setEnabled(False)

                self.checkRemoveSuffix.setEnabled(False)
                self.removeSuffixEdit.setEnabled(False)

                self.checkConvertToLowercase.setEnabled(False)
                self.checkConvertToUppercase.setEnabled(False)
                self.checkUnderscoreToCamelcase.setEnabled(False)
                self.checkCamelcaseToUnderscore.setEnabled(False)
            else:
                self.checkReplacePartOfName.setEnabled(True)
                self.replaceOldSubstringEdit.setEnabled(True)
                self.labelWith.setEnabled(True)
                self.replaceNewSubstringEdit.setEnabled(True)

                self.checkAddPrefix.setEnabled(True)
                self.addPrefixEdit.setEnabled(True)

                self.checkRemovePrefix.setEnabled(True)
                self.removePrefixEdit.setEnabled(True)

                self.checkAddSuffix.setEnabled(True)
                self.addSuffixEdit.setEnabled(True)

                self.checkRemoveSuffix.setEnabled(True)
                self.removeSuffixEdit.setEnabled(True)

                self.checkConvertToLowercase.setEnabled(True)
                self.checkConvertToUppercase.setEnabled(True)
                self.checkUnderscoreToCamelcase.setEnabled(True)
                self.checkCamelcaseToUnderscore.setEnabled(True)

        def disable_checkboxes_Replace(self):
            if self.checkReplacePartOfName.isChecked():
                self.checkNewName.setEnabled(False)
                self.newNameEdit.setEnabled(False)

                self.checkAddPrefix.setEnabled(False)
                self.addPrefixEdit.setEnabled(False)

                self.checkRemovePrefix.setEnabled(False)
                self.removePrefixEdit.setEnabled(False)

                self.checkAddSuffix.setEnabled(False)
                self.addSuffixEdit.setEnabled(False)

                self.checkRemoveSuffix.setEnabled(False)
                self.removeSuffixEdit.setEnabled(False)

                self.checkConvertToLowercase.setEnabled(False)
                self.checkConvertToUppercase.setEnabled(False)
                self.checkUnderscoreToCamelcase.setEnabled(False)
                self.checkCamelcaseToUnderscore.setEnabled(False)
            else:
                self.checkNewName.setEnabled(True)
                self.newNameEdit.setEnabled(True)

                self.checkAddPrefix.setEnabled(True)
                self.addPrefixEdit.setEnabled(True)

                self.checkRemovePrefix.setEnabled(True)
                self.removePrefixEdit.setEnabled(True)

                self.checkAddSuffix.setEnabled(True)
                self.addSuffixEdit.setEnabled(True)

                self.checkRemoveSuffix.setEnabled(True)
                self.removeSuffixEdit.setEnabled(True)

                self.checkConvertToLowercase.setEnabled(True)
                self.checkConvertToUppercase.setEnabled(True)
                self.checkUnderscoreToCamelcase.setEnabled(True)
                self.checkCamelcaseToUnderscore.setEnabled(True)

        def disable_checkboxes_AddPrefix(self):
            if self.checkAddPrefix.isChecked():
                self.checkNewName.setEnabled(False)
                self.newNameEdit.setEnabled(False)

                self.checkReplacePartOfName.setEnabled(False)
                self.replaceOldSubstringEdit.setEnabled(False)
                self.labelWith.setEnabled(False)
                self.replaceNewSubstringEdit.setEnabled(False)

                self.checkRemovePrefix.setEnabled(False)
                self.removePrefixEdit.setEnabled(False)

                self.checkConvertToLowercase.setEnabled(False)
                self.checkConvertToUppercase.setEnabled(False)
                self.checkUnderscoreToCamelcase.setEnabled(False)
                self.checkCamelcaseToUnderscore.setEnabled(False)
            else:
                self.checkNewName.setEnabled(True)
                self.newNameEdit.setEnabled(True)

                self.checkReplacePartOfName.setEnabled(True)
                self.replaceOldSubstringEdit.setEnabled(True)
                self.labelWith.setEnabled(True)
                self.replaceNewSubstringEdit.setEnabled(True)

                self.checkRemovePrefix.setEnabled(True)
                self.removePrefixEdit.setEnabled(True)

                self.checkConvertToLowercase.setEnabled(True)
                self.checkConvertToUppercase.setEnabled(True)
                self.checkUnderscoreToCamelcase.setEnabled(True)
                self.checkCamelcaseToUnderscore.setEnabled(True)

        def disable_checkboxes_RemovePrefix(self):
            if self.checkRemovePrefix.isChecked():
                self.checkNewName.setEnabled(False)
                self.newNameEdit.setEnabled(False)

                self.checkReplacePartOfName.setEnabled(False)
                self.replaceOldSubstringEdit.setEnabled(False)
                self.labelWith.setEnabled(False)
                self.replaceNewSubstringEdit.setEnabled(False)

                self.checkAddPrefix.setEnabled(False)
                self.addPrefixEdit.setEnabled(False)

                self.checkConvertToLowercase.setEnabled(False)
                self.checkConvertToUppercase.setEnabled(False)
                self.checkUnderscoreToCamelcase.setEnabled(False)
                self.checkCamelcaseToUnderscore.setEnabled(False)
            else:
                self.checkNewName.setEnabled(True)
                self.newNameEdit.setEnabled(True)

                self.checkReplacePartOfName.setEnabled(True)
                self.replaceOldSubstringEdit.setEnabled(True)
                self.labelWith.setEnabled(True)
                self.replaceNewSubstringEdit.setEnabled(True)

                self.checkAddPrefix.setEnabled(True)
                self.addPrefixEdit.setEnabled(True)

                self.checkConvertToLowercase.setEnabled(True)
                self.checkConvertToUppercase.setEnabled(True)
                self.checkUnderscoreToCamelcase.setEnabled(True)
                self.checkCamelcaseToUnderscore.setEnabled(True)

        def disable_checkboxes_AddSuffix(self):
            if self.checkAddSuffix.isChecked():
                self.checkNewName.setEnabled(False)
                self.newNameEdit.setEnabled(False)

                self.checkReplacePartOfName.setEnabled(False)
                self.replaceOldSubstringEdit.setEnabled(False)
                self.labelWith.setEnabled(False)
                self.replaceNewSubstringEdit.setEnabled(False)

                self.checkRemoveSuffix.setEnabled(False)
                self.removeSuffixEdit.setEnabled(False)

                self.checkConvertToLowercase.setEnabled(False)
                self.checkConvertToUppercase.setEnabled(False)
                self.checkUnderscoreToCamelcase.setEnabled(False)
                self.checkCamelcaseToUnderscore.setEnabled(False)
            else:
                self.checkNewName.setEnabled(True)
                self.newNameEdit.setEnabled(True)

                self.checkReplacePartOfName.setEnabled(True)
                self.replaceOldSubstringEdit.setEnabled(True)
                self.labelWith.setEnabled(True)
                self.replaceNewSubstringEdit.setEnabled(True)

                self.checkRemoveSuffix.setEnabled(True)
                self.removeSuffixEdit.setEnabled(True)

                self.checkConvertToLowercase.setEnabled(True)
                self.checkConvertToUppercase.setEnabled(True)
                self.checkUnderscoreToCamelcase.setEnabled(True)
                self.checkCamelcaseToUnderscore.setEnabled(True)

        def disable_checkboxes_RemoveSuffix(self):
            if self.checkRemoveSuffix.isChecked():
                self.checkNewName.setEnabled(False)
                self.newNameEdit.setEnabled(False)

                self.checkReplacePartOfName.setEnabled(False)
                self.replaceOldSubstringEdit.setEnabled(False)
                self.labelWith.setEnabled(False)
                self.replaceNewSubstringEdit.setEnabled(False)

                self.checkAddSuffix.setEnabled(False)
                self.addSuffixEdit.setEnabled(False)

                self.checkConvertToLowercase.setEnabled(False)
                self.checkConvertToUppercase.setEnabled(False)
                self.checkUnderscoreToCamelcase.setEnabled(False)
                self.checkCamelcaseToUnderscore.setEnabled(False)
            else:
                self.checkNewName.setEnabled(True)
                self.newNameEdit.setEnabled(True)

                self.checkReplacePartOfName.setEnabled(True)
                self.replaceOldSubstringEdit.setEnabled(True)
                self.labelWith.setEnabled(True)
                self.replaceNewSubstringEdit.setEnabled(True)

                self.checkAddSuffix.setEnabled(True)
                self.addSuffixEdit.setEnabled(True)

                self.checkConvertToLowercase.setEnabled(True)
                self.checkConvertToUppercase.setEnabled(True)
                self.checkUnderscoreToCamelcase.setEnabled(True)
                self.checkCamelcaseToUnderscore.setEnabled(True)

        def disable_checkboxes_ConvertToLowercase(self):
            if self.checkConvertToLowercase.isChecked():
                self.checkNewName.setEnabled(False)
                self.newNameEdit.setEnabled(False)

                self.checkReplacePartOfName.setEnabled(False)
                self.replaceOldSubstringEdit.setEnabled(False)
                self.labelWith.setEnabled(False)
                self.replaceNewSubstringEdit.setEnabled(False)

                self.checkAddPrefix.setEnabled(False)
                self.addPrefixEdit.setEnabled(False)

                self.checkRemovePrefix.setEnabled(False)
                self.removePrefixEdit.setEnabled(False)

                self.checkAddSuffix.setEnabled(False)
                self.addSuffixEdit.setEnabled(False)

                self.checkRemoveSuffix.setEnabled(False)
                self.removeSuffixEdit.setEnabled(False)

                self.checkConvertToUppercase.setEnabled(False)
                self.checkUnderscoreToCamelcase.setEnabled(False)
                self.checkCamelcaseToUnderscore.setEnabled(False)
            else:
                self.checkNewName.setEnabled(True)
                self.newNameEdit.setEnabled(True)

                self.checkReplacePartOfName.setEnabled(True)
                self.replaceOldSubstringEdit.setEnabled(True)
                self.labelWith.setEnabled(True)
                self.replaceNewSubstringEdit.setEnabled(True)

                self.checkAddPrefix.setEnabled(True)
                self.addPrefixEdit.setEnabled(True)

                self.checkRemovePrefix.setEnabled(True)
                self.removePrefixEdit.setEnabled(True)

                self.checkAddSuffix.setEnabled(True)
                self.addSuffixEdit.setEnabled(True)

                self.checkRemoveSuffix.setEnabled(True)
                self.removeSuffixEdit.setEnabled(True)

                self.checkConvertToUppercase.setEnabled(True)
                self.checkUnderscoreToCamelcase.setEnabled(True)
                self.checkCamelcaseToUnderscore.setEnabled(True)

        def disable_checkboxes_ConvertToUppercase(self):
            if self.checkConvertToUppercase.isChecked():
                self.checkNewName.setEnabled(False)
                self.newNameEdit.setEnabled(False)

                self.checkReplacePartOfName.setEnabled(False)
                self.replaceOldSubstringEdit.setEnabled(False)
                self.labelWith.setEnabled(False)
                self.replaceNewSubstringEdit.setEnabled(False)

                self.checkAddPrefix.setEnabled(False)
                self.addPrefixEdit.setEnabled(False)

                self.checkRemovePrefix.setEnabled(False)
                self.removePrefixEdit.setEnabled(False)

                self.checkAddSuffix.setEnabled(False)
                self.addSuffixEdit.setEnabled(False)

                self.checkRemoveSuffix.setEnabled(False)
                self.removeSuffixEdit.setEnabled(False)

                self.checkConvertToLowercase.setEnabled(False)
                self.checkUnderscoreToCamelcase.setEnabled(False)
                self.checkCamelcaseToUnderscore.setEnabled(False)
            else:
                self.checkNewName.setEnabled(True)
                self.newNameEdit.setEnabled(True)

                self.checkReplacePartOfName.setEnabled(True)
                self.replaceOldSubstringEdit.setEnabled(True)
                self.labelWith.setEnabled(True)
                self.replaceNewSubstringEdit.setEnabled(True)

                self.checkAddPrefix.setEnabled(True)
                self.addPrefixEdit.setEnabled(True)

                self.checkRemovePrefix.setEnabled(True)
                self.removePrefixEdit.setEnabled(True)

                self.checkAddSuffix.setEnabled(True)
                self.addSuffixEdit.setEnabled(True)

                self.checkRemoveSuffix.setEnabled(True)
                self.removeSuffixEdit.setEnabled(True)

                self.checkConvertToLowercase.setEnabled(True)
                self.checkUnderscoreToCamelcase.setEnabled(True)
                self.checkCamelcaseToUnderscore.setEnabled(True)

        def disable_checkboxes_UnderscoreToCamelcase(self):
            if self.checkUnderscoreToCamelcase.isChecked():
                self.checkNewName.setEnabled(False)
                self.newNameEdit.setEnabled(False)

                self.checkReplacePartOfName.setEnabled(False)
                self.replaceOldSubstringEdit.setEnabled(False)
                self.labelWith.setEnabled(False)

                self.replaceNewSubstringEdit.setEnabled(False)

                self.checkAddPrefix.setEnabled(False)
                self.addPrefixEdit.setEnabled(False)

                self.checkRemovePrefix.setEnabled(False)
                self.removePrefixEdit.setEnabled(False)

                self.checkAddSuffix.setEnabled(False)
                self.addSuffixEdit.setEnabled(False)

                self.checkRemoveSuffix.setEnabled(False)
                self.removeSuffixEdit.setEnabled(False)

                self.checkConvertToLowercase.setEnabled(False)
                self.checkConvertToUppercase.setEnabled(False)
                self.checkCamelcaseToUnderscore.setEnabled(False)
            else:
                self.checkNewName.setEnabled(True)
                self.newNameEdit.setEnabled(True)

                self.checkReplacePartOfName.setEnabled(True)
                self.replaceOldSubstringEdit.setEnabled(True)
                self.labelWith.setEnabled(True)
                self.replaceNewSubstringEdit.setEnabled(True)

                self.checkAddPrefix.setEnabled(True)
                self.addPrefixEdit.setEnabled(True)

                self.checkRemovePrefix.setEnabled(True)
                self.removePrefixEdit.setEnabled(True)

                self.checkAddSuffix.setEnabled(True)
                self.addSuffixEdit.setEnabled(True)

                self.checkRemoveSuffix.setEnabled(True)
                self.removeSuffixEdit.setEnabled(True)

                self.checkConvertToLowercase.setEnabled(True)
                self.checkConvertToUppercase.setEnabled(True)
                self.checkCamelcaseToUnderscore.setEnabled(True)

        def disable_checkboxes_CamelcaseToUnderscore(self):
            if self.checkCamelcaseToUnderscore.isChecked():
                self.checkNewName.setEnabled(False)
                self.newNameEdit.setEnabled(False)

                self.checkReplacePartOfName.setEnabled(False)
                self.replaceOldSubstringEdit.setEnabled(False)
                self.labelWith.setEnabled(False)
                self.replaceNewSubstringEdit.setEnabled(False)

                self.checkAddPrefix.setEnabled(False)
                self.addPrefixEdit.setEnabled(False)

                self.checkRemovePrefix.setEnabled(False)
                self.removePrefixEdit.setEnabled(False)

                self.checkAddSuffix.setEnabled(False)
                self.addSuffixEdit.setEnabled(False)

                self.checkRemoveSuffix.setEnabled(False)
                self.removeSuffixEdit.setEnabled(False)

                self.checkConvertToLowercase.setEnabled(False)
                self.checkConvertToUppercase.setEnabled(False)
                self.checkUnderscoreToCamelcase.setEnabled(False)
            else:
                self.checkNewName.setEnabled(True)
                self.newNameEdit.setEnabled(True)

                self.checkReplacePartOfName.setEnabled(True)
                self.replaceOldSubstringEdit.setEnabled(True)
                self.labelWith.setEnabled(True)
                self.replaceNewSubstringEdit.setEnabled(True)

                self.checkAddPrefix.setEnabled(True)
                self.addPrefixEdit.setEnabled(True)

                self.checkRemovePrefix.setEnabled(True)
                self.removePrefixEdit.setEnabled(True)

                self.checkAddSuffix.setEnabled(True)
                self.addSuffixEdit.setEnabled(True)

                self.checkRemoveSuffix.setEnabled(True)
                self.removeSuffixEdit.setEnabled(True)

                self.checkConvertToLowercase.setEnabled(True)
                self.checkConvertToUppercase.setEnabled(True)
                self.checkUnderscoreToCamelcase.setEnabled(True)


    except Exception as e:
        print(e)


app = QApplication([])
window = MyGUI()
app.exec_()
