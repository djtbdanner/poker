'''
This beautiful code found here
https://medium.com/python-pandemonium/json-the-python-way-91aac95d4041
'''

def convert_to_dict(obj):
    """
    A function takes in a custom object and returns a dictionary representation of the object.
    This dict representation includes meta data such as the object's module and class names.
    """
#     print("Object Class: " + str(obj.__class__))
#     print("Object Dictionary : " + str(obj.__dict__))
#     print("Object Module: " + str(obj.__module__))
    obj_dict = {
        "__class__": obj.__class__.__name__,
        "__module__": obj.__module__
        }
    obj_dict.update(obj.__dict__)
    return obj_dict

def dict_to_obj(our_dict):
#     print("our dictionary: " + str(our_dict))
    """
    Function that takes in a dict and returns a custom object associated with the dict.
    This function makes use of the "__module__" and "__class__" metadata in the dictionary
    to know which object type to create.
    """
    if "__class__" in our_dict:
        class_name = our_dict.pop("__class__")
        module_name = our_dict.pop("__module__")
        module = __import__(module_name)
        class_ = getattr(module,class_name)
        obj = class_(**our_dict)
        
    else:
        obj = our_dict
    return obj
