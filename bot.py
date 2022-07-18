import discord
import mysql.connector
from asyncio import sleep
from datetime import datetime
from mysqlconfig import host, user, password, db_name
from config import settings
from discord.ext import commands
from datetime import timedelta, datetime
from dislash import *


intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)
slash = InteractionClient(bot)
con = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=db_name
)
cur = con.cursor()


# Команды / Новости


@slash.slash_command(description='Список оновлень', )
async def new(ctx):
    embed = discord.Embed(title="Список оновлень версії № 1.2.2",
                          description=f"**1.** Додана команда `/poll` для голосування \n"
                                      f"**2.** Додана команда  `/balance` (виключно адміністрації)\n "
                                      f"**3.** Додані логи(список всіх дій гравців)\n"
                                      f"**4.** Виправлено численну кількість багів",
                          colour=discord.Colour.from_rgb(0, 0, 255))
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/996726573434671154/996780435457724477/2.png")
    embed.set_footer(text=f"Творець: Zicnet \nВерсія: 1.2.2")
    await ctx.reply(embed=embed)


# Информационные команды

@slash.slash_command(description='Підтримки роботи бота', )
async def donat(ctx):
    embed = discord.Embed(title="Підтримки",
                          description=f"Привіт, учасник клану, або ж просто добра людина, хочу сказати що не важливо, скільки ти відправиш мені 1,2,10,300 грн. "
                                      f"\n Знай я буду вдячний кожній гривні, відправленій мені для підтримки працездатності бота. "
                                      f"\n Дякую тобі за можливу надану мені матеріальну підтримку.",
                          url="https://send.monobank.ua/jar/88V1KpQ5t4", colour=discord.Colour.from_rgb(0, 0, 255))
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/621287645200384025/997454287762366545/F98o.gif")
    embed.set_footer(text=f"Для переходу на сайт підтримки натисніть кнопку 'підтримка' "
                          f"\nТворець: Zicnet \nВерсія: 1.2.2")
    await ctx.author.send(embed=embed)


@slash.slash_command(description='Початко информація для роботи с ботом', )
async def start(ctx):
    embed = discord.Embed(title="Правила користування",
                          description=f"Галичина Bot - це електронний помічник клану Галичина. Створений для зручнішого проживання у місті. "
                                      f"Ось все, що я вмію (поки що), у майбутньому цей список буде поповнитися з кожним оновленням: \n "
                                      f"\n `/debit` ** - [суму яку ви хочете покласти у скарбницю]**"
                                      f"\n `/credit` ** - [суму, яку ви хочете зняти з рахунку в скарбниці]**"
                                      f"\n `/new` ** - Переглянути список оновлень**"
                                      f"\n `/register` ** - Зареєструватися у системи Галичинни**"
                                      f"\n `/donat` ** - Підтримка роботи бота** "
                                      f"\n `/poll` ** - [питання]"
                                      f"\n `/balance` ** - Сумма всіх діамантів у скарбниці (тільки для адміністраціі)",
                          colour=discord.Colour.from_rgb(0, 0, 255))
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/996726573434671154/996780435457724477/2.png")
    embed.set_footer(text=f"Творець: Zicnet \nВерсія: 1.2.2")
    await ctx.reply(embed=embed)


# Команды

@slash.slash_command(description='Зареєструватися у системи Галичинни', options=[
    Option("minecraftnick", description="Майнкрафт нік", type=OptionType.STRING, required=True)
])
async def register(ctx, minecraftnick: str):
    member = ctx.author
    cur.execute(f"SELECT userid FROM accounting.accounting WHERE(userid = {member.id})")
    record = cur.fetchall()
    if len(record) == 0:
        cur.execute(
            f"INSERT INTO accounting.accounting(userid,minecraftNick,debit,credit) VALUES({member.id}, '{minecraftnick}',0, 0)")
        role = discord.utils.get(member.guild.roles, id=995722908305457332)
        await member.add_roles(role)
        await ctx.author.send(
            embed=discord.Embed(
                title="Повідомлення",
                description=f"Ви зарееструвалися",
                colour=discord.Colour.from_rgb(0, 255, 0)
            ))
    con.commit()
    if len(record) >= 1:
        await ctx.author.send(
            embed=discord.Embed(
                title="Повідомлення",
                description=f"Ти дебіл, інструкцію читай. Прописувати команду ТІЛЬКИ один під час реєстрації в системі",
                colour=discord.Colour.from_rgb(70,255,230)
            ))

