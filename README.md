Introduction
In this assignment, you will implement a web application using Python, Flask, MySQL, and Docker Compose. The web application you will develop is a generic Todo-list application where users can manage their todo list.

Description
In this web application, the user can create tasks in different categories such as health, job, lifestyle, family, hobbies. The tasks need to have a deadline. The user can finish the task by marking the task as Done. The user can also delete or edit the task. You should provide a user registration page. Upon registration, the users can login via the login page by providing their username and password. After successful login, in the main page, you list the tasks of the user sorted by their deadline (the topmost should be the one with the closest deadline). You also show the completed tasks separately in this page, sorted by their completion time. In this page, allow the user to add a task, delete a task, edit a task, and finish a task. The following is an example database schema you can use to create the application. You should setup the primary and foreign keys yourself. You will create a file called the schema.sql.
• User (id:int, password:varchar, username:varchar, email:varchar)
• Task (id:int, title:varchar, description:text, status:varchar, deadline:datetime, creation_time:datetime, done_time: datetime, user_id: int, task_type:varchar)
• TaskType (type: varchar)
In the schema.sql, use the following tables to initially populate the database.

You should also create an analysis page that could be reached from the main page, that lists various statistics about the task history of the user. You should use SQL queries (i.e., not python logic) to solve the following (query results will form the analysis page).
1. List the title and latency of the tasks that were completed after their deadlines (for the user).
2. Give the average task completion time of the user.
3. List the number of the completed tasks per task type, in descending order (for the user).
4. List the title and deadline of uncompleted tasks in increasing order of deadlines (for the user).
5. List the title and task completion time of the top 2 completed tasks that took the most time, in descending order (for the user). (You can use the LIMIT clause).
Finally, implement the logout function.
