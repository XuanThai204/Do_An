from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2

app = Flask(__name__)
app.secret_key = 'secret_key'

DATABASE_CONFIG = {
    'dbname': 'dbtest',
    'user': 'postgres',
    'password': '123456',
    'host': 'localhost',
    'port': 5432
}

def get_db_connection():
    conn = psycopg2.connect(**DATABASE_CONFIG)
    return conn

@app.route('/')
def dangnhap():
    return render_template('dangnhap.html')

@app.route('/dangnhap', methods=['POST'])
def handle_dangnhap():
    username = request.form['username']
    password = request.form['password']
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, password FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    
    if user and check_password_hash(user[1], password):
        session['user_id'] = user[0]
        session['username'] = username
        return redirect(url_for('giaodienchinh'))
    else:
        return render_template('dangnhap.html', error='Tên tài khoản hoặc mật khẩu không đúng.')

@app.route('/dangky')
def dangky():
    return render_template('dangky.html')

@app.route('/dangky', methods=['POST'])
def handle_register():
    username = request.form['username']
    password = request.form['password']
    hashed_password = generate_password_hash(password)
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM users WHERE username = %s", (username,))
    user_exists = cur.fetchone()
    
    if user_exists:
        cur.close()
        conn.close()
        return render_template('dangky.html', error='Tên tài khoản đã tồn tại. Vui lòng chọn tên khác.')
    
    cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
    conn.commit()
    cur.close()
    conn.close()
    
    return redirect(url_for('dangnhap'))

@app.route('/giaodienchinh', methods=['GET', 'POST'])
def giaodienchinh():
    if 'user_id' not in session:
        return redirect(url_for('dangnhap'))

    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT id, mssv, name, grade, major, phone FROM students")
    students = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('giaodienchinh.html', username=session['username'], students=students)

@app.route('/themhocsinh', methods=['GET', 'POST'])
def themhocsinh():
    if 'user_id' not in session:
        return redirect(url_for('dangnhap'))
    
    if request.method == 'POST':
        mssv = request.form['mssv']
        name = request.form['ten']
        grade = request.form['diem']
        major = request.form['nganh']
        phone = request.form['sdt']
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO students (mssv, name, grade, major, phone) VALUES (%s, %s, %s, %s, %s)",
            (mssv, name, grade, major, phone)
        )
        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for('giaodienchinh'))

    return render_template('themhocsinh.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('dangnhap'))

@app.route('/xoa_hocsinh/<int:student_id>', methods=['GET'])
def xoa_hocsinh(student_id):
    if 'user_id' not in session:
        return redirect(url_for('dangnhap'))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id = %s", (student_id,))
    conn.commit()
    cur.close()
    conn.close()

    # Thêm thông báo vào session
    session['message'] = 'Xóa sinh viên thành công!'

    return redirect(url_for('giaodienchinh'))



if __name__ == '__main__':
    app.run(debug=True)
