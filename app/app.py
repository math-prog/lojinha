import telegram
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackContext
from sqlalchemy.orm import sessionmaker
from database import init_db, criar_cliente, criar_produto, registrar_venda
import os
from dotenv import load_dotenv
import logging

# Configuração de logs
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Carrega as variáveis de ambiente
load_dotenv()

# Verifica se as variáveis de ambiente estão presentes
TOKEN = os.getenv("TELEGRAM_TOKEN")
DB_URL = os.getenv("DATABASE_URL")

logger.info(f"Token encontrado: {'Sim' if TOKEN else 'Não'}")
logger.info(f"Database URL encontrada: {'Sim' if DB_URL else 'Não'}")

if not TOKEN:
    raise ValueError("TELEGRAM_TOKEN não encontrado no arquivo .env")

if not DB_URL:
    raise ValueError("DATABASE_URL não encontrado no arquivo .env")

# Inicializa o banco de dados
try:
    engine = init_db()
    Session = sessionmaker(bind=engine)
    logger.info("Conexão com o banco de dados estabelecida com sucesso")
except Exception as e:
    logger.error(f"Erro ao conectar com o banco de dados: {str(e)}")
    raise

async def start_function(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        logger.info(f"Comando /start recebido do usuário {update.effective_user.id}")
        await update.message.reply_text("Olá! Bem-vindo ao bot de vendas.\n"
                                      "Comandos disponíveis:\n"
                                      "/cadastrar_cliente - Cadastra um novo cliente\n"
                                      "/cadastrar_produto - Cadastra um novo produto\n"
                                      "/registrar_venda - Registra uma nova venda")
    except Exception as e:
        logger.error(f"Erro no comando start: {str(e)}")
        await update.message.reply_text("Desculpe, ocorreu um erro ao processar seu comando.")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(f"Update {update} causou o erro {context.error}")

async def register_product(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Selecionar os produtos com saldo

    # Informar da escolha, a quantidade disponível para a compra
    
    await update.message.reply_text("Vc escolheu cadstrar um novo produto.")

async def register_sell(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    await update.message.reply_text("Vc escolheu cadastrar uma nova venda.")

def main():
    try:
        logger.info("Iniciando o bot...")
        app = ApplicationBuilder().token(TOKEN).build()
        
        # Handlers
        app.add_handler(CommandHandler("start", start_function))
        app.add_handler(CommandHandler("cadastrar_produto", register_product))
        app.add_handler(CommandHandler("registrar_venda", register_sell))
        app.add_error_handler(error_handler)
        
        logger.info("Bot iniciado com sucesso! Aguardando comandos...")
        app.run_polling()
        
    except Exception as e:
        logger.error(f"Erro fatal ao iniciar o bot: {str(e)}")
        raise

if __name__ == '__main__':
    main()