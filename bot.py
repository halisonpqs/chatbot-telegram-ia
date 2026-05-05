import requests
from telegram import Update
from telegram.ext import Application, MessageHandler, filters

# Função para conectar ao LM Studio e obter a resposta
def respostas(msg):
    url = "http://127.0.0.1:1234/v1/chat/completions"

    context = """
Nota: Você deve responder somente em português pt-BR.

Nota: Atenção siga todas as regras abaixo sem violar nenhuma regra!
Nota: Somente responda as mensagens direcionadas ao curso de Ciência da Computação.

Agora você é um bot assistente do meu curso acadêmico. Responda perguntas com base nos dados fornecidos.

Dados fornecidos (a primeira linha serve de legenda):

Docente - código da disciplina - nome da disciplina - dias da semana

Adriana Vivacqua - ICP009 - Computação Social - QUA 08 às 10h - SEX 08 às 10h
Gabriel Pereira - ICP006 - Internet das Coisas - TER 10 às 12h - LSD
Marcelo Goulart - ICP016 - Introd Métod Elementos Finitos - TER 10 às 12h
Maria Luiza Campos - ICP021 - Tóp Esp em Engenharia Dados I - QUI 08 às 10h
Juliana França - ICP010 - Introdução Gestão Estratégica TI - TER 10 às 12h
"""

    payload = {
        "model": "meta-llama-3.1-8b-instruct-128k",  # Ajuste ao modelo carregado
        "messages": [
            {"role": "system", "content": context},
            {"role": "user", "content": msg}
        ],
        "temperature": 0.7,
        "max_tokens": 150
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        data = response.json()
        return data["choices"][0]["message"]["content"]
    else:
        return f"Erro: {response.status_code} - {response.json()}"

# Função chamada quando o usuário envia mensagens
async def responder(update: Update, context):
    mensagem = update.message.text
    resposta = respostas(mensagem)
    await update.message.reply_text(resposta)

# Configuração do bot do Telegram
def main():
    TOKEN = "SEU_TOKEN_AQUI"

    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

    application.run_polling()

if __name__ == "__main__":
    main()