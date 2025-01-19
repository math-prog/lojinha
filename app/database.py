from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os
from datetime import datetime

Base = declarative_base()

class Cliente(Base):
    __tablename__ = 'cliente'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    endereco = Column(String)
    contato = Column(String)
    
    vendas = relationship("Venda", back_populates="cliente")

class Catalogo(Base):
    __tablename__ = 'catalogo'
    
    id = Column(Integer, primary_key=True)
    nome_produto = Column(String)
    qtd = Column(Integer)
    imagem_produto = Column(String)
    valor_unt = Column(Float)
    unidade_medida = Column(String)
    
    movimentacoes = relationship("MovimentacaoEstoque", back_populates="produto")
    vendas = relationship("Venda", back_populates="produto")

class MovimentacaoEstoque(Base):
    __tablename__ = 'movimentacao_estoque'
    
    id = Column(Integer, primary_key=True)
    produto_id = Column(Integer, ForeignKey('catalogo.id'))
    tipo = Column(String)  # 'entrada' ou 'saida'
    quantidade = Column(Integer)
    data = Column(DateTime, default=datetime.now())
    
    produto = relationship("Catalogo", back_populates="movimentacoes")

class Venda(Base):
    __tablename__ = 'venda'
    
    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey('cliente.id'))
    produto_id = Column(Integer, ForeignKey('catalogo.id'))
    qtd = Column(Integer)
    metodo_pagamento = Column(String)
    data = Column(DateTime, default=datetime.now())
    
    cliente = relationship("Cliente", back_populates="vendas")
    produto = relationship("Catalogo", back_populates="vendas")

# Função para inicializar o banco de dados
def init_db():
    database_url = os.getenv('DATABASE_URL')
    if not database_url or database_url.strip() == 'DATABASE_URL':
        raise ValueError("Invalid or unset DATABASE_URL environment variable.")
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    return engine


# Funções de CRUD para Cliente
def criar_cliente(session, nome, endereco, contato):
    cliente = Cliente(nome=nome, endereco=endereco, contato=contato)
    session.add(cliente)
    session.commit()
    return cliente

def buscar_cliente(session, cliente_id):
    return session.query(Cliente).filter(Cliente.id == cliente_id).first()

# Funções de CRUD para Catalogo
def criar_produto(session, nome, qtd, imagem, valor, unidade):
    produto = Catalogo(
        nome_produto=nome,
        qtd=qtd,
        imagem_produto=imagem,
        valor_unt=valor,
        unidade_medida=unidade
    )
    session.add(produto)
    session.commit()
    return produto

def atualizar_estoque(session, produto_id, quantidade, tipo):
    movimento = MovimentacaoEstoque(
        produto_id=produto_id,
        quantidade=quantidade,
        tipo=tipo
    )
    session.add(movimento)
    
    produto = session.query(Catalogo).filter(Catalogo.id == produto_id).first()
    if tipo == 'entrada':
        produto.qtd += quantidade
    else:
        produto.qtd -= quantidade
    
    session.commit()

# Função para registrar venda
def registrar_venda(session, cliente_id, produto_id, qtd, metodo_pagamento):
    venda = Venda(
        cliente_id=cliente_id,
        produto_id=produto_id,
        qtd=qtd,
        metodo_pagamento=metodo_pagamento
    )
    session.add(venda)
    
    # Atualiza o estoque
    atualizar_estoque(session, produto_id, qtd, 'saida')
    
    session.commit()
    return venda