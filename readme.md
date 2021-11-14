# Algeo02-20016 - Web-based Image Compression using SVD Algorithm

<!-- ## Table of Contents
* [General Info](#general-information)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Screenshots](#screenshots)
* [Setup](#setup)
* [Usage](#usage)
* [Project Status](#project-status)
* [Room for Improvement](#room-for-improvement)
* [Acknowledgements](#acknowledgements)
* [Contact](#contact)
* [License](#license) -->


## General Information
A simple image compression website utilizing the Singular Value Decomposition algorithm of matrices.
Contributors:
- 13520016 Gagas Praharsa Bahar
- 13520045 Addin Nabilal Huda
- 135200101 Aira Thalca Avila Putra


## Technologies Used
- React
- Flask
- Numpy, Pillow


## Features
- Upload your desired photo and enter your compression coefficient
- Download your compressed photo


## Structure
```bash
│   readme.md
│
├───doc
│       Tugas Besar 2 IF2123 Aljabar Linier dan Geometri.pdf
│
├───src
│   │   .gitignore
│   │   package.json
│   │   README.md
│   │   yarn.lock
│   │
│   ├───backend
│   │       .flaskenv
│   │       app.py
│   │       compress.py
│   │       logging.conf
│   │       requirements.txt
│   │
│   ├───public
│   │       favicon.ico
│   │       index.html
│   │       logo192.png
│   │       logo512.png
│   │       manifest.json
│   │       robots.txt
│   │
│   └───src
│       │   App.css
│       │   App.js
│       │   App.test.js
│       │   index.css
│       │   index.js
│       │   logo.svg
│       │   reportWebVitals.js
│       │   setupTests.js
│       │
│       └───components
│               FileUpload.jsx
│
└───test
        1095253.jpg
        55b.png
        Cat03.jpg
        instagram.png
        pexels-jack-hawley-57905.jpg

```


## How to run?
(LOCAL)
1. (First use only): Clone this repository, then change directory to app. `cd app`
2. Install the required node dependencies using `yarn install`
3. Start the front-end part using `yarn start`
4. Install the python virtualenv (for windows):
`cd backend`<br/>
`python -m venv venv`<br/>
`venv\Scripts\activate`
5. Install the required python dependencies using `pip install -r requirements.txt`
6. Start the back-end part using `yarn start-backend`
7. Access on your default browser port in react (usually its localhost:3000)



## Acknowledgements

- Thanks to Allah SWT
- Thanks to Mr. Rinaldi Munir, Mr. Jodhi, Mr. Rila as our lecturers
- Thanks to Teaching Assistants
- Thanks to Spotify, Coffee, and Instant Mie


## Contact
Created by Algeo>Alstrukdat Group.
2021

