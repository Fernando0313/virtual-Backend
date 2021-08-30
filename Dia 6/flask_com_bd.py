from flask import Flask,request
from flask_mysqldb import MySQL

app=Flask(__name__)

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='password'
app.config['MYSQL_DB']='empresa'
app.config['MYSQL_PORT']=3306
mysql=MySQL(app)

@app.route('/departamento',methods=['GET','POST'])
def inicio():
    if request.method=='GET':
        cur=mysql.connection.cursor()
        cur.execute("SELECT * FROM DEPARTAMENTOS")
        result=cur.fetchall()
        print(result)
        return 'Bienvenido a mi api'
    elif request.method=='POST':
        
        data=request.get_json()
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO DEPARTAMENTOS (NOMBRE) VALUES('%s')" % data['nombre'])
        mysql.connection.commit()
        print(data)
        return{
            "message":"Departamento creado"
        }, 201
if __name__=='__main__':
    app.run(debug=True)
