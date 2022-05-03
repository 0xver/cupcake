from sys import argv
from os import mkdir, system
from yaml import safe_load
from simple_term_menu import TerminalMenu
from cupcake import compiler, installer, templates, utils
import pkg_resources

init = f"""{utils.colors.success}
  /$$$$$$                                          /$$                
 /$$__  $$                                        | $$                
| $$  \__/ /$$   /$$  /$$$$$$   /$$$$$$$  /$$$$$$ | $$   /$$  /$$$$$$ 
| $$      | $$  | $$ /$$__  $$ /$$_____/ |____  $$| $$  /$$/ /$$__  $$
| $$      | $$  | $$| $$  \ $$| $$        /$$$$$$$| $$$$$$/ | $$$$$$$$
| $$    $$| $$  | $$| $$  | $$| $$       /$$__  $$| $$_  $$ | $$_____/
|  $$$$$$/|  $$$$$$/| $$$$$$$/|  $$$$$$$|  $$$$$$$| $$ \  $$|  $$$$$$$
 \______/  \______/ | $$____/  \_______/ \_______/|__/  \__/ \_______/
                    | $$                                              
                    | $$                                              
                    |__/                                              
v{pkg_resources.get_distribution("cupcakes").version}
"""

options = ["Create cupcake factory", "Create empty project", "Create script workspace", "Exit"]

menu = TerminalMenu(options, menu_cursor_style={"fg_purple"}, menu_highlight_style={"underline", "fg_purple"}, )

options_message = f"""{utils.colors.success}✨
Compile contracts from source:        cupcake bake  || cupcake compile
Test contracts from source:           cupcake frost || cupcake test
Deploy contracts from source:         cupcake serve || cupcake deploy
Run scripts from workspace source:    cupcake shop  || cupcake script
Install latest version of sol:        cupcake prep  || cupcake install
✨"""

bake_message = f"{utils.colors.success}Cupcakes have been successfully baked!"

install_message = f"{utils.colors.success}Latest version of sol installed!"

def cupcake_factory(name):
    mkdir(f"{name}")
    init = open(f"{name}/config.yaml", "w")
    init.write(templates.greeter_config)
    mkdir(f"{name}/build")
    mkdir(f"{name}/contracts")
    init = open(f"{name}/contracts/Greeter.sol", "w")
    init.write(templates.greeter_contract)
    mkdir(f"{name}/deploy")
    init = open(f"{name}/deploy/deploy.py", "w")
    init.write(templates.greeter_deploy)
    mkdir(f"{name}/tests")
    init = open(f"{name}/tests/tests.py", "w")
    init.write(templates.greeter_tests)
    init_message = f"{utils.colors.success}{name} environment has been created!\n\ncd {name}\n"
    print(init_message)

def empty_project(name):
    mkdir(f"{name}")
    init = open(f"{name}/config.yaml", "w")
    init.write(templates.empty_config)
    mkdir(f"{name}/build")
    mkdir(f"{name}/contracts")
    init = open(f"{name}/contracts/Contract.sol", "w")
    init.write(templates.empty_contract)
    mkdir(f"{name}/deploy")
    init = open(f"{name}/deploy/deploy.py", "w")
    init.write(templates.empty_deploy)
    mkdir(f"{name}/tests")
    init = open(f"{name}/tests/tests.py", "w")
    init.write(templates.empty_tests)
    init_message = f"{utils.colors.success}{name} environment has been created!\n\ncd {name}\n"
    print(init_message)

def script_workspace(name):
    mkdir(f"{name}")
    init = open(f"{name}/config.yaml", "w")
    init.write(templates.workspace_config)
    mkdir(f"{name}/abi")
    mkdir(f"{name}/scripts")
    init = open(f"{name}/scripts/scripts.py", "w")
    init.write(templates.workspace_scripts)
    init_message = f"{utils.colors.success}{name} workspace has been created!\n\ncd {name}\n"
    print(init_message)

def bake():
    compiler._compile()
    print(bake_message)

def frost():
    try:
        open("tests/tests.py")
        sourceBool = True
    except:
        sourceBool = False
    if sourceBool == True:
        exec(open("tests/tests.py").read())
    else:
        print(f"{utils.colors.fail}Failed to frost cupcakes")

def serve():
    try:
        open("deploy/deploy.py")
        sourceBool = True
    except:
        sourceBool = False
    if sourceBool == True:
        exec(open("deploy/deploy.py").read())
    else:
        print(f"{utils.colors.fail}Failed to serve cupcakes")

def script():
    try:
        init = open("config.yaml", "r")
        config_file = safe_load(init)
        source = config_file["Scripts"]["Source"]
        sourceBool = True
    except:
        sourceBool = False
        print(f"{utils.colors.fail}Failed to shop cupcakes")
    if sourceBool == True:
        exec(open(f"scripts/{source}.py").read())

def install():
    try:
        installer._install()
        print(install_message)
    except:
        print(f"{utils.colors.fail}Failed to prep cupcakes")

def main():
    args = argv[1:]
    if len(args) == 0:
        if utils.config_exists() != True:
            print(init)
            index = menu.show()
            choice = options[index]
            if choice == "Create cupcake factory":
                name_input = input(f"{utils.colors.success}Project name: ")
                cupcake_factory(name_input)
            if choice == "Create empty project":
                name_input = input(f"{utils.colors.success}Project name: ")
                empty_project(name_input)
            if choice == "Create script workspace":
                name_input = input(f"{utils.colors.success}Project name: ")
                script_workspace(name_input)
            if choice == "Exit":
                system("clear")
        else:
            print(options_message)
    try:
        if len(args) == 1:
            arg2 = argv[1].lower()
            if arg2 == "bake" or arg2 == "compile":
                bake()
            elif arg2 == "frost" or arg2 == "test":
                frost()
            elif arg2 == "serve" or arg2 == "deploy":
                serve()
            elif arg2 == "prep" or arg2 == "install":
                install()
            elif arg2 == "shop" or arg2 == "script":
                script()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
