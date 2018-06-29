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

After generating the `.spec` file, make sure to remove all absolute directory references within it before adding it to
the VCS.


## Build using .spec file

```sh
cd ${PROJECT_HOME}
pipenv run pyinstaller ${SPEC_FILE}
```