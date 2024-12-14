# Django Quiz App

A simple web application built with Django that allows users to take a quiz, submit answers, and view their results. The app uses MongoDB for storing questions and answers.

## Features

- **Start Quiz**: Randomized questions presented one at a time.
- **Submit Answers**: Users can select answers, and the app checks for correctness.
- **Quiz Summary**: After completing the quiz, a summary of correct and incorrect answers is displayed.
- **Smooth Transitions**: The app has smooth transitions between questions.
- **MongoDB**: MongoDB Atlas is used for storing questions, options, and answers.

## Requirements

Before running this app locally, please make sure you have the following installed:

- Python 3.8+ 
- MongoDB (or MongoDB Atlas for remote storage)

## Setup Instructions

### Step 1: Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/Shorya-Dixit/Django_Quiz_App.git
cd my-django-project
```

### Step 2: Create a Virtual Environment (Recommended)

It’s recommended to use a virtual environment to manage dependencies. You can skip this step if you already have one set up, but it’s best practice to use isolated environments for each project.

#### Create a Virtual Environment:

**On Windows:**

```bash
python -m venv env
```

**On macOS/Linux:**

```bash
python3 -m venv env
```

#### Activate the Virtual Environment:

**On Windows:**

```bash
.\env\Scripts\activate
```

**On macOS/Linux:**

```bash
source env/bin/activate
```

### Step 3: Install Dependencies

Once the virtual environment is activated, install the required Python packages:

```bash
pip install -r requirements.txt
```

This will install all the necessary dependencies for your Django app.

### Step 4: Set Up MongoDB

Ensure that you have a MongoDB instance running. You can use MongoDB Atlas (a cloud service) or run a local MongoDB instance.

1. If you're using MongoDB Atlas, create a cluster and get the connection string.
2. Update your `settings.py` file to include your MongoDB connection string under `DATABASES`.

Example:

```python
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'quizdb',
        'CLIENT': {
            'host': 'your_mongodb_connection_string'
        }
    }
}
```

### Step 5: Migrate Database

Once MongoDB is set up, run the following command to apply migrations:

```bash
python manage.py migrate
```

This will set up the necessary tables (if needed) in MongoDB.

### Step 6: Run the Development Server

Run the development server to start the app locally:

```bash
python manage.py runserver
```

This will start the Django development server on [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

You should now be able to open your browser and access the app locally.

## How to Use the Quiz

1. **Home Page**: Click the "Start Quiz" button to begin the quiz.
2. **Answer Questions**: Select an option for each question.
3. **Submit Answer**: After each question, submit your answer, and the app will show whether it's correct or incorrect.
4. **Next Question**: Click "Next Question" to proceed to the next one.
5. **Quiz Summary**: After finishing the quiz, a summary will show how many questions you answered correctly and incorrectly.


## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push to your fork (`git push origin feature-name`).
5. Create a new pull request.
