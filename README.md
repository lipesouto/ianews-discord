# 🤖 AI News Bot – Discord


Um bot para Discord que busca e compartilha automaticamente notícias sobre Inteligência Artificial (IA), utilizando Processamento de Linguagem Natural (NLP) para identificar notícias relevantes a partir do contexto.

## 🚀 Funcionalidades

##### ✅ Busca de notícias: Coleta notícias recentes de IA usando a NewsAPI.
##### ✅ Filtragem com NLP: Utiliza Zero-Shot Classification (Hugging Face Transformers) para identificar se o artigo é realmente sobre IA.
##### ✅ Postagem automática: Publica diariamente um resumo das principais notícias em um canal específico do Discord.
##### ✅ Mensagens motivacionais: Envia mensagens engraçadas sobre IA e tecnologia em outro canal.
##### ✅ Execução programada: Funciona automaticamente a cada 24h, sem necessidade de intervenção manual.

## 🛠️ Tecnologias utilizadas
- [Discord.py] – Integração com Discord
- [Requests] – Requisições HTTP para buscar notícias
- [Transformers] – NLP para análise do contexto das notícias
- [Torch] – Suporte para execução do modelo de NLP
- [Certifi] – Certificados SSL seguros

## 🔧 Instalação e Configuração

1. Clone este repositório:
```sh
git clone https://github.com/seu-usuario/ai-news-bot.git
cd ai-news-bot
```

2. Crie um ambiente virtual (opcional, mas recomendado):

```sh
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:
```sh
pip install -r requirements.txt
```

4. Configure suas chaves de API no arquivo .env ou diretamente no código:
- `DISCORD_TOKEN` (Token do bot do Discord)
- `NEWS_API_KEY` (Chave da NewsAPI)

5. Execute o bot:
```sh
python bot.py
```

### 📌 Contribuições
Sinta-se à vontade para abrir `issues` ou enviar `pull requests` para melhorar o projeto! 🚀

[Discord.py]:https://discordpy.readthedocs.io/
[Requests]:https://
[Transformers]:https://
[Torch]:https://pytorch.org/
[Certifi]:https://pypi.org/project/certifi/


## License

Este projeto está sob a licença MIT.
