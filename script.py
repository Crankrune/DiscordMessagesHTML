import jinja2
import markdown
import regex
from DiscordMessages import DiscordServer, msg_with_context


# HarryCrankyMsgs = DiscordServer(
#     r"C:\DLs\Mini-Python\Discord Messages\Harry_Cranky chat logs.txt"
# )

onehundred = DiscordServer(
    filename="C:/DLs/Mini-Python/Discord Messages/💯chat logs_2020-06-07_14-06-00.txt",
    server_id="696904961828847627",
)


class JinjaMessage(object):
    def __init__(self, msg):
        pfp = {
            "Cranky": "./assets/pfp/Cranky.jpg",
            "Crankrune": "./assets/pfp/Cranky.jpg",
            # "SomeoneHarry": "./assets/pfp/Harry.jpg",
            "SomeoneHarry": "./assets/pfp/Harry_old.jpg",
            "JesusOfAV": "./assets/pfp/Jesus.jpg",
            # "CyborgDemonMan": "./assets/pfp/Cyborg.jpg",
            "CyborgDemonMan": "./assets/pfp/Cyborg_og.jpg",
        }
        url_reg = regex.compile("(https?://[^\s]+)")
        self.text = msg.content
        if self.text:
            if self.text.find("<") or self.text.find(">"):
                self.text = regex.sub("<", "&lt;", self.text)
                self.text = regex.sub(">", "&gt;", self.text)
            self.text = regex.sub("(?:^|\n)(?:\s|\n)*(?:\>|&gt;)\s*(.+)\n?", r'<div class="quote"><div class="blockquoteDivider"></div><blockquote><p>\1</p></blockquote></div>', self.text, regex.I | regex.M)
            self.text = regex.sub(r"\n", r"\n<br>\n", self.text, regex.I)
            self.text = regex.sub("~~(.*?)~~", r"<del>\1</del>", self.text, regex.I)
            self.text = regex.sub("__(.*?)__", r"<u>\1</u>", self.text, regex.I)
            self.text = regex.sub("\|\|(.*?)\|\|", r'<a class="spoiler">\1</a>', self.text, regex.I)
            self.text = url_reg.sub(r'<a class="link" href="\1">\1</a>', self.text)
            self.text = markdown.markdown(self.text)
            self.text = regex.sub("<p>|</p>", "", self.text)
        
        if msg.attachment_list:
            embeds = []
            for atch in msg.attachment_list:
                embeds.append(f'<img src="{atch}" align="left" class="embed"></img>')
            embeds_text = '<div class="embed-container">\n' + "\n".join(embeds) + '\n</div>\n'
            self.text = self.text + "\n" + embeds_text
        
        if msg.time.year == 2020:
            self.time = msg.time.strftime("%Y-%m-%d %I:%M %p")
        else:
            self.time = msg.time.strftime("%m-%d %I:%M %p")
        self.user = msg.user
        self.pfp = pfp[msg.user]


# msgs = HarryCrankyMsgs.messages[::-1][:50][::-1]
# msgs = HarryCrankyMsgs.messages

msgs = msg_with_context(
    list(onehundred.messages),
    msg_id="704246290967429462",
    count=90,
    with_id=True,
    align="right",
    get_list=True,
    _print=False,
)

jmsgs = [JinjaMessage(msg) for msg in msgs]


jfile = (
    jinja2.Environment(
        loader=jinja2.FileSystemLoader("./"),
        extensions=["jinja_markdown.MarkdownExtension"],
    )
    .get_template("discord_template_css.html")
    .render(title="💯", messages=jmsgs)
)

with open("100_convo_1.html", "w", encoding="utf-8") as f:
    f.write(jfile)
