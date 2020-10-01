from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.popup import Popup
import smtplib, ssl


def sendEmail(destinatario, messaggio):
    port = 587
    smtp_server = "smtp.gmail.com"
    sender_email = "pythontestapp12@gmail.com"
    password = "***"
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.login(sender_email, password)
        server.sendmail(sender_email, destinatario, messaggio)


class WindowManager(ScreenManager):
    pass


class LoginWindow(Screen):
    loginemail = ObjectProperty(None)
    loginpassword = ObjectProperty(None)

    def submitLogin(self):
        if self.checkLogin():
            show_popup(Logged, "Logged in")
        else:
            show_popup(NotLogged, "Wrong data")

    def checkLogin(self):
        with open("database.txt", "r") as f:
            for line in f.readlines():
                if line == self.loginemail.text + ";" + self.loginpassword.text + "\n":
                    return True
            return False

    def clearData(self):
        self.loginemail.text = ""
        self.loginpassword.text = ""


class RegisterWindow(Screen):
    registerusername = ObjectProperty(None)
    registeremail = ObjectProperty(None)
    registerpassword = ObjectProperty(None)

    def submitRegister(self):
        if not self.checkInvalid() and not self.alreadyMade():
            with open("database.txt", "a") as f:
                f.write(self.registeremail.text + ";" + self.registerpassword.text + "\n")
            messaggio = f"Ti sei registrato usando come username {self.registerusername.text} e hai messo come password {self.registerpassword.text}.\nAesh\nAeshhh"
            sendEmail(self.registeremail.text, messaggio)
            self.clearData()
            show_popup(Registrated, "Registration")

    def checkInvalid(self):
        if len(self.registerusername.text) < 3:
            show_popup(ShortUsername, "Invalid Username")
            return True
        elif len(self.registerusername.text) > 15:
            show_popup(LongUsername, "Invalid Username")
            return True
        if "@" not in self.registeremail.text or not "." in self.registeremail.text or self.registeremail.text[
            0] == "@" or self.registeremail.text[-1] == "@" or self.registeremail.text[-1] == "." or \
                self.registeremail.text[self.registeremail.text.find("@") + 1] == "." or self.registeremail.text.count(
                "@") > 1 or ",;?!\\^()" in self.registeremail.text:
            show_popup(InvalidEmail, "Invalid e-mail")
            return True
        if len(self.registerpassword.text) < 5:
            show_popup(ShortPassword, "Invalid Password")
            return True
        elif len(self.registerpassword.text) > 50:
            show_popup(LongPassword, "Invalid Password")
            return True
        return False

    def alreadyMade(self):
        with open("database.txt", "r") as f:
            for line in f.readlines():
                if self.registeremail.text in line:
                    show_popup(AlreadyMade, "Error")
                    return True
            return False

    def clearData(self):
        self.registeremail.text = ""
        self.registerusername.text = ""
        self.registerpassword.text = ""


class ShortUsername(FloatLayout):
    pass


class LongUsername(FloatLayout):
    pass


class InvalidEmail(FloatLayout):
    pass


class ShortPassword(FloatLayout):
    pass


class LongPassword(FloatLayout):
    pass


class Registrated(FloatLayout):
    pass


class AlreadyMade(FloatLayout):
    pass


class Logged(FloatLayout):
    pass


class NotLogged(FloatLayout):
    pass


def show_popup(c, title):
    popupWindow = Popup(title=title, content=c(), size_hint=(.6, .4))
    popupWindow.open()


kv = Builder.load_file("kvfile.kv")


class MyApp(App):
    def build(self):
        return kv

if __name__ == "__main__":
    MyApp().run()

