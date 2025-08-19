📝 Bills Bot
Descrição:
Bills Bot é um bot do Telegram para controle de gastos. Ele permite que usuários enviem áudios com informações de despesas, que são salvos localmente no servidor.

⚙️ Funcionalidades atuais
Receber mensagens de áudio do usuário.

Salvar os áudios localmente no servidor.

🚀 Tecnologias
Python 3.13

python-telegram-bot

python-dotenv para variáveis de ambiente

📝 Pré-requisitos
Ter o Python 3 instalado.

Ter o token do bot do Telegram (obtido via BotFather).

Instalar dependências:

bash
Copiar
Editar
pip install -r requirements.txt
Criar arquivo .env com:

ini
Copiar
Editar
TELEGRAM_TOKEN=seu_token_aqui
💻 Como rodar
bash
Copiar
Editar
# ativar ambiente virtual
venv\Scripts\activate  # Windows
# ou
source venv/bin/activate  # Mac/Linux

# rodar o bot
python bot.py
Depois, abra o Telegram e envie /start ou áudios para o bot.

📁 Estrutura do projeto
bash
Copiar
Editar
bills-bot/
├─ bot.py          # código do bot
├─ requirements.txt
├─ .env            # arquivo com token do bot
├─ venv/           # ambiente virtual
└─ audios/         # áudios enviados pelos usuários
