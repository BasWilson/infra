# Infra

**Infra allows you to manage your infrastructure via code** (A very basic terraform).

I have made providers for platforms that I've used. You can make your own provider by checking out the [Create a provider section](#creating-a-provider).


## Providers supported by Infra
- [DigitalOcean](https://www.digitalocean.com/)

## Installation
```bash
pip3 install git+https://github.com/baswilson/infra.git
```

## Usage
Create an infra.yaml file. This is an example to deploy a droplet on DigitalOcean:
```yaml
resources:
  - id: droplet-by-infra
    provider: digitalocean
    type: droplet
    size: 20gb
    cpu: 1
    memory: 1gb
    count: 1
    image: ubuntu-18-04-x64
    region: ams3
```

### Variables
You can use two types of variables (**provider generated** or **environment variables**).
Order of importance when Infra selects variables: provider generated -> environment variable

Here is an example where we will use the pokemon provider to randomly generate a pokemon name and then use the provider generated variable as a tag in the next resource:
```yaml
resources:
  - id: random-pokemon-name
    provider: pokemon

  - id: droplet-by-infra
    provider: digitalocean
    ...
    tags:
      - ${random-pokemon-name.pokemonName}
      - ${ENVIRONMENT}
    user_data: |
      echo "${random-pokemon-name.pokemonName}" > /root/pokemon.txt
```

You can use variables in anywhere in the infra.yaml file as shown above.

### Deploying

Run the following command to deploy the infrastructure:
```bash
infra apply
```

## To do
- [ ] Add more providers
- [ ] Use sqlite instead of yaml for state file
- [x] Add a way to use variables in the infra.yaml file
- [x] Install providers from the backend


## Installing providers
You can install providers from the backend. To get a full list of available providers, run:
```bash
infra provider list
```

To install a provider, run:
```bash
infra provider install <provider> <wheel?>
```


## Creating a provider
For this example, we will create a basic provider for DigitalOcean. 


### Creating the provider' files
Create a folder with the name of your provider. 
```bash
mkdir -p providers/digitalocean
```

Create a file called `main.py` in the folder you just created. This file will contain the code for your provider.
```bash
touch providers/digitalocean/main.py
```

Create a file called `config.yaml` in the folder you just created. This file will contain the configuration for your provider.
```bash
touch providers/digitalocean/config.yaml
```

### config.yaml

The config.yaml file contains the configuration for your provider. This is an example of a config.yaml file for DigitalOcean:
```yaml
name: "digitalocean"
env_vars:
  - "DIGITALOCEAN_TOKEN"
```
What this means:
- `name`: The name of your provider.ß
- `env_vars`: The environment variables that are required for your provider to work.

All of these except for `env_vars` are required.

### main.py
The main.py file contains the code for your provider. This is an example of a main.py file for DigitalOcean:
```python
def Apply(resources):
    print("Applying digitalocean resources")
    return {
        "any": "data that you want, you can use this in Destroy(). This data is saved in the state file",
    }

def Destroy(resources):
    print("Destroying digitalocean resources")
    return None;
```

### Building the provider
To build the provider, run:
```bash
infra provider build
```

### Publishing the provider
First sign in with your Infra account:
```bash
infra auth login <username> <password> 
```

To publish the provider, run:
```bash
infra provider publish
```

It is currently not possible to create a provider via the backend (I have not made a way to create your user account yet). You can create a provider by creating a pull request to this repository.