from abc import ABC


#Chain of Responsibility 
class Parser(ABC):
    
    def __init__(self,next_parser = None):
        self.next_parser = next_parser
        
    def apply(self,input_string:str):
        if self.next_parser:
            return self.next_parser.apply(input_string)
        return input_string

class ParseStartingAtCase(Parser):
    def apply(self,input_string:str):
        input_string = input_string.strip("Starting at:").strip("₹")
        return super().apply(input_string)
    
class ParsePrice(Parser):
    def apply(self,input_string:str):
        if "₹" in input_string:
            input_string = input_string.split("₹")[0]
        return super().apply(input_string)
    
class ParsePriceWithComma(Parser):
    def apply(self,input_string:str):
        input_string = input_string.replace("₹", "").replace(",", "").strip()
        return super().apply(input_string)
    

class ParserChainOfResponsibility:
    def __init__(self):
        self.parser = ParseStartingAtCase(ParsePrice(ParsePriceWithComma()))
    
    def apply(self,input_string:str):
        return self.parser.apply(input_string)

parser_chain_of_responsibility = ParserChainOfResponsibility()