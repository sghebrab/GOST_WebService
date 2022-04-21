# GOST_WebService

This simple self-hosted website lets you enjoy the experience of encrypting and decrypting messages using the GOST cryptosystem.
The idea is very simple: the website is made of 2 main tabs, one for encrypting and the other one for decrypting. In each tab, the website will ask you to fill in the needed fields; if you don't fill them, then it won't proceed until you do it.

# Encryption

The first tab is used for encryption. The required fileds are: 
<ul>Operation mode (between ECB, CBC, OFB, OCB and CTR);</ul>
<ul>The message to encrypt (A.K.A. plaintext);</ul>
<ul>The password;</ul>
<ul>Wether you want to choose the salt yourself or if you want it randomly generated.</ul>

If you choose to pick the salt yourself, then another input will appear for you to fill in.

Pushing the "Encrypt" button will take you to another page containing a resume of your choices, plus the ciphertext produced by the program).

# Decryption

The second tab is pretty similar to the first one, but instead of performing encryption it performs decryption. Again, the required fields are:
<ul>Operation mode (between ECB, CBC, OFB, OCB and CTR);</ul>
<ul>The ciphertext (in hex form);</ul>
<ul>The password;</ul>
<ul>The salt;</ul>
<ul>The IV (if operation mode is NOT ECB).</ul>

After pushing the "Decrypt" button you'll be redirected to another page containing a resume of the data you typed in, plus the decrypted message.

# Project organization:

  1 - Main dir: it contains the GOST.py library which allows you to encrypt and decrypt messages. The main file is used to make the web server run.
  
  2 - Templates dir: contains the HTML files. Index is of course the homepage, while the other ones' purpose can be guessed easily.
  
  3 - Static dir: it contains favicons and JS scripts, plus some CSS styling.
