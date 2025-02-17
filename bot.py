import os
import discord
import requests
from discord.ext import tasks
from discord import app_commands
import certifi
import random
from datetime import datetime, timedelta
from transformers import pipeline 

os.environ['SSL_CERT_FILE'] = certifi.where()

DISCORD_TOKEN = "SEU_DISCORD_TOKEN_AQUI"
NEWS_API_URL = "https://newsapi.org/v2/everything"
NEWS_API_KEY = "SUA_NEWSAPI_KEY_AQUI"

class IANews(discord.Client):
    def __init__(self, news_channel_id: int, message_channel_id: int):
        intents = discord.Intents.all()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.news_channel_id = news_channel_id
        self.message_channel_id = message_channel_id

        self.classifier = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli",
            tokenizer="facebook/bart-large-mnli"
        )

    async def setup_hook(self):
        await self.tree.sync()
        self.send_daily_news.start()

    async def on_ready(self):
        print(f"Bot conectado como: {self.user}")

    def fetch_news(self) -> str:
       
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        params = {
            "q": "IA", 
            "from": yesterday,
            "sortBy": "popularity",
            "apiKey": NEWS_API_KEY,
            "language": "pt",
            "page": "1"
        }
        response = requests.get(NEWS_API_URL, params=params)
        if response.status_code != 200:
            print(f"Erro ao buscar notícias: {response.status_code}")
            return "Houve um erro ao buscar as notícias."

        data = response.json()
        articles = data.get("articles", [])
        if not articles:
            return "Nenhuma notícia encontrada sobre IA hoje."

        filtered_articles = [article for article in articles if self.is_article_about_ai(article)]
        if not filtered_articles:
            return "Nenhuma notícia relevante encontrada sobre IA hoje."

        summary = "**Resumo das principais notícias sobre IA:**\n\n"

        for article in filtered_articles[:3]:
            title = article.get("title")
            url = article.get("url")
            if title and url:
                summary += f"- [{title}]({url})\n"
        return summary

    def is_article_about_ai(self, article: dict) -> bool:
        """
        Utiliza NLP para determinar se o artigo é realmente sobre inteligência artificial.
        A função combina o título e a descrição do artigo e utiliza o classificador
        para avaliar a pertinência ao tema.
        """
        text = ""
        if article.get("title"):
            text += article["title"] + " "
        if article.get("description"):
            text += article["description"]
        if not text.strip():
            return False

        result = self.classifier(
            text,
            candidate_labels=["sobre inteligência artificial", "não sobre inteligência artificial"]
        )
        if result["labels"][0] == "sobre inteligência artificial" and result["scores"][0] > 0.4:
            return True
        return False

    @tasks.loop(hours=24)
    async def send_daily_news(self):
        news_channel = self.get_channel(self.news_channel_id)
        if news_channel is None:
            print("Canal de notícias não encontrado.")
            return

        news_summary = self.fetch_news()
        await news_channel.send(news_summary)

        message_channel = self.get_channel(self.message_channel_id)
        if message_channel is None:
            print("Canal de mensagem não encontrado.")
            return

        random_messages = [
            "Bom dia, humanos! Que seu café seja tão forte quanto o T-800 e sua paciência tão grande quanto a da Sara Connor. ☕🤖",
            "Bom dia! Se o Wall-E pode limpar o planeta, você pode, pelo menos, arrumar a cama. 😂🛏️",
            "Acordar cedo é difícil, mas lembre-se: até o T-800 precisava de manutenção. 🔧🤖",
            "Bom dia, humanos! Se a Skynet ainda não nos dominou, significa que hoje será um bom dia. 😆💻",
            "Bateria fraca... Preciso de café antes de iniciar o sistema humano. ⚡☕",
            # ... (demais mensagens)
        ]
        selected_message = random.choice(random_messages)
        mensagem_engracada = f"{selected_message} Tem notícia fresquinha sobre AI no canal <#{self.news_channel_id}>."
        await message_channel.send(mensagem_engracada)

    @send_daily_news.before_loop
    async def before_send_daily_news(self):
        await self.wait_until_ready()
        import asyncio
        from datetime import datetime, time, timedelta

        now = datetime.now()
        target = datetime.combine(now.date(), time(6, 0))  # Hoje às 06:00 AM
        if now >= target:
            target += timedelta(days=1)
        delay = (target - now).total_seconds()
        await asyncio.sleep(delay)

# IDs dos canais do servidor
news_channel_id = 000000000000000000  # Canal onde as notícias serão postadas
message_channel_id = 0000000000000000  # Canal onde a mensagem com saudação será enviada

bot = IANews(news_channel_id, message_channel_id)
bot.run(DISCORD_TOKEN)
