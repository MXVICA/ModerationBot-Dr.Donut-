import discord
from discord.ext import commands
import mysql.connector
import random
import requests
import openai
import os

# Replace 'YOUR_TOKEN' with your actual bot token
TOKEN = "your_bot_token_here"

# Replace the following with your MySQL database credentials
DB_HOST = "your_database_host"
DB_USER = "your_database_user"
DB_PASSWORD = "your_database_password"
DB_NAME = "your_database_name"

console_start_message = "Message to send to console when started"
discord_start_message = "Message to send to chat when started"

# Create an instance of the bot with intents
intents = discord.Intents.default()
intents.message_content = True  # Enable message-related events

bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'), intents=intents)

# Remove the default help command
bot.remove_command("help")

# Connect to MySQL database
conn = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)
cursor = conn.cursor()
'''
@bot.event
async def on_ready():
    print(console_start_message)
    # Get the specific channel by ID
    channel_id = 1033272269230845994
    target_channel = bot.get_channel(channel_id)

    if target_channel:
        await target_channel.send(discord_start_message)
    else:
        print(f"Channel with ID {channel_id} not found.")
'''

#This is called in the Report Command which logs all the information into the database. All the values can be changed to match your database.
#There is an additional script which creates all the needed Database values into your SQL Server
async def log_report(ctx, author_id, username, responses, channel_id):
    try:
        # Log or store the responses in the "discord_reports" table
        cursor.execute(
            'INSERT INTO discord_reports (discord_id, username, dis_report_who, dis_report_what, dis_report_when, dis_report_contact, dis_report_other, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
            (author_id, username, responses[0], responses[1], responses[2], responses[3], responses[4], 'Open')
        )
        conn.commit()

        # Create an embed message
        embed = discord.Embed(
            title="New Report",
            description=f"Report logged by user {username}:",
            color=0x00ff00  # Green color (you can customize this)
        )
        embed.add_field(name="User in question:", value=responses[0], inline=False)
        embed.add_field(name="What they did:", value=responses[1], inline=False)
        embed.add_field(name="Event Occurred on:", value=responses[2], inline=False)
        embed.add_field(name="Do they want to be contacted", value=responses[3], inline=False)
        embed.add_field(name="Other Details/Comments:", value=responses[4], inline=False)

        # Get the specific channel by ID
        target_channel = bot.get_channel(channel_id)

        if target_channel:
            # Send the embed message to the specified channel
            await target_channel.send(embed=embed)
            print(f"Embed message sent to channel {channel_id}")
        else:
            print(f"Channel with ID {channel_id} not found.")

        # Notify completion
        await ctx.author.send("Thank you for the report. It has been logged.")
    except Exception as e:
        print(f"An error occurred while processing the report: {str(e)}")
        await ctx.author.send("An error occurred while processing the report. Please try again.")

@bot.command(name='Report')
async def report(ctx):
    try:
        # No need to check if the user is registered, insert them automatically
        user_id = ctx.author.id
        username = ctx.author.name

        # Notify completion
        await ctx.author.send("Thank you for reporting. Let's get some information.")

        # Define questions for the report
        questions = [
            "Who are you reporting?",
            "What did they do?",
            "When did this event occur?",
            "Would you like us to contact you?",
            "Are there any other details or comments you would like to add?"
        ]

        # Ask questions and collect responses
        responses = []
        for question in questions:
            await ctx.author.send(question)
            response = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
            responses.append(response.content)

        # Specify the channel ID where you want to send the embed message ( USUALLY THIS WOULD BE AN ADMIN CHANNEL )
        target_channel_id = "YOUR ADMIN CHAT CHANNEL ID"

        # Log responses and send the embed message
        await log_report(ctx, user_id, username, responses, target_channel_id)

        # Notify completion
        await ctx.author.send("Thank you for the report. It has been logged.")

    except discord.errors.Forbidden:
        # Handle Forbidden error (unable to send DM)
        await ctx.send("Unable to send a direct message. Please check your privacy settings and try again.")

    except Exception as e:
        # Handle other exceptions
        print(f"An error occurred during the report command: {str(e)}")
        await ctx.author.send("An error occurred during the report. Please try again.")

