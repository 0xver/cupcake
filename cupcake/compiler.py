from cupcake import packages, installer, utils

def _compile(source=None):
    print(utils.colors.fail, end="\r")
    init = open("config.yaml", "r")
    config_file = packages.safe_load(init)
    version = str(config_file["Solidity"]["Version"])
    installer._install(version)
    packages.set_solc_version(version)
    compiler_standard = {
        "language": "Solidity",
        "sources": {},
        "settings": {
            "optimizer": {
            "enabled": True
            },
            "outputSelection": {
                "*": {
                    "*": [
                        "metadata", "evm.bytecode", "abi"
                    ]
                }
            }
        }
    }
    try:
        dir_object = packages.glob("contracts/**/**/*.sol")
        for file in dir_object:
            source_file = packages.os.path.basename(file)
            source_path = {f"{file[10:]}": {"urls": [f"{file}"]}}
            compiler_standard["sources"].update(source_path)
    except:
        pass
    try:
        dir_object = packages.glob("contracts/**/*.sol")
        for file in dir_object:
            source_file = packages.os.path.basename(file)
            source_path = {f"{file[10:]}": {"urls": [f"{file}"]}}
            compiler_standard["sources"].update(source_path)
    except:
        pass
    dir_object = packages.glob("contracts/*.sol")
    for file in dir_object:
        if ".sol" in file:
            source_file = packages.os.path.basename(file)
            source_path = {f"{source_file}": {"urls": [f"{file}"]}}
            compiler_standard["sources"].update(source_path)
    convert_to_json = packages.dumps(compiler_standard, indent = 4)
    try:
        init = open("build/compiler/interface.json", "w")
    except:
        packages.os.mkdir("build/compiler")
        init = open("build/compiler/interface.json", "w")
    init.write(convert_to_json)
    init.close()
    f = open("build/compiler/interface.json", "r")
    json_standard = packages.load(f)
    packages.os.remove("build/compiler/interface.json")
    packages.os.rmdir("build/compiler")
    compiled = packages.compile_standard(json_standard, solc_version=version, allow_paths=".")
    for name in json_standard["sources"]:
        abi = compiled["contracts"][name][packages.os.path.basename(name)[:-4]]["abi"]
        with open(f"build/{packages.os.path.basename(name)[:-4]}.json", "w") as f:
            packages.dump(abi, f)
            f.close()
    if source != None:
        abi = compiled["contracts"][f"{source}.sol"][source]["abi"]
        bytecode = compiled["contracts"][f"{source}.sol"][source]["evm"]["bytecode"]["object"]
        return bytecode, abi
