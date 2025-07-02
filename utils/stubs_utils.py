import os
import pickle

def save_stub(stub_path, object): 
    if not os.path.exists(os.path.dirname(stub_path)): 
        os.makedirs(os.path.dirname(stub_path))
    
