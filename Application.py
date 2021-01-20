import sqlite3
import os
import csv
import time
import sys
import threading
import keyboard
import re
from threading import *

if not os.path.exists(os.getcwd()+"\\quiz_wise_responses"):
    os.mkdir("quiz_wise_responses")
if not os.path.exists(os.getcwd()+"\\individual_responses"):
    os.mkdir("individual_responses")

responses = {1:"q1",
            2:"q2",
            3:"q3"   
        }

t = -1
conn=sqlite3.connect("Project1_Quiz_cs384.db")
c=conn.cursor()
#basic structure of database
c.execute(
'''
CREATE TABLE IF NOT EXISTS Project1_registration(
name VARCHAR(20) NOT NULL,
roll_number VARCHAR(20) NOT NULL,
password VARCHAR(20) NOT NULL,
whatsapp_num INT NOT NULL);
'''
)

c.execute(
'''
CREATE TABLE IF NOT EXISTS Project1_marks(
roll_num VARCHAR(20) NOT NULL,
quiz_num INT NOT NULL,
total_marks INT NOT NULL);
'''
)

conn.commit()

temp = 0
def countdown(): 
    global t
    global temp
    while t: 
        mins, secs = divmod(t, 60) 
        timer = '{:02d}:{:02d}'.format(mins, secs) 
        print(timer, end="\r") 
        time.sleep(1) 
        t -= 1
        if temp == 1:
            t = 0
            print('\nYour responses have been saved')
            temp = 0
            return
      
    print('\nTime Up!! Your responses have been saved \nEnter any valid key to exit')
def register():
    found=0
    print('\n'*4+'*'*25+'REGISTRATION PORTAL'+'*'*25)
    while found==0:
        roll_number=input("Please enter your roll number: ")
        find_user=("SELECT * FROM Project1_registration WHERE roll_number=?")
        c.execute(find_user,[(roll_number)])
        if c.fetchall():
            print("Your account already exists please log in")
            return
        else:
            found=1
    name=input("Please enter your name: ")
    password=input("Please enter your password: ")
    whatsapp_num=input("Please enter your whatsapp number: ")
    insertData='''INSERT INTO Project1_registration(name,roll_number,password,whatsapp_num)
    VALUES(?,?,?,?)'''
    c.execute(insertData,[(name),(roll_number),(password),(whatsapp_num)])
    conn.commit()

def login():
    while True:
        print('\n'*4+'*'*25+'LOGIN PORTAL'+'*'*25)
        username=input("Please enter your username: ")
        password=input("Please enter your password: ")
        find_user=("SELECT * FROM Project1_registration WHERE roll_number=? AND password=?")
        c.execute(find_user,[(username),(password)])
        results=c.fetchall()
        if results:
            for i in results:
                  multi_quiz([i[0],i[1],i[2],i[3]])
                  return
        else:
            print("username or password incorrect,try again")
