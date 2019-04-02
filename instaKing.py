from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
import time
import random
import urllib.request
import sys

pageLoadingWaitTime = 2
likeWaitTime = 10   # 3h LIKES 120 per hour max, 300 to 450 per day max (1,5x daily follow)
commentWaitTime = 10 # 2h COMMENTS 120 per hour max, 250 per day max
followWaitTime = 10  # RULE...h FOLLOW/UNFOLLOW 30 per hour max
saveImageWaitTime = 1

class bot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        #self.driver = webdriver.Chrome('/Users/lbillou/Documents/OTO/instaluv/chromedriver')
        self.driver = webdriver.Chrome('./chromedriver')

    def closeBrowser(self):
        self.driver.close()

    def login(self):
        # Function for logging in on instagram.com (FR)
        self.driver.get('https://www.instagram.com/')
        time.sleep(pageLoadingWaitTime)
        # Going to log in page
        login_button = self.driver.find_element_by_xpath("//a[@href='/accounts/login/?source=auth_switcher']")
        login_button.click()
        time.sleep(pageLoadingWaitTime)
        # FIlling in credentials
        user_name_field = self.driver.find_element_by_xpath("//input[@name='username']")
        user_name_field.clear()
        user_name_field.send_keys(self.username)
        password_field = self.driver.find_element_by_xpath("//input[@name='password']")
        password_field.clear()
        password_field.send_keys(self.password)
        password_field.send_keys(Keys.RETURN)
        time.sleep(pageLoadingWaitTime)
        return print("Logged in.")

    def retrievePostsFromHashtag(self, hashtag, scroll=1):
        # Funtion to retrieve posts from a specified hashtag
        self.driver.get('https://www.instagram.com/explore/tags/' + hashtag + '/?hl=fr')
        time.sleep(pageLoadingWaitTime)
        # Scrolling down for more posts
        for i in range(0, scroll): # retrieves 51 post's url
            self.driver.find_element_by_tag_name("html").send_keys(Keys.END)
            time.sleep(pageLoadingWaitTime)
        # Retrieving webelements and returning posts urls
        hrefs = self.driver.find_elements_by_xpath("//*[@href]")
        pic_hrefs = [elem.get_attribute('href') for elem in hrefs]
        pic_hrefs = [href for href in pic_hrefs if '/p/' in href]
        print('*** ' + str(len(pic_hrefs)) + ' posts retrieved from the hashtag "' + hashtag + '"')
        return pic_hrefs

    def likePost(self, instaPostLink):
        # Function to like a post using its URL link
        if self.driver.current_url != instaPostLink:
            self.driver.get(instaPostLink)
            time.sleep(pageLoadingWaitTime)
        try:
            self.driver.find_element_by_xpath("//*[@class='fr66n']")
        except NoSuchElementException:
            print("ERROR : like button not found")
            return False
        else:
            try:
                self.driver.find_element_by_xpath("//*[@class='glyphsSpriteHeart__filled__24__red_5 u-__7']")
            except NoSuchElementException:
                self.driver.find_element_by_xpath("//*[@class='fr66n']").click()
                print('Post liked > ' + instaPostLink)
                time.sleep(likeWaitTime)
                return True
            else:
                print('Post link  │ ' + instaPostLink)
                return False

    def commentPost(self, instaPostLink, commentsList):
        # Function to comment posts from posts url list
        if self.driver.current_url != instaPostLink:
            self.driver.get(instaPostLink)
            time.sleep(pageLoadingWaitTime)
        try:
            commentButton = lambda: self.driver.find_element_by_xpath("//button[@class='dCJp8 afkep _0mzm-']")
            commentButton().click()
        except NoSuchElementException:
            print("ERROR : comment button not found")
            return False
        try:
            commentField = lambda: self.driver.find_element_by_xpath("//*[@aria-label='Ajouter un commentaire...']")
            commentField().send_keys('')
            commentField().clear()
        except NoSuchElementException:
            print("ERROR : comment field not found")
            return False
        else:
            commentToWrite = commentsList[random.randint(0, len(commentsList)-1)]
            for letter in commentToWrite:
                commentField().send_keys(letter)
                time.sleep((random.randint(2, 10) / 50))
            time.sleep(pageLoadingWaitTime)
            commentField().send_keys(Keys.RETURN)
            print('Commented  > "' + commentToWrite + '"')
            time.sleep(commentWaitTime)
            return True

    def retrieveSrcFromPost(self, instaPostLink):
        # Funtion to retrieve image source link from post link
        if self.driver.current_url != instaPostLink:
            self.driver.get(instaPostLink)
            time.sleep(pageLoadingWaitTime)
        # FFVAD for image, _8jZFN for video image
        try:
            src_elem = self.driver.find_element_by_class_name('FFVAD')
        except NoSuchElementException:
            try:
                src_elem = self.driver.find_element_by_class_name('tWeCl')
            except NoSuchElementException:
                # 404 error when post has been deleted
                return False
        src_link = src_elem.get_attribute('src')
        if src_link == None:
            # src_link = None, src is not retrived within webElement...
            #print(str(self.driver.execute_script("var items = {}; for (index=0; index<arguments[0].attributes.length;++index) {items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;", src_elem)))
            return False
        else:
            return src_link

    def saveImage(self, imgSrc):
            # Function to save an image locally from its source link
            current_milli_time = lambda: int(round(time.time()))
            # Managing jpg vs mp4 from src
            fileExt = imgSrc.split('?')[0][-4:]
            if fileExt == '.jpg':
                filepath = "./photos/" + str(current_milli_time()) + str(fileExt)
            elif fileExt == '.mp4':
                filepath = "./videos/" + str(current_milli_time()) + str(fileExt)
            else:
                filepath = "./other/" + str(current_milli_time()) + str(fileExt)
            urllib.request.urlretrieve(imgSrc, filepath)
            print('File Saved > ' + filepath)
            time.sleep(saveImageWaitTime)
            return True

    def followFromPost(self, instaPostLink):
        # Function to follow a user from post link
        ###print('Follow...xxx')
        if self.driver.current_url != instaPostLink:
            self.driver.get(instaPostLink)
            time.sleep(pageLoadingWaitTime)
        self.driver.execute_script("window.scrollTo(0, 0);")
        try:
            # Get user's name
            name = self.driver.find_element_by_xpath("//*[@class='FPmhX notranslate nJAzx']").get_attribute('title')
            # Click on follow button, try if not already subscribed
            follow_button = self.driver.find_element_by_xpath("//*[@class='oW_lN _0mzm- sqdOP yWX7d        ']")
            follow_button.click()
            print('Followed   > ' + name)
            time.sleep(followWaitTime)
            return True
        except Exception:
            return False

