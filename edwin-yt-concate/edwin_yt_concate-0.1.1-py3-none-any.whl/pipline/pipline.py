from .steps.step import StepException


class Pipline:
    def __init__(self,steps):
        self.steps = steps

    def run(self,inputs,utils):
        data = None

        for step in self.steps:
            try:
                data = step.process(data,inputs,utils) #將每次執行完的data回傳出去
            except StepException as e:
                print('Exception happened: ',e)
                break
