##########################################################################################################
'''
I've expanded the task somewhat to try out some functionality I came across on online searches, 
and I wanted something a bit more complex to include in my portfolio.

The menus may appear a bit labyrinthine at first so I've included a basic flowchart in the dropbox folder.

During testing I found it tidier to get the program to create a new folder to save all the files to.
I don't know if this will affect your testing scripts, so feel free to change / comment out the 
_testing_confirm_dialogue() and _save_folder_location() functions if desired (lines 487 to 519)
'''

'''
REFERENCES
https://stackoverflow.com/questions/70235696/checking-folder-and-if-it-doesnt-exist-create-it
https://www.geeksforgeeks.org/python-os-path-join-method/
https://www.geeksforgeeks.org/change-current-working-directory-with-python/
https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
https://stackoverflow.com/questions/1320731/count-number-of-files-with-certain-extension-in-python
https://stackoverflow.com/questions/706721/how-do-i-pass-a-method-as-a-parameter-in-python
https://www.geeksforgeeks.org/python-generate-random-string-of-given-length/
https://stackoverflow.com/questions/32490629/getting-todays-date-in-yyyy-mm-dd-in-python
https://stackoverflow.com/questions/51885913/using-f-string-with-format-depending-on-a-condition
'''
##########################################################################################################



import os.path
import random
import string
from datetime import date

def menu_1():
    '''Displays main menu and takes user input to choose menu item'''

    print('\nSelect option:')
    print('1:   Exit')
    print('2:   Read calculations from file')
    print('3:   Perform calculation(s)\n')
    
    while True:
        menu_option = input()    
    
        if menu_option == '1':
            print('\n--- exiting program ---')
            exit()
        
        elif menu_option == '2':
            return read_file_menu()
        
        elif menu_option == '3':
            return save_menu()

        else:
            print('Invalid entry')



def read_file_menu():
    '''Displays menu and takes user input to select option for choosing file to read'''

    print('\nSelect option:')
    print('1:   Back')
    print('2:   Enter name of file')
    print('3:   List all files in save folder')
    
    # displays list of recently accessed files (if any exist) and option to choose one of them
    if len(recently_accessed_files) > 0:
        print('\nOr select from recently accessed files:')
        for num, file in enumerate(recently_accessed_files, start=4):
            print(f'{num}:   {file}')

    while True:
        menu_option = input()    

        if menu_option == '1':
            return menu_1()
        
        elif menu_option == '2':
            file_to_read = select_existing_file(read_file_menu)
            read_file(file_to_read)
            return menu_1()
        
        elif menu_option == '3':
            file_to_read = list_and_select_from_all_save_files(read_file_menu)
            read_file(file_to_read)
            return menu_1()

        elif menu_option.isdecimal():
            if int(menu_option) in range(4, len(recently_accessed_files) + 4):
                file_to_read = recently_accessed_files[int(menu_option) - 4]
                read_file(file_to_read)
                return menu_1()

        print('Invalid entry')



def select_existing_file(return_path):
    '''User inputs name of existing file.
    Returns file name if file exists or returns user to previous menu if file does not exist.'''

    # user input. checks that input is not empty
    while True:
        file_name = input('Enter name of file:  ')
        
        if file_name:
            break
        
        else:
            print('\nError. File name cannot be empty\n')

    # check if user included .txt file extension and add if necessary
    if not file_name.endswith('.txt'):
        file_name = file_name + '.txt'

    # check if file aleady exists
    path = f'./{file_name}'
    
    # returns file name if it exists or returns to previous menu if not
    if os.path.isfile(path):
        return file_name
    
    else:
        print('\nError. File not found')
        return return_path()   



def list_and_select_from_all_save_files(return_path):
    '''Displays list of all save files in save folder. User chooses a file or returns to previous menu.
    Only displays .txt files. If no files present in save folder, returns to previous menu.
    '''

    all_files_and_folders = os.listdir(os.getcwd())
    txt_files = []

    # select only .txt files from folder
    for file in all_files_and_folders:
        if file.endswith('.txt'):
            txt_files.append(file)
    
    # returns to previous menu if no .txt files in folder
    if len(txt_files) == 0:
        print('\n--- No files found ---\n')
        return return_path()
    
    # prints list of files
    print()
    for index, file in enumerate(txt_files, start=1):
        print(f'{index: <3} {file}')

    # user selects file or returns to previous menu
    while True:
        print('\nSelect file number or select "0" to go back')
        selection = input()
        
        if selection == '0':
            return return_path()
        
        elif selection.isdecimal():
            if int(selection) in range(1, len(txt_files) + 1):
                return txt_files[int(selection) - 1]

        print('Invalid entry')



