# Appreciative Inquiry Interactive Session Reports

A Flask webapp that reads data from Appreciative Inquiry sessions from the user's Dropbox and presents it in an interactive form using imagery of a tree, where each part of the tree represents a particular phase of the Inquiry.

Space is also available for including photographs from the session, such as photos of Dreams craft projects.

A landing page contains links to all reports generated; these links are also at the bottom of each individual report.

### Demo
A working live demo is available [here](https://erogers.pythonanywhere.com/forest?tree=Demo%20Data).

### Usage
OAuth functionality does not presently exist; you will need to [create an App](https://www.dropbox.com/developers/) within Dropbox and generate a token, which should be added to line 9 in flask_app.py.

### Source data requirements
This app assumes separate folders for each Appreciative Inquiry session, and uses the name of the folder (not the file!) to title each session. Session data should follow the structure of the included Excel template, with each phase of the session on separate worksheets. Raw data / observations are expected in column A, and their corresponding theme in column B. Themes with no observations are accepted; blank rows and observations without a theme will be ignored.

To include images in the report, place them in the folder for their corresponding session. These will be rendered at the bottom of the report.


### Languages
* Python 3.8 (extraction and transformation of data)
* [Jinja2](https://jinja.palletsprojects.com/en/2.11.x/) (a templating language for Python, used to insert data into html templates)
* html & css
* Javascript (very basic interactivity)

