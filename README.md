Zyhmantovich Mikita 22210475

Nikiforov Andrei 22211653

Title name: "Hi, Deggster!"

MyGit repository link: https://mygit.th-deg.de/mz02475/sas-project.git
# Project description
**Hi, Deggster!**  is a domain specific chat-bot, that helps international exchange students to find information about their first steps in THD! To know more about the project, please, visit our [wiki](https://mygit.th-deg.de/mz02475/sas-project/-/wikis/home)

# Instalation

## Prerequisites

Before you begin, ensure you have the following prerequisites installed on your system:

- Python >= 3.6 and <= 3.10 
- pip (Python package installer)
- Virtualenv (optional but recommended)
- Python and git should be added to PATH

## Step 1: Clone Repository

Clone repository to your local machine using the following command:

```bash
git clone https://mygit.th-deg.de/mz02475/sas-project.git
cd sas-project
```

## Step 2: Create a Virtual Environment (Optional)

Creating a virtual environment is a good practice to isolate your project dependencies. To create a virtual environment, run the following commands:

```bash
# Install virtualenv
pip install virtualenv

# Create a virtual environment
virtualenv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate

# On Linux/macOS
source venv/bin/activate
```

## Step 3: Install Rasa Open Source and Dependencies

Install Rasa Open Source and its dependencies using the following command:

```bash
pip install -r requirements.txt
```


## Step 4: Train Your Rasa Model

Train your Rasa model using the following command:

```bash
rasa train
```

This will train the NLU (Natural Language Understanding) and Core models based on the data provided in the `data` directory.

## Step 5: Run the Rasa Action Server

Start the Rasa action server to handle custom actions:

```bash
cd actions
rasa run actions
```

This command will start the custom action server that executes the actions defined in your `actions.py` file.

## Step 6: Run the Flask Server

Start the Flask server to send messages to the bot and receive answers:

```bash
cd ..
cd webserver
python app.py
```

This assumes you have a Flask application (e.g., `app.py`) that handles user inputs and communicates with the Rasa bot.

## Step 7: Interact with Bot

You can now interact with bot via console using following command:
```bash
cd.. # if you are in webserver folder
rasa shell # you must be in sas-project folder to run this
```
To stop the chat use:
```bash
/stop
```
## Additional Step : Interact with Bot hi_deggster.py or webserver
You can also interact with your Rasa bot by executing hi_deggster.py or sending messages to the Flask server. Use curl or postman to issue POST request on `http://localhost:5000/bot`:
```bash
curl -X POST -H "Content-Type: application/json" -d '{"message": "Your message here"}' http://localhost:5000/bot
```

## Additional Resources

- [Rasa Documentation](https://rasa.com/docs/)
- [Rasa Community Forum](https://forum.rasa.com/)

# Basic usage
## Dialogue start
To start the dialogue simply greet the bot. For example say "Hi, Deggster!". Depending on what you are using to communicate, either requests to localserver or console, send a message to the bot appropriately.
## Dialogue flow
After greeting the bot, it will guide you through every step towards the information you want to know.
## Use cases
You can ask bot about:
 

 - student reviews 
 - exchange cource choice 
 - application information  
 - language courses
 - orientation week

## Notes
Sometimes, if key-words are written badly by user, bot can misunderstand it and will ask user to repeat their request without mistakes in key-words

Unhappy paths were implemented using form validation and fallback mechanism
## Help
If you are lost, you can ask bot for help. It will list the options to choose from to proceed.
# Implementation of requests

### Personas
We have created 1 system persona and 3 user personas

### Use cases
We have made 5 critical use cases, use case diagram and also added unhappy cases 

### Example dialogs
We came up with 10 example dialogs and also a couple unhappy paths

### Rasa Implementation
we have created:

- 15 intents(nlu.yml)
- 11 custom actions(actions.py)
- 15 rules(rules.yml)
- 9 entities(domain.yml)
- 9 slots(domain.yml)
- 9 look-up tables(nlu.yml)
- 4 forms(domain.yml)
- two step fallback mechanism
- JSON database for answers(database.json)

We used forms to achieve the best dialogue flow and specify information needed by user by asking questions with increasing specificity. Look-up tables were created to ensure better entity spotting. Two step fallback mechanism ensures the proper continuation of dialogue even if the user intent was not recognized

Validate actions in actions.py were used to validate the values in slots for form filling. If the slot is not correctly filled, bot asks the user to try again

Custom actions were used to provide the flexibility in answer choices and to retrieve information from JSON database

We have created a simple REST-API that allows user to interact with bot using POST request to local server. 

# Work done
Andrei Nikiforov:
- Personas
- Example dialogs
- Implementation yml-files (domain, nlu)

Mikita Zyhmantovich:
- Use cases
- Dialog flow
- Implementation yml-files (stories, rules)

Both: Rasa Implementation(actions.py, forms, fallback, pipeline, Flask server)

We helped each other during the whole project with our respective parts, discussed Implementation and implemented it together. 
