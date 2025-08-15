# Online-Voting-System
**Overview**

Online Poll is a Django-based web application designed to conduct secure, web-based elections. It allows voters to register, log in, and cast their vote for a candidate. The system includes an admin interface for managing polls, candidates, and voters, as well as modules for result calculation and voting conduct.

**Features**

**Admin Login:** Managed by the authority, with full rights to approve candidates, verify documents, remove faulty accounts, and oversee polls.

**Voter Registration & Login:** Generates unique IDs and passwords for voters, allowing them to vote only once per poll.

**Candidate Login:** Candidates can create profiles, upload background details, and track their participation.

**View Candidate Details:** Voters can view profiles and past achievements before voting.

**Result Calculation Module:** Computes and displays the results.

**Voting Conduction Module:** Manages the active voting process.

**System-Generated Credentials:** Automated creation of secure credentials for both candidates and voters.

**Technology Stack**

**Backend:** Python 3.x, Django Framework (MVT pattern)

**Frontend:** Django Templates, HTML/CSS

**Database:** SQLite3 (default with Django)

**Tools:** Visual Studio Code (or any preferred code editor)

**Prerequisites**

Basic knowledge of Python and Django

Python 3.x installed

Django installed (pip install django)

SQLite3 (bundled with Django)

Code editor such as VS Code

**Installation & Setup**

**Clone the repository**

git clone https://github.com/<your-username>/Online-Poll.git

cd Online-Poll

**Create and activate a virtual environment**

python -m venv venv

venv\Scripts\activate   # On Windows

source venv/bin/activate  # On macOS/Linux

**Install dependencies**

pip install -r requirements.txt

**Run migrations**

python manage.py migrate

**Create a superuser (for admin access)**

python manage.py createsuperuser

**Start the development server**

python manage.py runserver

**Access the application**

Voter/Candidate Portal: http://localhost:8000

Admin Dashboard: http://localhost:8000/admin

**Usage**

Admin logs in to create elections, approve candidates, and manage voters.

Voters register, log in, and cast their votes.

Candidates upload their profiles and election details.

System automatically calculates and displays results after voting ends.
