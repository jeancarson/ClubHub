# ClubHub
ClubHub is a dynamic and user-friendly web application designed to streamline the management of
sports clubs. 

This project aims to create a seamless experience for both students and
coordinators in organizing and participating in various sports clubs and events.
<br />

## How to run the application
Before following the steps below, ensure you have the latest version of Python installed
(Python 3.12.2 or higher).
 
Follow [Python's Installation Guide](https://www.python.org/downloads) to download
the latest version for your platform.
<br />

>1. Navigate to an appropriate directory and clone the GitHub repository.
>   ```
>   cd projects
>   git clone https://github.com/darragh0/ClubHub.git
>   ``` 
>2. Navigate to the `ClubHub` folder and create a virtual environment.
>   ```
>   cd ClubHub
>   python -m venv .venv
>   ```
>3. Activate the virtual environment you just created.
>   ```
>   .venv/Scripts/activate
>   ```
>4. Install the requirements listed in ``requirements.txt``.
>   ```
>   pip install -r requirements.txt
>   ```
>5. Finally, use the following command to run the Flask application.
>   ```
>   flask run
>   ```
>6. You should see an output similar to the following:
>   <pre>
>    * Serving Flask app 'app'
>    * Debug mode: off
>   WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
>    * Running on <a>http://127.0.0.1:5000</a>
>   Press CTRL+C to quit
>   </pre>
>7. To see the website, click the link in the output.
<br />

Assuming you are on windows, the commands above should work in a standard ``cmd.exe`` command shell.
If they do not work, or if you are on a different platform, refer to Python's [Virtual Environment Documentation](https://docs.python.org/3/library/venv.html).<br><br>
