from flask import*
from flask import request
import datetime as dt
from flask import request, render_template
import os
import shutil as sl
import smtplib

def verify_mail(at,u,p):
	try:
	    sttt = smtplib.SMTP('smtp.domain.com', 587)
	    sttt.starttls()
	    sttt.login("user@domain.com", "password")
	    message="From:website name\nSubject:Login verification\nThank you for signing up with our website.\nYou can now login to members area using the details below:\nURL: \nUsername: "+u+"\nPassword: "+p+"\n\nThank you :)\n\nIf this was not you then you can delete your account."
	    sttt.sendmail("user@domain.com", at, message)
	    return "Y"
	except:
		return "X"

class arw:
		def add_issue(a):
			open("ISSUES/"+str(dt.datetime.now()).replace(":","").replace(".","")+".txt","a").write(a)
		def add_post(a,b):
				name="static/"+str(dt.datetime.now()).replace(":","").replace(".","")+" "+a
				open(name,"a").write(b)
		def get_content():
				l = os.listdir("static")
				#l.reverse()
				n=0
				k=""
				if (l==None):
					return ""
				else:
					while(len(l)>n):
						k=k+open("static/"+l[n],"r+").read()+"\n"
						n=n+1
					return k
		def create(a,b,c):
			if (a in os.listdir("ACC")):
				return "X"
			else:
				if (verify_mail(c,a,b)=="Y"):
					os.mkdir("ACC/"+a)
					os.mkdir("ACC/"+a+"/"+"Name-"+c)
					os.mkdir("ACC/"+a+"/"+"Password-"+b)
					return "Y"
				else:
					return "x"
		def change_pass(a,b):
			oo=os.listdir(("ACC/"+a))
			if ("Password-" in oo[0]):
				sl.rmtree("ACC/"+a+"/"+oo[0])
				os.mkdir("ACC/"+a+"/"+"Password-"+b)
			else:
				sl.rmtree("ACC/"+a+"/"+oo[1])
				os.mkdir("ACC/"+a+"/"+"Password-"+b)
			return "Y"
		def delete_comment(a):
				bc = os.listdir("static")
				n=0
				while(len(bc)>n):
					if(a == bc[n].split(" ")[2]):
						os.remove("static/"+bc[n])
					else:
						tg=""
					n=n+1
		def delete(a):
			arw.delete_comment(a)
			sl.rmtree("ACC/"+a)
		def verify(a,b):
				if (a in os.listdir("ACC")):
						f = os.listdir("ACC/"+a)
						n=0
						k=[]
						while(len(f) > n):
								if ("Password-"in f[n]):
										if(b == f[n].replace("Password-","")):
												k.append("d")
										else:
												jk=""
								else:
										jk=""
								n=n+1
						if (len(k)>0):
								return "Y"
						else:
								return "Xpassword"
				else:
						return "X"

app = Flask(__name__, static_folder="assets", template_folder=os.getcwd())

@app.route("/")
def main():
		return render_template("main.html")

@app.route("/create",methods=["GET","POST"])
def a():
		if (request.method == "POST"):
				c = request.form["name"]
				a = request.form["username"]
				b = request.form["password"]
				if (len(b)>5):
						if (len(a)<4):
							return render_template("create.html", msg="Please enter the valid username")
						else:
								r = arw.create(a,b,c)
								if (r == "X"):
									return render_template("create.html", msg="Account with this username already exist")
								elif(r == "x"):
									return render_template("create.html", msg="Enter the valid email ID")
								else:
									return render_template("create.html", msg="Your account has been made , now sign in with those credentials")
				else:
					return render_template("create.html", msg="Enter the password of more than 5 digits")
		else:
			return render_template("create.html", msg="none")

@app.route("/login",methods=["GET","POST"])
def b():
		if (request.method == "POST"):
				g = arw.verify(request.form["username"],request.form["password"])
				if (g == "X"):
					return render_template("login.html", msg="There is no such account")
				elif (g=="Xpassword"):
					return render_template("login.html", msg="Your password is wrong")
				else:
					return render_template("post.html", cttntbntt=arw.get_content(), username=username, msg="none")
		else:
			 return render_template("login.html", msg="none")

@app.route("/change_pss",methods=["GET","POST"])
def b1():
		if (request.method == "POST"):
			g = arw.change_pass(request.form["username"],request.form["password"])
			return render_template("post.htmt", msg="Your password has been changed", cttntbntt=arw.get_content())
		else:
			return render_template("reset.html")
tcca="""
Make sure you are 15+ and know the basics of tech and coding related stuffs.
"""
@app.route("/tc",methods=["GET"])
def mm():
    return tcca

@app.route("/post",methods=["GET","POST"])
def c():
		if (request.method == "POST"):
			if (len(request.form["text"])>3000):
				return render_template("post.html", msg="Don't exceed the limit of 3000 characters", cttntbntt=arw.get_content())
			elif (len(request.form["text"])<5):
				return render_template("post.html", msg="Enter the valid information", cttntbntt=arw.get_content())
			else:
				arw.add_post(request.form["username"],request.form["text"])
				return render_template("post.html", msg="none", cttntbntt=arw.get_content())
		else:
			return render_template("post.html", msg="none" , cttntbntt=arw.get_content())

@app.route("/refresh",methods=["GET"])
def e():
	return render_template("post.html", cttntbntt=arw.get_content())

@app.route("/delete",methods=["GET","POST"])
def d():
	if (request.method== "POST"):
			if(arw.verify(request.form["username"],request.form["password"])=="Y"):
				arw.delete(request.form["username"])
				arw.delete_comment(request.form["username"])
				return render_template("delete_arg.html")
			else:
				return render_template("delete.html", msg="Your password or username is wrong")
	else:
		return render_template("delete.html", msg="none")

@app.route("/delete_comment",methods=["GET","POST"])
def g():
	if (request.method == "POST"):
		if (request.form["text"] in os.listdir("ACC")):
			arw.delete_comment(request.form["text"])
			return render_template("post.html", msg="Your all comments are deleted", cttntbntt=arw.get_content())
		else:
			return "ERROR 501"
	else:
		return render_template("post.html", msg="none", cttntbntt=arw.get_content())

@app.route("/help",methods=["GET","POST"])
def f():
	if (request.method == "POST"):
		arw.add_issue(request.form["text"])
		return render_template("post.html", cttntbntt=arw.get_content(),msg="Your report has been submitted")
	else:
		return render_template("help.html")

@app.errorhandler(404)
def ls(e):
	return render_template("404.html")

if "__main__" == __name__:
	app.run()