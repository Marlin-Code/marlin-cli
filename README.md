# Marlin: The fastest path to modern web apps

90% of software is the exact same; the final 10% is what differentiates a product. Marlin helps developers build the first 90% fast, so they can focus on what matters.

## Installation

Marlin can be built from source with the included build.sh script. Run the script and a single file executable will be written to `./dist/marlin`. Add this to your path or envoke it directly.

## Documentation

Eventually we're going to put docs here

## Contribute

Marlin-cli uses pyenv for environment management and Poetry for dependcy management. These can be installed with the included `dev_setup.sh` script.


## VSCode

Open VSCode and run the following commands in the terminal
```
poetry shell
poetry env info --path | pbcopy
```

Open the VSCode command palette with `cmd+shift+P` and search for `Python: select interpretor`. Open it, click `Enter interpreter path...` and paste the path copied from poetry above.