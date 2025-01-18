import telegram
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackContext
from sqlalchemy.orm import sessionmaker
from database import init_db, criar_cliente, criar_produto, registrar_venda
import os
from dotenv import load_dotenv

load_dotenv()

# Inicializa o banco de dados
engine = init_db()
Session = sessionmaker(bind=engine)

API_TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start_function(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Olá! Bem-vindo ao bot de vendas.\n"
                                  "Comandos disponíveis:\n"
                                  "/cadastrar_cliente - Cadastra um novo cliente\n"
                                  "/cadastrar_produto - Cadastra um novo produto\n"
                                  "/registrar_venda - Registra uma nova venda")

async def cadastrar_cliente(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    session = Session()
    try:
        # Exemplo simples - em produção você deve implementar um fluxo de conversação
        args = context.args
        if len(args) < 3:
            await update.message.reply_text("Use: /cadastrar_cliente nome endereco contato")
            return
            
        nome = args[0]
        endereco = args[1]
        contato = args[2]
        
        cliente = criar_cliente(session, nome, endereco, contato)
        await update.message.reply_text(f"Cliente cadastrado com ID: {cliente.id}")
    
    finally:
        session.close()

async def cadastrar_produto(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    session = Session()
    try:
        args = context.args
        if len(args) < 5:
            await update.message.reply_text("Use: /cadastrar_produto nome quantidade imagem valor unidade")
            return
            
        produto = criar_produto(
            session,
            nome=args[0],
            qtd=int(args[1]),
            imagem=args[2],
            valor=float(args[3]),
            unidade=args[4]
        )
        await update.message.reply_text(f"Produto cadastrado com ID: {produto.id}")
    
    finally:
        session.close()

app = ApplicationBuilder().token(API_TOKEN).build()
app.add_handler(CommandHandler("start", start_function))
app.add_handler(CommandHandler("cadastrar_cliente", cadastrar_cliente))
app.add_handler(CommandHandler("cadastrar_produto", cadastrar_produto))

if __name__ == '__main__':
    app.run_polling()