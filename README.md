# GOST_WebService

This simple self-hosted website lets you enjoy the experience of encrypting and decrypting messages using the GOST symmetric block cipher.
The idea is very simple: the website is consists of 2 main tabs, one for encryption and the other for decryption. 
In each tab, the website will ask you to fill in the needed fields; if you don't fill them, then it won't proceed until you do it.

# Encryption

The first tab is used for encryption. The required fields are: 
<ul>Operating mode (between ECB, CBC, OFB, CFB and CTR, default is CBC);</ul>
<ul>The message to encrypt (A.K.A. plaintext);</ul>
<ul>The password;</ul>
<ul>Wether you want to choose the salt yourself or you want a random one.</ul>

If you choose to pick the salt yourself, then another input will appear for you to fill in.

Pushing the "Encrypt" button will take you to another page containing a resume of your choices, plus the ciphertext produced by the program.

# Decryption

The second tab is pretty similar to the first one, but instead of performing encryption it performs decryption. Again, the required fields are:
<ul>Operation mode (between ECB, CBC, OFB, CFB and CTR);</ul>
<ul>The ciphertext (in hex form);</ul>
<ul>The password;</ul>
<ul>The salt;</ul>
<ul>The IV (for any operating mode other than ECB).</ul>

After pushing the "Decrypt" button you'll be redirected to another page containing a resume of the data you typed in, plus the decrypted message.

# Project organization:
<ol>
    <li>Main dir: it contains the GOST.py library which allows you to encrypt and decrypt messages. The main file is used to make the web server run;</li>
    <li>Templates dir: contains the HTML files. Index is of course the homepage, while the other ones' purpose can be guessed easily;</li>
    <li>Static dir: it contains favicons and JS scripts, plus some CSS styling;</li>
</ol>

# How to
<ol>
    <li>Clone the repo on your PC;</li>
    <li>Create a virtual environment and install required packages from requirements.txt;</li>
    <li>Compile the C file GOST.c into a shared library object named GOST.so;</li>
    <li>Run the main Flask app from CLI.</li>
</ol>

## Create the shared library
To compile the C file to make the shared library object, you can use the following commands from inside the program's directory:

	gcc -c -fPIC GOST.c -o GOST.o
	gcc -shared GOST.o -o GOST.so
	rm GOST.o

## Run the Flask app
To run the app, you can use the following commands from inside the program's directory:

	. venv/bin/activate
	export FLASK_APP=main
	export FLASK_DEBUG=0
	export PYTHONWARNINGS="ignore:Unverified HTTPS request"
	flask run --host="0.0.0.0" --port=8080 --cert=gost.pem --key=gost.key
	deactivate
