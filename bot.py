import discord
import psycopg2

client = discord.Client()

conn1 = psycopg2.connect(*****)
cur = conn1.cursor()

@client.event
async def on_ready():
    print("Working")

@client.event
async def on_message(message):
    #ignore the bot itself
    if message.author == client.user:
        return

    #example: !addEvent 1.2 HW 9/4/2020
    elif message.content.startswith('!addEvent'):
        try:
            split = message.content.split()
            event = split[1 : len(split) - 1]
            event = ' '.join(event)
            subject = str(message.channel)
            date = split[len(split) - 1]

            cur.execute('INSERT INTO events (date, event, class) VALUES (%s, %s, %s)', [date, event, subject])
            conn1.commit()

            combined = event + ' added to ' + subject
            await message.channel.send(combined)
        except:
            await message.channel.send("I do not understand that.")

    elif message.content == '!commands':
        embed = discord.Embed(title="Commands for CalendarBot", description="", colour=0xd10a07)
        embed.add_field(name="!addEvent", value="Adds an event (Example: !addEvent Section 1.2 HW 9-4-2020). Add the event in the channel the homework belongs to.")
        embed.add_field(name="!events", value="Prints all the upcoming events for that class")
        await message.channel.send(content=None, embed = embed)

    elif message.content == '!events':
        cur.execute('SELECT * FROM events WHERE class=%s ORDER BY date', [str(message.channel)])
        text = ''
        events = list(cur.fetchall())
        for item in events:
            text += str(item[0]) + ' <> ' + str(item[1]) + ' <> ' + str(item[2]) + '\n'
        channel = "Events for " + str(message.channel)
        embed = discord.Embed(title=channel, description="")
        embed.add_field(name="", value=text)
        await message.channel.send(text)
    conn1.commit()

client.run(token)
