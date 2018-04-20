# Environment setup
In order to run this program, you need to set up a virtual environment with
Python3 installed. The following is the step by step instruction:

1. get the path of python3<python3_path> on your local machine with
```
  which python3
```
2. install virtual environment on your machine
```
  virtualenv -p <python3_path> final_project_vir_env
```

# How to run the program
The following are the instructions to run the program

1. start the virtual environment
```
  source final_project_vir_env/bin/activate
```

2. run the program
```
  python3 main_program.py
```

# About data.py
```
  data.py is used to crawl webpages and call Twitter API to fetch data and store it
  in a cache file. Then crimes.db will be created based on the data fetched.
```

```
  Note: the test file final_project_test.py is based on the data I fetched a while ago.
        If you call data.py to generate a new cache file, the final_project_test.py might fail
        since the data on Twitter might change. So to ensure the success of unit tests, please
        use the cache.json currently have on this repository.
```


# Program options
Once the program starts, there are five menu options:
1. shows the total number of different types of crime since 09/20/2016.
2. shows the percentage of different types of crime since 09/20/2016.
3. shows the total number of crimes each month since 09/20/2016.
4. shows the percentage of theft each month since 09/20/2016.
5. A flask web page that shows the most recent 30 tweets of three crimes(Theft, Assault and Robbery) and any news about arrest(Arrest) in Michigan.

```
  Note: your menu inputs have to be integer 1, 2, 3, 4 or 5.
```

# Menu option 5
If you choose menu option 5, then the program will jump to the second level menu option, where you need to input one of three crimes: Theft, Assault or Robbery). A flask webpage will open up
with 30 tweets about the type of crime you pick.

```
  Note: Once you choose option 5, the program will not let you choose other menu options and you have to manually end the program with control + C.
```
