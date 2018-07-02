# pyinstaller Cheatsheet

## Install using pipenv (recommended)

```sh
cd ${PROJECT_HOME}
pipenv install --dev pyinstaller
```

## Install globally

```sh
python3 -m pip install pyinstaller
```

## Generate .spec file

Once a `.spec` file is generated, it can be used to perform all subsequent builds.

```sh
cd ${PROJECT_HOME}
pipenv run pyinstaller --noconfirm --onefile --clean --path src src/${MAIN_FILE}

```

Notes:
*  After generating the `.spec` file, make sure to remove all absolute directory references within it before adding it
   to the VCS.

*  In order for these commands to work, the Python development package needs to be installed.
   
   *  For Python v3.5, "python3.5-dev" needs to be installed.
   *  For Python v3.6, "python3.6-dev" needs to be installed.

   After the appropriate package has been installed the Pipenv environment might need to be reinstalled:

   *  `pipenv --python 3.6 && pipenv install --dev`


## Build using .spec file

```sh
cd ${PROJECT_HOME}
pipenv run pyinstaller ${SPEC_FILE}
```