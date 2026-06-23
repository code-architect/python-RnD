from pprint import pprint
from typeguard import typechecked
import inspect
from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime
from abc import ABC, abstractmethod


"""

create a calcualtor class at the beginning (ABSTRACT)   ===>    [Done]
create a helper class
create a database class
    create to insert into redis
    create to insert into mongodb
    create to insert intoi mysql
Error handling for everything
create APIs, use fast api
    



"""

class StandardCalculator(ABC):        
    
    @abstractmethod
    def calPlus(self, value1: int|float, value2: int|float) -> float:        
        pass
    
    
    @abstractmethod
    def calMinus(self, value1: int|float, value2: int|float) -> float:
        pass
            
    
    @abstractmethod
    def calMultiply(self, value1: int|float, value2: int|float) -> float:
        pass   
    
    
    @abstractmethod
    def calDivide(self, value1: int|float, value2: int|float) -> float:
        pass
    
    
    


class Helper:
        
    def storeData(self, *data):
        log = Path("app.log")
        if not log.exists():
            log.touch()  # creates empty file
            print("created new log")
        else:
            print("appending to existing log")

        with log.open("a", encoding="utf-8") as f:
            entry = " ".join(str(item) for item in data)
            f.write(entry + "\n")
    
    
    @staticmethod
    def valuFormatter(value1, value2, operation, outcome):
        now = datetime.now()
        readable_time = now.strftime("%Y-%m-%d %H:%M:%S")
        return f"{readable_time}: input was {value1} and {value2} operation: {operation} output is: {outcome}"
        
        

@dataclass
class Calculator(StandardCalculator):
    def __init__(self):
        self.helper = Helper()
    
    @typechecked
    def calPlus(self, value1: int|float, value2: int|float) -> float:        
        data = value1 + value2
        formatted_data = self.helper.valuFormatter(value1, value2, "addition", data)
        self.helper.storeData(formatted_data)
        return data
    
    
    @typechecked
    def calMinus(self, value1: int|float, value2: int|float) -> float:
        data = value1 - value2
        formatted_data = self.helper.valuFormatter(value1, value2, "substraction", data)
        self.helper.storeData(formatted_data)
        return data
            
    
    @typechecked
    def calMultiply(self, value1: int|float, value2: int|float) -> float:
        data = value1 * value2
        formatted_data = self.helper.valuFormatter(value1, value2, "multiply", data)
        self.helper.storeData(formatted_data)
        return data
        
    
    
    @typechecked
    def calDivide(self, value1: int|float, value2: int|float) -> float:
        data = value1 / value2
        formatted_data = self.helper.valuFormatter(value1, value2, "divide", data)
        self.helper.storeData(formatted_data)
        return data
    
   

calac = Calculator()
pprint(calac.calPlus(2, 8))
pprint(calac.calMinus(2, 8))
pprint(calac.calMultiply(2, 8))
pprint(calac.calDivide(2, 8))