def read_file(file):
    '''Prints contents of file.'''

    # double check that file exists
    if os.path.isfile(file):
        
        # prints contents of file along with decorative header and footer
        try:
            # gets max of header and footer length; for display purposes
            header_length = max(len(file), 11) + 10
            
            # header
            print('\n', f' {file} '.center(header_length, '-'), '\n', sep='')
            
            # file contents
            with open(file, 'r') as f:
                print(f.read())
            
            # footer
            print(' end of file '.center(header_length, '-'))
        
        except:
            print('\nError. Something went wrong')
    
    else:
        print('\nError. File does not exist')



def save_menu():
    '''Displays menu and takes user input to select option for choosing where to save calculation(s).'''

    print('\nSelect option:')
    print('1:   Perform calculation(s) without saving')
    print('2:   Perform calculation(s) and save to new file')
    print('3:   Perform calculation(s) and append to existing file\n')
    
    while True:
        menu_option = input()       
    
        if menu_option == '1':
            return calculator()
        
        elif menu_option == '2':
            file_name = file_name_input('new')         
            return calculator(file_name)
        
        elif menu_option == '3':
            file_name = append_menu()
            return calculator(file_name)
        
        else:
            print('Invalid entry')



def recently_accessed_files_stack(file):
    '''Adds file to stack of recently accessed files.'''

    # if file not already in stack, add to stack 
    if file not in recently_accessed_files:
        recently_accessed_files.insert(0, file)
        
        if len(recently_accessed_files) > 5:
            recently_accessed_files.pop()
    
    # if file already in stack, move to top of stack
    # (so displays as first item when list is called)
    else:
        recently_accessed_files.remove(file)
        recently_accessed_files.insert(0, file)



def append_menu():
    '''Displays menu and takes user input to select option for choosing file to append calculation(s) to.'''

    print('\nSelect option:')
    print('1:   Back to save options')
    print('2:   List all files in save folder')
    print('3:   Type file name to append to')
    
    # displays list of recently accessed files (if any exist) and option to choose one of them
    if len(recently_accessed_files) > 0:
        print('\nOr select from recently accessed files to append to:')
        for num, file in enumerate(recently_accessed_files, start=4):
            print(f'{num}:   {file}')
    
    while True:
        menu_option = input()

        if menu_option == '1':
            return save_menu()
        
        elif menu_option == '2':
            return list_and_select_from_all_save_files(append_menu)

        elif menu_option == '3':
            return file_name_input('append')

        elif menu_option.isdecimal():
            if int(menu_option) in range(4, len(recently_accessed_files) + 4):
                return recently_accessed_files[int(menu_option) - 4]

        print('Invalid entry')



def file_name_input(option):
    '''User enters file name to save calculation(s) to.
    If trying an existing file, returns file name if valid or returns user to previous menu.
    If trying a new file, returns file name if valid or sends user to list of suggested file names.'''

    while True:
        file_name = input('Enter name of file:  ')
        
        if file_name:
            break
        
        else:
            print('\nError. File name cannot be empty\n')

    # check if user included .txt file extension and add if necessary:
    if not file_name.endswith('.txt'):
        file_name = file_name + '.txt'

    # check if file aleady exists:
    path = f'./{file_name}'
    file_name_exists = os.path.isfile(path)

    # if appending to an existing file, ensure that file already exists:
    if option == 'append':
        if file_name_exists == True:
            return file_name
        
        else:
            print('\nError. File not found')
            return append_menu()

    # if creating a new file, ensure that file name not already in use:
    if option == 'new':
        if file_name_exists == False:
            return file_name
        
        else:
            print('\nError. File name already in use')
            # sends user to list of suggested file names
            return new_file_name_options(file_name)



def new_file_name_options(file_name):
    '''Creates three options for valid file names, based on the invalid file name previously entered.
    Takes user input to choose an option.'''

    suggestions = []

    # number suffix option:
    # adds a number suffix (2 - 100) to the file name 
    for i in range(1, 101):
        # take file name excluding file extension; adds suffix number; adds back file extension
        number_suffix_option = f'{file_name[:-4]}_{i}.txt'
        
        # checks to see if file does not already exist and appends to list of suggestions if it doesn't
        if os.path.isfile(f'./{number_suffix_option}') == False:
            suggestions.append(number_suffix_option)
            break
    

    # date suffix option:
    # adds today's date as a suffix to the file name
    todays_date = str(date.today())
    date_option = f'{file_name[:-4]} {todays_date}.txt'
    if os.path.isfile(f'./{date_option}') == False:
        suggestions.append(date_option)
    
    else:
        # if that file already exists, tries adding an additional number (2 - 100) in brackets 
        for i in range(2, 101):
            alt_date_suffix = f'{file_name[:-4]} {todays_date} ({i}).txt'
            if os.path.isfile(f'./{alt_date_suffix}') == False:
                suggestions.append(alt_date_suffix)
                break


    # random alpha-numeric suffix option:
    # adds three randomly-selected letters and numbers as a suffix to the file name; attempts up to 100 times
    for i in range(100):
        random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
        random_suffix_option = f'{file_name[:-4]}-{random_string}.txt'
        if os.path.isfile(f'./{random_suffix_option}') == False:
            suggestions.append(random_suffix_option)
            break


    # if all attempted file names already exist, return to previous menu
    if len(suggestions) == 0:
        return file_name_input('new')

    # else allow user to select one of the suggestions or return to previous menu
    print('\nSelect option:')
    print('1:   Enter new file name ')
    print('\nOr choose one of the following file names:')
    for index, item in enumerate(suggestions, 2):
        print(f'{index}:   {item}')

    while True:
        selection = input()

        if selection == '1':
            return file_name_input('new')

        elif selection.isdigit() and int(selection) in range(2, len(suggestions) + 2):
            return suggestions[int(selection) - 2]
        
        else:
            print('Invalid selection')



