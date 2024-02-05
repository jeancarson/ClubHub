# ClubHub
ClubHub is a dynamic and user-friendly web application designed to streamline the management of
sports clubs. 

This project aims to create a seamless experience for both students and
coordinators in organizing and participating in various sports clubs and events.

## How to run the application

>1. Navigate to an appropriate directory and clone the GitHub repository.
>   ```commandline
>   cd projects
>   git clone https://github.com/darragh0/ClubHub.git
>   ``` 
>2. Navigate to the `ClubHub` folder and create a virtual environment.
>   ```commandline
>   cd ClubHub
>   python -m venv .venv
>   ```
>3. Activate the virtual environment you just created.
>   ```
>   .venv/Scripts/activate
>   ```
>       Assuming you are on windows, the previous commands should work in a standard ``cmd.exe`` command shell. If they do not work, or if you are on a different platform, refer to Python's [Virtual Environment Documentation](https://docs.python.org/3/library/venv.html).<br><br>
> 4. Install the requirements listed in ``requirements.txt``.
>   ```commandline
>   pip install -r requirements.txt
>   ```
>5. Finally, use the following command to run the Flask application.
>   ```commandline
>   flask run
>   ```
>6. You should see an output similar to the following:
>   <pre lang="">
>    * Serving Flask app 'app'
>    * Debug mode: off
>   <span style="color: #db4f4f; font-weight: bold;">WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.</span>
>    * Running on <a>http://127.0.0.1:5000</a>
>   <span style="color: #cfcf63;">Press CTRL+C to quit</span>
>   </pre>