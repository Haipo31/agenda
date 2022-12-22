from flask import render_template, request, redirect, flash, url_for,session
from main import db, app
from models.evento import Evento
from models.usuario import Usuario

#jean
from controller import authjean
import calendar

@app.route('/')
def index():
    print(session)
    if session:
        if (session['usuario_logado'] == True):
            print("Entrou")

            cal = calendar.Calendar(firstweekday=6)
            DIAS_DA_SEMANA = ("SUNDAY", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY")
            calDays = cal.monthdayscalendar(2022, 12)

            return render_template('calendario.html', calDays=calDays, aux=0, DIAS_DA_SEMANA=DIAS_DA_SEMANA)
        else:
            return redirect(url_for('login'))
    else:
        return redirect('/login')

@app.route('/novo-usuario')
def novo():
    return render_template('cadastro-usuario.html', titulo = 'Criar Novo Usuário')

@app.route('/cadastrar-usuario', methods = ['POST'])
def cadastro_usuario():

    nome = request.form['nome']
    userName = request.form['username']
    senha = request.form['senha'] #ver com a parte do Jean.

    usuario = Usuario.query.filter_by(username = userName).first()
    
    if usuario:
        flash('Usuário já cadastrado')
        return redirect(url_for('index'))
    
    novo_usuario = Usuario(nome = nome, username = userName, senha = senha)
    
    db.session.add(novo_usuario)

    db.session.commit()

    return redirect(url_for(index))

#url_for chama a função.
# nome, hora e descrição
# nome de usuario e senha

@app.route('/login')
def login():
    return render_template('login.html', titulo = 'Login Usuario')

@app.route('/autenticar', methods=['POST',])
def autenticar():
    autenticado = authjean.validaLogin(request.form['usuario'], request.form['senha'])
    
    print("Esta logado ou não")
    print(autenticado)
    
    if autenticado == True:
        session['usuario_logado'] = True

        flash('Logado com sucesso')

        return redirect(url_for("index"))
    return redirect(url_for("login"))
@app.route('/logout')
def logout():
    session.clear()
    session['usuario_logado'] = False
    print(session)
    flash('VOCE FOi DESCONECTADO')
    return redirect(url_for('login'))

@app.route('/cadastrar-evento')
def cadastrar_evento():
    
    data_evento = request.form['data_evento']
    titulo_evento = request.form['titulo_evento']
    descricao_evento = request.form['descricao_evento']
    publico = request.form['publico']
    ativo = request.form['ativo']

    evento = Evento.query.filter_by(data_evento = data_evento).first()
    
    if evento:
        flash('Já existe um evento nessa data')
        return redirect(url_for('calendario'))

    novo_evento = Evento(data_evento = data_evento, titulo_evento = titulo_evento, descricao_evento = descricao_evento, publico = publico, ativo = ativo)
    
    db.session.add(novo_evento)

    db.session.commit()

    return redirect(url_for('calendario'))

@app.route('/calendario')
def calendario():
    return render_template('calendario.html')

@app.route('/editar/<int:id>')
def editar(id):

    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proximo = url_for('editar')))
    evento = Evento.query.filter_by(id=id).first() #verificar qual é o ID que virá, se é do usuário ou do evento.
    return render_template('HTML DO EDITAR - COLOCAR AQUI', titulo = 'Editar Evento', evento = evento)

@app.route('/deletar/<int:id>')
def deletar(id):

    if 'usuario_logado' not in session or session['usuario_logado' == None]:
        return redirect(url_for('login'))
    
    Evento.query.filter_by(id=id).delete()

    db.session.commit()

    flash('Evento deletado com sucesso')
    return redirect(url_for('index'))