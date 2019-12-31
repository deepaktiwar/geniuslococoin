

"""
Main Discord bot script
"""
import discord
import asyncio
import re
import phonenumbers
from string import Template
import loco_functions

 

TOKEN ="NTkwOTc4MjkxNDgyMjMwODE0.XQqFoA.W5nxHRw5WpYwLE2-dXdCvX_eliY"

CANT_SEND_VERIF_CODE_MSG = discord.Embed(title="Error sending verification code!", color=0x142c9c)
CANT_SEND_VERIF_CODE_MSG.set_footer(text=f"Made with ♥ by ⎝⧹𝗗𝗿. BOSS™╱⎠#0928", \
                icon_url="https://cdn.discordapp.com/avatars/503905683163578368/e8e8948881e34bcaf4e67573ae58b8b3.png?size=256")
 
WAITING_MSG = "**Enter verification Code: XXXX**"

PRACTICE_STATUS_TEMPLATE1 = \
"""
**$total_coins Coins Earned**
**$games Game Played**
"""

PRACTICE_STATUS_TEMPLATE2 = \
""" 
$questions
Coins: $coins
"""
PRACTICE_STATUS_TEMPLATE3 = \
"""
**$games Game Played**
"""
PRACTICE_STATUS_TEMPLATE4 = \
"""
$question
"""
PRACTICE_STATUS_TEMPLATE5 = \
"""
**Coins For this question: $coins**
"""
 
BOT_OWNER_ROLE = '' # change to what you need

