# Welcome to Project Open House

## Team
- Diane
- Owen
- Luis
- Maggie
- Maddie
- Spencer

# _Dev Setup_
## Step 1: Installing Interpreter
```angular2html
PyCharm -> Settings -> Python Interpreter -> Add New Interpreter -> Add Local Interpreter -> 
Conda Environment -> Create new environment -> Set Python Version to 3.11 -> Click OK
```
## Step 2: Confirm Python Version 3.11.0
```angular2html
Make sure Python's Version is set to 3.11.0.
If not, double click the version -> Specify Version -> 3.11 -> Wait for install -> Reset IDE
```
![img.png](readme-imgs/img.png)

## Step 3: Test Interpreter is setup

```angular2html
python ./tests/test-version.py
```

### Result should be something similar to this
```angular2html
3.11.0 (main, Mar  1 2023, 12:33:14) [Clang 14.0.6 ]
```

## Step 4: Install Requirements
### Anytime you want to add a library make sure to add it to the .txt
```angular2html
pip install -r ./requirements.txt
```

## Step 5: Download Data
### Follow this [link](https://northeastern-my.sharepoint.com/:f:/r/personal/igortn_northeastern_edu/Documents/DoCs/UTS-Projects/Rental%20prediction?csf=1&web=1&e=IPnzKu) to access data.

In a git bash terminal run this to create a folder labeled `data` in `open-house` or just create the folder.

```angular2html
mkdir data
```

Download files labeled part 1-12. Add to the data folder.
Run data-imports.py. This will create `housing_data.csv`