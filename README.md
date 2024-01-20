# Discord Moderation Bot
## Introduction
###### This Discord bot is designed to assist staff in moderating their Discord channels by creating tickets, updating their status, and performing various moderation tasks. The bot interacts with a MySQL database to store and retrieve information. Below is a guide on how to set up and use the bot effectively.

## Getting Started
###### Clone the repository to your local machine.
###### Install the required dependencies using the following command:

`pip install -r requirements.txt`

## Configuration
#### This Bot makes use of an SQL Database to store and fetch data. While it can be modified to store the information in a JSON file, I have found that utilizing a SQL Database can help it scale across many different machines utilizing the same Database. This ensures that the data matches regardless of what server it is in.

#### Before running the bot, make sure to configure the following variables in the code:

## Bot Token
###### Replace 'YOUR_TOKEN' with your actual Discord bot token.
`TOKEN = "your_bot_token_here"`

## MySQL Database Credentials
###### Replace the following with your MySQL database credentials.

```python
DB_HOST = "your_database_host"
DB_USER = "your_database_user"
DB_PASSWORD = "your_database_password"
DB_NAME = "your_database_name"
```

## Running the Bot
###### Run the bot script using the following command:

`python bot.py`


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
#####Play Music through URL
#####Re-Open closed tickets
#####Search Tickets by User

# Contributors
### Alexander Carrillo (MXVI)

##### Feel free to contribute to the project by submitting issues or pull requests.
#####Thank you for using the Discord Moderation Bot! If you have any questions or encounter issues, feel free to reach out to the contributors.