@bot.command(name='Tickets')
async def tickets(ctx):
    try:
        # Fetch all open tickets from the database
        cursor.execute('SELECT * FROM discord_reports WHERE status = %s', ('Open',))
        tickets = cursor.fetchall()

        if tickets:
            for ticket in tickets:
                print(ticket)  # Print the entire row to inspect its structure

            # Create an embed message
            embed = discord.Embed(
                title="All Open Tickets",
                description="List of all pending tickets:",
                color=0x00ff00  # Green color (you can customize this)
            )

            # Add fields for each ticket
            for ticket in tickets:
                ticket_number = ticket[0]  # Adjust the index based on the actual position in the result
                username = ticket[3]  # Adjust the index based on the actual position in the result
                reported_user = ticket[4]  # Adjust the index based on the actual position in the result
                details = ticket[5]  # Adjust the index based on the actual position in the result

                embed.add_field(name=f"Ticket #{ticket_number}",
                                value=f"User: {username}\nReported: {reported_user}\nDetails: {details}",
                                inline=False)

            # Send the embed message to the same channel where the command was invoked
            await ctx.send(embed=embed)

        else:
            await ctx.send("No open tickets found.")

    except Exception as e:
        print(f"An error occurred during the OpenTickets command: {str(e)}")
        await ctx.send("An error occurred while fetching open tickets. Please try again.")

@bot.command(name='OpenTicket')
async def open_ticket(ctx, ticket_number: int):
    try:
        # Fetch the specific ticket from the database
        cursor.execute('SELECT * FROM discord_reports WHERE ticket_number = %s', (ticket_number,))
        ticket = cursor.fetchone()

        if ticket:
            # Check if the ticket is marked as 'Open'
            if ticket[1] == 'Open':
                # Get the username of the person running the command
                assigned_user = ctx.author.name

                # Update the 'dis_report_assigned' column with the assigned username
                cursor.execute('UPDATE discord_reports SET dis_report_assigned = %s WHERE ticket_number = %s',
                               (assigned_user, ticket_number))
                conn.commit()

                # Create an embed message
                embed = discord.Embed(
                    title=f"Ticket #{ticket_number} - Open",
                    description=f"Ticket opened by {assigned_user}:",
                    color=0x00ff00  # Green color (you can customize this)
                )
                embed.add_field(name="Reported by:", value=ticket[3], inline=False)
                embed.add_field(name="User in question:", value=ticket[4], inline=False)
                embed.add_field(name="What they did:", value=ticket[5], inline=False)
                embed.add_field(name="Event Occurred on:", value=ticket[6], inline=False)
                embed.add_field(name="Do they want to be contacted", value=ticket[7], inline=False)
                embed.add_field(name="Other Details/Comments:", value=ticket[8], inline=False)

                # Send the embed message to the same channel where the command was invoked
                await ctx.send(embed=embed)

            else:
                await ctx.send(f"Ticket #{ticket_number} is not open.")

        else:
            await ctx.send(f"Ticket #{ticket_number} not found.")

    except Exception as e:
        print(f"An error occurred during the Open command: {str(e)}")
        await ctx.send("An error occurred while processing the Open command. Please try again.")

@bot.command(name='CloseTicket')
@commands.has_role('Elder Owls')  # Adjust the ADMIN role name as needed
async def close_ticket(ctx, ticket_number: int):
    try:
        # Fetch the specific ticket from the database
        cursor.execute('SELECT * FROM discord_reports WHERE ticket_number = %s', (ticket_number,))
        ticket = cursor.fetchone()

        if ticket:
            # Check if the ticket is marked as 'Open'
            if ticket[1] == 'Open':
                # Update the 'status' column to 'Closed'
                cursor.execute('UPDATE discord_reports SET status = %s WHERE ticket_number = %s', ('Closed', ticket_number))
                conn.commit()

                # Create an embed message
                embed = discord.Embed(
                    title=f"Ticket #{ticket_number} - Closed",
                    description=f"Ticket closed by {ctx.author.name}:",
                    color=0xff0000  # Red color (you can customize this)
                )
                embed.add_field(name="User in question:", value=ticket[4], inline=False)
                embed.add_field(name="What they did:", value=ticket[5], inline=False)
                embed.add_field(name="Event Occurred on:", value=ticket[6], inline=False)
                embed.add_field(name="Do they want to be contacted", value=ticket[7], inline=False)
                embed.add_field(name="Other Details/Comments:", value=ticket[8], inline=False)

                # Send the embed message to the same channel where the command was invoked
                await ctx.send(embed=embed)

            else:
                await ctx.send(f"Ticket #{ticket_number} is not open.")

        else:
            await ctx.send(f"Ticket #{ticket_number} not found.")

    except Exception as e:
        print(f"An error occurred during the TicketClose command: {str(e)}")
        await ctx.send("An error occurred while processing the TicketClose command. Please try again.")

