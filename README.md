

# Instalation

## Prerequisites

Before you begin, ensure you have the following prerequisites installed on your system:

- Python 3.6 or higher
- pip (Python package installer)
- Virtualenv (optional but recommended)

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
rasa run actions
```

This command will start the custom action server that executes the actions defined in your `actions.py` file.

## Step 6: Run the Flask Server

Start the Flask server to send messages to the bot and receive answers:

```bash
cd webserver
python app.py
```

This assumes you have a Flask application (e.g., `app.py`) that handles user inputs and communicates with the Rasa bot.

## Step 7: Interact with Bot

You can now interact with your Rasa bot by sending messages to the Flask server. Use curl or postman to issue POST request on `http://localhost:5002/api`:
```bash
curl -X POST -H "Content-Type: application/json" -d '{"message": "Your message here"}' http://localhost:5002/api
```

## Additional Step : Interact with Bot via console

You can also interact with bot via console using following command:
```bash
rasa shell
```

## Additional Resources

- [Rasa Documentation](https://rasa.com/docs/)
- [Rasa Community Forum](https://forum.rasa.com/)
