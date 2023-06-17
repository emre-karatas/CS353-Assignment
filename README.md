# Project Grade: A+ (96)

## Project: Todo-list Web Application

### Overview

In this project, you are tasked with crafting an elegant and efficient web application utilizing Python, Flask, MySQL, and Docker Compose. This will not be just any application, but a comprehensive, feature-rich Todo-list application that serves to manage tasks under varying categories such as health, employment, lifestyle, family, and hobbies.

### Key Features 

#### Task Management
Each task will be time-bound, marked with a deadline, and will provide options to denote completion ("Done"). Users will have the flexibility to edit and delete tasks as they see fit. 

#### User Registration & Authentication
The application will feature a dedicated registration page where new users can create an account. Registered users can then log in through the login page by providing their unique username and password. 

#### User Dashboard
Upon successful login, the main page will greet the user with their tasks, sorted according to the proximity of their deadlines. The completed tasks will also find a special mention on this page, ordered by their completion time. Here, users can add, delete, modify, and mark tasks as finished.

### Database Schema
Below is a suggested database schema for the application. You are required to set up the primary and foreign keys yourself. A `schema.sql` file should encapsulate this information:

- **User** `(id:int, password:varchar, username:varchar, email:varchar)`
- **Task** `(id:int, title:varchar, description:text, status:varchar, deadline:datetime, creation_time:datetime, done_time: datetime, user_id: int, task_type:varchar)`
- **TaskType** `(type: varchar)`

Initially populate the database using these tables in your `schema.sql`.

### Analysis Page
From the main page, users should have the ability to access an "Analysis" page, presenting insightful statistics about their task history. 

Ensure to derive these insights using SQL queries and not Python logic. This page will present the following analytics:

1. Display the title and latency of the tasks completed after their deadlines.
2. Compute and display the user's average task completion time.
3. Enumerate the number of completed tasks per task type, in descending order.
4. Show the title and deadline of uncompleted tasks in ascending order of their deadlines.
5. Showcase the title and task completion time of the top two completed tasks that took the most time, in descending order (Use the LIMIT clause).

### User Logout
Finally, ensure to implement a secure and effective user logout function.

This project presents an opportunity for you to showcase your ability to develop a full-fledged web application. It will challenge and thereby refine your skills in Python, Flask, MySQL, and Docker Compose, all while building something functional and meaningful. Enjoy your coding journey!
