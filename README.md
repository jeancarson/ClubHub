# ClubHub
ClubHub is a dynamic and user-friendly web application designed to streamline the management of
sports clubs. 

This project aims to create a seamless experience for both students and
coordinators in organizing and participating in various sports clubs and events.

---

## How to run the application
Before following the steps below, ensure you have the latest version of Python installed
(We recommend Python 3.12.2 or higher).<br />
Follow [Python's Installation Guide](https://www.python.org/downloads) to download
the latest version for your platform.

&nbsp;<br />

>1. Navigate to an appropriate directory and clone the GitHub repository.
>   ```
>   cd projects
>   git clone https://github.com/darragh0/ClubHub.git
>   ``` 
>2. Navigate to the `app` folder within the `ClubHub` directory and create a virtual environment.<br />
>   This folder contains everything needed for the app to run.
>   ```
>   cd ClubHub/app
>   python -m venv .venv
>   ```
>3. Activate the virtual environment you just created.
>   ```
>   .venv/Scripts/activate
>   ```
>4. Install the requirements listed in `requirements.txt`.
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
>7. To view the web application, click the link in the output.

&nbsp;<br />
Assuming you are on windows, the commands above should work in a standard ``cmd.exe`` command shell.
If they do not work, or if you are on a different platform, refer to Python's [Virtual Environment Documentation](https://docs.python.org/3/library/venv.html).<br><br>

> **_NOTE:_** If you do not follow the steps exactly as described, the application may not run properly.
