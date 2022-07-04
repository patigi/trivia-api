# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## UdaciTrivia REST API

Here is a list of all the possible API calls you can make:

#### Get Categories
----
  Returns json data for all categories.

* **URL**

  /categories

* **Method:**

  `GET`
  
* **URL Params**

  None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** 
    ```
    {
      "categories": {
        "1": "Science", 
        "2": "Art", 
        "3": "Geography", 
        "4": "History", 
        "5": "Entertainment", 
        "6": "Sports"
      }, 
      "success": true
    }
    ```

* **Sample Call:**

  ```javascript
    $.ajax({
      url: `/categories`,
      type: "GET",
      success: (result) => {
        this.setState({ categories: result.categories })
        return;
      },
      error: (error) => {
        alert('Unable to load categories. Please try your request again')
        return;
      }
    })
   }
  ```

#### Get Questions
----
  Returns json data including a list of questions, number of total questions, and categories.

* **URL**

  /questions?page=:page

* **Method:**

  `GET`
  
*  **URL Params**

   **Optional:**
 
   `page=[integer]`

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** 
    ```
    {
    "categories": {
      "1": "Science", 
      "2": "Art", 
      "3": "Geography", 
      "4": "History", 
      "5": "Entertainment", 
      "6": "Sports"
    }, 
    "questions": [
      {
        "answer": "Yes?", 
        "category": 1, 
        "difficulty": 1, 
        "id": 25, 
        "question": "Is this going to work?"
      }, 
      {
        "answer": "Blood", 
        "category": 1, 
        "difficulty": 4, 
        "id": 22, 
        "question": "Hematology is a branch of medicine involving the study of what?"
      }
    ],
     "success": true, 
    "total_questions": 18
    }
    
    ```
 
* **Error Response:**

  * **Code:** 404 NOT FOUND <br />
    **Content:**
    ```
    {
    "success": False,
    "message": "Resource not found"
    }
    ```
* **Sample Call:**

  ```javascript
    $.ajax({
      url: `/questions?page=${this.state.page}`, 
      type: "GET",
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          categories: result.categories,
          currentCategory: result.current_category })
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again')
        return;
      }
    })
    }
  ```

#### Delete Question
----
  Endpoint to DELETE a question based on id

* **URL**

  /questions/:id

* **Method:**

  `GET`
  
*  **URL Params**

   **Required:**
 
   `id=[integer]`

* **Data Params**

  None

* **Success Response:**

  * **Code:** 204 <br />
 
* **Error Response:**

  * **Code:** 422 UNPROCESSABLE <br />
    **Content:**
    ```
    {
    "success": False,
    "message": "Unprocessable"
    }
    ```
* **Sample Call:**

  ```javascript
    $.ajax({
      url: `/questions/${id}`, 
      type: "DELETE",
      success: (result) => {
        this.getQuestions();
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again')
        return;
      }
    })
  ```

**Create Question**
----
  Returns json data for newly created question

* **URL**

  /questions

* **Method:**

  `POST`
  
*  **URL Params**

  None

* **Data Params**

   **Required:**

  ```
  question=[String]
  answer=[String]
  category=[integer]
  difficulty=[integer]
  ```

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** 
    ```
    {
      'question': 'Is this a new question?', 
      'answer': 'Yes', 
      'difficulty': 1, 
      'category': 1, 
      'success': True
    }
    ```
 
* **Error Response:**

  * **Code:** 422 UNPROCESSABLE <br />
    **Content:**
    ```
    {
    "success": False,
    "message": "Unprocessable"
    }
    ```
    
* **Sample Call:**

  ```javascript
    $.ajax({
      url: '/questions',
      type: "POST",
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({
        question: this.state.question,
        answer: this.state.answer,
        difficulty: this.state.difficulty,
        category: this.state.category
      }),
      xhrFields: {
        withCredentials: true
      },
      crossDomain: true,
      success: (result) => {
        document.getElementById("add-question-form").reset();
        return;
      },
      error: (error) => {
        alert('Unable to add question. Please try your request again')
        return;
      }
    })
  ```

#### Search Questions
----
  Endpoint to POST search term and returns matching questions

* **URL**

  /search/questions

* **Method:**

  `POST`
  
*  **URL Params**

  None

* **Data Params**

  **Required:**
 
   `searchTerm=[String]`

* **Success Response:**

  * **Code:** 200 <br />
    **Response:**
    ```
    {
      'total_questions': 2, 
      'questions': [
        {
          'id': 5, 
          'question': "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?", 
          'answer': 'Maya Angelou', 
          'category': 4, 
          'difficulty': 2
        }, 
        {
          'id': 6, 
          'question': 'What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?', 
          'answer': 'Edward Scissorhands', 
          'category': 5, 
          'difficulty': 3
        }
      ], 
      'success': True
    }
    ```
 
* **Sample Call:**

  ```javascript
    $.ajax({
      url: `/search/questions`,
      type: "POST",
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({searchTerm: searchTerm}),
      xhrFields: {
        withCredentials: true
      },
      crossDomain: true,
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          currentCategory: result.current_category })
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again')
        return;
      }
    })
  ```

#### Get Question By Category
----
  Returns questions by category.

* **URL**

  /categories/:category_id/questions

* **Method:**

  `POST`
  
*  **URL Params**

   **Required:**

  `category_id: [integer]`

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** 
    ```
    {
      'success': True, 
      'current_category': 1, 
      'total_count': 2, 
      'questions': [
        {
          'id': 22, 
          'question': 'Hematology is a branch of medicine involving the study of what?', 
          'answer': 'Blood', 
          'category': 1, 
          'difficulty': 4
        }, 
        {
          'id': 25, 
          'question': 'Is this going to work?', 
          'answer': 'Yes', 
          'category': 1, 
          'difficulty': 1
        }
      ]
    }
    ```
 
* **Error Response:**

  * **Code:** 404 NOT FOUND <br />
    **Content:**
    ```
    {
    "success": False,
    "message": "Resource not found"
    }
    ```
    
* **Sample Call:**

  ```javascript
    $.ajax({
      url: `/categories/${id}/questions`,
      type: "GET",
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          currentCategory: result.current_category })
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again')
        return;
      }
    })
  ```

#### Get Quiz Questions
----
  Returns questions for quiz, by category if applicable.

* **URL**

  /quizzes

* **Method:**

  `POST`
  
*  **URL Params**

  None

* **Data Params**

   **Required:**
   
   `previous_questions: [List]`

   **Optional:**

  `quiz: [integer]`
  
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** 
    ```
    {
      'success': True, 
      'question': 
        {
          'id': 27, 
          'question': 'Is this a new question?', 
          'answer': 'Yes', 
          'category': 1, 
          'difficulty': 1
        }
     }
    ```
 
* **Error Response:**

  * **Code:** 404 NOT FOUND <br />
    **Content:**
    ```
    {
    "success": False,
    "message": "Resource not found"
    }
    ```
    
* **Sample Call:**

  ```javascript
    $.ajax({
      url: '/quizzes',
      type: "POST",
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({
        previous_questions: previousQuestions,
        quiz_category: this.state.quizCategory
      }),
      xhrFields: {
        withCredentials: true
      },
      crossDomain: true,
      success: (result) => {
        this.setState({
          showAnswer: false,
          previousQuestions: previousQuestions,
          currentQuestion: result.question,
          guess: '',
          forceEnd: result.question ? false : true
        })
        return;
      },
      error: (error) => {
        alert('Unable to load question. Please try your request again')
        return;
      }
    })
  ```

## Testing
To run the tests, run
```
./test_script.sh
```
