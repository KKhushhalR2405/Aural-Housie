from flask import Flask,render_template,request,redirect
import flask
import time
import random
from jinja2 import Environment
from jinja2.loaders import FileSystemLoader

import numpy as np
import pandas as pd
from random import randint
import random
import numpy as np
import sys
import speech_recognition as sr
from win32com.client import Dispatch
from tabulate import tabulate


app = Flask(__name__)

#-------------------------------------------
def list_gen():
        return list(range(1,91))
#-------------------------------------------
#-------------------------------------------
def random_number(l):
        n = random.choice(l)
        return n
#-------------------------------------------
#-------------------------------------------
def create_dict(t):
        values = [0]*len(range(t))
        return dict(list(enumerate(values)))
#-------------------------------------------
#-------------------------------------------
def get_ticket():
        """
        #1 - Maintain array of total_numbers between 1 and 90. Initialize ticket_array as 3x9 array of 0s
        #2 - Generate 15 random indices from the array of total_indices. 
        #3 - Compute index to drop the value into based on RULE #1, RULE #2
        #4 - Remove values used in the ticket from the base array (RULE #1, RULE #2)
        #5 - Repeat till 15 numbers are populated into ticket
        #6 - Sort numbers in every column of the ticket based on RULE #3
        """

        # Create a 2D array [3x9] of 0s
        ticket_array = np.zeros((3, 9), dtype=int)
        # Create an a list of numbers from 1 to 90.
        total_numbers = [num for num in range(1, 90)]
        # Create a list of tupele of all the indices of 3x9 ticket_array . i.e (0,0),(0,1),...,(2,8)
        total_indices = [(i, j) for i in range(3) for j in range(9)]
        # Create an empty list to store 15 random indices to fill in the value.
        random_indices = []

        # Generate 15 random indices that satisfies RULE #1 and store them in random_indices array.
        np.random.seed(57)
        first_row = random.sample(total_indices[:9], 5)
        second_row = random.sample(total_indices[9:18], 5)
        third_row = random.sample(total_indices[-9:], 5)

        for i in first_row:
            random_indices.append(i)

        for i in second_row:
            random_indices.append(i)

        for i in third_row:
            random_indices.append(i)

        # Populate values in the randomly generated indices such that it satisfies RULE #2 and replace the  value of the used value in total_numbers array by 0.

        for num in random_indices:
            if num[1] == 0:
                number = random.choice(total_numbers[:10])
                ticket_array[num] = number
                total_numbers[total_numbers.index(number)] = 0
            elif num[1] == 1:
                number = random.choice(total_numbers[10:20])
                ticket_array[num] = number
                total_numbers[total_numbers.index(number)] = 0
            elif num[1] == 2:
                number = random.choice(total_numbers[20:30])
                ticket_array[num] = number
                total_numbers[total_numbers.index(number)] = 0
            elif num[1] == 3:
                number = random.choice(total_numbers[30:40])
                ticket_array[num] = number
                total_numbers[total_numbers.index(number)] = 0
            elif num[1] == 4:
                number = random.choice(total_numbers[40:50])
                ticket_array[num] = number
                total_numbers[total_numbers.index(number)] = 0
            elif num[1] == 5:
                number = random.choice(total_numbers[50:60])
                ticket_array[num] = number
                total_numbers[total_numbers.index(number)] = 0
            elif num[1] == 6:
                number = random.choice(total_numbers[60:70])
                ticket_array[num] = number
                total_numbers[total_numbers.index(number)] = 0
            elif num[1] == 7:
                number = random.choice(total_numbers[70:80])
                ticket_array[num] = number
                total_numbers[total_numbers.index(number)] = 0
            elif num[1] == 8:
                number = random.choice(total_numbers[80:89])
                ticket_array[num] = number
                total_numbers[total_numbers.index(number)] = 0

        # Sort the ticket_array column wise to satisfy the RULE #3

        for col in range(9):
            # if all the rows are filled with random number
            if(ticket_array[0][col] != 0 and ticket_array[1][col] != 0 and ticket_array[2][col] != 0):
                for row in range(2):
                    if ticket_array[row][col] > ticket_array[row+1][col]:
                        temp = ticket_array[row][col]
                        ticket_array[row][col] = ticket_array[row+1][col]
                        ticket_array[row+1][col] = temp

            # if 1st and 2nd row are filled by random number
            elif(ticket_array[0][col] != 0 and ticket_array[1][col] != 0 and ticket_array[2][col] == 0):
                if ticket_array[0][col] > ticket_array[1][col]:
                    temp = ticket_array[0][col]
                    ticket_array[0][col] = ticket_array[1][col]
                    ticket_array[1][col] = temp

            # if 1st and 3rd row are filled by random number
            elif(ticket_array[0][col] != 0 and ticket_array[2][col] != 0 and ticket_array[1][col] == 0):
                if ticket_array[0][col] > ticket_array[2][col]:
                    temp = ticket_array[0][col]
                    ticket_array[0][col] = ticket_array[2][col]
                    ticket_array[2][col] = temp

            # if 2nd and 3rd rows are filled with random numbers
            elif(ticket_array[0][col] == 0 and ticket_array[1][col] != 0 and ticket_array[2][col] != 0):
                if ticket_array[1][col] > ticket_array[2][col]:
                    temp = ticket_array[1][col]
                    ticket_array[1][col] = ticket_array[2][col]
                    ticket_array[2][col] = temp

        return ticket_array
