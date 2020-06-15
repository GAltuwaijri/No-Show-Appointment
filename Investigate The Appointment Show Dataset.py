#!/usr/bin/env python
# coding: utf-8

# # Medical Appointment No Shows 
# #### *GHAIDA S. ALTUWAIJRI*
# #### *May 21, 2020*

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sn

import csv
from datetime import datetime as dt
from collections import defaultdict
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# <a id='wrangling'></a>
# ## Data Wrangling
# 
# ### General Properties

# In[4]:


#loading the dataset 
nsa = pd.read_csv('NoShowAppointments-kagglev2-may-2016.csv' ,                         parse_dates=['ScheduledDay', 'AppointmentDay']) 


# In[5]:


nsa.head()


# In[6]:


#Removing the Unneeded columns
columns = ['Neighbourhood', 'Scholarship', 'Hipertension', 'Diabetes', 'Alcoholism', 'Handcap']
nsa.drop(columns, inplace=True, axis=1)


# In[7]:


# Rename for 'No-show', 'SMS_received' and 'NoShow'.
nsa.rename(columns={ 'No-show' : 'NoShow' }, inplace = True) 
nsa.rename(columns={ 'SMS_received' : 'SMSReceived' }, inplace = True) 
nsa.rename(columns={ 'NoShow' : 'Show' }, inplace = True) 


# In[8]:


# Removing the time from 'ScheduledDay' and 'AppointmentDay'
nsa['AppointmentDay'] = pd.to_datetime(nsa['AppointmentDay']).dt.date
nsa['ScheduledDay'] = pd.to_datetime(nsa['ScheduledDay']).dt.date

# Creating new column with deference between 'ScheduledDay' and AppointmentDay.
SAdifferents = nsa["AppointmentDay"] - nsa["ScheduledDay"]
nsa["ScheduledToAppointment"] = SAdifferents
# Convert the new column to integer type.
nsa['ScheduledToAppointment'] = pd.to_numeric(nsa['ScheduledToAppointment'].dt.days, downcast='integer')


# In[9]:


# For the show column, We will replace No with 1 and yes with 0, And covert it to integar type.
nsa['Show'] = nsa['Show'].replace( 'No', 1)
nsa['Show'] = nsa['Show'].replace( 'Yes', 0)
nsa.Show = nsa.Show.astype(int)


# In[10]:


nsa.dtypes


# In[11]:


# Changing the types of 'PatientId' and 'AppointmentID' to String
nsa.PatientId = nsa.PatientId.astype(str)
nsa.AppointmentID = nsa.AppointmentID.astype(str)


# In[12]:


nsa.head(10)


# In[13]:


nsa.info()


# In[14]:


nsa.nunique() 


# In[15]:


nsa.hist(figsize=(10,8));


# ### Checking if there is any wrong or missing data

# In[16]:


#check if there is any NaN values in our dataset
show_null = nsa.isnull().sum() 
show_null


# In[17]:


#check if there is any zero ages 
show_zero = nsa['Age'][(nsa[['Age']] == 0).all(axis=1)]  
show_zero


# In[18]:


#check if there is very old ages
show_old = nsa['Age'][(nsa[['Age']] > 100).all(axis=1)] 
show_old


# In[19]:


#check if there is any minus ages 
show_minus = nsa['Age'][(nsa[['Age']] < 0).all(axis=1)] 
show_minus


# In[20]:


#check if there is any minus days between Scheduled day and Appointment day
nsa['ScheduledToAppointment'][(nsa[['ScheduledToAppointment']] < 0).all(axis=1)]


# in this part of our project we load and discoverd the data, check for cleanliness, and then trim and clean our dataset for analysis.

# ### Doing some calculations for 'NoShow' , 'Gender' and 'SMSReceived' columns.

# In[21]:


# returning a number of patints who shows and who did not (did use it)
showing_counts = nsa["Show"].value_counts()
show_counts = showing_counts[1] 
no_show_counts = showing_counts[0] 

# returning a table with patints who shows or who did not
didshow= nsa [nsa.Show == True]
did_not_show= nsa [nsa.Show == False]

