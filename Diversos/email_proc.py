#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
import socket

hostname = socket.gethostname()
sender = 'joahannes@lrc.ic.unicamp.br'
receivers = ['joahannes@gmail.com']

# define header
headers = """From: Joahannes Costa <joahannes@lrc.ic.unicamp.br>
To: <joahannes@gmail.com>
Subject: Status de Simulação
"""

# define body
body = """Prezado, Joahannes Bruno Dias da Costa

Sua simulação TERMINOU. :)

att,

"""
# message + hostname
message = headers + body + hostname 

try:
   smtpObj = smtplib.SMTP('atena')
   smtpObj.sendmail(sender, receivers, message)
   print "Email enviado com sucesso!"
except SMTPException:
   print "Erro: não foi possível enviar o email."

