[![Build Status][build-shield]][build-url]
[![Contributors][contributors-shield]][contributors-url]
[![MIT License][license-shield]][license-url]

<!-- PROJECT LOGO -->
<br />
<div>
  <div align="center">
    <h1 style="font-weight: bold">MovieDB</h1>
    <a href="https://github.com/helloitsm3/ICT2103-Team-8">
        <img src="./static/popcorn.svg" alt="Logo" width="200" height="auto">
    </a>
    <p align="center" style="margin-top: 30px">
        A web application written in Flask to keep track of user activity as well as to recommend movies based on their watch list.
        <br />
        <a href="https://github.com/helloitsm3/ICT2103-Team-8"><strong>Explore the docs »</strong></a>
        <br />
        <a href="https://github.com/helloitsm3/ICT2103-Team-8">View Demo</a>
        ·
        <a href="https://github.com/helloitsm3/ICT2103-Team-8/issues">Report Bug</a>
        ·
        <a href="https://github.com/helloitsm3/ICT2103-Team-8/issues">Request Feature</a>
    </p>
  </div>
</div>

<!-- TABLE OF CONTENTS -->

## Table of Contents

- [About the Project](#about-the-project)
  - [Built With](#built-with)
  - [Project Summary](#project-summary)
- [Getting Started](#getting-started)
  - [Installation](#installation)
- [License](#license)
- [Acknowledgements](#acknowledgements)
- [Contributions](#contributions)

<!-- ABOUT THE PROJECT -->

<h2 align="center"> About The Project </h2>

The overall objective of this course project is to design and develop a database application using real-life data, in line with Singapore's Smart Nation movement. The application that you develop should consist of a graphical interface as the front-end and a database management system (DBMS) as the backend.

### Built With

- [Python](https://www.python.org/)
- [Psycopg2](https://www.psycopg.org/docs/)
- [Chart.js](https://www.chartjs.org/)
- [Flask](https://flask.palletsprojects.com/en/1.1.x/)
- [Visual Studio Code](https://code.visualstudio.com/)

<!-- GETTING STARTED -->

### Project Summary

```sh
Framework
    - Python with flask
    - PostgreSQL / MongoDB
    - https://github.com/helloitsm3/ICT2103-Team-8

Movie Dataset
    - crawling of "now showing" dataset
    - old_idea of using static dataset:
        https://www.kaggle.com/rounakbanik/the-movies-dataset?select=ratings.csv

Ideas
    - https://letterboxd.com/
    - timeout to live dataset (24hrs fetch once)
    - can track activities of users

19 Sep TASK BREAKDOWN

1. Data crawling (Ian)
2. CSV Reader / Writer
3. Login / Registration system
4. Database connection
5. upload inital static dataset
6. Web design

- Sign in / out page
- Home page
- Profile page
- update profile page
- Analytics page
- Movie details page (Full / analytics data)
```

## Getting Started

This is an example of how you can set up your project locally. To get a local copy up and running follow these simple example steps.

### Installation

1. Clone the repo

```sh
git clone with HTTPS https://github.com/helloitsm3/ICT2103-Team-8.git
git clone with SSH   git@github.com:helloitsm3/ICT2103-Team-8.git
```

2. Install the necessary libraries

```sh
# This creates a virtual environment so that when you install the libraries
# it's only isolated to this environment
1. python -m venv venv (optional)
    # This is to activate the virtual environment you just downloaded
    - venv\Scripts\activate

# This installs all the require libraries needed for this project
2. pip install -r requirements.txt

# Sets the main.py file as the main app for flask
3. set FLASK_APP=main.py

# Sets the project environment to development so that the project will refresh upon
# changes to the code without needing to restart the server
4. set FLASK_ENV=development

# Runs the flask project
5. flask run
```

<!-- LICENSE -->

## License

Distributed under the MIT License. See `LICENSE` for more information.

<!-- Acknowledgements -->

## Acknowledgements

- [Img Shields](https://shields.io)
- [Choose an Open Source License](https://choosealicense.com)

<!-- Contributions -->

## Contributions

- Sean Leng
- Ian
- Alex Lee
- Joel Wee
- Clement Ang
- Chiu Jing Xiong

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[build-shield]: https://img.shields.io/badge/build-passing-brightgreen.svg?style=flat-square
[build-url]: #
[contributors-shield]: https://img.shields.io/badge/contributors-1-orange.svg?style=flat-square
[contributors-url]: https://github.com/helloitsm3/ict2x01/graphs/contributors
[license-shield]: https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square
[license-url]: https://choosealicense.com/licenses/mit
