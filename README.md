
# Discord Moderation Bot - WORK IN PROGRESS
## Introduction
#### This Discord bot is designed to assist staff in moderating their Discord channels by creating tickets, updating their status, and performing various moderation tasks. The bot interacts with a MySQL database to store and retrieve information. Below is a guide on how to set up and use the bot effectively.

## Getting Started
#### Clone the repository to your local machine.
#### Install the required dependencies using the following command:


`pip install -r requirements.txt`

## Creating a Discord Bot

1.  **Create a Discord Account:** If you don't already have a Discord account, create one by visiting [Discord's website](https://discord.com/).
    
2.  **Access the Developer Portal:**
    
    -   Log in to your Discord account.
    -   Visit the Discord Developer Portal.
3.  **Create a New Application:**
    
    -   Click on the "New Application" button.
    -   Give your application a name. This name will be your bot's username.
4.  **Create a Bot User:**
    
    -   In the application settings, navigate to the "Bot" tab.
    -   Click on the "Add Bot" button. Confirm when prompted.
5.  **Retrieve Token:**
    
    -   In the "Bot" tab, under the "Token" section, click on "Copy" to copy the bot token.
    -   **Important:** Keep your bot token secure. Do not share it publicly.
6.  **Add the Bot to Your Server:**
    
    -   Still in the application settings, go to the "OAuth2" tab.
    -   In the "OAuth2 URL Generator" section, select the "bot" scope.
    -   Scroll down and choose the necessary permissions for your bot.
    -   Copy the generated URL and paste it in your browser. Follow the prompts to add the bot to a server.

Now, you have successfully created a Discord bot and added it to your server. You can use the bot token in your code to interact with the Discord API.

## Configuration
#### This Bot makes use of an SQL Database to store and fetch data. While it can be modified to store the information in a JSON file, I have found that utilizing a SQL Database can help it scale across many different machines utilizing the same Database. This ensures that the data matches regardless of what server it is in.

#### Before running the bot, make sure to configure the following variables in the code:

## Bot Token
#### Replace 'YOUR_TOKEN' with your actual Discord bot token.
```python
TOKEN = "your_bot_token_here"
```
## MySQL Database Credentials
#### Replace the following with your MySQL database credentials.

```python
DB_HOST = "your_database_host"
DB_USER = "your_database_user"
DB_PASSWORD = "your_database_password"
DB_NAME = "your_database_name"
```

## Running the Bot
#### Run the bot script using the following command:
```python
python bot.py
```

## Commands
### !Report
Initiate a report and answer a series of questions to log the report into the database. The report is then sent to a specified channel for further review.

### !Tickets
Fetch all open tickets from the database and display them in an embed message.

### !OpenTicket (Ticket Number)
Open a specific ticket by assigning it to the person running the command. Displays details of the ticket in an embed message.

### !CloseTicket (Ticket Number)
Close a specific ticket. Restricted to users with the 'Elder Owls' role.

### !AssignTicket (Ticket Number) <@mention>
Assign a specific ticket to a mentioned Discord member. Restricted to users with the "Admin" role.

### !delete_last_messages
Delete the last 20 messages in the channel. Restricted to users with the 'Elder Owls' role.

# Notes
The bot uses a MySQL database to store and retrieve information related to reports and tickets.
Make sure to customize the role names and channel IDs as per your Discord server configuration.
Review the code comments for additional information and customization options.

# Upcoming Features
Play Music through URL
Re-Open closed tickets
Search Tickets by User
Create dynamic values for "!Delete_Last_Messages" including a cooldown timer
Run Commands Regardless of Case-Sensitivity

# Contributors
### Alexander Carrillo (MXVI)

Feel free to contribute to the project by submitting issues or pull requests.
Thank you for using the Discord Moderation Bot! If you have any questions or encounter issues, feel free to reach out to the contributors.
