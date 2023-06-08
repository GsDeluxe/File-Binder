import sys
from pathlib import Path
from PyQt5 import QtWidgets, QtCore, QtGui
from tkinter import filedialog as fd
import os
import base64
import random
import threading
from functools import partial

files = []
def bind_files(save_location, FILE_ICON):
	print("="*50, save_location, "\n", "="*50)
	files = window.files
	file_encoded = []
	for file in files:
		with open(file, "rb") as f:
		
			file_encoded.append(base64.b64encode(f.read()))
			f.close()
	if file_encoded[0] == file_encoded[1]:
				
		print("HMM")
				
	file_structure = """
import os
import base64
import win32process
import win32con
temp = os.getenv("TEMP")
os.chdir(temp)
"""

	random_file_ints = []
	file_exts = []
	for index, file in enumerate(files):
		f_split = file.split(".")[-1]
		if f_split == file:
			file_exts.append(None)
		else:
			file_exts.append(f_split)
	with open("Out.py", "w") as o:
		o.write(file_structure)
		counter = 0
		for index, file_e in enumerate(file_encoded):
			o.write(f"file{index} = {file_e}\n")
			counter += 1
		for y in range(counter):
			r = random.randint(69, 6969)
			random_file_ints.append(r)
		for x in range(counter):
			if file_exts[x] != None:
				o.write(f"""
with open('{random_file_ints[x]}.{file_exts[x]}', 'wb') as f:
	f.write(base64.b64decode(file{x}))
	f.close()
""")
			else:
				o.write(f"""
with open('{random_file_ints[x]}', 'wb') as f:
		f.write(base64.b64decode(file{x}))
		f.close()
""")


		for z in range(counter):
			if file_exts[z] == None:
				o.write(f'os.startfile(' + "f'" +  '"{temp}\\\\' + f'{random_file_ints[z]}"' + "')\n")
			else:
				o.write(f'os.startfile(' + "f'" + '"{temp}\\\\' + f'{random_file_ints[z]}.{file_exts[z]}"' + "')\n")
								
		o.close()
	file_name = save_location.split("/")[-1]
	file_path = '\\'.join(save_location.split('/')[0:-1])

	print(file_name)
	print(file_path)
	print(FILE_ICON)
	if FILE_ICON == None:
		command = f'pyinstaller --onefile --noconsole --icon=NONE --distpath "{file_path}" --name "{os.path.splitext(file_name)[0]}" Out.py && rmdir /S /Q build && del {os.path.splitext(file_name)[0]}.spec'
		print(command)
	else:
		command = f'pyinstaller --onefile --noconsole --icon="{FILE_ICON}" --distpath "{file_path}" --name "{os.path.splitext(file_name)[0]}" Out.py && rmdir /S /Q build && del {os.path.splitext(file_name)[0]}.spec'
		print(command)

	os.system(command)

	os.remove("Out.py")



class FileBinderGUI(QtWidgets.QWidget):
	def __init__(self):
		super().__init__()

		self.save_location = os.getcwd().replace("\\", "/")
		self.icon = None

		self.setWindowTitle("Simple File Binder - By GsDeluxe")
		self.setAcceptDrops(True)
		self.resize(700, 400)
		self.list_widget = QtWidgets.QListWidget()
		self.list_widget.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
		self.list_widget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

		self.bind_button = QtWidgets.QPushButton("Bind")
		self.bind_button.clicked.connect(self.bind_button_clicked)

		self.select_icon_button = QtWidgets.QPushButton("Select Icon")
		self.select_icon_button.clicked.connect(self.select_icon)

		layout = QtWidgets.QVBoxLayout()
		layout.addWidget(self.list_widget)
		layout.addWidget(self.select_icon_button)
		layout.addWidget(self.bind_button)
		self.setLayout(layout)

		# Initialize the files list
		self.files = []

		# Context menu for deleting items
		self.create_context_menu()

	def select_icon(self):
		FILE_ICON = fd.askopenfilename(filetypes=[("Icon Files", "*.ico"),("PNG Files", "*.png"),("JPEG Files", "*.jpg")])
		print(FILE_ICON)
		self.icon = FILE_ICON

	def bind_button_clicked(self):
		print(self.files)
		if not self.files:
			QtWidgets.QMessageBox.question(
				None,
				"Error",
				"No Files In Binder",
				QtWidgets.QMessageBox.Ok
			)
		elif len(self.files) == 1:
			QtWidgets.QMessageBox.question(
				None,
				"Error",
				"No Other Files To Bind",
				QtWidgets.QMessageBox.Ok
			)
		else:
			f = fd.asksaveasfilename(initialfile = 'Binded.exe', defaultextension=".exe",filetypes=[("Executable","*.exe")])
			if not f:
				print("Canceled")
				return
			else:
				self.save_location = f
				print(self.save_location)
			
			self.bind_button.setEnabled(False)
			self.show_progress_dialog()

	def show_progress_dialog(self):
		global bind_progress_dialog
		bind_progress_dialog = QtWidgets.QProgressDialog("Binding files...", None, 0, 0, self)
		bind_progress_dialog.setWindowTitle("Binding")
		bind_progress_dialog.setWindowModality(QtCore.Qt.WindowModal)
		bind_progress_dialog.show()

		bind_files_thread = threading.Thread(target=partial(self.bind_files_async, self.save_location, self.icon), daemon=True)
		bind_files_thread.start()

	def bind_files_async(self, save_location, FILE_ICON):
		bind_files(save_location=save_location, FILE_ICON=FILE_ICON)
		QtCore.QTimer.singleShot(0, self.on_binding_complete)

	def on_binding_complete(self):
		bind_progress_dialog.deleteLater()
		QtWidgets.QMessageBox.information(self, "Info", "Files binding complete.")
		self.bind_button.setEnabled(True)


	def dragEnterEvent(self, event):
		if event.mimeData().hasUrls():
			event.acceptProposedAction()

	def dragMoveEvent(self, event):
		if event.mimeData().hasUrls():
			event.acceptProposedAction()

	def dropEvent(self, event):
		if event.mimeData().hasUrls():
			urls = event.mimeData().urls()
			for url in urls:
				file_path = url.toLocalFile()
				if file_path:
					self.files.append(file_path)
					self.list_widget.addItem(Path(file_path).name)

	def create_context_menu(self):
		self.list_widget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.list_widget.customContextMenuRequested.connect(self.show_context_menu)

		self.context_menu = QtWidgets.QMenu(self)
		delete_action = self.context_menu.addAction("Delete")
		delete_action.triggered.connect(self.delete_selected_items)

	def show_context_menu(self, position):
		self.context_menu.exec_(self.list_widget.mapToGlobal(position))

	def delete_selected_items(self):
		selected_items = self.list_widget.selectedItems()
		for item in selected_items:
			index = self.list_widget.row(item)
			self.list_widget.takeItem(index)
			file_path = self.files.pop(index)
			print("Deleted file:", file_path)

	def closeEvent(self, event):
		reply = QtWidgets.QMessageBox.question(
			self,
			"Exit",
			"Are you sure you want to exit?",
			QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
		)
		if reply == QtWidgets.QMessageBox.Yes:
			event.accept()
		else:
			event.ignore()


if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = FileBinderGUI()
	window.show()
	sys.exit(app.exec_())
