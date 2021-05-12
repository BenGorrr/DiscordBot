# -*- coding: utf-8 -*-
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
import time, os
import lyricsgenius, discord
from discord.ext import commands

""" useful attribute:
        element.tag_name
        element.text
        element.get_attribute('value')
"""

class Lyrics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.lyricsMethod = 1

    @commands.command(help="Set lyric search method, 1. mulanci, 2.kugeci, 3.genius")
    async def method(self, ctx, m=None):
        if m:
            await ctx.send("Changed method: {} -> {}".format(self.lyricsMethod, m))
            self.lyricsMethod = m
        else:
            await ctx.send("Current method: {}".format(self.lyricsMethod))

    @commands.command(aliases=['lyrics'])
    async def lyric(self, ctx, *, name=None):
        if name:
            content = self.getLyric(name, int(self.lyricsMethod))
            if content != "":
                #await ctx.send(content)
                embed = discord.Embed(
                    title = "Lyrics:",
                    description = content
                )
                await ctx.send(embed=embed)
        else:
            await ctx.send("Please type the song name as \".lyrics name\"")

    def exportText(self, filename, text):
        with open(filename, mode='w', encoding="utf-8") as file:
            file.write(text)

    def mulanciGetLyric(self, driver, name):
        url = "https://www.mulanci.org/zhs/search/#gsc.tab=0&gsc.q="

        driver.get(url+name)

        link_div = driver.find_element_by_class_name('gs-title')
        link_a = link_div.find_element_by_class_name('gs-title')
        link = link_a.get_attribute("data-ctorig")
        #driver.close()
        driver.get(link)
        try:
            content_div = driver.find_element_by_id('lyric-content')
            content = content_div.text
            self.exportText("text.txt", content)
        except NoSuchElementException:
            content = ""
        driver.close()
        return content

    def kugeciGetLyric(self, driver, name):
        url = "https://www.kugeci.com/search?q="

        driver.get(url+name)
        try:
            link_a = driver.find_element_by_css_selector('#tablesort tbody tr td a')
            link = link_a.get_attribute("href")
            driver.get(link)
            content_div = driver.find_element_by_id("lyricsContainer")
            content = content_div.text
            self.exportText("text.txt", content)
        except NoSuchElementException:
            content = ""
        driver.close()
        return content

    def geniusGetLyric(self, name):
        """ Using lyricsgenius wrapper to get lyrics from genius """
        genius = lyricsgenius.Genius(os.environ.get('GENIUS_ACCESS_TOKEN', '-1'))
        song = genius.search_song(name)
        #print(song)
        if song:
            return song.lyrics
        return ""

    def filterLyric(self, lyrics, method=1):
        """ filter out unwanted text in the lyric list
            method 1 is for mulanci filtering
            method 2 is for kulanci filtering
        """
        if method == 1:
            for i in lyrics[10:]:
                if i.find("：") != -1:
                    index = lyrics[10:].index(i) + 10
                    lyrics = lyrics[:index]
                    self.exportText("text.txt", "\n".join(lyrics))
                    break
            for i in range(len(lyrics)):
                if lyrics[i] != '':
                    if lyrics[i][0] == "[":
                        lyrics = lyrics[:i]
                        break
        elif method == 2:
            #list comprehension, for lyric in lyrics, if lyric start with '[', remove the first 9 characters
            # else lyric remains same
            lyrics = [lyric[10:] if lyric[0] == '[' else lyric for lyric in lyrics]
        return "\n".join(lyrics)

    def getLyric(self, name, method):
        """ wrapper for different site scrap"""
        if method == 1 or method == 2:
            gChromeOptions = webdriver.ChromeOptions()
            gChromeOptions.add_argument("window-size=1920x1480")
            gChromeOptions.add_argument("disable-dev-shm-usage")
            gChromeOptions.add_argument('headless')
            driver = webdriver.Chrome(
                chrome_options=gChromeOptions, executable_path=ChromeDriverManager().install()
            )
            #DRIVER_PATH = r"C:\Program Files (x86)\chromedriver.exe"
            #op = webdriver.ChromeOptions()
            #op.add_argument('headless')
            #driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=op)

        lyric = ""
        if method == 1: #mulanci search
            lyric = self.mulanciGetLyric(driver, name)
        elif method == 2: #kugeci search
            lyric = self.kugeciGetLyric(driver, name)
        elif method == 3: #genius search
            lyric = self.geniusGetLyric(name)
        if lyric != "":
            lyric = lyric.split("\n")
            lyric = self.filterLyric(lyric, method=method)
        else:
            print("Can't find lyric")
        self.exportText("text_filtered.txt", lyric)
        return lyric

def setup(bot):
    bot.add_cog(Lyrics(bot))

if __name__ == '__main__':
    name = "Best part"
    getLyric(name, 3)
