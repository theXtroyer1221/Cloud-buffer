[![Gitpod Ready-to-Code](https://img.shields.io/badge/Gitpod-Ready--to--Code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/theXtroyer1221/Cloud-buffer)

# Cloud-buffer

**Cloud buffer** is an webapp displaying a weather of the selected city by using open source api's that provide json data for use.
This data is later parsed and put on the website with using python Flask micro web framework.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install for the project and how to install them

```
python-dotenv
flask
requests
Google-Images-Search
flask_wtf
flask-simple-geoip
Flask-Bcrypt
Flask-SQLAlchemy
Flask-mail
Pillow
```

### Installing

A step by step series of examples that tell you how to get a development env running

You need to install all the python packages using pip. In the main directory, just run this command

```
pip install -r requirementx.txt
```

You might need to install another packages, please report the packages that the **requirement.txt** is missing

```
pip install [package]
```

To run the website fully okay, you need to acquire api-keys to the diffrent api's used in the program.

- [Openweather API](https://openweathermap.org/)
- [ipstack](https://ipstack.com/)
- [Google custom search](https://console.developers.google.com/projectselector2/apis/dashboard?pli=1&supportedpurview=project)
*This is an api for the image search, for more information about setting it up read here https://pypi.org/project/Google-Images-Search/*

### Running the project

Installing all the projects will make you able to run the project. Go to the main directory of the prject and run the **run.py** file

```
python run.py
```

*Be careful that the app is originally ran on debug mode one and development server. The app is also does run on host 0.0.0.0, to change that go and cange the run.py file. These settings are not recommended for production*

### Built With

- [Python](https://www.python.org/) - Programming language used 
- [Flask](https://flask.palletsprojects.com/en/1.1.x/) - The web framework used
- [Openweather API](https://openweathermap.org/) - The weather api used

## Contributing

Please read [CONTRIBUTING.md](https://github.com/theXtroyer1221/Cloud-buffer/blob/master/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

- **TheXtroyer1221** - _Initial work_ - [TheXtroyer github account](https://github.com/tgeXtroyer1221)

See also the list of [contributors](https://github.com/theXtroyer1221/Cloud-buffer/graphs/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

> Jad Alnabki / TheXtroyer1221
