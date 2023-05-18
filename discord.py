import discord
from discord.ext import commands

TOKEN = 'Discord_Bot_Token'
SOURCE_GUILD_ID = 123456789  # Kaynak sunucu ID'si
TARGET_GUILD_ID = 987654321  # Hedef sunucu ID'si

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print('Bot giriş yaptı.')

    source_guild = bot.get_guild(SOURCE_GUILD_ID)
    target_guild = bot.get_guild(TARGET_GUILD_ID)

    if source_guild is None or target_guild is None:
        print('Kaynak veya hedef sunucu bulunamadı.')
        return

    print('Sunucu kopyalama işlemi başladı.')

    # Rolleri kopyalama
    for source_role in source_guild.roles:
        if not source_role.is_default():
            permissions = source_role.permissions
            target_role = await target_guild.create_role(name=source_role.name, permissions=permissions)
            print(f'"{source_role.name}" rolü kopyalandı.')

    # Kanalları kopyalama
    for source_channel in source_guild.channels:
        if isinstance(source_channel, discord.TextChannel):
            overwrites = {
                target_guild.default_role: source_channel.overwrites_for(source_channel.guild.default_role),
                target_guild.me: source_channel.overwrites_for(source_channel.guild.me)
            }
            target_channel = await target_guild.create_text_channel(name=source_channel.name, overwrites=overwrites)
            print(f'"{source_channel.name}" kanalı kopyalandı.')

            # Mesajları kopyalama (tüm mesajları kopyalamak performans sorunlarına neden olabilir)
            async for message in source_channel.history(limit=None):
                if message.author != bot.user:
                    await target_channel.send(content=message.content,
                                              username=message.author.name,
                                              avatar_url=message.author.avatar_url)
                    print(f'Mesaj kopyalandı: "{message.content}"')

    print('Sunucu kopyalama işlemi tamamlandı.')
    await bot.close()


bot.run(TOKEN)
