# bulk-email-validation-using-mailgun-and-python

Bulk Email Validation Using Mailgun and Python

# Instructions to Start the Django Project

[Refer this site](https://www.django-rest-framework.org/tutorial/quickstart/) for more information on how to get quickly started with a Django REST Framework application used in this tutorial. 

Given below is a quick set of instructions to interact with the Django application bundled with this tutorial.

1. From the Project Directory: **Run Migrations:**
    ```sh
    python manage.py migrate
    ```

2. **Start the Development Server:**
    ```sh
    python manage.py runserver
    ```

3. **Access the Application:**
    Open your web browser and go to `http://localhost:8000/` to access the Django application. 
    
4. Access the endpoints defined in the Django application to perform job sumbission and job status check actions:

* [Submit Job](http://localhost:8000/api/validation/job/submit)
* [Check Job Status](http://localhost:8000/api/validation/job/status)

