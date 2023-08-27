import discord
import socket
from discord.ext import commands
from discord.ext import tasks
from discord import Embed, Color
from discord.ext import tasks
import requests
# Function to fetch FiveM server info
# Function to fetch FiveM server info
def convert_to_dict(data_list):
    # Skip the first value and convert the rest into a dictionary
    return {data_list[i]: data_list[i + 1] for i in range(1, len(data_list) - 1, 2)}
def fetch_fivem_server_info(ip, port):
    try:
        print(f"Attempting to connect to {ip}:{port}")
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(1)
            s.connect((ip, port))
            
            # Send a query request to the server
            print("Sending query request...")
            s.send(b'\xFF\xFF\xFF\xFFgetinfo xxx')
            
            # Receive the response
            print("Waiting for response...")
            data, addr = s.recvfrom(4096)
            
            # Parse the data
            print("Parsing response...")
            # data = data[16:].decode('utf-8')
            # data = data.split('\\')
            data = data[12:].decode('utf-8').split('\\')
            # Create a dictionary from the received data
            converted_data = convert_to_dict(data)
                
            print(f"Received data info: {data}")
            print(f"Received server info: {converted_data}")
            return converted_data
    except Exception as e:
        print(f"An exception occurred: {e}")
        return {"error": str(e)}
    


# The rest of your bot code remains the same







# Create a new instance of the bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Enables the member update events
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print(f'Bot ID: {bot.user.id}')



@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f"An error occurred: {str(error)}")
# @bot.event
# async def on_message(message):
#     print(f"Received message from {message.author}: {message.content}")
#     await bot.process_commands(message)  # Important if you have commands in your bot
@bot.command()
async def test(ctx):
    print("Received test command")
    await ctx.send("Test successful!")


@bot.command()
async def player(ctx):
    # Static IP and port
    ip = "168.100.15.145"
    port = 30120
    info = fetch_fivem_server_info(ip, port)
    if "error" in info:
        await ctx.send(f"Could not fetch server info: {info['error']}")
        return

    current_players = info.get('clients', 'Unknown')
    max_players = info.get('sv_maxclients', 'Unknown')
    # Create an embed with a title, description, and color
    embed = Embed(title="FiveM Server Status", description=f"Server Name: {info.get('hostname', 'Unknown')}", color=Color.blue())
    
    # Add a field for player count
    embed.add_field(name="Players", value=f"{current_players}/{max_players}", inline=True)
    await ctx.send(embed=embed)

from discord.ext import tasks

status_mode = "normal"  # default mode

@tasks.loop(seconds=5)  # Adjust the interval as needed
async def update_bot_status():
    global status_mode

    if status_mode == "maintenance":
        game = discord.Game("Server is maintaining, come back later")
    else:
        info = fetch_fivem_server_info("168.100.15.145", 30120)
        current_players = info.get('clients', 'Unknown')
        max_players = info.get('sv_maxclients', 'Unknown')
        game = discord.Game(f"{current_players}/{max_players} players on ANT City")

    await bot.change_presence(status=discord.Status.online, activity=game)

@bot.command()
async def setstatus(ctx, mode: str):
    global status_mode

    if mode.lower() == "true":
        status_mode = "normal"
        await ctx.send("Status set to normal.")
    elif mode.lower() == "false":
        status_mode = "maintenance"
        await ctx.send("Status set to maintenance mode.")
    else:
        await ctx.send("Invalid mode. Use true or false.")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print(f'Bot ID: {bot.user.id}')
    update_bot_status.start()  # Start the background task






# Run the bot
try:
    bot.run("MTE0NTI3MjUwMTQwNDk3OTI2MA.G0WXWC.glMla0P8rY3-5jUWxoszV2TTJu886mYYrfb-uo")
except Exception as e:
    print(f"Error: {e}")


