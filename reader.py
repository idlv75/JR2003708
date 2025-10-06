import yaml

def get_data_from_yaml(filepath:str)->dict:
    with open(filepath,"r") as file:
        data=yaml.safe_load(file)
    return data
