# Appreciative Inquiry Interactive Session Reports

A Flask webapp that reads data from [Appreciative Inquiry](https://en.wikipedia.org/wiki/Appreciative_inquiry) sessions from the user's Dropbox and presents it in an interactive form using imagery of a tree, where each part of the tree represents a particular phase of the Inquiry.

Space is also available for including photographs from the session, such as photos of Dreams craft projects.

A landing page contains links to all reports generated; these links are also at the bottom of each individual report.

### Demo
A working live demo is available [here](https://erogers.pythonanywhere.com/forest?tree=Demo%20Data).

### Setup
See the [Setup page in the wiki](https://github.com/esther-rogers/appreciative-inquiry-tree/wiki/Setup).

### Source data requirements
To avoid problems with reading data from excel files, please use the [provided template](https://github.com/esther-rogers/appreciative-inquiry-tree/blob/main/excel_template.xlsx) to enter your data.

This app assumes separate folders for each Appreciative Inquiry session, and uses the name of the folder (not the file!) to title each session. Session data should follow the structure of the included Excel template, with each phase of the session on separate worksheets. Raw data / observations are expected in column A, and their corresponding theme in column B. Themes with no observations are accepted; blank rows and observations without a theme will be ignored.

To include images in the report, place them in the folder for their corresponding session. These will be rendered at the bottom of the report.


### Languages
* Python 3.8
* [Jinja2](https://jinja.palletsprojects.com/en/2.11.x/) (a templating language for Python)
* html & css
* Javascript
