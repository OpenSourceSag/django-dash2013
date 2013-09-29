Django Dash 2013 (OpenSourceSag)
============

This application allows you to create and manage your project in a SCRUM way.

Installation
------------
1. To set up the environment, you need to run the command:
python manage.py install your_username your_email

With these two parameters ('your_username' and 'your_email') a manager account will be created (you'll be ask for a password during the process).


2. You can launch the server with this command:
python manage.py runserver 127.0.0.1 --setting agile_board.settings.local


3. You can now login to our interface by going to the address:
127.0.0.1


How to use it ?
----------------
1. Log in to our interface

2. You are on the Project list page. You can add a new project with the '+'

3. You are now on your new project page. 
   The first field is the project name and the second one is it description.
   You can add stories easily with the field '___________' bellow 'Stories'. To add or update a story or a task, press Enter or Tab	
   You can add tasks to a story by selecting a story first. The task will be associated with the selected story.
   To add a sprint, just click on the '+' next to it. To add task to a sprint, just drag and drop a task by clicking on the '*' next to it.
   Just click on a sprint to show the associated tasks.
   
4. You can now return to the main page with the link 'Back to project list' and you can see your project. The whiteboard button will redirect you to your project page.
   If you created a sprint, you can click on the sprint button, you'll be redirected to the sprint page.
   Here you can see all the sprint's task and easily change their status by drag and drop them.

   

Team members
------------

- Alexandre Lessard
- Franck Coiffier
- Frédérique Boulay