@bot.command(name='AssignTicket')
@commands.has_role('Elder Owls')  # Adjust the ADMIN role name as needed
async def assign_ticket(ctx, ticket_number: int, member: discord.Member):
    try:
        # Fetch the specific ticket from the database
        cursor.execute('SELECT * FROM discord_reports WHERE ticket_number = %s', (ticket_number,))
        ticket = cursor.fetchone()

        if ticket:
            # Check if the ticket is open
            if ticket[1] == 'Open':
                # Update the 'dis_report_assigned' column with the assigned admin's username
                assigned_admin = member.name
                cursor.execute('UPDATE discord_reports SET dis_report_assigned = %s WHERE ticket_number = %s',
                               (assigned_admin, ticket_number))
                conn.commit()

                # Create an embed message
                embed = discord.Embed(
                    title=f"Ticket #{ticket_number} - Assigned",
                    description=f"Ticket assigned to {member.mention} by {ctx.author.name}:",
                    color=0x0000ff  # Blue color (you can customize this)
                )
                embed.add_field(name="User in question:", value=ticket[4], inline=False)
                embed.add_field(name="What they did:", value=ticket[5], inline=False)
                embed.add_field(name="Event Occurred on:", value=ticket[6], inline=False)
                embed.add_field(name="Do they want to be contacted", value=ticket[7], inline=False)
                embed.add_field(name="Other Details/Comments:", value=ticket[8], inline=False)

                # DM the assigned admin with the embed message
                await member.send(embed=embed)

                # Notify the admin who ran the command through DM
                await ctx.author.send(f"{member.mention} has been assigned Ticket #{ticket_number}.")

            else:
                await ctx.send(f"Ticket #{ticket_number} is not open.")

        else:
            await ctx.send(f"Ticket #{ticket_number} not found.")

    except Exception as e:
        print(f"An error occurred during the AssignTicket command: {str(e)}")
        await ctx.send("An error occurred while processing the AssignTicket command. Please try again.")

@bot.command(name='delete_last_messages')
@commands.has_role('Elder Owls')  # Restrict command to users with 'ELDER OWLS' role
async def delete_last_messages(ctx):
    channel = ctx.channel

    # Fetch the last 20 messages in the channel
    messages = []
    async for message in channel.history(limit=20): #Eventually I will have it to be dynamic
        messages.append(message)

    # Delete each fetched message
    for message in messages:
        await message.delete()

    # Send a confirmation message after deletion
    await ctx.send("Last 20 messages deleted.")

# This command will send all tickets in the database through DMs
@bot.command(name='DebugTickets')
async def debug_tickets(ctx):
    try:
        # Fetch all tickets from the database
        cursor.execute('SELECT * FROM discord_reports')
        tickets = cursor.fetchall()

        if tickets:
            # Create an embed
            embed = Embed(title="Debug Tickets - Discord Bot", color=0x00ff00)

            # Add fields for each ticket
            for ticket in tickets:
                embed.add_field(name=f"Ticket #{ticket[0]}", value=f"User: {ticket[3]}\nReported User: {ticket[4]}\nDetails: {ticket[5]}", inline=False)

            # Send the embed as a direct message
            await ctx.author.send(embed=embed)
            await ctx.send("Debug tickets sent to your DMs.")

        else:
            await ctx.send("No tickets found in the database.")

    except Exception as e:
        print(f"An error occurred during the DebugTickets command: {str(e)}")
        await ctx.send("An error occurred while processing the DebugTickets command. Please try again.")

# Run the bot with the provided token
bot.run(TOKEN)
