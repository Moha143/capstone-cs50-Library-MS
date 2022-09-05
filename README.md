# CS50W CAPSTONE PROJECT

A library management system is software that is designed to manage all the functions of a library. It helps librarian to maintain the database of new books and the books that are borrowed by members along with their due dates. It tracks the records of the number of books in the library, how many books are available, or how many books have been returned or late fine charges, etc.

# Structure

The web platform is structured as follows

- **apschedule:** Advanced Python Scheduler (APScheduler) is a Python library that lets you schedule your Python code to be executed later, either just once or periodically.
- **LMS:** The Library folder contains the main Django app.
- **Library:** This folder app handles the models and funtions relating to staffs and members.
- **media:** This folder are stored all images of the system.
- **statis:** This folder contains all css and js of the system.
- **Templates:** This folder handles html files.

# File Contents

## Front End:

- `static` - Holds all static files.

  - `static\bootstrap\css` - Holds all css files.
    - `static\bootstrap\css\fontawesome\` - Holds all fontawesome icons.
  - `static\bootstrap\js` - Holds some javascript files for the bootstrap.
  - `static\bootstrap\script` - Holds all javascript files that relate to the back-end of the system.
    - `static\bootstrap\script\account` - contains all files for staff and members.
      - `static\bootstrap\script\add-member.js` - javascript that allows to add new member.
      - `static\bootstrap\script\add-staff.js` - javascript that allows to add new staff.
      - `static\bootstrap\script\member-list.js` - javascript that allows to view member list and also can change staff information.
      - `static\bootstrap\script\staff-list.js` - javascript that allows to view/display staff list and also can change staff information.
