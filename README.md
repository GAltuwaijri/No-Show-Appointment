# No-Show-Appointment
On this project, we aimed to explore the 'Medical Appointment No Shows' dataset from Kaggle bu using python, and finding answers for our questions.

## Table of Contents
<ul>
<li><a href="#intro">Introduction</a></li>
<li><a href="#wrangling">Data Wrangling</a></li>
<li><a href="#eda">Exploratory Data Analysis</a></li>
<li><a href="#conclusions">Conclusions</a></li>
<li><a href="#bibliography">Bibliography</a></li>    
</ul>

## Setup
In order to run the notebook, you'll need to install:
- Python 3.6
- Jupyter (notebook or lab)
- Pandas
- Numpy
- Matplotlib

This notebook will not be maintained.

<a id='intro'></a>
## Introduction
This dataset collects information from 100k medical appointments inBrazil and is focused on the question of whether or not patients showup for their appointment. A number of characteristics about the patient are included in each row.
- ‘ScheduledDay’ tells us on what day the patient set up their appointment.
- ‘Neighborhood’ indicates the location of the hospital.
- ‘Scholarship’ indicates whether or not the patient isenrolled in Brasilian welfare program Bolsa Família.
- the last column says ‘No’ if the patient showed up to their appointment, and ‘Yes’ if they did not show up

On this project, we aimed to explore the 'Medical Appointment No Shows' dataset from Kaggle and finding answers for these questions:
- what is the percentage of attending or not attending the appointments?
- which gender have more commitment to attend the appointment?
- Does age affect the attendance of appointments?
- Is sending reminder messages help the patient to remember and attend the appointments?
- Is scheduling the appointment long time before will affect attending?
- What factors are important for us to know in order to predict if a patient will show up for their scheduled appointment?

### Limitations
there is a few limitations of our dataset:
- It would be interesting if there is a column for review or rate for the previous appointment.
- It would be more accurate if the appointment time provided with appointment data.
- It would be interesting if we know the individual education for each appointment.

### License
No-Show-Appointment is Copyright © 2020 Ghaida Altuwaijri. The content of this repository is licensed under a Creative Commons Attribution License
