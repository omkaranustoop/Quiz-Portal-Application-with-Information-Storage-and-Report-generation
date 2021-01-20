# Quiz-Portal-Application-with-Information-Storage-and-Report-generation
A quiz based application with negative marking, timer, scores and report generation. The information for each Candidate is stored in SQLite3 DataBase and exported into CSV.

## Directory Structure :-

This Directory Consists of the following files :-

**1.Application.py** :- Python file which has entire code for User Registration and Information Storage in DataBase, Conducting Quiz with Timer, storing and exporting results from DataBase into CSV files as final Reports.

**2.Data_Base.db** :- A Sample SQLite3 DataBase File which has registration information and quiz results of Users.

**3.Quiz_Wise_Questions** :- This folder contains some sample Question files in csv format.

**4.Individual_Responses** :- This folder contains some sample Result Reports for each user and the corresponding quiz in csv format.

**5.Quiz_Wise_Responses** :- This folder contains some sample Quiz Summaries, i.e for each 
quiz what were the marks obtained by different users in it.

## Project Summary

This is a CLI Quiz Portal Application which uses Core Python Concepts. The main goals accomplished in this Project are:-

1. Storage of User Registration Information in a SQLite3 DataBase and Retrieval for login.
2. Conducting Quizzes based on choice of user on which quiz he/she wants to give. The quiz has a timer attached which uses concept of Multi-Threading.
3. Short-Cut Keys which can be used by the user to see his/her response to a particular question, Submit the quiz at any instant, Export DataBase information into CSV, show Unattempted Questions.