# creating masks with patints who shows or who did not
didNotShow = nsa.Show == False
didShow = nsa.Show == True


# In[22]:


# returning a number of males and females 
gender_counts = nsa["Gender"].value_counts()
female_counts = gender_counts['F']
male_counts = gender_counts['M']

# returning a table with only males or only females
male_gender = nsa [nsa["Gender"] == ('M')]
female_gender = nsa [nsa["Gender"] == ('F')]


# In[23]:


# returning a total number of receiving SMS or not 
SMS_counts = nsa["SMSReceived"].value_counts()
one_counts = gender_counts[1]
zero_counts = gender_counts[0]

# returning a table with males or females only
didNotReceived = nsa [nsa["SMSReceived"] == (0)]
didReceived = nsa [nsa["SMSReceived"] == (1)]


# In the above set of code cells, We did some calculations on the 'NoShow' column by counting the number of patients who shows and who did not. also, returning new separate tables for only the patients who show or only who did not.
# 
# We did the same for the 'Gender' and 'SMSReceived' columns, so we count the total number for each value and returning new separate tables for these values.

# ### Data Cleaning
# 
# #### Replacing the Zero and Minus ages with the age mean

# In[24]:


age_mean = nsa['Age'].mean() # find the 'Age' mean 
age_mean = (round(age_mean)) # convert the mean to the nearest integer 
print(age_mean) 


# In[25]:


nsa['Age'] = nsa['Age'].replace( 0, age_mean) #replace the 0 values to the age_mean
nsa['Age'] = nsa['Age'].replace( -1, age_mean) #replace the -1 value to the age_mean


# In[26]:


nsa.loc[ 99832 , : ] # check if the minus value changed 


# In[27]:


nsa['Age'][(nsa[['Age']] == 0).all(axis=1)]  #check if there is any zero ages 


# #### Replacing the Minus values for 'ScheduledToAppointment' with it's mean

# In[28]:


days_mean = nsa['ScheduledToAppointment'].mean() # find the 'ScheduledToAppointment' mean 
days_mean = days_mean.astype(int) # convert the mean to integer 
print(days_mean) 


# In[29]:


#replace the -1 value to the days_mean
nsa['ScheduledToAppointment'] = nsa['ScheduledToAppointment'].replace( [-1, -6], days_mean)


# In[30]:


# check if the minus value changed 
nsa['ScheduledToAppointment'][(nsa[['ScheduledToAppointment']] < 0).all(axis=1)]


# After discussed the structure of the data and the problems that need to be cleaned, we performed those cleaning steps in the above part.

# <a id='eda'></a>
# ## Exploratory Data Analysis
# 
# 
# In the exploration part, After trimmed and cleaned our data we will Compute statistics and create visualizations with the goal of addressing the following research questions.

# ##### Getting a Visual Representation of the Correlation Matrix using Seaborn and Matplotlib

# In[41]:


def histogram_intersection(df):

    corrMatrix = df.corr()

    sn.heatmap(corrMatrix, annot=True)
    plt.title("Relationship Between Dataset Columns", y=1.02, fontsize=10);
    v = plt.show()
    return v


histogram_intersection(nsa)


# This scatter plot or correlation matrix is to show the relationship between Age, SMSReceived, Show and ScheduledToAppointment.

# ### What is the ***percentage*** of attending or not attending the appointments?

# In[31]:


# Data to plot
labels = 'Not Show', 'Show'
sizes = [no_show_counts, show_counts]
colors = ['lightcoral', 'yellowgreen']
explode = (0.1, 0 )  # explode 1st slice
 
# Plot
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=140)

plt.title("people who attend or not their appointments", y=1.02, fontsize=10);
plt.axis('equal')
plt.show()


# this pie-chart shows the percentage of attending the appointments or not, and we notice that there is ***20.2%*** of patients didn't show on the appointments and ***79.8%*** for the people who attend. the next charts will illustrate not attending these appointments and find a solutions for that or predict the people who will not attend in the future.

# ### Which gender have more commitment to attend the appointment?

# In[32]:


