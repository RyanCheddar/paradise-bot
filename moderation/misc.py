async def read_member_id(members):
    members_list: list = []
    for member in members:
        members_list.append(str(member[0]))
    return members_list


async def split(content, number):
    content_list: list = []
    content_str: str = ""
    returned: bool = False
    number = int(number)
    number -= 1
    content = str(content)
    content = content+" "
    print("content recieved: ", content)
    for b in enumerate(range(len(content))):
        i = b[1]
        print(i)
        if content[i] == " ":
            content_list.append(content_str)
            print("apppeded to list")
            content_str = ""
        else:
            content_str = content_str+content[i]
        if len(content_list)-1 == number:
            print("limit found")
            print(content_list)
            try:
                optional_arg = content[i + 1:]
                content_list.append(optional_arg)
                if str(content_list[-1]) == "":
                    content_list.remove(optional_arg)
            except IndexError:
                print("No optional arguement found")
            return content_list
            returned = True
    print(content_list)
    if returned == False:
        return content_list


async def punish_log(embed):
    print("getting log channel")
    devlog = bot.get_channel(int("683331993634603068"))
    await devlog.send(embed=embed)


async def log(text):
    print("getting log channel")
    devlog = bot.get_channel(int("683331960705515570"))
    print("sending logs")
    await devlog.send(text)
    print("log sent")


async def get_digit(input):
    to_be_return: str = ""
    for i in input:
        i = str(i)
        if i in "1234567890":
            to_be_return = to_be_return+i
    return to_be_return


async def Not_enough_perms():
    embed = discord.Embed(title="Not enough Permissions", description="You do you not have the perms to do this",
                          timestamp=datetime.datetime.now(datetime.timezone.utc), color=65280)
    embed.set_footer(text="Paradise Bot")
    return embed


async def Invalid_Time_send():
    Invalid_Time = discord.Embed(title="Invalid Time format", description="'s' for seconds\n'm' for minutes\n'h for hours'\n 'd' for days\n 'w' for weeks",
                                 color=53247, timestamp=datetime.datetime.now(datetime.timezone.utc))
    Invalid_Time.add_field(name="Please use this format",
                           value="This is not case sensitive", inline=False)
    Invalid_Time.set_footer(text="Paradise Bot")
    return Invalid_Time
