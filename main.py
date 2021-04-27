from flask import Flask, render_template, request, redirect, url_for
from GOST import GOST
import my_utils as my_ut

app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template('index.html')


@app.route('/encrypt', methods=['POST'])
def encrypt():
    op_mode = request.form['enc-op-mode']
    plaintext = request.form['enc-plaintext']
    password = request.form['enc-password']
    choose_salt = request.form['choose-salt']
    if choose_salt == "Yes":
        salt = request.form['salt-input']
    else:
        salt = None
    gost = GOST()
    gost.set_operation_mode(op_mode)
    gost.set_message(my_ut.string_to_bytes(plaintext))
    key, salt = my_ut.pbkdf2(password, salt)
    gost.set_key(key)
    ciphertext = my_ut.leading_zeros_hex(gost.encrypt())
    if op_mode != "ECB":
        iv = my_ut.leading_zeros_hex(gost.get_iv())
    else:
        iv = None
    return render_template('encrypt.html', op_mode=op_mode, plaintext=plaintext, salt=salt, iv=iv, ciphertext=ciphertext)


@app.route('/decrypt', methods=['POST'])
def decrypt():
    op_mode = request.form['dec-op-mode']
    ciphertext = request.form['dec-ciphertext']
    password = request.form['dec-password']
    salt = request.form['salt-textarea-dec']
    gost = GOST()
    gost.set_operation_mode(op_mode)
    gost.set_encrypted_msg(my_ut.hex_to_bin_mult_64(ciphertext))
    key, salt = my_ut.pbkdf2(password, salt)
    gost.set_key(key)
    if op_mode != "ECB":
        iv = request.form['iv-textarea']
        gost.set_iv(my_ut.hex_to_bin_mult_64(iv))
    else:
        iv = None
    plaintext = my_ut.bytes_to_string(gost.decrypt())
    if plaintext is not None:
        return render_template('decrypt.html', op_mode=op_mode, ciphertext=ciphertext, salt=salt, iv=iv, plaintext=plaintext)
    else:
        return redirect(url_for('decrypt_error'))


@app.route('/decrypt/error')
def decrypt_error():
    return render_template('decrypt_error.html')


@app.route("/info", methods=['GET'])
def info():
    return render_template("info.html")


app.run(host="0.0.0.0", port=42069, debug=True)  # , ssl_context=('server-cert.pem', 'server-key.pem'))
