import discord
from discord.ext import commands, tasks
import random
from datetime import date

TOKEN = "tolken"
CANAL_ID = 1465496669700358164

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

usuarios = {}
meta_diaria = {}
fecha_actual = date.today()

metas_posibles = [
    {"tipo": "reciclar", "cantidad": 2, "texto": "♻️ Recicla 2 objetos hoy"},
    {"tipo": "reutilizar", "cantidad": 1, "texto": "🔁 Reutiliza 1 objeto hoy"},
    {"tipo": "reducir", "cantidad": 1, "texto": "🌱 Reduce un consumo hoy"}
]

@bot.event
async def on_ready():
    print("EcoBot con metas listo")
    if not tarea_diaria.is_running():
        tarea_diaria.start()

@tasks.loop(hours=24)
async def tarea_diaria():
    global fecha_actual, meta_diaria
    fecha_actual = date.today()
    meta = random.choice(metas_posibles)
    meta_diaria.clear()
    meta_diaria.update(meta)

    canal = bot.get_channel(CANAL_ID)
    if canal:
        await canal.send(
            "🌍 **Nueva meta del día**\n"
            + meta["texto"]
            + "\n¡Registra tus acciones con comandos!"
        )

    for u in usuarios:
        usuarios[u]["reciclar"] = 0
        usuarios[u]["reutilizar"] = 0
        usuarios[u]["reducir"] = 0

def get_user(user_id):
    if user_id not in usuarios:
        usuarios[user_id] = {
            "reciclar": 0,
            "reutilizar": 0,
            "reducir": 0,
            "puntos": 0
        }
    return usuarios[user_id]

@bot.command()
async def reciclar(ctx):
    user = get_user(ctx.author.id)
    user["reciclar"] += 1
    user["puntos"] += 1
    await ctx.send("♻️ Reciclaje registrado (+1 punto)")

@bot.command()
async def reutilizar(ctx):
    user = get_user(ctx.author.id)
    user["reutilizar"] += 1
    user["puntos"] += 2
    await ctx.send("🔁 Reutilización registrada (+2 puntos)")

@bot.command()
async def reducir(ctx):
    user = get_user(ctx.author.id)
    user["reducir"] += 1
    user["puntos"] += 3
    await ctx.send("🌱 Reducción registrada (+3 puntos)")

@bot.command()
async def progreso(ctx):
    user = get_user(ctx.author.id)

    progreso = user.get(meta_diaria.get("tipo", ""), 0)
    meta = meta_diaria.get("cantidad", 0)

    estado = "❌ Meta no cumplida"
    if progreso >= meta:
        estado = "✅ Meta cumplida"

    await ctx.send(
        f"📊 **Progreso de {ctx.author.name}**\n"
        f"♻️ Reciclado: {user['reciclar']}\n"
        f"🔁 Reutilizado: {user['reutilizar']}\n"
        f"🌱 Reducido: {user['reducir']}\n"
        f"⭐ Puntos: {user['puntos']}\n\n"
        f"{estado}"
    )

@bot.command()
async def meta(ctx):
    if meta_diaria:
        await ctx.send("🎯 Meta de hoy:\n" + meta_diaria["texto"])
    else:
        await ctx.send("⚠️ Aún no hay meta asignada")

bot.run(TOKEN)


#comandos:

#!reciclar
#!reutilizar
#!reducir
#!progreso
#!meta


