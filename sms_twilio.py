from twilio.rest import TwilioRestClient
import smtplib
import Tkinter as tk
def send_sms(to):
    try:
        client = TwilioRestClient("ACdfd1792e2ca520e1a669b216a9e125d0", "0fcacb480a7d2ecb13ca32ef16696322")
        client.messages.create(to=to, from_="+19382232505",
                               body="I am Okay !!!")
        popup = tk.Tk()
        popup.wm_title("success")
        label = tk.Label(popup, text="message sent", pady=10)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(popup, text="Okay", command=popup.destroy)
        button.pack()
        popup.mainloop()
    except:
        popup = tk.Tk()
        popup.wm_title("failed")
        label = tk.Label(popup, text="messages not sent", pady=10)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(popup, text="Okay", command=popup.destroy)
        button.pack()

def send_email(to):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("akarshan.gandotra@gmail.com", "passwordoftheemail")
        msg = "I am Okay"
        server.sendmail("akarshan.gandotra@gmail.com",to, msg)
        server.quit()
        popup = tk.Tk()
        popup.wm_title("success")
        label = tk.Label(popup, text="message sent", pady=10)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(popup, text="Okay", command=popup.destroy)
        button.pack()
        popup.mainloop()
    except:
        popup = tk.Tk()
        popup.wm_title("failed")
        label = tk.Label(popup, text="messages not sent", pady=10)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(popup, text="Okay", command=popup.destroy)
        button.pack()

