# TourRadar - Cloud Data Engineer Test Case

## Introduction
Please see below the following three sample business problems for the role of Cloud Data Engineer at TourRadar. The purpose of these tasks is for us to get a more rigorous preliminary assessment of your approach to problem solving, technical capabilities and communication skills.

The exercises should take no more than a couple of hours each as we are just looking to understand how would you resolve these problems and how would you communicate your solution. We are not looking for a rigorous and comprehensive white paper into every consideration of these problems. You are welcome to use any tools you’d like, but we would ask you to send us the solutions for these problems in one of the widely used formats, so we don’t need to install or run any specific tools to check the results.

For each exercise, we have provided you with a problem and would ask that you perform the appropriate analytical and/or technical tasks on them in order to arrive at your solution.

## Output

We are interested in seeing three outputs from your work:

1. An explanation of your approach
    * Any initial/high-level observations of the problem that we’ve shared
    * Which problem-solving methods have you considered applying and why
2. Any code (eg. SQL, PHP, Python, etc.) that you’ve used in processing/analysing the
problem
3. Final output
4. Your next steps if you had more time and resources (different ways to solve the problem,
more time, more data, etc.)

## Challenge #1: MySQL Requests

We have provided you with a MySQL database dump [​dump.zip​](https://drive.google.com/file/d/1L4BX84yEK_au3CGauTcRsdfqcTSsJ2FU/view?usp=sharing) of fabricated data, which contains approximately 300,000 employee records with 2.8 million salary entries. The data was originally taken from ​[this project​](https://github.com/datacharmer/test_db), but we highly recommend that you use the dump file provided.

We would like you to write two SQL queries to uncover the following:

1. The name of the employee with the highest salary on ​March 15, 1998​ whose position on
that day was ​Senior Engineer​.
2. Find all employees who simultaneously satisfy all conditions:
    1. started working in the company as an ​Engineer
    2. whose ​highest salary​ at the peak of their career (be careful - it’s not necessarily
the latest salary) was at least twice as high as the ​lowest salary​ (again, it’s not
necessarily their first salary)
    3. who’s ​highest salary​ doesn’t exceed 80,000.

## Challenge #2: ETL Pipeline Design

### Find the Busiest Airport in Europe!

#### Data Source :
The OpenSky Network API lets you retrieve live & historical airspace information for research and non-commerical purposes.
Link : https://openskynetwork.github.io/opensky-api/

Note: You won't need to create an account since certain APIs are public and do not require credentials

#### Busiest Airport Specification :

 - Airport with the **highest number of departures** from 1st Sep 2019 12 AM till 14th Sep 2019 12 AM
 - Retrieve data only for below 3 airports
	 1. Heathrow Airport , London
	 2. Charles de Gaulle Airport, Paris
	 3. Amsterdam Airport Schiphol, Amsterdam

#### Requirements :
1. Create a data pipeline in Python to extract data via the Rest API from OpenSky network and store it into a MySQL table
2. The MySQL table should atleast store
	- Flight ICAO 24 number
	- Flight Departure Date
	- Flight Departure Time
	- Source Airport Code
	- Destination Airport Code
3.  The Solution should be an end-to-end MVP solution that can be easily extended for any future modifications/enhancements

Please provide us the Python script/modules and the name of the identified busiest airport as a solution

## When is this test case due?
You should submit the solution to this testcase within 72 hours.

## How to ask questions?
Is there something ambiguous in the test case? Some of the ambiguity has been intentionally left in there to give room to your creativity.

If there is a question that appears to be a blocker, please head over to issues and create a New Issue. Make sure to assign the newly created issue to one of the available options (except tourradar-testcases). Being explicit in your question will help us provide better and more contextual answers.

## How to submit?
- Create a new branch in this repository.
- Add your solution in a subdirectory; say *solution* in that branch.
- Push the branch to this repository.
- Create a new Pull Request for your branch against `master`.

## How does the review process happen?
- One or more TourRadar Senior Engineers will go through your solution and leave their feedback.
In most cases this happens within 2 business days of the submission. If you do not hear anything back from
reviewers in 72 hours please reach out to your contact in our recruiter team.
- Based on our evaluation of your solution, a decision will be made about whether to advance you in the progress.
- Once the solution has been reviewed and evaluated, our Recruiting team will get back to you with next steps.
