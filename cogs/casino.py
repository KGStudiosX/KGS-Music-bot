import random
from diskord.ext import commands

class Casino(commands.Cog):
    def __init__(self, bot):
    	self.bot = bot

    @commands.command()
    async def casino(self, ctx, something: int):
    	await ctx.send(f"{something} Говоришь?")
    	for i in range(1, 100):
    		something2 = random.randint(1, 2)
    	if something2 == something:
    		await ctx.send("Ты выиграл!")
    	else:
    		await ctx.send("Ты проиграл!")
    		await ctx.send(f"Ответ: {something2}")

def setup(bot):
    bot.add_cog(Casino(bot))