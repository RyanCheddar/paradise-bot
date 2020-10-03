import asyncio

# ===================================================
# || Update Balance - Updates Para Rewards balance ||
# ||                                               ||
# || userid - The user's id                        ||
# ||                                               ||
# || action - The action being done, valid options ||
# || are "add" and "subtract"                      ||
# ||                                               ||
# || baltype - The balance type, can be "credits"  ||
# || or "points"                                   ||
# ||                                               ||
# || amount - The amount being changed             ||
# ===================================================
async def updatebalance(userid, action, baltype, amount):
  # TODO - I have no fucking clue how Github works so this is just test
