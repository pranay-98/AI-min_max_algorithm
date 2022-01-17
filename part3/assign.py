#!/usr/local/bin/python3
# assign.py : Assign people to teams
#
# Code by: "Pranay Reddy / pdasari, Vamsee Krishna Sai / vnarams, Anil Ravi/ anilravi "
#
# Based on skeleton code by D. Crandall and B551 Staff, September 2021
#

import sys
import time
from itertools import combinations
import numpy
import random as rn
import math



#Giving preference to Team Size_3 followed by Team Size_2,Team Size_1
def team_Formation(size,users):
    Final_Team_Combinations=[]
    Team_size_3,size_3=0,0
    Team_size_2,size_2=0,0
    Team_size_1,size_1=0,0
    if size>0:
        Team_size_3=size//3
        size_2=size%3
    if size_2>0:
        Team_size_2=size_2//2
        size_1=size_2%2
    if size_1>0:
        Team_size_1=size_1//1
        size_0=size_1%1
    no_Of_Teams=int(Team_size_3)+int(Team_size_2)+int(Team_size_1)
    if Team_size_3>0:
        while Team_size_3>0:
            Final_Team_Combinations.append(rn.sample(list(combinations(users,3)),1))
            User_list_tuples=[X[0] for X in Final_Team_Combinations]
            User_list = [item for t in User_list_tuples for item in t]
            users = [i for i in users if i not in User_list]
            Team_size_3-=1  
    if Team_size_2>0:
        while Team_size_2>0:
            Final_Team_Combinations.append(rn.sample(list(combinations(users,2)),1))
            User_list_tuples=[X[0] for X in Final_Team_Combinations]
            User_list = [item for t in User_list_tuples for item in t]
            users = [i for i in users if i not in User_list]
            Team_size_2-=1
    if Team_size_1>0:
        while Team_size_1>0:
            Final_Team_Combinations.append(rn.sample(list(combinations(users,1)),1))
            User_list_tuples=[X[0] for X in Final_Team_Combinations]
            User_list = [item for t in User_list_tuples for item in t]
            users = [i for i in users if i not in User_list]
            Team_size_2-=1  
    return User_list_tuples,no_Of_Teams

def cost_Function(FinalGroups,dict_User_Expected_Team,dict_User_Not_Expected_TeamMembers,no_Of_Teams):
    total_time=0
    total_wrong_size=0
    total_wrong_person_time=0
    cost=1
    total_share_code_score=0
    members_wanted=dict()
    time_taken_for_grading=no_Of_Teams*5
    for k,v in dict_User_Expected_Team.items():
        each_user=v.split('-')
        members_wanted[k]=len(each_user)
    for k,v in members_wanted.items():
        for user in FinalGroups:
            if k in user:
                if v<len(user):
                    total_wrong_size=cost*2+total_wrong_size
    for k,v in dict_User_Not_Expected_TeamMembers.items():
        for user in FinalGroups:
            if v in user:
                    total_wrong_person_time=cost*10+total_wrong_person_time
   
    for k,v in dict_User_Expected_Team.items():
        for user in FinalGroups:
            if v not in user:
                total_share_code_score=cost*0.05*60+total_share_code_score
    total_time=time_taken_for_grading+total_wrong_size+total_wrong_person_time+total_share_code_score
    return total_time
          
def solver(input_file):
    """
    1. This function should take the name of a .txt input file in the format indicated in the assignment.
    2. It should return a dictionary with the following keys:
        - "assigned-groups" : a list of groups assigned by the program, each consisting of usernames separated by hyphens
        - "total-cost" : total cost (time spent by instructors in minutes) in the group assignment
    3. Do not add any extra parameters to the solver() function, or it will break our grading and testing code.
    4. Please do not use any global variables, as it may cause the testing code to fail.
    5. To handle the fact that some problems may take longer than others, and you don't know ahead of time how
       much time it will take to find the best solution, you can compute a series of solutions and then
       call "yield" to return that preliminary solution. Your program can continue yielding multiple times;
       our test program will take the last answer you 'yielded' once time expired.
    """
    dict_User_Expected_Team=dict()
    dict_User_Not_Expected_TeamMembers=dict()
    Users=[]
    file=open(sys.argv[1],'r')
    for f in file:
        line=f.rstrip('\n')
        each_line=line.split(' ')
        Users.append(each_line[0])
        dict_User_Expected_Team[each_line[0]]=(each_line[1])
        if each_line[2] is not None and each_line[2] != '_':
            dict_User_Not_Expected_TeamMembers[each_line[0]]=(each_line[2])
    file.close()

    max_Groups=len(dict_User_Expected_Team)
    FinalGroups,no_Of_Teams=team_Formation(max_Groups,Users)
    staff_Time=cost_Function(FinalGroups,dict_User_Expected_Team,dict_User_Not_Expected_TeamMembers,no_Of_Teams)

    final_teams = ['-'.join(i) for i in FinalGroups]





    yield({"assigned-groups": final_teams,
               "total-cost" : staff_Time})

 
    time.sleep(10)
    yield({"assigned-groups": final_teams,
               "total-cost" :staff_Time})


    while True:
        pass
    
    yield({"assigned-groups": final_teams,
               "total-cost" : staff_Time})

if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected an input filename"))

    for result in solver(sys.argv[1]):
        print("----- Latest solution:\n" + "\n".join(result["assigned-groups"]))
        print("\nAssignment cost: %d \n" % result["total-cost"])
    
