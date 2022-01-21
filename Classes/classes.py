from models import *
import discord
from discord.ext import commands
from run import isBen

class ClassesLinks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.engine = bot.engine
        #Base.metadata.create_all(self.engine)
        self.Session = bot.Session

    @commands.command(aliases=['links'])
    async def link(self, ctx, operation='all', code=' ', name=' '):
        """
            Operation:
            *Default* all (display all classes)  Usage: .link / .link all
            add (Add class)  Usage: .link add course_code course_name link type(L, T or P)
            delete (Delete Classes with course code)  Usage: .link delete course_code
        """
        # global s
        # s = Session() #create session object
        s = self.Session()
        try:
            if operation == "all":
                class_list = self.get_all_class(s)
                #print(class_list)
                embed = discord.Embed( #CREATE EMBED
                    title = "Classes:",
                    description = "Google Meet Links of Y2S3",
                    color = discord.Color.green()
                )
                #Add fields into embed
                for c in class_list:
                    class_links = c.urls
                    links_embed = ""
                    for class_link in class_links:
                        links_embed += "[{}]({}) ".format(class_link.url_name, class_link.url)
                    embed.add_field(name = c.course_name,
                            value = "{}: {}"\
                            .format(c.course_code, links_embed),
                            inline=False
                        )
                await ctx.send(embed=embed)
            elif operation == "add":
                if not code == ' ' and not name == ' ':
                    exist = False
                    class_list = self.get_all_class(s)
                    for c in class_list:
                        if c.course_code == code and c.course_name == name:
                            exist = True
                            await ctx.send("Class already exist!")
                            break
                    if not exist:
                        if self.add_class(s, code, name):
                            await ctx.send(f"Added {code}")
                        else: await ctx.send("Something went wrong!")
                    s.commit()
                else:
                    await ctx.send("Usage: .link add course_code course_name")
            elif operation == "delete":
                if not code == ' ':
                    if (self.delete_class_bycode(s, code)):
                        await ctx.send(f"Deleted {code}")
                    else: await ctx.send("Class not found!")
                    s.commit()
                else:
                    await ctx.send("Usage: .link delete course_code")
            else:
                await ctx.send("Invalid Operation\nAvailable Op: all(default/no args), add, delete")
        except:
            s.rollback()
            await ctx.send("Something went wrong!")
            raise
        finally:
            s.close()

    @commands.command(help="Usage: .editlink course_code link_name/title new_link")
    async def editlink(self, ctx, code=' ', url_name=' ', link=' ', type='link'):
        s = self.Session()
        try:
            if not code == ' ' and not link == ' ' and not url_name == ' ': #if all args given
                if type == 'link':
                    if self.update_link(s, code, url_name, link):
                    #if (update_classLink_bycode(s, code, link, c_type)):
                        await ctx.send(f"Updated {code} {url_name}")
                        s.commit()
                    else: await ctx.send("Link not found!")
                elif type == 'title':
                    if self.update_link_name(s, code, url_name, link):
                        await ctx.send(f"Updated {code} {link}")
                        s.commit()
            else:
                await ctx.send("Usage: .editlink course_code link_name new_link whattoedit(link(default), title)")
        except:
            s.rollback()
            await ctx.send("Something went wrong!")
            raise
        finally:
            s.close()

    @commands.command(help="Usage: .addlink course_code link_name new_link")
    async def addlink(self, ctx, code=' ', url_name=' ', link=' '):
        s = self.Session()
        try:
            if not code == ' ' and not link == ' ' and not url_name == ' ': #if all args given
                if self.add_link_bycode(s, code, url_name, link):
                    await ctx.send(f"Added {code} {url_name}")
                    s.commit()
                else: await ctx.send("Class not found!")
            else:
                await ctx.send("Usage: .addlink course_code link_name new_link")
        except:
            s.rollback()
            await ctx.send("Something went wrong!")
            raise
        finally:
            s.close()

    @commands.command(help="Usage: .deletelink course_code link_name")
    async def deletelink(self, ctx, code=' ', url_name=' '):
        s = self.Session()
        try:
            if not code == ' ' and not url_name == ' ': #if all args given
                if self.delete_link(s, code, url_name):
                # if add_link_bycode(s, code, url_name, link):
                    await ctx.send(f"Deleted {code} {url_name}")
                    s.commit()
                else: await ctx.send("Link not found!")
            else:
                await ctx.send("Usage: .deletelink course_code link_name")
        except:
            s.rollback()
            await ctx.send("Something went wrong!")
            raise
        finally:
            s.close()

    @commands.command(help="Delete all the class links from DB (only owner)")
    @commands.check(isBen)
    async def deleteallclass(self, ctx):
        #self.recreate_db()
        #await ctx.send("Deleted everything.")
        pass

    def recreate_db(self):
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)

    def add_class(self, s, code, name=" "):
        new_class = Classes(
            course_code = code,
            course_name = name
        )
        s.add(new_class)
        return 1

    def get_all_class(self, s):
        c = s.query(Classes).all()
        return c

    def get_class_byname(self, s, name):
        c = s.query(Classes).filter_by(course_name=name).first()
        return c

    def get_class_byid(self, s, id):
        c = s.query(Classes).get(id)
        return c

    def get_class_bycode(self, s, code):
        c = s.query(Classes).filter_by(course_code=code).first()
        return c

    def delete_class_byid(self, s, id):
        s.delete(self.get_class_byid(s, id))

    def delete_class_bycode(self, s, code):
        c = self.get_class_bycode(s, code)
        if c != None:
            s.delete(c)
            return 1
        else:
            print("Class not found")
            return 0

    def update_classCode_byid(self, s, id, new_code):
        c = self.get_class_byid(s, id)
        c.course_code = new_code

    def update_classCode_bycode(self, s, code, new_code):
        c = self.get_class_bycode(s, code)
        c.course_code = new_code

    def update_className_byid(self, s, id, new_name):
        c = self.get_class_byid(s, id)
        c.course_name = new_name

    def update_className_bycode(self, s, code, new_name):
        c = self.get_class_bycode(s, code)
        c.course_name = new_name

    def new_add(self, s):
        new_class = Classes(course_code="Acas", course_name="course name")
        new_link = Links(url_name="Tuto", url="meetlinkhere")
        new_class.urls.append(new_link)
        s.add(new_class)

    def add_link_byid(self, s, course_id, url_name, url):
        c = self.get_class_byid(s, course_id)
        new_link = self.Links(url_name=url_name, url=url)
        c.urls.append(new_link)

    def add_link_bycode(self, s, course_code, url_name, url):
        c = self.get_class_bycode(s, course_code)
        if c != None:
            new_link = Links(url_name=url_name, url=url)
            c.urls.append(new_link)
            return 1
        else:
            print("Class not found")
            return 0

    def get_all_links_in_course(self, s, course_code):
        return self.get_class_bycode(s, course_code).urls

    def update_link(self, s, course_code, url_name, new_link):
        urls = self.get_all_links_in_course(s, course_code)
        for l in urls:
            if l.url_name == url_name:
                l.url = new_link
                return 1
        return 0

    def update_link_name(self, s, course_code, url_name, new_name):
        urls = self.get_all_links_in_course(s, course_code)
        for l in urls:
            if l.url_name == url_name:
                l.url_name = new_name
                return 1
        return 0

    def delete_link(self, s, course_code, url_name):
        urls = self.get_all_links_in_course(s, course_code)
        for l in urls:
            if l.url_name == url_name:
                s.delete(l)
                return 1
        return 0

    def delete_all_links_in_course(self, s, course_code):
        urls = self.get_all_links_in_course(s, course_code)
        for l in urls:
            s.delete(l)

def setup(bot):
    bot.add_cog(ClassesLinks(bot))

if __name__ == '__main__':
    # add_class("AACS2034", "FCN")
    # add_class("AACS2284", "OS")
    # add_class("AAMS3163", "Algebra")
    # delete_class_byid(1)
    #update_classLink_byid(1, r'https://meet.google.com/xby-eben-awt?authuser=0')
    # c = get_class_byid(1)
    # print(c.course_code)
    # update_className_byid(2, "Operating System")
    #recreate_db()
    s = Session()
    #delete_link(s, "course name", "Tuto")
    #delete_class_byid(s, 1)
    #new_add(s)
    #update_link(s, "Tuto", "new link")
    #add_link_byid(s, 1, "Lec", "lec link")
    #s.commit()
    print(get_all_class(s))
    s.close()
    #pass
