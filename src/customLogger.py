from datetime import datetime

class LoggingObject:

    """ This is a custom logging object"""

    def log(self, fileObject ,message):
        self.now=datetime.now()
        self.date = self.now.date()
        self.current_time = self.now.strftime("%H:%M:%S")
        fileObject.write(
          f'[{self.date} {self.current_time}] :  {message}\n'
        )