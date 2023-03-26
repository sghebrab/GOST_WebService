from flask import Flask, render_template, request, redirect, url_for
import my_utils
import ctypes

OP_MODES = {"ECB": 0, "CBC": 1, "OFB": 2, "CFB": 3, "CTR": 4}

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

    plaintext_as_bin_str = my_utils.string_to_bytes(plaintext)
    # If plaintext in binary form is not multiple of 64, pad it to the right with enough zeros
    if len(plaintext_as_bin_str) % 64 != 0:
        plaintext_as_bin_str += "0"*((len(plaintext_as_bin_str)//64 + 1)*64 - len(plaintext_as_bin_str))
    # Now, take 64 binary characters at a time and convert them to an int
    plaintext_as_int_arr = []
    for i in range(0, len(plaintext_as_bin_str), 64):
        plaintext_as_int_arr.append(int(plaintext_as_bin_str[i:i+64], 2))

    # Do the same for the key
    key, salt = my_utils.pbkdf2(password, salt)
    key_as_int_arr = []
    for i in range(0, 256, 32):
        key_as_int_arr.append(int(key[i:i+32], 2))

    # Load the shared library
    lib = ctypes.cdll.LoadLibrary('./GOST.so')

    # Define the argument and return types for the encrypt function
    lib.encrypt.argtypes = [
        ctypes.POINTER(ctypes.c_uint64),  # uint64_t *blocks
        ctypes.c_uint32,                  # uint32 blocks_len
        ctypes.POINTER(ctypes.c_uint32),  # uint32_t *sub_keys
        ctypes.c_uint8,                   # uint8 op_mode
        ctypes.c_uint64,                  # uint64_t iv
        ctypes.POINTER(ctypes.c_uint64),  # uint64_t *result
    ]
    lib.encrypt.restype = None

    # Always generate an IV for simplicity, even if ECB is used
    lib.generate_iv.argtypes = []
    lib.generate_iv.restype = ctypes.c_uint64
    iv = lib.generate_iv()

    # This is e pointer to the result, as the encrypt function returns void but modifies the array in place
    ciphertext_ptr = (ctypes.c_uint64 * len(plaintext_as_int_arr))()

    # Call the C function with all the arguments needed
    lib.encrypt((ctypes.c_uint64 * len(plaintext_as_int_arr))(*plaintext_as_int_arr), len(plaintext_as_int_arr),
             (ctypes.c_uint32 * 8)(*key_as_int_arr), OP_MODES[op_mode], iv, ciphertext_ptr)

    # Load data starting from the pointer, at the end you will have a list of 64-bit integers
    ciphertext = [ciphertext_ptr[i] for i in range(len(plaintext_as_int_arr))]

    # Now, just for representation, convert the integer result to hex form
    ciphertext_as_hex_str = ""
    for i in range(len(ciphertext)):
        ciphertext_as_hex_str += my_utils.leading_zeros_hex(bin(ciphertext[i])[2:].zfill(64))

    return render_template('encrypt.html', op_mode=op_mode, plaintext=plaintext, salt=salt, iv=hex(iv)[2:].zfill(16), ciphertext=ciphertext_as_hex_str)


@app.route('/decrypt', methods=['POST'])
def decrypt():
    op_mode = request.form['dec-op-mode']
    ciphertext = request.form['dec-ciphertext']
    password = request.form['dec-password']
    salt = request.form['salt-textarea-dec']

    # Ciphertext is a hex string, so take 16 chars at a time and convert them to an int
    ciphertext_as_int_arr = []
    for i in range(0, len(ciphertext), 16):
        ciphertext_as_int_arr.append(int(ciphertext[i:i+16], 16))

    # Same logic for the key
    key, salt = my_utils.pbkdf2(password, salt)
    key_as_int_arr = []
    for i in range(0, 256, 32):
        key_as_int_arr.append(int(key[i:i+32], 2))

    if op_mode != "ECB":
        iv = int(request.form['iv-textarea'], 16)
    else:
        iv = 0

    # Load the shared library
    lib = ctypes.cdll.LoadLibrary('./GOST.so')

    lib.decrypt.argtypes = [
        ctypes.POINTER(ctypes.c_uint64),  # uint64_t *blocks
        ctypes.c_uint32,                  # uint32 blocks_len
        ctypes.POINTER(ctypes.c_uint32),  # uint32_t *sub_keys
        ctypes.c_uint8,                   # uint8 mode
        ctypes.c_uint64,                  # uint64_t iv
        ctypes.POINTER(ctypes.c_uint64),  # uint64_t *result
    ]
    lib.decrypt.restype = None
    plaintext_ptr = (ctypes.c_uint64 * len(ciphertext_as_int_arr))()

    # Call the C function with all the arguments needed
    lib.decrypt((ctypes.c_uint64 * len(ciphertext_as_int_arr))(*ciphertext_as_int_arr), len(ciphertext_as_int_arr),
             (ctypes.c_uint32 * 8)(*key_as_int_arr), OP_MODES[op_mode], iv, plaintext_ptr)

    # Same as before, plaintext is a pointer so you have to load data starting from it
    plaintext = [plaintext_ptr[i] for i in range(len(ciphertext_as_int_arr))]

    # Take the integers, convert them to binary (with 0 padding), then convert the whole binary result to UTF-8
    plaintext_as_bin_str = ""
    for i in range(len(plaintext)):
        plaintext_as_bin_str += bin(plaintext[i])[2:].zfill(64)
    plaintext = my_utils.bytes_to_string(plaintext_as_bin_str)

    if plaintext is not None:
        return render_template('decrypt.html', op_mode=op_mode, ciphertext=ciphertext, salt=salt, iv=request.form['iv-textarea'] if iv != 0 else None, plaintext=plaintext)
    else:
        return redirect(url_for('decrypt_error'))


@app.route('/decrypt/error')
def decrypt_error():
    return render_template('decrypt_error.html')


@app.route("/info", methods=['GET'])
def info():
    return render_template("info.html")

