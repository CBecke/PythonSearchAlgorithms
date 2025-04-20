from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPlainTextEdit, QPushButton, QHBoxLayout


class CustomHeuristicPopup(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Custom Heuristic Creation")
        self.setModal(True) # block the main window until closed
        self.setFixedSize(750, 600)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # label
        self.label = QLabel("Please write the heuristic function to be used by the currently chosen informed search.")
        self.layout.addWidget(self.label)

        # code window
        self.code_edit = QPlainTextEdit()
        self.code_edit.setPlainText(self.default_heuristic_text())
        self.layout.addWidget(self.code_edit)

        # button and status
        self.button_and_status_layout = QHBoxLayout()
        self.layout.addLayout(self.button_and_status_layout)
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.maybe_update_heuristic)
        self.button_and_status_layout.addWidget(self.submit_button)

        self.status = QLabel("")
        self.button_and_status_layout.addWidget(self.status)


    def default_heuristic_text(self):
        with open("Main/model/searcher/informed/heuristic/manhattan_distance.txt", 'r') as default_file:
            return default_file.read()

    def maybe_update_heuristic(self):
        # TODO: implement
        # check to see if the new heuristic compiles as a python file
        program = self.code_edit.toPlainText()
        test_code = "h(5)"
        program = program + "\n\n" + test_code

        with open("Main/model/searcher/informed/heuristic/user_heuristic.txt", 'w') as user_file:
            user_file.write(program)

        exec(program)
        try:
            exec(program)
        except:
            self.status.setText("Program Syntax Error")
            self.status.setStyleSheet(f"background-color: {"red"}; border: 1px solid gray; color: white;")



        # validate that the new heuristic is able to find a solution in some test map

        # if both of the above succeed then load in the new heuristic
            # make a_star take a heuristic as input, with the default being manhattan distance

        pass