#-------------------------------------------
#-------------------------------------------
def main1(t):
    
    ticket=[]
    
    
    for i in range(t):
        tick = get_ticket()
        ticket.append(tick)
    return ticket
#-------------------------------------------
#-------------------------------------------
def main2(t,ticket):
    result_array = []
    arr=[]
    row_1=create_dict(t)
    row_2=create_dict(t)
    row_3=create_dict(t)
    count = create_dict(t)
    final = create_dict(t)
    c=0
    r_1=0
    r_2=0
    r_3=0
    
    
    l = list_gen()
    F=0
    while (F==0):
        
        n = random_number(l)
        
        arr.append(n)
        l.remove(n)
        for i in range(t):
            if n in ticket[i]:
                count[i]+=1
            ticket[i][ticket[i]==n] -= n
            if np.all((ticket[i][0] == 0)):
                row_1[i]+=1
            if np.all((ticket[i][1] == 0)):
                row_2[i]+=1
            if np.all((ticket[i][2] == 0)):
                row_3[i]+=1
            if np.all((ticket[i] == 0)):
                final[i]+=1
        
        
        
        if c==0:
            for k in count.keys():
                    if count[k] == 5:

                        arr.append("Jaldhi 5 for ticket {}".format(k+1))
                        result_array.append('Jaldhi 5 for ticket {}'.format(k+1))
                        
                        c +=1  

        if r_1==0:
            for N in row_1.keys():
                if row_1[N]>0:
                    
                    arr.append('Row 1 is Completed for ticket {}'.format(N+1))
                    result_array.append('Row 1 is Completed for ticket {}'.format(N+1))
                    r_1+=1
                    
           
        if r_2==0:
            for M in row_2.keys():
                if row_2[M]>0:
                    
                    arr.append('Row 2 is Completed for ticket {}'.format(M+1))
                    result_array.append('Row 2 is Completed for ticket {}'.format(M+1))
                    r_2+=1
        
        if r_3==0:
            for L in row_3.keys():
                if row_3[L]>0:
                    
                    arr.append('Row 3 is Completed for ticket {}'.format(L+1))
                    result_array.append('Row 3 is Completed for ticket {}'.format(L+1))
                    r_3+=1
        
        for O in final.keys():
            if final[O]>1:

                arr.append("Bingo! Congratulations for ticket {}".format(O+1))
                result_array.append('Bingo! Congratulations for ticket {}'.format(O+1))
                F+=1
    
    i=0
    while(i<len(arr)):
        
        time.sleep(2)
        yield '%s' % arr[i]
        i+=1


 
#-------------------------------------------
#-------------------------------------------
def maindf(ticket_list):  #to convert numpy array to pandas dataframe
    k=[]
    l=[]
    for i in ticket_list:
        k.append((pd.DataFrame(i)).replace(0," "))
    
    return k
#-------------------------------------------
#-------------------------------------------
#-------------------------------------------







@app.route('/')
def main():   #default route
   return render_template('main.html')



@app.route("/result",methods = ['POST', 'GET'])
def show_tables():

    if request.method == 'POST':
        t = int(request.form["Name"])
      
        final_ticket = main1(t)

        final_number = main2(t,final_ticket)
        
        
        
        final_df = maindf(final_ticket)

        
        table_list = [i.to_html(classes='female') for i in final_df]
        title_list = ["Ticket "+str(i) for i in range(t+1)]

        
        env = Environment(loader=FileSystemLoader('templates'))
        tmpl = env.get_template('output.html')
        return flask.Response(tmpl.generate(tables=table_list,titles = title_list,result=final_number))
        
    else:
        return "RETRY"








if __name__ == "__main__":
    app.run(debug=True)

"""
         """