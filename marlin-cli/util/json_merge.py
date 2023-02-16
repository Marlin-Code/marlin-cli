import json

def json_merge(source, destination):
    """
    Add source json objects to destination json
    """
    with open(source, 'r') as s: 
        source_json = json.load(s)
    with open(destination, 'r') as d: 
        destination_json = json.load(d)
        
    def item_gen(source, dest):
      if isinstance(source, dict):
        for key, val in source.items():
          if key not in dest:
            dest[key] = val
          
          item_gen(val, dest[key])
      
    item_gen(source_json, destination_json)
    
    with open(destination, 'w') as d:
      json.dump(destination_json, d, indent=2)
