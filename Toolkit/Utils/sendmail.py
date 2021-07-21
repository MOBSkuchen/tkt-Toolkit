import smtplib, time, random
def sendmail(froms, getter, subject, mail, email_login, pw_login, port, server):
    try:
        msg = str("From: Sendmail <" + getter + ">") + "\n"
        msg = msg + time.strftime("%a, %d %b %Y %H:%M:%S +0200", time.gmtime()) + "\n"
        msg = msg + "Message-ID: <Sendmail" + str(random.uniform(1000000, 9999999)) + "@gmail.com>" + "\n"
        msg = msg + "Subject: " + subject + "\n"
        msg = msg + "To: " + getter + "\n\n"
        msg = msg + mail + "\n"
        print(msg)
        server = smtplib.SMTP_SSL(server, port)
        server.login(email_login, pw_login)
        server.sendmail(
            getter,
            froms,
            msg)
        server.quit()
    except:
        print("...")
        print("Error: Cant send Mail.")
        print("...")