showToGender = nsa.groupby(['Gender', 'Show']).size().plot(kind='bar',stacked=False)
showToGender.set_xlabel("Gender who show or not")
showToGender.set_ylabel("No. of people for each ")
plt.title("Gender per Patients Who Attend or Not", y=1.02, fontsize=14)
plt.show()


GenderPerNo = nsa['Gender'].hist(); #there is females more that males
GenderPerNo.set_xlabel("Number of females and males ")
plt.title("Gender Per No. of Patients", y=1.02, fontsize=14)
plt.show()


# The above graph shows that the number of females is greater than males. So we will compare between the (f, 1) which is the females did show and (f, 0) which is the female who did not show, and the same for (M, 1) and (M, 0).
# 
# We notice that **Females are more committed than males**, And that is because of the number of females who show almost four times bigger than females who did not show. And for males who show only three times bigger than those who did not.

# ### Does age affect the attendance of appointments?

# In[33]:


showToAge = nsa.Age[didNotShow].hist(alpha=0.9 ,label='Did Not Show')
showToAge = nsa.Age[didShow].hist(alpha=0.4 ,label='Did Show')
showToAge.set_xlabel("Age")
showToAge.set_ylabel("No. of Patients")
plt.title("Age per Patients Who Attend or Not", y=1.02, fontsize=14)
plt.legend();


# the Age deferences histogram 
PeoplePerAge = nsa[['Age']].plot( kind='hist',bins=[0,20,40,60,80,100],rwidth=0.8) 
PeoplePerAge.set_xlabel("Age")
PeoplePerAge.set_ylabel("No. of Patients")
plt.title("No. of Patients For Each Age", y=1.02, fontsize=14)
plt.show()


# The first chart shows that **Age is an affecting factor for the attending appointments**. As seen for the second graph,we have a different number of people per each age. but we can notice that the kids between 0-12years are showing on appointments more than people between 12-23. and people between 35-46 are committed more than between 23-35 on attending their appointments.

# ### Is sending reminder messages helps the patient to remember and attend the appointments?

# In[34]:


#the SMS Recived histogram
sizes = ['Show']
colors = ['lightcoral', 'yellowgreen']
ShowToSMS = nsa.groupby(['Show', 'SMSReceived']).size().unstack().plot( kind='bar', color=colors )
ShowToSMS.set_xlabel("People who show or not")
ShowToSMS.set_ylabel("No. of Patients")
plt.title("SMS Received Per People Who Attend or Not", y=1.02, fontsize=14)
plt.show()


# In[35]:


nsa.groupby(['Show', 'SMSReceived']).size().unstack()


# This bar graph illustrates the relation between receiving messages and attending appointments. The 0 values in the X axis represent people who didn't show and 1 for people who show. We know that number of people who received 0 messages is more that who received 1. In this case, we will answer our question by comparing the people who don't show and people who show separately. So for the people who show there is a bigger difference between who received 1 and 0 message. And for the people who don't show it almost the same between who received message or not, So the answer is: **receiving SMS doesn't positively affect showing on appointments**.

# ### Is scheduling the appointment long time before will affect attending?

# In[36]:


showSMS = nsa.ScheduledToAppointment[didNotShow].hist(alpha=0.5, bins=20 ,label='did not show', color='green')
showSMS = nsa.ScheduledToAppointment[didShow].hist(alpha=0.5,  bins=20 ,label='did show')
showSMS.set_xlabel("Days between Scheduled day and Appointment day")
showSMS.set_ylabel("No. of People")
plt.title("Days per people who show or not", y=1.02, fontsize=14)
plt.legend();


# This histogram shows that most of the people scheduled their appointment very short time before it's date, And it's cleared by the chart that most people attend their appointments when they scheduled it on the same day of the appointment and vise versa if they sceduled a long time before.
# 
# So, our answer is YES

# ### What factors are important for us to know in order to predict if a patient will show up for their scheduled appointment?

# by doing the above calculations and visualizations, we came up that we can predict if a patient will show up for their scheduled appointment by ***Scheduling Date, Age, and Gender*** factors.

# And now, we answered all of our questions by computed some statistics and created visualizations to make it easier to understand for all people.
