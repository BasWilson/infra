import yaml
yaml.Dumper.ignore_aliases = lambda *args : True

def StoreState(state):
    # with open('state.json', 'w') as json_file:
    #     json.dump(state, json_file)
    with open('.infra/state/state.yaml', 'w') as yaml_file:
        yaml.dump(state, yaml_file, default_flow_style=False)

def GetState():
    state = None
    try:
        with open(".infra/state/state.yaml", 'r') as stream:
            state = yaml.safe_load(stream)
    except:
        state = {}
    return state