message_id = 0 # Переменная для сообщения голосования

@slash.slash_command(description='Провести опитування', options=[
    Option("content", description="Текст питання", type=OptionType.STRING, required=True)
])
async def poll(ctx,content):
    embed = discord.Embed(title=f'Голосование',
                        description=f"{content}",
                        colour=discord.Color.purple())
    embed.set_footer(text='Голосування триватиме 3 хвилини')
    message = await ctx.send(embed=embed)
    await message.add_reaction('✅')
    await message.add_reaction('❌')
    global message_id
    message_id = message.id
    await sleep(5)
    embed = discord.Embed(title=f'Повідомлення',
                        description=f"Пройшла хвилина",
                        colour=discord.Colour.from_rgb(0, 255, 0))
    embed.set_footer(text='Залишилося 2 хвилину')
    await ctx.send(embed=embed)
    await sleep(5)
    embed = discord.Embed(title=f'Повідомлення',
                        description=f"Пройшли 2 хвилини",
                        colour=discord.Colour.from_rgb(0, 255, 0))
    embed.set_footer(text='Залишилося 1 хвилину')
    await ctx.send(embed=embed)
    await sleep(5)
    channel = ctx.channel
    message = await channel.fetch_message(message_id)
    resactions = [reaction for reaction in message.reactions if reaction.emoji in ['✅', '❌']]
    result = ''
    for reaction in resactions:
        result += reaction.emoji + ": " + str(reaction.count - 1)
    emb = discord.Embed(title=f'Результат',
                        description='Підсумок голосування: ' + str(result),
                        colour=discord.Colour.from_rgb(70,255,230))
    await ctx.send(embed=emb)
    await ctx.author.send(embed=emb)


@slash.slash_command(
    description='Покласти до скарбниці',
    options=[
        Option("message", description="Кіл-сть діамантів", type=OptionType.INTEGER, required=True)
    ])
async def debit(ctx, message):
    member = ctx.author
    cur.execute(f"SELECT userid FROM accounting.accounting WHERE(userid = {member.id})")
    record = cur.fetchall()
    if len(record) <= 0:
        await ctx.author.send(
            embed=discord.Embed(
                title="Повідомлення",
                description=f"**Спочатку зарееструйтись - `/register`\n Більш детально можно прочитати, прописавши команду - `/start`**",
                colour=discord.Colour.from_rgb(0, 255, 0)
            ))
    elif len(record) >= 1:
        cur.execute(f"SELECT debit FROM accounting.accounting WHERE(userid ={member.id})")
        fet_debit_output = cur.fetchone()
        i = int(fet_debit_output[0])
        message_int = int(message)
        debit_input = i + message_int
        cur.execute(f"UPDATE accounting.accounting SET debit = {debit_input} WHERE(userid = {member.id})")
        con.commit()
        channel = bot.get_channel(998100162247409764)
        embed=discord.Embed(
            title="Повідомлення",
            description=f"{ctx.author.mention} поклав до скарбниці `{message}` діамантів.",
            colour=discord.Colour.from_rgb(0, 255, 0)
        )
        embed.set_footer(text=f"{datetime.now()}")
        await channel.send(embed=embed)

        await ctx.author.send(
            embed=discord.Embed(
                title="Повідомлення",
                description=f"Ви поклали до скарбниці `{message}` діамантів.\n Сумма всіх попередніх депозитів покладенних до скарбниці `{debit_input}`",
                colour=discord.Colour.from_rgb(0, 255, 0)
            ))


@slash.slash_command(  # обход
    description='Узяти с скарбниці',
    options=[
        Option("message", description="Кіл-сть діамантів", type=OptionType.INTEGER, required=True)
    ])