def main():
    startTime = datetime.now()
    retrievedPosts = 0
    reachedPosts = 0
    likeCount = 0
    commentCount = 0
    followCount = 0
    savedCount = 0
    commentRate = 0.99
    followRate = 0.99

    commentsList = open('comments.csv').readlines()
    for i in range(len(commentsList)): commentsList[i] = commentsList[i][:-1]

    givenHashtags = sys.argv[1:]

    botUsername = 'l0b5@outlook.com'
    botPassword = 'instaluv'
    bizgo = bot(botUsername, botPassword)
    bizgo.login()

    for hashtag in givenHashtags:
        bizgoList = bizgo.retrievePostsFromHashtag(hashtag)
        retrievedPosts += len(bizgoList)

        #for i in range(1):
        for i in range(len(bizgoList)):
            print('-- ' + str(i+1) + '/' + str(len(bizgoList)) +' ---- ' + hashtag)
            reachedPosts += 1
            if bizgo.likePost(bizgoList[i]): likeCount += 1
            # COMMENT, 50% chance of happening
            #if random.random() < commentRate:
                #if bizgo.commentPost(bizgoList[i], commentsList): commentCount += 1
            #else: print('No comment │')
            # FOLLOW, top posts only : 9 first posts
            if random.random() < followRate:
                if bizgo.followFromPost(bizgoList[i]): followCount += 1
                else: print('Following  │')
            else: print('No follow  │')
            # SAVE, if src retrieved
            srcLink = bizgo.retrieveSrcFromPost(bizgoList[i])
            if srcLink:
                bizgo.saveImage(srcLink)
                savedCount += 1
            else: print('No src file│')

    print('-----------')
    print('')
    print('Hashtags : [' + str(givenHashtags) + ']')
    print('Total  : ' + str(retrievedPosts) + ' -> ' + str(reachedPosts))
    print('')
    print('Likes : ' + str(likeCount) + ' │ ' + str(round(likeCount/reachedPosts, 2)*100) + '%')
    print('Comments : ' + str(commentCount) + ' │ ' + str(round(commentCount/reachedPosts, 2)*100) + '%')
    print('Follow : ' + str(followCount) + ' │ ' + str(round(followCount/reachedPosts, 2)*100) + '%')
    print('Saved : ' + str(savedCount) + ' │ ' + str(round(savedCount/reachedPosts, 2)*100) + '%')
    print('')
    print('Elapsed Time : ' + str(datetime.now() - startTime))
    print('Start : ' + str(startTime))
    print('End   : ' + str(datetime.now()))
    # print('')
    bizgo.closeBrowser()

# py2exe...
### Function tagging people comment

main()

# TOP25 : instadaily picoftheday cute happy love beautiful photooftheday food
# cat cats catsofinstagram instacat instacats
# kitty chat chats instachats gato mycat meow ilovecat doglover
# ねこ or 猫 CAT IN JAPANESE

#{'alt': 'L’image contient peut-être\xa0: chat et intérieur', 'class': 'FFVAD', 'decoding':
#'auto', 'style': 'object-fit: cover;'}
# self.driver.execute_script("var items = {}; for (index=0; index<arguments[0].attributes.length;++index) {items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;", src_elem)
