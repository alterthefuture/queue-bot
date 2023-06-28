from discord.colour import Color
from discord.ext import commands
import discord
import datetime
import asyncio

qplayers = []
qchannels = []

class queuecommands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot  

    @commands.command()
    async def setup(self,ctx):
        if ctx.author.id == ctx.guild.owner:
            try:
                await ctx.guild.create_role(name="Queue Admin",colour=discord.Colour(0xFF0000))
                await ctx.guild.create_role(name="registered",colour=discord.Colour(0x00FF00))

                embed=discord.Embed(description=f"Successfully setup queue system and roles.",color=discord.Color.green())
                embed.set_footer(text="Bot Created By Kxrby#0")

                return await ctx.send(embed=embed)
            except:
                embed=discord.Embed(description=f"Failed to setup queue system and roles.",color=discord.Color.red())
                embed.set_footer(text="Bot Created By  Kxrby#0")

                return await ctx.send(embed=embed)
        else:
            embed=discord.Embed(description=f"You have to be server owner to run this command.",color=discord.Color.red())
            embed.set_footer(text="Bot Created By  Kxrby#0")

            return await ctx.send(embed=embed)

    @commands.command(aliases=['r'])
    async def register(self,ctx):
        data = await self.bot.config.get_by_id(ctx.author.id)

        if not data:
            try:
                await self.bot.config.upsert({"_id": ctx.author.id, "points": 0})
                data = await self.bot.config.get_by_id(ctx.author.id)

                points = data["points"]

                registered_role = discord.utils.get(ctx.guild.roles, name="In Queue")

                await ctx.author.add_roles(registered_role)
                return await ctx.author.edit(nick=f"[{points}] {ctx.author.name}")
            except:
                embed=discord.Embed(description=f"{ctx.author.mention} I have failed to register you, please try again later.",color=discord.Color.red())
                embed.set_footer(text="Bot Created By  Kxrby#0")

                return await ctx.send(embed=embed)
        else:
            embed=discord.Embed(description=f"{ctx.author.mention} you are already registered.",color=discord.Color.red())
            embed.set_footer(text="Bot Created By  Kxrby#0")

            return await ctx.send(embed=embed)

    @commands.command(aliases=['q'])
    @commands.has_role("registered")
    async def queue(self,ctx):
        data = await self.bot.config.get_by_id(ctx.author.id)

        if not data:
            embed=discord.Embed(description=f"{ctx.author.mention} you're not registered, please register first.",color=discord.Color.red())
            embed.set_footer(text="Bot Created By  Kxrby#0")

            return await ctx.send(embed=embed)
        else:
            if ctx.author in qplayers:
                embed=discord.Embed(description=f"{ctx.author.mention} you are already in a queue, please be patient.",color=discord.Color.red())
                embed.set_footer(text="Bot Created By  Kxrby#0")

                await ctx.send(embed=embed)
                return

            qplayers.append(ctx.author)

            if len(qplayers) == 1:
                embed=discord.Embed(description=f"Queue is full, setting up channel...",color=discord.Color.blue())
                embed.set_footer(text="Bot Created By  Kxrby#0")

                await ctx.send(embed=embed)

                category_id = your_category_id

                for category in ctx.guild.categories:
                    if category.id == category_id:
                        break

                channel_amount = 1 if len(category.channels) == 0 else int(category.channels[-1].name.split("-")[-1]) + 1
                game_channel = await category.create_text_channel(f"game {channel_amount}", permission_synced=True)
                await game_channel.set_permissions(qplayers[0], read_messages=True,send_messages=True)
           

                embed=discord.Embed(title="Match Found!",description=f"Your first in queue!.\n\n**COMMANDS**\n`;win [@user]` - Decides who wins **(ADMIN ONLY)**\n`;lose [@user]` - Decides who loses **(ADMIN ONLY)**\n`;close` - Ends game and deletes channel **(ADMIN ONLY)**\n\n**MATCH DETAILS**\nCreation Time: **{datetime.datetime.utcnow()}**\nPlayers: **{qplayers[0]}** vs **{qplayers[1]}**", color=discord.Color.blue())
                embed.set_footer(text="Bot Created By  Kxrby#0")

                await game_channel.send(f"{qplayers[0].mention , your next in queuey.",embed=embed) 

                qchannels.append(game_channel.id)
                return qplayers.clear()
            else:
                embed=discord.Embed(description=f"**[{len(qplayers)}/2]** {ctx.author.mention} has joined queue.",color=discord.Color.green())
                embed.set_footer(text="Bot Created By  Kxrby#0")

                return await ctx.send(embed=embed)
    
    @commands.command(aliases=['lq'])
    @commands.has_role("registered")
    async def leavequeue(self,ctx):
        data = await self.bot.config.get_by_id(ctx.author.id)

        if not data:
            embed=discord.Embed(description=f"{ctx.author.mention} you're not registered, please register first.",color=discord.Color.red())
            embed.set_footer(text="Bot Created By  Kxrby#0")

            return await ctx.send(embed=embed)
        else:
            if ctx.author in qplayers:
                try:
                    qplayers.remove(ctx.author)
                    embed=discord.Embed(description=f"**[{len(qplayers)}/2]** {ctx.author.mention} has left queue",color=discord.Color.green())
                    embed.set_footer(text="Bot Created By  Kxrby#0")

                    return await ctx.send(embed=embed)
                except:
                    pass
            elif ctx.author not in qplayers:
                embed=discord.Embed(description=f"{ctx.author.mention} you are not in queue, join queue first.",color=discord.Color.red())
                embed.set_footer(text="Bot Created By  Kxrby#0")

                return await ctx.send(embed=embed)
            else:
                pass

    @commands.command(aliases=['w'])
    @commands.has_role("Queue Admin")
    async def win(self,ctx,member: discord.Member):
        data = await self.bot.config.get_by_id(member.id)
    
        if not data:
            embed=discord.Embed(description=f"{member.mention} is not registered, please register first.",color=discord.Color.red())
            embed.set_footer(text="Bot Created By  Kxrby#0")

            return await ctx.send(embed=embed)
        else:
            new_amount = data['points'] + 1

            try:
                await self.bot.config.upsert({"_id": member.id, "points": new_amount})

                embed=discord.Embed(description=f"{member.mention} move 1 in queue.",color=discord.Color.green())
                embed.set_footer(text="Bot Created By  Kxrby#0")

                await ctx.send(embed=embed)

                data = await self.bot.config.get_by_id(member.id)
                points = data['points']

                return await member.edit(nick=f"[{points}] {member.name}")
            except:
                embed=discord.Embed(description=f"Failed to give {member.mention} 1 queue.",color=discord.Color.red())
                embed.set_footer(text="Bot Created By Kxrby#0")

                return await ctx.send(embed=embed)
    
    @commands.command(aliases=['l'])
    @commands.has_role("Queue Admin")
    async def lose(self,ctx,member: discord.Member):
        data = await self.bot.config.get_by_id(member.id)
        
        if not data:
            embed=discord.Embed(description=f"{member.mention} is not registered, please register first.",color=discord.Color.red())
            embed.set_footer(text="Bot Created By  Kxrby#0")

            return await ctx.send(embed=embed)
        else:
            new_amount = data['points'] - 5
            
            try:
                if data["points"] == 0:
                    embed=discord.Embed(description=f"{member.mention} has no points.",color=discord.Color.red())
                    embed.set_footer(text="Bot Created By  Kxrby#0")

                    return await ctx.send(embed=embed)
                else:
                    await self.bot.config.upsert({"_id": member.id, "points": new_amount})

                    embed=discord.Embed(description=f"{member.mention} lost 5 points.",color=discord.Color.green())
                    embed.set_footer(text="Bot Created By  Kxrby#0")

                    await ctx.send(embed=embed)

                    data = await self.bot.config.get_by_id(member.id)
                    points = data['points']

                    return await member.edit(nick=f"[{points}] {member.name}")
            except:
                embed=discord.Embed(description=f"Failed to remove queue from {member.mention}",color=discord.Color.red())
                embed.set_footer(text="Bot Created By  Kxrby#0")

                return await ctx.send(embed=embed)

    @commands.command(aliases=['c'])
    @commands.has_role("Queue Admin")
    async def close(self,ctx):
        if ctx.channel.id not in qchannels:
            embed=discord.Embed(description=f"Channel is not a queue channel.",color=discord.Color.red())
            embed.set_footer(text="Bot Created By  Kxrby#0")

            return await ctx.send(embed=embed)
        else:
            qchannels.remove(ctx.channel.id)

            embed=discord.Embed(description=f"Deleting channel in a few seconds...",color=discord.Color.green())
            embed.set_footer(text="Bot Created By  Kxrby#0")

            await ctx.send(embed=embed)

            await asyncio.sleep(2)

            try:
                return await ctx.channel.delete()
            except:
                embed=discord.Embed(description=f"Failed to delete game channel.",color=discord.Color.red())
                embed.set_footer(text="Bot Created  Kxrby#0")

                return await ctx.send(embed=embed)




def setup(bot):
    bot.add_cog(queuecommands(bot))
