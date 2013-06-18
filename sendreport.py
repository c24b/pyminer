import os, csv 
from time import gmtime, strftime
from datetime import datetime
import smtplib
from jinja2 import Environment, FileSystemLoader

def print_html_doc(twitter, facebook):
	title ="Bilan veille Hello Bank !"
	now = datetime.now()
	date = now.strftime("%d Juin %Y %H:%M")
	THIS_DIR = os.path.dirname(os.path.abspath(__file__))
	j2_env = Environment(loader=FileSystemLoader(THIS_DIR),
	trim_blocks=True)
	return j2_env.get_template('template.html').render(
	title=title, date=date, twitter=twitter, facebook= facebook)

def createhtmlmail (html, text, subject, fromEmail):
	"""Create a mime-message that will render HTML in popular
	MUAs, text in better ones"""
	import MimeWriter
	import mimetools
	import cStringIO

	out = cStringIO.StringIO() # output buffer for our message 
	htmlin = cStringIO.StringIO(html)
	txtin = cStringIO.StringIO(text)

	writer = MimeWriter.MimeWriter(out)
	#
	# set up some basic headers... we put subject here
	# because smtplib.sendmail expects it to be in the
	# message body
	#
	writer.addheader("From", fromEmail)
	writer.addheader("Subject", subject)
	writer.addheader("MIME-Version", "1.0")
	#
	# start the multipart section of the message
	# multipart/alternative seems to work better
	# on some MUAs than multipart/mixed
	#
	writer.startmultipartbody("alternative")
	writer.flushheaders()
	#
	# the plain text section
	#
	subpart = writer.nextpart()
	subpart.addheader("Content-Transfer-Encoding", "quoted-printable")
	pout = subpart.startbody("text/plain", [("charset", 'us-ascii')])
	mimetools.encode(txtin, pout, 'quoted-printable')
	txtin.close()
	#
	# start the html subpart of the message
	#
	subpart = writer.nextpart()
	subpart.addheader("Content-Transfer-Encoding", "quoted-printable")
	#
	# returns us a file-ish object we can write to
	#
	pout = subpart.startbody("text/html", [("charset", 'us-ascii')])
	mimetools.encode(htmlin, pout, 'quoted-printable')
	htmlin.close()
	#
	# Now that we're done, close our writer and
	# return the message body
	#
	writer.lastpart()
	msg = out.getvalue()
	out.close()
	return msg

def send_report(msg):
	html = unicode(msg).encode('utf-8')
	text = 'test version'
	date = strftime("%d-%M %Hh%M:", gmtime())
	subject = "Bilan Hello Bank! du %s" %date
	message = createhtmlmail(html, text, subject, 'From Constance de Quatrebarbes <constance@quatrebarbes.com>')
	server = smtplib.SMTP("smtp.gmail.com","587")
	# Credentials (if needed)
	username = 'labomatixxx'
	password = 'Lavagea70degres'

	# The actual mail send
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.starttls()
	server.login(username,password)
	server.sendmail('labomatixxx@gmail.com', 'constance@comptoirsdumultimedia.com', message)
	server.quit()
	return 'ok'


