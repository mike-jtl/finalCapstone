# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True




while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - generate reports
ds - Display statistics
e - Exit
: ''').lower()
    

    def reg_user(menu):
        '''Add a new user to the user.txt file'''
        # - Request input of a new username
        new_username = input("New Username: ")

         # - Open file and check username until the ;
        with open('user.txt','r+') as check_user:
                for line in check_user:
                    #this ensures that only the name is selected and not the whole line, including the password
                    name_end = line.index(";")
                    line = line[:name_end]
                    while new_username in line:
                        print("User already exists \n")
                        new_username = input("New Username: ")

        # - Request input of a new password
        new_password = input("New Password: ")

        # - Request input of password confirmation.
        confirm_password = input("Confirm Password: ")

        # - Check if the new password and confirmed password are the same.
        if new_password == confirm_password:
            # - If they are the same, add them to the user.txt file,
            print("New user added")
            username_password[new_username] = new_password
            
            with open("user.txt", "w") as out_file:
                user_data = []
                for k in username_password:
                    user_data.append(f"{k};{username_password[k]}")
                out_file.write("\n".join(user_data))

        # - Otherwise you present a relevant message.
        else:
            print("Passwords do no match")

    def add_task(menu):
        
        '''Allow a user to add a new task to task.txt file
            Prompt a user for the following: 
             - A username of the person whom the task is assigned to,
             - A title of a task,
             - A description of the task and 
             - the due date of the task.'''
        task_username = input("Name of person assigned to task: ")
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
            pass
        task_title = input("Title of Task: ")
        task_description = input("Description of Task: ")
        while True:
            try:
                task_due_date = input("Due date of task (YYYY-MM-DD): ")
                due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                break

            except ValueError:
                print("Invalid datetime format. Please use the format specified")


        # Then get the current date.
        curr_date = date.today()
        ''' Add the data to the file task.txt and
            Include 'No' to indicate if the task is complete.'''
        new_task = {
            "username": task_username,
            "title": task_title,
            "description": task_description,
            "due_date": due_date_time,
            "assigned_date": curr_date,
            "completed": False
        }

        task_list.append(new_task)
        with open("tasks.txt", "w") as task_file:
            task_list_to_write = []
            for t in task_list:
                str_attrs = [
                    t['username'],
                    t['title'],
                    t['description'],
                    t['due_date'].strftime(DATETIME_STRING_FORMAT),
                    t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if t['completed'] else "No"
                ]
                task_list_to_write.append(";".join(str_attrs))
            task_file.write("\n".join(task_list_to_write))
        print("Task successfully added.")

    
    def view_all(menu):
        
        '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling) 
        '''

        for t in task_list:
            disp_str = f"Task: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            print(disp_str)


    ########################################################################
    # - VIEWING A TASK HELP - #   








    
    def view_mine(menu):
        
        '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling)
        '''
        task_number = 0                    
        # display tasks
        for t in task_list:
            if t['username'] == curr_user:
                #changing task completed True to 'Yes' or 'No'
                if t['completed'] == True or t['completed'] == 'Yes':
                    t['completed'] = 'Yes'
                else:
                    t['completed'] = 'No'

                # task counter
                task_number += 1
                # inserts a new task number key to reference
                t['Task Number'] = task_number
                disp_str = "_____________________________________________________\n\n"
                disp_str += "Task {}: \t {}\n".format(t['Task Number'],t["title"])
                disp_str += f"Assigned to: \t {t['username']}\n\n"
                disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n\n"
                disp_str += f"Task Description:\n{t['description']}\n\n"
                disp_str += f"Task Completed:\t {t['completed']}\n\n"
                disp_str += "_____________________________________________________\n\n"
                print(disp_str)


        # Making sure a user will be offered to enter a task number when incorrect
        while True:
            specific_task = input("Enter a specific task number to view or -1 to exit to main menu: ")

            if specific_task == str(-1):
                break

            while t['Task Number'] != specific_task:
                print("Please enter an existing Task")
                break


            for t in task_list:
                if t['username'] == curr_user:
                    if str(t['Task Number']) == specific_task:
                        disp_str = ''
                        disp_str += "_____________________________________________________\n\n"
                        disp_str += "Task {}: \t {}\n".format(t['Task Number'],t["title"])
                        disp_str += f"Assigned to: \t {t['username']}\n\n"
                        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n\n"
                        disp_str += f"Task Description:\n{t['description']}\n\n"
                        disp_str += f"Task Completed:\t {t['completed']}\n\n"
                        disp_str += "_____________________________________________________\n\n"
                        print(disp_str)
                        print()
                        # Input to know if user wants to mark a task as completed or edit a task
                        complete = input("Do you wish to mark the task as completed, [Yes/No] or edit the task? [edit] ").lower()
                        while complete != 'no':
                            if complete == 'yes':
                                if t['completed'] == 'No' or False:
                                    # This ensures that the user wont input to edit a task that has been completed
                                    t['completed'] = 'Yes'
                                    print("                  UPDATED TASK                ")
                                    disp_str = ''
                                    disp_str += "_____________________________________________________\n\n"
                                    disp_str += "Task {}: \t {}\n".format(t['Task Number'],t["title"])
                                    disp_str += f"Assigned to: \t {t['username']}\n\n"
                                    disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                                    disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n\n"
                                    disp_str += f"Task Description:\n{t['description']}\n\n"
                                    disp_str += f"Task Completed:\t {t['completed']}\n\n"
                                    disp_str += "_____________________________________________________\n\n"
                                    print(disp_str)
                                    


                                else:

                                    print("You cannot edit a task that has been completed")
                                    break

                            

                                
                            # task edit
                            elif complete == 'edit':
                                if t['completed'] != 'Yes' or t['completed'] != True:
                                    
                                    while True:
                                        task_change = input('\nChange who the task is assigned to or change the due date of task. [ assignment / due date ] ').lower()


                                        if task_change == 'assignment':
                                            
                                            while True:
                                                print()
                                                task_assign = input('Who would you like to allocate this task to? ').lower()
                                                print()

                                                # this creates a list with all the users to reference to, this is repeated to bypass the original restriction of only being able to view the user that is logged in
                                                all_users = []
                                                with open('user.txt','r+') as all_users_in_file:
                                                    for user_line in all_users_in_file:
                                                        #this ensures that only the name is selected and not the whole line, including the password
                                                        name_end = user_line.index(";")
                                                        task_user = user_line[:name_end]
                                                        all_users.append(task_user)

                                                print(all_users)
                                                while True:
                                                    if task_assign not in all_users:
                                                        print("User not found")
                                                        print()
                                                        task_assign = input('Who would you like to allocate this task to? ').lower()
                                                        
                                                        

                                                    else:
                                                        print()
                                                        print('The task is assigned to',task_assign)
                                                        print()
                                                        t['username'] = task_assign
                                                        print()
                                                        print("                  UPDATED TASK                ")
                                                        disp_str = ''
                                                        disp_str += "_____________________________________________________\n\n"
                                                        disp_str += "Task {}: \t {}\n".format(t['Task Number'],t["title"])
                                                        disp_str += f"Assigned to: \t {t['username']}\n\n"
                                                        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                                                        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n\n"
                                                        disp_str += f"Task Description:\n{t['description']}\n\n"
                                                        disp_str += f"Task Completed:\t {t['completed']}\n\n"
                                                        disp_str += "_____________________________________________________\n\n"
                                                        print(disp_str)
                                                        break
                                                    break
                                                break
                                            
                                            break
                                    
                                            
                                        elif task_change == 'due date':
                                            while True:
                                                task_due = input("Date of task due: [YYYY-MM-DD]")

                                                from datetime import datetime

                                                def valDate(task_due):

                                                    try:
                                                        dateObject = datetime.strptime(task_due, '%Y-%m-%d')
                                                        return True
                                                    except ValueError:
                                                        return False
                                                    
                                                if valDate(task_due) == True:
                                                    t['due_date'] = task_due
                                                    print()
                                                    print("                  UPDATED TASK                ")
                                                    disp_str = ''
                                                    disp_str += "_____________________________________________________\n\n"
                                                    disp_str += "Task {}: \t {}\n".format(t['Task Number'],t["title"])
                                                    disp_str += f"Assigned to: \t {t['username']}\n\n"
                                                    disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                                                    disp_str += f"Due Date: \t {t['due_date']}\n\n"
                                                    disp_str += f"Task Description:\n{t['description']}\n\n"
                                                    disp_str += f"Task Completed:\t {t['completed']}\n\n"
                                                    disp_str += "_____________________________________________________\n\n"
                                                    print(disp_str)
                                                    break
                                                        
                                                
                                                else:
                                                    print('Incorrect Date Format')
                                                    

                                        # ensure the user enters the correct values
                                        else:
                                            print("Make sure you enter [assignment] or [due date]\n")
                                            task_change = input('Change who the task is assigned to or change the due date of task. [assignment/due date] ')

                                        break

                                    break
                                else:
                                    print("You can not edit this task as it has been completed")
                                break
                            
                            # this ensures that the user only inputs yes,no or edit, else it will loop again
                            else:
                                print('Please enter [Yes/No/Edit]')
                                complete = input("Do you wish to mark the task as completed, [Yes/No] or edit the task? [edit] ").lower()

                            break
                        else:
                            break

                        break
                    break
                
            
        

            
                    

                    
       

            
        

       









        

    def generate_report(menu):
        
        total_tasks = 0
        completed_tasks = 0
        uncompleted_tasks = 0
        overdue_uncompleted = 0
        unique_users = []
        all_users = []

        from datetime import date

        today = date.today()

        for task in task_list:
            due_Date = datetime.strptime(str(task['due_date']),'%Y-%m-%d %H:%M:%S')
            due_Date = due_Date.date()
            total_tasks += 1

            all_users.append(task['username'])

            #This ensures only unique users are added to the list, can find the total amount of users
            if task['username'] not in unique_users:
                unique_users.append(task['username'])


            if task['completed'] == True:
                completed_tasks += 1
            else:
                uncompleted_tasks += 1

            
            if task['completed'] == False and due_Date < today:
                overdue_uncompleted += 1

                
        
        incomplete_percentage = int((uncompleted_tasks/(completed_tasks+uncompleted_tasks))*100)
        overdue_percentage = int((overdue_uncompleted/(completed_tasks+uncompleted_tasks))*100)
        
        

        # writing the task_overview file
        # overwriting any previous tasks in file as will give an updated amount
        with open('task_overview.txt','w') as task_overview:
            task_overview.write(

                "Total Tasks: " + str(total_tasks)+"\n"
                "Completed Tasks: " + str(completed_tasks)+"\n"
                "Uncompleted Tasks: " + str(uncompleted_tasks)+"\n"
                "Uncompleted and OVERDUE Tasks: " + str(overdue_uncompleted)+"\n"
                "Percentage of tasks Incomplete: " + str(incomplete_percentage)+"%"+"\n"
                "Percentage of tasks Overdue: "+str(overdue_percentage)+"%"

                

            )
        
        total_users = 0
        for person in unique_users:
            total_users += 1


        user_task = {}
        for person in unique_users:
            user_task.update({person:all_users.count(person)})
            

    




        


        # USER_OVERVIEW
        with open('user_overview.txt','w') as user_overview:
            user_overview.write(
                        "Total Users: " + str(total_users)+'\n'
                        "Total Tasks: " + str(total_tasks)+"\n\n"

            )
            user_completed = {}
            for one_user in user_task:
                completed = 0
                overdue = 0
                #this ensures that only tasks that have been completed are added to the dictionary which is then referenced
                for task in task_list:
                    if task['username'] == one_user:
                        if task['completed'] == True:
                            completed = completed + 1
                            user_completed.update({one_user:completed})
                        else:
                            if due_Date < today:
                                overdue += 1

                awaiting_completion = int(user_task[one_user])-int(completed)
                

                user_overview.write(

                                
                                str(one_user)+"\n"
                                "Number of Tasks: " + str(user_task[one_user])+"\n"+
                                "Total Tasks: " + str(total_tasks) + "\n"+
                                "Percentage of all Tasks: " + str(int((user_task[one_user]/total_tasks)*100))+"%"+"\n"+
                                "Completed Tasks: " + str(completed)+"\n"+
                                "Completion Percentage: " + str(int((completed/user_task[one_user])*100))+"%"+"\n"+
                                "Number of Tasks Awaiting Completion: " + str(awaiting_completion)+"\n"+
                                "Percentage of Tasks Overdue: " + str(int((overdue/user_task[one_user])*100))+"%"+"\n"
                                "\n"


                        )

        
            

        pass
                

        print("\nThe reports have been created in seperate files.")

    if menu == 'r':
        reg_user(menu)
    

    elif menu == 'a':
        add_task(menu)
    


    elif menu == 'va':
        view_all(menu)
            


    elif menu == 'vm':
        view_mine(menu)



    elif menu == 'gr':
        generate_report(menu)
    
    
    elif menu == 'ds' and curr_user == 'admin': 
        #If the user is an admin they can display statistics about number of users
         #   and tasks.
        num_users = len(username_password.keys())
        num_tasks = len(task_list)

        
        try:
            print("-----------------------------------")
            print(f"Number of users: \t\t {num_users}")
            print(f"Number of tasks: \t\t {num_tasks}")
            print("-----------------------------------")    
            print()
            task_file = open('task_overview.txt')
            print('TASK OVERVIEW')
            print()
            print(task_file.read(),'\n\n')
            user_file = open('user_overview.txt')
            print('USER OVERVIEW')
            print()
            print(user_file.read())

        except:
            generate_report(menu)                  
        


    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")