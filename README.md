# DiscordBot

Hi,
  
This is a discord bot I developed. It utilizes a neural network, currently I trained the neural network to play tic tac toe, but I am currently working on making it do a lot more fun and complex things such as chatbots and more complex games.

if you encounter any errors or have any feature requests/queries feel free to dm me on twitter or discord @HarryOC493#5941 or submit an issue

Usage:  
  -- You Need to install the requirements.txt using pip3  
  -- train.py use this file to retrain the network in the event your not happy with its current training, or if you wish to change an 
     aspect off the game
     My network:
         Epochs    : 100
         Batch Size: 100

-- main.py is the actual bot scipt, all you need to do is run this script on a machine connected to the internet and is 
     capable of running a neural net  
-- <h2>main.py<h2>
   Setup:
      Connecting your discord bot:
          Create a bot on discord <a href='https://discordpy.readthedocs.io/en/stable/discord.html'>here!</a>
          Using the api key you generated paste it into this line on main.py
          "client.run("123456xxx")"
  
      main.py is the actual game, this script imports the trained model, interfaces with discord and runs the actual game
