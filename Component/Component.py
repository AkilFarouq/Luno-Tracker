import os
import importlib.util
import json
from config.loadenv import *
from requests.auth import HTTPBasicAuth
import requests

class Component:

    def __init__(self):
        self.classname =  self.__class__.__name__
        self.os = os
        self.util = importlib.util
        self.json = json
        self.loadEnv()
        self.requests = requests
        self.HTTPBasicAuth = HTTPBasicAuth
    
    def loadEnv(self):
        self.env = {}
        for osparam in os.environ.items():
            key, value = osparam
            self.env[key] = value
    
    def getEnv(self,key):
        return self.env.get(key,"NOTENV")
    
    def listError(self):
        self.errorList = {
            "NOTENV":"Not In Environment Data"
        }
    
    def isError(self,str):
        if(str in list(self.errorList.keys())):return True
        else: return False
    
    def getComp(self):
        return self

    @staticmethod
    def loadComponent(compName, *args, **kwargs):
        # Define the file path
        file_path = f'{os.path.dirname(__file__)}/{compName}/src/{compName}.py'
        # print(f"file_path={file_path}")
        
        # Check if the file exists
        if os.path.exists(file_path):
            # Dynamically load the module
            spec = importlib.util.spec_from_file_location(compName, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Return the class object by name if it exists in the module
            if hasattr(module, compName):
                class_obj = getattr(module, compName)
            # If the class is callable (e.g., has an __init__ method), instantiate it with parameters
            if callable(class_obj):
                return class_obj(*args, **kwargs)
        
        # Return False if the file doesn't exist or class is not found
        return False
    
    def createPath(self,filepath):
        if(not self.pathExist(filepath)):
            self.os.makedirs(filepath)
    
    def getCompPath(self):
        return f"{COMP_DIR}/{self.classname}/"
    
    def getLibPath(self):
        return f"{self.getCompPath()}lib/"
    
    def getDataPath(self):
        return f"{self.getCompPath()}data/"
    
    def getSrcPath(self):
        return f"{self.getCompPath()}src/"
    
    def NewComponent(self,ComponentName):
        tempCompName = self.classname
        self.classname = ComponentName

        self.createPath(self.getCompPath())
        self.createPath(self.getLibPath())
        self.createPath(self.getDataPath())
        self.createPath(self.getSrcPath())
        filepath = f"{self.getSrcPath()}{self.classname}.py"
        
        if(not self.pathExist(filepath=filepath)):
            compbody = f"""from Component.Component import Component

class {self.classname}(Component):
    def __init__(self):
        super().__init__()
            """
            
            with open(filepath, "w") as f:
                f.write(compbody)

        self.classname = tempCompName
    
    def createJsonFile(self,filepath,filedata,overwrite='N',indent=4):
        if(overwrite == 'Y' and self.pathExist(filepath)):
            with open(filepath, "w") as f:
                    self.json.dump(filedata,f, indent=indent)
    
    def pathExist(self,filepath):
        return self.os.path.exists(filepath)