async def credit(ctx, message):
    member = ctx.author
    cur.execute(f"SELECT userid FROM accounting.accounting WHERE(userid ={member.id})")
    record = cur.fetchall()
    if len(record) <= 0:
        await ctx.author.send(
            embed=discord.Embed(
                title="Повідомлення",
                description=f"**Спочатку зарееструйтись - `/register`\n Більш детально можно прочитати, прописавши команду - `/start`**",
                colour=discord.Colour.from_rgb(0, 255, 0)
            ))
    elif len(record) >= 1:
        cur.execute(f"SELECT debit FROM accounting.accounting WHERE(userid = {member.id})")
        fet_debit_output = cur.fetchone()
        i = int(fet_debit_output[0])
        message_int = int(message)
        debit_input = i - message_int
        cur.execute(f"UPDATE accounting.accounting SET debit = {debit_input} WHERE(userid = {member.id})")
        con.commit()
        channel = bot.get_channel(998100162247409764)
        embed=discord.Embed(
            title="Повідомлення",
            description=f"{ctx.author.mention} узяв с скарбниці `{message}` діамантів.",
            colour=discord.Colour.from_rgb(0, 255, 0)
        )
        embed.set_footer(text=f"{datetime.now()}")
        await channel.send(embed=embed)
        await ctx.author.send(
            embed=discord.Embed(
                title="Повідомлення",
                description=f"Ви узяли з скарбниці `{message}` діамантів.\n Сумма всіх попередніх депозитів покладенних до скарбниці `{debit_input}`",
                colour=discord.Colour.from_rgb(0, 255, 0)
            ))


@slash.slash_command(description='Сумма всіх діамантів у скарбниці', )
@commands.has_any_role(995718829625851976)
async def balance(ctx):
    cur.execute("SELECT SUM(debit) FROM accounting.accounting")
    sum_fet = cur.fetchone()
    sum = int(sum_fet[0])
    con.commit()
    embed = discord.Embed(title="Інформація",
                          description=f"Сумма всіх діамантів у скарбниці: `{sum}`",
                          colour=discord.Colour.from_rgb(0, 0, 255))
    await ctx.reply(embed=embed)

@slash.slash_command(description='Информація про себе', )
async def info(ctx):
    member = ctx.author
    cur.execute(f"SELECT id FROM accounting.accounting WHERE(userid = {member.id})")
    fet_id = cur.fetchone()
    id = int(fet_id[0])
    con.commit()
    cur.execute(f"SELECT debit FROM accounting.accounting WHERE(userid = {member.id})")
    fet_debit = cur.fetchone()
    debit_output = int(fet_debit[0])
    con.commit()
    cur.execute(f"SELECT minecraftNick FROM accounting.accounting WHERE(userid = {member.id})")
    fet_nick = cur.fetchone()
    nick = str(fet_nick[0])
    con.commit()
    embed = discord.Embed(title="Інформація",
                          description=f"ID: `{id}` | Майнкрафт ник: `{nick}\n`"
                                      f"Сумма `{debit_output}` діамантів на вашому рахунку у скарбниці",
                          colour=discord.Colour.from_rgb(0, 0, 255))
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"{datetime.now()}")
    await ctx.reply(embed=embed)

@bot.command()
async def support(ctx):
    user = bot.get_user(296642001619648513)
    embed = discord.Embed(
        title="Повідомлення",
        description = f"Я клоун не зміг зареєструватися. Моє ім'я {ctx.author.mention},зв'яжиться зі мною",
        colour=discord.Colour.from_rgb(0, 255, 0))
    await user.send(embed=embed)
    embed = discord.Embed(
        title="Повідомлення",
        description=f"Чекайте... З вами зв'яжуться ",
        colour=discord.Colour.from_rgb(126,75,255))
    await ctx.author.send(embed=embed)

@bot.event
async def on_member_join(member):
    embed = discord.Embed(title="Повідомлення",
                          description=f"Галичина Bot - це електронний помічник клану Галичина. Створений для зручнішого проживання у місті. "
                                      f"\n Для проходження першого этапу отримання громадянство напишить у чат «**__Регистация__**» команду `/register`"
                                      f"\n УВАГА: коректної реєстрації використовуйте слэш-команди",
                          colour=discord.Colour.from_rgb(126, 75, 255))
    embed.set_footer(text="Уважно читайте 'підказки', коли пишите команди")
    await member.send(embed=embed)


@bot.event
async def on_ready():
    print(f'{datetime.now()} ON READY')
    while True:
        await bot.change_presence(status=discord.Status.online, activity=discord.Game("Zicnet"))
        await sleep(15)
        await bot.change_presence(status=discord.Status.online, activity=discord.Game("#StandWithUkraine"))
        await sleep(15)
        await bot.change_presence(status=discord.Status.online, activity=discord.Game("/donat = Підтримка"))
        await sleep(15)

print(f'{datetime.now()} BOT START')
bot.run(settings['token'])


