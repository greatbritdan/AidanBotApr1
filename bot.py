import os
from notaidanbot import os NotAidanBot

def main():
	client = NotAidanBot()
	client.run(os.getenv("DISCORD_TOKEN"))

if __name__ == '__main__':
    main()
