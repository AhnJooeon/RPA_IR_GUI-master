from Model.Singleton_Instance import SingletonInstance
class ProgressPresenter(SingletonInstance):
    def __init__(self, parent=None):
        super().__init__()
        self.task_name = ""
        self.max_value = 0
        self.cur_value = 0
        self.word = ""
        self.tmp_name = ""

    def Set_Task(self, name, value):
        self.task_name = name
        self.tmp_name = name
        self.max_value = value
        self.cur_value = 0

    def Set_Progress(self, value):
        value += 1  # Zero base
        self.cur_value = value
        # print(f"{value} in Progress Presneter")

    def Set_ProgressText(self, value, word):
        value += 1  # Zero base
        self.cur_value = value
        if self.word != word:
            self.word = word
            self.task_name = f"{self.tmp_name} ({word})"

        # print(f"{value} in Progress Presneter")
