import jinja2
import markdown
import regex
from DiscordMessages import DiscordServer


HarryCrankyMsgs = DiscordServer(
    r"C:\DLs\Mini-Python\Discord Messages\Harry_Cranky chat logs.txt"
)


class JinjaMessage(object):
    def __init__(self, msg):
        pfp = {
            "Cranky": "./assets/pfp/Cranky.jpg",
            "SomeoneHarry": "./assets/pfp/Harry.jpg",
            "JesusOfAV": "./assets/pfp/Jesus.jpg",
            "CyborgDemonMan": "./assets/pfp/Cyborg.jpg",
        }
        url_reg = regex.compile("(https?://[^\s]+)")
        self.text = msg.content
        if self.text.find("<") or self.text.find(">"):
            self.text = regex.sub("<", "&lt;", self.text)
            self.text = regex.sub(">", "&gt;", self.text)
        self.text = regex.sub(r"\n", r"\n<br>\n", self.text, regex.I)
        self.text = regex.sub("~~(.*?)~~", r"<del>\1</del>", self.text, regex.I)
        self.text = regex.sub("__(.*?)__", r"<u>\1</u>", self.text, regex.I)
        self.text = url_reg.sub(r'<a href="\1">\1</a>', self.text)
        self.text = markdown.markdown(self.text)
        self.text = regex.sub("<p>|</p>", "", self.text)
        self.time = msg.time.strftime("%m-%d %I:%M %p")
        self.user = msg.user
        self.pfp = pfp[msg.user]


msgs = HarryCrankyMsgs.messages[::-1][:50][::-1]
# msgs = HarryCrankyMsgs.messages

jmsgs = [JinjaMessage(msg) for msg in msgs]


jfile = (
    jinja2.Environment(
        loader=jinja2.FileSystemLoader("./"),
        extensions=["jinja_markdown.MarkdownExtension"],
    )
    .get_template("discord_template_css.html")
    .render(title="SomeoneHarry", messages=jmsgs)
)

with open("DiscordMessages_test_css.html", "w", encoding="utf-8") as f:
    f.write(jfile)