unattempted = []           
def quiz(info):
    global t
    global question_list
    global unattempted
    global response
    global total_marks_obtained
    global total_marks
    global unattempted_num
    global correct_questions
    global wrong_choices
    global total_questions
    global attempted_questions
    print('\n'*4+'*'*25+'WELCOME'+'*'*25)
    quiz_num=input("please choose a quiz which you want to attempt(Please enter quiz number) \n1.Quiz1\n2.Quiz2\n3.Quiz3\n")
    path=os.getcwd()+'\\'+'quiz_wise_questions'
    curpath = os.getcwd()
    os.chdir(path)
    filename = responses[int(quiz_num)] + '.csv'
    f = open(filename, 'r')
    with f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == 'ques_no':
                temp = row[10]
                t = temp[5:-1]
    qfile = open(filename, 'r')
    freader = csv.DictReader(qfile)
    os.chdir(curpath)
    t = 120
    response=[]
    correct_questions=0
    total_marks = 0
    attempted_questions=0
    total_marks_obtained=0
    total_questions = 0
    unattempted_num = 10
    wrong_choices=0
    unattempted=[1,2,3,4,5,6,7,8,9,10]
    question_list = []
    t1 = threading.Thread(target = countdown)
    t1.start()
    for row in freader:
        question_list.append(row)
        total_questions += 1
        
    print('\n'*4+'*'*25+'QUIZ STARTS'+'*'*25)
    
    for row in question_list:
        if t == 0:
            break
        print("Timer: "+str(t)+'\n'+"Roll Number: "+info[1]+'\n'+"Name: "+info[0]+'\n')
        print("Press Ctrl+Alt+U to see the unattempted questions")
        print("Question"+row['ques_no']+": "+row['question'])
        print("Option "+'1'+") "+row['option1'])
        print("Option "+'2'+") "+row['option2'])
        print("Option "+'3'+") "+row['option3'])
        print("Option "+'4'+") "+row['option4'])
        print("\n")
        print("Credits if correct option: "+row['marks_correct_ans'])
        print("Negative Marking: "+row['marks_wrong_ans'])
        print("Is compulsory: "+row['compulsory'])
        valid_response=['1','2','3','4','S','s']
        while True:
            choice=input("\nEnter Choice 1, 2, 3, 4, S(S is to skip question): \n")
            if choice in valid_response:
                break
            else:
                print("please enter valid choice")
        if t == 0:
            break
        #keyboard.add_hotkey("ctrl+alt+U", lambda : print("Unattempted Questions are:",unattempted))
        response.append(choice)
        if choice.lower()=='s':
            if row['compulsory'].lower()=='y':
                total_marks_obtained+=int(row['marks_wrong_ans'])
        else:
            unattempted.remove(int(row['ques_no']))
            attempted_questions+=1
            if row['correct_option']==choice:
                correct_questions+=1
                total_marks_obtained+=int(row['marks_correct_ans'])
            else:
                wrong_choices+=1
                total_marks_obtained+=int(row['marks_wrong_ans'])
        print('\n'*2)
    
    total_marks=0
    with open(path+'\\'+'q'+quiz_num+'.csv','r') as file:
        questions=csv.reader(file)
        for question in questions:
            if question[0]=='ques_no':
                continue
            if int(question[0]) in unattempted and question[9].lower()=='y':
                total_marks_obtained+=int(question[8])
            total_marks+=int(question[7])
    with open(path+'\\'+'q'+quiz_num+'.csv','r') as file:
        questions=csv.reader(file)
        itr=0
        response=response+['s']*(10-len(response))
        for question in questions:
            with open(os.getcwd()+'\\'+'individual_responses'+'\\'+'q'+quiz_num+'_'+info[1]+'.csv','a',newline='') as wfile:
                writer=csv.writer(wfile)
                if question[0]=='ques_no':
                    writer.writerow(question+['marked_choice','Total','Legend'])
                    continue
                if itr==0:
                    writer.writerow(question+[response[itr],correct_questions,'Correct Choices'])
                elif itr==1:
                    writer.writerow(question+[response[itr],wrong_choices,'Wrong Choices'])
                elif itr==2:
                    writer.writerow(question+[response[itr],len(unattempted),'Unattempted'])
                elif itr==3:
                    writer.writerow(question+[response[itr],total_marks_obtained,'Marks Obtained'])
                elif itr==4:
                    writer.writerow(question+[response[itr],total_marks,'Total Quiz Marks'])
                else:
                    writer.writerow(question+[response[itr],'',''])
                itr+=1
    total_quiz_questions=len(response)
    print('''Total Quiz Questions:{}
Total Quiz Questions Attempted:{}
Total Correct Question:{}
Total Wrong Questions:{}
Total Marks: {}/{}'''.format(total_quiz_questions,attempted_questions,correct_questions,wrong_choices,total_marks_obtained,total_marks))
    
    print("Press Ctrl+Alt+U to see the unattempted questions")
    print("Press Ctrl+Alt+G to go to your desired question")
    print("Press Ctrl+Alt+F to submit the quiz finally")
    print("Press Ctrl+Alt+E to export the database to csv")
    t1.join()
    quiz_num=int(quiz_num)
    find_user=("SELECT * FROM Project1_marks WHERE roll_num=? AND quiz_num=?")
    c.execute(find_user,[(info[1]),(quiz_num)])
    results=c.fetchall()
    if results:
        c.execute('DELETE FROM Project1_marks WHERE roll_num=? AND quiz_num=?',(info[1],quiz_num))
    insertData='''INSERT INTO Project1_marks(roll_num,quiz_num,total_marks)
    VALUES(?,?,?)'''
    c.execute(insertData,[(info[1]),(quiz_num),(total_marks_obtained)])
    conn.commit()
def gotoQuestion():
    quesNum = int(input("Enter the question number you want to go to: "))
    row = question_list[quesNum-1]
    print("Question "+row['ques_no']+") "+row['question'])
    print("Option 1) "+row['option1'])
    print("Option 2) "+row['option2'])
    print("Option 3) "+row['option3'])
    print("Option 4) "+row['option4'])
    print("\n")
    print("Credits if Correct Option: "+row['marks_correct_ans'])
    print("Negative Marking: "+row['marks_wrong_ans'])
    
    if row['compulsory'].lower() == 'y':
        print("Is compulsory: YES")
    else:
        print("Is compulsory: NO")
    
    if len(response) >= quesNum:
        print("Your marked choice is:",response[quesNum-1])
    else:
        print("You have not attempted this question yet")
    print("\n")
def showUnattempted():
    global unattempted
    print("\nUnattempted questions are:",unattempted,"\n")
def final_submit():
    global temp
    x=input('Are you sure you want to submit?(Y/N)')
    if x.lower()=='y':
        temp=1
def exportdb():
    conn=sqlite3.connect("Project1_Quiz_cs384.db")
    entries = conn.execute("SELECT * FROM Project1_marks")
    for entry in entries:
        quiz_num = entry[1]
        rollNo = entry[0]
        marks = entry[2]
        if not os.path.exists(os.getcwd()+"\\quiz_wise_responses\\"+"scores_q"+str(quiz_num)+".csv"):
            qfile = open(os.getcwd()+"\\quiz_wise_responses\\"+"scores_q"+str(quiz_num)+".csv","a",newline='')
            fwriter = csv.DictWriter(qfile, ["roll_number","total_marks"])
            fwriter.writeheader()
            fwriter.writerow({"roll_number":rollNo,"total_marks":marks})
        else:
            qfile = open(os.getcwd()+"\\quiz_wise_responses\\"+"scores_q"+str(quiz_num)+".csv","a",newline='')
            fwriter = csv.DictWriter(qfile, ["roll_number","total_marks"])
            fwriter.writerow({"roll_number":rollNo,"total_marks":marks})
def multi_quiz(info):
    while True:
        quiz(info)
        res=input("would you like to attempt one more quiz:(Y/N) ")
        if res.lower()!='y':
            break
    return
keyboard.add_hotkey("Ctrl+Alt+G", gotoQuestion)
keyboard.add_hotkey("Ctrl+Alt+U", showUnattempted)
keyboard.add_hotkey("Ctrl+Alt+F", final_submit)
keyboard.add_hotkey("Ctrl+Alt+E", exportdb)
if __name__ == '__main__':
    while True:
        new=input("Do you have an account(y/n)  ")
        if(new.lower()=='n'):
            register()
            break
        elif(new.lower()=='y'):
            break
        else:
            print("/nplease enter a valid key")
    login()