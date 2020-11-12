#Author: YP
#Date 2020.11
#Abour: Small web novel grabber

import urllib
import urllib.request
import time

url_main = 'https://***/novel/reverend-insanity/chapter-'

last_page = 5

def to_file(str):
    file = open('file_text.txt','at')
    file.write(str)
    file.write("\n" +"=================================" + "\n")
    file.close()

def to_file_chapter(chap, str_ch):
    ''' Write one chapter in file
    
    Create or rewrite file for the selected chapter number "chap". '''
    chap = str(chap)
    file = open('file_text_ch'+chap+'.txt','wt')
    file.write(str_ch)
    file.close()

def remove_in_between(text, str_start, str_end):
    
    #number of replaces
    it = 0
    pos_script_start = 0
    tag_script_e_len = len(str_end)

    while pos_script_start < len(text):
        pos_script_start = text.find(str_start,0)
        if pos_script_start == -1:
            break
        pos_script_end = text.find(str_end,0) + tag_script_e_len
        if pos_script_end == -1 + tag_script_e_len:
            break
        
        if pos_script_start > pos_script_end:
            print("Error: start > stop")
            break
        
        #need to change each iteration
        pos_end = len(text)

        print("start = "+str(pos_script_start))
        print(str(pos_script_end))
        print("len = " + str(pos_end))

        text = text[0:pos_script_start] + text[pos_script_end:pos_end]

        it = it + 1
        pos_script_start = 0
        pos_script_end = 0
    
    return text

#=== Main part ===

for i in range(1,last_page+1):
    
    url_part = str(i)
    url_full = url_main + url_part + '/'

    print("=== "+url_full+"\n")

    response = urllib.request.urlopen(url_full)
    webContent = str(response.read())
    webContent_len = len(webContent)
    #print(webContent[0:3000])

    tag_1 = '<div class="read-container"><div class="reading-content">'
    pos_start_content = webContent.find(tag_1)
    pos_start_content = pos_start_content + len(tag_1)
    pos_end_content = webContent.find('<div class="entry-header footer" id="manga-reading-nav-foot"')

    #keep the main part (text)
    if (pos_start_content != -1 + len(tag_1) and pos_end_content != -1):
        webContent = webContent[pos_start_content:pos_end_content]

    #print(webContent)
    #to_file(webContent)
    #to_file_chapter(i, webContent)

    #remove tag <script></script> and all between
    #first tag script could be with "/>" or " " (space) at the end, so...
    webContent = remove_in_between(webContent, "<script", "</script>")

    #remove tags <ins></ins>
    webContent = remove_in_between(webContent, "<ins", "</ins>")
    
    #replace ASCII / UTF back
    # &#8212; [Em dash]
    webContent = webContent.replace('&#8212;',' - ')
    # &#8220; [Left double quotation mark] -> "
    webContent = webContent.replace('&#8220;','"')
    # &#8221; [Right double quotation mark] -> "
    webContent = webContent.replace('&#8221;','"')
    # &#8216; [Left single quotation mark] -> '
    webContent = webContent.replace('&#8216;',"'")
    # &#8217; [Right single quotation mark] -> '
    webContent = webContent.replace('&#8217;',"'")
    # \xe3\x80\x8a [LEFT DOUBLE ANGLE BRACKET] -> "
    webContent = webContent.replace('\\xe3\\x80\\x8a','"')
    # \xe3\x80\x8b [RIGHT DOUBLE ANGLE BRACKET] -> "
    webContent = webContent.replace('\\xe3\\x80\\x8b','"')

    #print(webContent)
    
    to_file(webContent)
    to_file_chapter(i, webContent)

    time.sleep(0.5)
    #file = open('file_text.txt','at')
    #file.write(webContent)
    #file.write("\n" +"=================================" + "\n")
    #file.close()