class LocoCoinsBot(discord.Client):
    async def on_ready(self):
        print('Logged in as: %s' % self.user.name)
        self.play_requests = {}
        await self.change_presence(activity=discord.Game(name='Official || Coin-help'))

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return
        """
        -help
        """

        if message.content.startswith("-ping"):
           await message.delete()
          
           await message.channel.send('Pong! {0}'.format(round(bot.latency, 1)))
           
        if message.author==bot.user:
            return
        if message.content.startswith('-help'):
          await message.delete()
          embed = discord.Embed(title="Help Commands!", description="HI! I'm Loco coins bot :wink:\n\n"+"**User:**\n"+message.author.mention, color=0xFF00FF)
          embed.set_author(name="Loco Coins", icon_url="https://lh3.googleusercontent.com/X6YnhAu9xcb3qQ89mDHdDtJzb9Dyf2DytQTQRvLP8CloXhygKuicDyMsMmrK6S1uD1yY")
          embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/587736810332094467/587980733558292483/unnamed.png")
          embed.add_field(name="To Get Some Loco Coins By Loco Practice Type.", value="**-loco** +91`<your_loco_number>`", inline=False)
          embed.add_field(name="For Verify Loco Account", value="**-code** `<you_received_otp>`", inline=False)
          embed.set_footer(text=f"Made with ♥ by ⎝⧹𝗗𝗿. BOSS™╱⎠#0928", \
                icon_url="https://cdn.discordapp.com/attachments/626463527301021735/639093471382077440/images_1.jpeg") 
          await message.channel.send(embed=embed)
          return
            

        """
        -play <phone_number>
     
        """
        if message.author==bot.user:
            return
        if message.content.startswith('-loco'): 
            await message.delete()
            
            if BOT_OWNER_ROLE not in [role.name for role in message.author.roles]:
              lol =discord.Embed(title="**Lol You Not Have **Access** role to use this bot",description="**User:**\n"+message.author.mention,color=0x142c9c)
              #lol.set_thumbnail(url=message.author.avatar_url)
              lol.set_footer(text=f"Made with ♥ by ⎝⧹𝗗𝗿. BOSS™╱⎠#0928", \
                icon_url="https://cdn.discordapp.com/attachments/626463527301021735/639093471382077440/images_1.jpeg")
              await message.channel.send(embed=lol)
              return
            # parse phone number
            try:
                phone = message.content.split()[1]
                pp = phonenumbers.parse(phone)
                country_abbrev = phonenumbers.region_code_for_number(pp).lower()
                national_number = str(pp.national_number)
            except:
              worng =discord.Embed(title="worng use:",description="**Usage:\n-loco +91**`<your_loco_number>`\n"+message.author.mention,color=0x0000FF)
              worng.set_footer(text=f"Made with ♥ by ⎝⧹𝗗𝗿. BOSS™╱⎠#0928", \
                icon_url="https://cdn.discordapp.com/attachments/626463527301021735/639093471382077440/images_1.jpeg")
              await message.channel.send(embed=worng)
              return

            # requesting sms code to user phone from Loco
            res = loco_functions.get_sms_code_from_Loco(country_abbrev=country_abbrev,\
                                                  national_number=national_number)
            if res is None:
                await message.channel.send(embed=CANT_SEND_VERIF_CODE_MSG)
                return
            if message.author==bot.user:
                return
            em = discord.Embed(title="Check Your phone!",description="**User:**\n"+message.author.mention, color=0x00FFCC)
            em.set_author(name="Loco Coins", icon_url="https://lh3.googleusercontent.com/X6YnhAu9xcb3qQ89mDHdDtJzb9Dyf2DytQTQRvLP8CloXhygKuicDyMsMmrK6S1uD1yY")
            em.set_thumbnail(url="https://cdn.discordapp.com/attachments/587736810332094467/587980733558292483/unnamed.png")
            em.add_field(name="verification code is sent!", value="**-code** `<you_received_otp>`", inline=False)
            em.set_footer(text=f"Made with ♥ by ⎝⧹𝗗𝗿. BOSS™╱⎠#0928", 
                icon_url=f"https://cdn.discordapp.com/attachments/626463527301021735/639093471382077440/images_1.jpeg")
            await message.channel.send(embed=em)
            wait=discord.Embed(title="**User:**",description=message.author.mention,color=0x142c9c)
            play_answer = await message.channel.send(embed=wait)
            
         
            try:
                def is_correct_sms_code(m):
                    if m.author != message.author:
                        return False
                    m = re.match(r'-code ([\d]{4})', m.content)
                    if m is None:
                        return False
                    global sms_code
                    sms_code = m.group(1)
                    return True
          # if message.content.startswith('-verifyloco'): 
          #   await message.delete()      
                await self.wait_for('message', check=is_correct_sms_code,\
                                                   timeout=60.0)
                                                
            except asyncio.TimeoutError:
                return await play_answer.edit(content=\
                                 play_answer.content)
            # await play_answer.edit(embed=em)
            # await play_answer.edit(content=SENT_VERIF_CODE_MSG+WAITING_MSG)

            profile_token = loco_functions.authorize(country_abbrev=country_abbrev,
                                                  national_number=national_number,
                                                  sms_code=sms_code)
            if profile_token is None:
                CANT_AUTH_MSG = discord.Embed(title="User:",description=message.author.mention, color=0xFF0000)
                CANT_AUTH_MSG.add_field(name="all games play !",value="**try after 1day  .**\n**Please try again.**")
                CANT_AUTH_MSG.set_author(name="Loco Coins", icon_url="https://lh3.googleusercontent.com/X6YnhAu9xcb3qQ89mDHdDtJzb9Dyf2DytQTQRvLP8CloXhygKuicDyMsMmrK6S1uD1yY")
                CANT_AUTH_MSG.set_thumbnail(url="https://cdn.discordapp.com/attachments/587736810332094467/587980733558292483/unnamed.png")
                CANT_AUTH_MSG.set_footer(text=f"Made with ♥ by ⎝⧹𝗗𝗿. BOSS™╱⎠#0928", 
                icon_url="https://cdn.discordapp.com/attachments/626463527301021735/639093471382077440/images_1.jpeg")
                await message.channel.send(embed=CANT_AUTH_MSG)
                # await play_answer.edit(content=CANT_AUTH_MSG)
                return

            try:
                for res in loco_functions.main_play_loop(country_abbrev=country_abbrev,
                        national_number=national_number,
                        profile_token=profile_token):

                    if 'error' in res.keys():
                      PRACTICE_ERR_MSG = discord.Embed(title="User:",description=message.author.mention, color=0x33FFFF)
                      PRACTICE_ERR_MSG.add_field(name="Something went wrong!",value="**Try Again Later.**")
                      PRACTICE_ERR_MSG.set_author(name="Loco Coins", icon_url="https://lh3.googleusercontent.com/X6YnhAu9xcb3qQ89mDHdDtJzb9Dyf2DytQTQRvLP8CloXhygKuicDyMsMmrK6S1uD1yY")
                      PRACTICE_ERR_MSG.set_thumbnail(url="https://cdn.discordapp.com/attachments/587736810332094467/587980733558292483/unnamed.png")
                      PRACTICE_ERR_MSG.set_footer(text=f"Made with ♥ by ⎝⧹𝗗𝗿. BOSS™╱⎠#0928", \
                       icon_url="https://cdn.discordapp.com/attachments/626463527301021735/639093471382077440/images_1.jpeg")
                      await message.channel.send(embed=PRACTICE_ERR_MSG)
                        # await play_answer.edit(content=PRACTICE_ERR_MSG)
                      return
                    # practice_msg = discord.Embed(title="Game status",description="", color=0xFF0099)
                    practice_msg1 = Template(PRACTICE_STATUS_TEMPLATE1).substitute(res)
                    # practice_msg2 = Template(PRACTICE_STATUS_TEMPLATE2).substitute(res)
                    # practice_msg3 = Template(PRACTICE_STATUS_TEMPLATE3).substitute(res)
                    practice_msg4 = Template(PRACTICE_STATUS_TEMPLATE4).substitute(res)
                    practice_msg5 = Template(PRACTICE_STATUS_TEMPLATE5).substitute(res)
                     
                    emm=discord.Embed(title=practice_msg4,description=practice_msg5,color=0xFF00FF)
                    emm.set_thumbnail(url="https://cdn.discordapp.com/attachments/587736810332094467/587980733558292483/unnamed.png")
                    # emm.add_field(name=practice_msg4)
                    emm.add_field(name="Game Stats:",value=practice_msg1)
                    # emm.add_field(name="Questions Answered:",value=practice_msg2)
                    # emm.add_field(name="Game Played:",value=practice_msg3)
                    emm.set_footer(text=f"Request By:- "+str(message.author), \
                       icon_url=message.author.avatar_url)
                    await play_answer.edit(embed=emm)
                    # await message.edit(embed=emm)
                    # await message.channel.send(content=practice_msg)
                    # await play_answer.edit(content=practice_msg)
                    

   
            except:
                message=await play_answer.edit(content=play_answer.practice_msg)
                
                # await message.channel.send(()+"\n{0.author.mention}".format(message))
                return
            else:
                await play_answer.edit(content=play_answer.content)
                al =discord.Embed(title="All games are played!",description="**User**\n"+message.author.mention,color=0xFF0066)
                al.add_field(name="Game Stats:",value=practice_msg1)
                al.set_footer(text=f"Made with ♥ by ⎝⧹𝗗𝗿. BOSS™╱⎠#0928", \
                icon_url="https://cdn.discordapp.com/attachments/626463527301021735/639093471382077440/images_1.jpeg")
                await message.channel.send(embed=al)
                return

        if message.content.startswith('-verifycode'):
              await message.delete()

bot = LocoCoinsBot()
bot.run('NjM4NDM0OTA5OTE1OTcxNTk0.XdLAWA.Y1Jlpd44LLg2KeRFDpszndf_TJg')
