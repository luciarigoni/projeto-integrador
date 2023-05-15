from flask import Flask, render_template, url_for, request, g, jsonify
from mysql.connector import MySQLConnection, connect, Error

import sys

#No terminal Digite
#pip install flask
#pip install mysql-connector-python

app = Flask(__name__)

#Configuração das informações do servidor MYSQL
#Para acessar a base de dados utilize o endereço
#https://www.phpmyadmin.co/

app.config['MYSQL_HOST'] = 'sql10.freesqldatabase.com'
app.config['MYSQL_USER'] = 'sql10616390'
app.config['MYSQL_PASSWORD'] = 'Y2kIxARidQ'
app.config['MYSQL_DB'] = 'sql10616390'

db_config={'host':app.config['MYSQL_HOST'],
           'user':app.config['MYSQL_USER'],
           'password':app.config['MYSQL_PASSWORD'],
           'database':app.config['MYSQL_DB'],
           'raise_on_warnings': True
           }


#Para cada página html de haver um app.route
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/funcionarios')
def funcionarios():
    return render_template('funcionarios.html', Status='', dados='')

@app.route('/inserirFunc', methods=('GET', 'POST'))
def inserirFunc():

    if request.method == 'POST':
        idfunc = request.form['funcionarioid']
        nomec = request.form['nomecompleto']
        apelido = request.form['nomeapelido']
        cargo = request.form['cargo']
        usuario= request.form['usuario']
        senha= request.form['senha']
        telefone= request.form['telefone']

        query = "INSERT INTO funcionarios (funcionarioid, nomecompleto, nomeapelido, cargo, usuario, senha, telefone)\
                 VALUES (%s, %s, %s, %s, %s, %s, %s);"
        dados = (idfunc, nomec, apelido, cargo, usuario, senha, telefone)
        print(query, flush=True)
        sys.stdout.flush()
        data = ({'funcionarioid': idfunc, 'nomecompleto': nomec, 'nomeapelido': apelido,
                 'cargo': cargo, 'usuario': usuario, 'senha': senha, 'telefone': telefone})
        try:
            g.db = MySQLConnection(**db_config)
            cursor = g.db.cursor()
            cursor.execute(query, dados)
            g.db.commit()
            cursor.close()
            g.db.close()
        except Exception as error:
            return jsonify({'error': error})
        return render_template('funcionarios.html', Status='Ok', dados=data)
    else:
        return render_template('funcionarios.html', Status='Erro')

@app.route('/pesquisaFunc/', methods=('GET', 'POST'))
def pesquisaFunc():
    if request.method == 'POST':

        pesquisa= ('%' + request.form['pesquisar'] + '%')
        query = 'SELECT * FROM funcionarios WHERE nomecompleto LIKE %s'
        print(query +  ' ' + pesquisa)
        try:
            g.db = MySQLConnection(**db_config)
            cursor = g.db.cursor()
            cursor.execute(query, (pesquisa,))
            for (funcionarioid, nomecompleto, nomeapelido, cargo, usuario, senha, telefone) in cursor:
                data = ({'funcionarioid':funcionarioid, 'nomecompleto':nomecompleto, 'nomeapelido':nomeapelido,
                          'cargo':cargo, 'usuario':usuario, 'senha':senha, 'telefone':telefone})
            cursor.close()
            g.db.close()
        except Exception as error:
            return jsonify({'error': error})
        return render_template('funcionarios.html', Status='', dados=data)
    return render_template('funcionarios.html', title='Listar', Status='NE')

if __name__ == '__main__':
    app.run(debug=True)
