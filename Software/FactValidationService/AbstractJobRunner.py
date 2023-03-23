import threading
import socket
import logging
from datastructures.Assertion import Assertion
from datastructures.exceptions.FactValidationApproachTypeException import FactValidationApproachTypeException
from FactValidationService.Message import Message

class AbstractJobRunner(threading.Thread):
    """
    Abstract class that implements basic functionality.
    - Connect to a fact validation approach
    - Get the type of a fact validation approach (supervised / unsupervised)
    - Send training assertion to supervised approaches
    - Send assertions to approaches for validation
    """

    def __init__(self, approach:str, port:int):
        threading.Thread.__init__(self)
        self.approach = approach
        self.port = port
        self.server = None
        self._type = None
        
    @property
    def type(self):
        if self._type != None:
            return self._type
        self._send(Message(type="call", content="type"))
        response = Message(text=self._receive())
        
        if response.type == "type_response":
            self._type = response.content
            return response.content

        if response.type == "error":
            logging.error(response.content)
            raise FactValidationApproachTypeException(response.content)
    
    @type.setter
    def type(self, type):
        if type in ["supervised", "unsupervised"]:
            self._type = type
    
    def _validateAssertion(self, assertion:Assertion):
        """
        Validate a single assertion.
        """
            
        # Send assertion
        self._send(Message(type="test", subject=assertion.subject, predicate=assertion.predicate, object=assertion.object, score=assertion.expectedScore))
        
        # Receive score
        return Message(text=self._receive())
    
    def _trainAssertion(self, assertion:Assertion):
        """
        Send the assertion to a supervised approach as training data.
        """
        self._send(Message(
            type="train", subject=assertion.subject, predicate=assertion.predicate, object=assertion.object, score=assertion.expectedScore))
        return Message(text=self._receive())

    def _trainingStart(self):
        self._send(Message(type="call", content="training_start"))
        return Message(text=self._receive())
    
    def _trainingComplete(self):
        self._send(Message(type="call", content="training_complete"))
        return Message(text=self._receive())

    def _testingUploadComplete(self):
        self._send(Message(type="call", content="test_upload_complete"))
        return Message(text=self._receive())

    def _connect(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.connect(("127.0.0.1", self.port))
        except ConnectionRefusedError as ex:
            logging.error("Cannot connect to approach '{}'".format(self.approach))
            raise(ex)
        
    def _send(self, message:Message):
        if self.server == None:
            self._connect()
        logging.debug("Sending messege: {}".format(message.serialize()))
        self.server.send(message.serialize().encode())
        
    def _receive(self):
        tmp = self.server.recv(1024).decode()
        logging.debug("Received message: {}".format(tmp))
        return tmp
