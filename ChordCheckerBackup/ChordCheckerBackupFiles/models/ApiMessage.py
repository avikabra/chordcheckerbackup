from enum import Enum

class MessageType(Enum): 
    ERROR = 1
    SUCCESS = 2
    INFORMATION = 3

class ApiMessage:
    def __init__(self, type, message):
        """constructor"""
        self.type = type
        self.message = message