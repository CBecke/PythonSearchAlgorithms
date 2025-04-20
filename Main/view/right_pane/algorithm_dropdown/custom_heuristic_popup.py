from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPlainTextEdit, QPushButton, QHBoxLayout

from Main.communication.event.impl.heuristic_update_event import HeuristicUpdateEvent
from Main.model.searcher.informed.impl.a_star import AStarSearcher


class CustomHeuristicPopup(QDialog):
    def __init__(self, publisher):
        super().__init__()
        self.publisher = publisher

        self.setWindowTitle("Custom Heuristic Creation")
        self.setModal(True) # block the main window until closed
        self.setFixedSize(750, 600)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # label
        self.label = QLabel("Please write the heuristic function to be used by the currently chosen informed search.\n")
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
        heuristic_function = self.code_edit.toPlainText()

        if self.has_correct_syntax(heuristic_function) and self.can_solve_problem(heuristic_function):
            self.status.setText("Successfully updated the heuristic")
            self.status.setStyleSheet(f"background-color: {"green"}; border: 1px solid gray; color: white;")

            environment = self.get_user_program_environment(heuristic_function)
            self.publisher.notify(HeuristicUpdateEvent(environment['h']))

        # validate that the new heuristic is able to find a solution in some test map

        # if both of the above succeed then load in the new heuristic
            # make a_star take a heuristic as input, with the default being manhattan distance

        pass

    def has_correct_syntax(self, heuristic_function_text: str):
        try:
            # to be able to use the imports in a function, we need to create an environment, since the function will
            # live in a different namespace in exec()
            environment = self.get_user_program_environment(heuristic_function_text)
            user_heuristic = environment['h']
            user_heuristic(environment['problem'], environment['current'])
            return True
        except:
            self.status.setText("Program syntax error")
            self.status.setStyleSheet(f"background-color: {"red"}; border: 1px solid gray; color: white;")
            return False

    def can_solve_problem(self, heuristic_function: str):
        assert self.has_correct_syntax(heuristic_function)

        try:
            environment = self.get_user_program_environment(heuristic_function)
            searcher = AStarSearcher(environment['h'])
            problem = environment['problem']
            search_log = searcher.logged_search(problem)
            return problem.is_goal_state(search_log.expanded.tail.value.state)
        except:
            self.status.setText("Heuristic could not solve a problem.")
            self.status.setStyleSheet(f"background-color: {"red"}; border: 1px solid gray; color: white;")
            return False


    def get_user_program_environment(self, heuristic_function: str) -> dict:
        with open("Main/model/searcher/informed/heuristic/example_context.txt", 'r') as context_file:
            context = context_file.read()

        program = heuristic_function + "\n\n" + context
        environment = dict()
        exec(program, environment, environment)
        return environment