def calculator(save_file = None):
    '''User enters two numbers and an operator, and function returns the calculation as a string'''
    
    while True:
        print()
        print()
        if save_file:
            print(f'New calculation will be saved to:')
            print(f'{os.getcwd()}\\{save_file}')
            print()
        
        # user enters first nuber or 'e' to return to main menu
        while True:
            number_1 = (input('Enter first number or "e" to exit: '))
            
            if number_1 in ['e', 'E']:
                return menu_1()
            
            else:
                try:
                    number_1 = float(number_1)
                    break
                
                except:
                    print('Error. Invalid input')


        # user enters operator
        while True:
            operator = str(input('Enter operator: '))
            
            if operator in ['+', '-', '*', '**', '/', '//', '%']:
                break
            
            else:
                print('Error. Valid operator are:  +   -   *   **   /   //   %')


        # user enters second number
        # if trying to divide, checks for divide by zero error
        while True:
            try:
                number_2 = float(input('Enter second number: '))
                if operator in ['/', '//']:
                    if number_2 == 0:
                        print("Error. You can't divide by zero")
                        continue
                break
            
            except:
                print('Error. Input must be a numerical value')


        # calculates the equation
        try:
            answer = eval(f'{number_1} {operator} {number_2}')
            # formats numbers to add comma separators and remove superfluous trailing zeros for integers
            calculation = f'{number_1:{",.0f" if number_1.is_integer() else ","}} {operator} {number_2:{",.0f" if number_2.is_integer() else ","}} = {answer:{",.0f" if answer.is_integer() else ","}}'
            print()
            print(calculation)

            # saves calculation to file if required
            if save_file:
                save_calculation_to_file(save_file, calculation)
        
        # handling error for attempting to calculate an exceptionally large answer
        except OverflowError:
            print('\nSorry the answer is too large to calculate')
        
        # handling any other errors, e.g. infinities
        except:
            print('\nSomething went wrong with the calculation')



def save_calculation_to_file(file_name, calculation):
    '''Writes calculation to file. Creates new file if required or appends to existing file.'''
    try:
        with open(file_name, 'a') as f:
            f.write(calculation + '\n')
            
        # add file name to stack of recently accessed files:
        recently_accessed_files_stack(file_name)
    
    except:
        print('\nError. Something went wrong with saving calculation to file')











def _testing_confirm_dialogue(folder_name):
    '''Confirmation dialogue to notify user that a new folder will be created in the current working directory
    to save files to. For testing purposes only.'''

    text_width = max(len(os.getcwd()) + len(folder_name) + 22, 90)

    print(f'{"#"*(text_width + 4)}')
    print('#', f'{" " * text_width}', '#')
    print('#', f'For testing purposes a new folder will be created in the current working directory'.center(text_width), '#')
    print('#', f'New folder location: {os.getcwd()}\\{folder_name}'.center(text_width), '#')
    print('#', f'If desired, change "_new_save_folder_name" variable under "if __name__ == \'__main__\'":'.center(text_width), '#')
    print('#', f'{" " * text_width}', '#')
    print('#', f'Proceed?  (Y / N)'.center(text_width), '#')
    print('#', f'{" " * text_width}', '#')
    print(f'{"#"*(text_width + 4)}')

    confirm = input().upper()
    if confirm != 'Y':
        print(f' aborting '.center((text_width + 4), '-'))
        exit()



def _save_folder_location(folder_name):
    '''Creates a new folder within the current working directory to save calculations to'''

    # creates a new folder if it doesn't already exist:
    cwd = os.getcwd()
    new_path = os.path.join(cwd, folder_name)
    os.makedirs(new_path, exist_ok=True)

    # switches current working directory to new folder:
    os.chdir(new_path)



if __name__ == '__main__':
    
    # name of new folder which will be created to save calculation files to
    _new_save_folder_name = 'temp_HyperionDev_T09_calculations_files'
    
    _testing_confirm_dialogue(_new_save_folder_name)
    _save_folder_location(_new_save_folder_name)

    recently_accessed_files = []

    menu_1()
