import discord
from discord.ext import commands

class bot_on(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='.', intents=discord.Intents.all())
    #Adiciona os botões sempre que o bot inicia para não ter que usar o comando novamente
    async def setup_hook(self):
        self.add_view(entrarnafila())
        self.add_view(sairdafila())

client = bot_on()

@client.command()
async def fila(ctx: commands.Context):
    embed = discord.Embed(
        title='Fila de Controle',
        colour=discord.Colour(5763719),
    )
    #Adiciona o botão entrar
    view1 = entrarnafila()
    #Adiciona o botão sair, na mesma linha
    view1.add_item(sairdafila().children[0])
    # Salva IDs da mensagem e do canal
    mensagem = await ctx.send(embed=embed, view=view1)
    with open("mensagem_info.txt", "w") as file:
        file.write(f"{mensagem.id}\n{ctx.channel.id}")


class entrarnafila(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Entrar na fila', custom_id='entranafila', style=discord.ButtonStyle.success)
    async def entrar(self, interact: discord.Interaction, button: discord.ui.Button):
        user = interact.user.id

        # Ler IDs da mensagem e do canal
        with open("mensagem_info.txt", "r") as file:
            mensagem_id, canal_id = map(int, file.read().split())

        # Obter o canal e a mensagem
        guild = interact.guild
        canal = guild.get_channel(canal_id)
        mensagem = await canal.fetch_message(mensagem_id)
        novo_embed1 = mensagem.embeds[0]  
        user_mention = f'<@{user}>'
        user_in_queue = any(field.value.startswith(f'> {user_mention}') for field in novo_embed1.fields)
        if not user_in_queue:
            novo_embed1.add_field(name='', value=f'> {user_mention}', inline=False)
            await mensagem.edit(embed=novo_embed1)
        await interact.response.defer()


class sairdafila(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Sair da fila', custom_id='sairfila', style=discord.ButtonStyle.danger)
    async def sair(self, interact: discord.Interaction, button):
        user = interact.user.id
        # Ler IDs da mensagem e do canal
        with open("mensagem_info.txt", "r") as file:
            mensagem_id, canal_id = map(int, file.read().split())

        # Obter o canal e a mensagem
        guild = interact.guild
        canal = guild.get_channel(canal_id)
        mensagem = await canal.fetch_message(mensagem_id)

        novo_embed1 = mensagem.embeds[0]  # Obtém o embed atual da mensagem

        new_fields = []
        for idx, field in enumerate(novo_embed1.fields):
            if not field.value.startswith(f'> <@{user}>'):
                new_fields.append(field)
        
        # Atualiza o embed removendo o campo do usuário
        novo_embed1.clear_fields()
        for field in new_fields:
            novo_embed1.add_field(name=field.name, value=field.value, inline=False)

        await mensagem.edit(embed=novo_embed1)
        await interact.response.defer()

client.run('Seu Token aqui')
