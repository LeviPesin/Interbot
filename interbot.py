#!/usr/bin/env python
# coding: utf-8
import pywikibot, pywikibot.pagegenerators, requests
def ind(temples):
        global indexes
        lowertext=text.lower()
        if len(temples)>1:
                try:
                        indexes.append(lowertext.index(temples[0]))
                except:
                        pass
                finally:
                        ind(temples[1:])
        else:
                try:
                        indexes.append(lowertext.index(temples[0]))
                except:
                        pass
def main(page1):
        page=page1
        text=page.text
        textnew=[]
        while True:
                indexes=[]
                ind(u"{{не переведено 5", u"{{нп5", u"{{iw", u"{{нп4", u"{{ut4", u"{{не переведено 4")
                if indexes!=[]:
                        index=min(indexes)
                else:
                        break
                textnew.append([0, text[:index]])
                text=text[index:]
                index=text.index("}}")
                template=[]
                vertical=-1
                for i in range(index):
                        if text[i]=="|":
                                if vertical==-1:
                                        template.append(text[2:i])
                                else:
                                        template.append(text[vertical+1:i])
                                vertical=i
                template.append(text[vertical+1:index])
                try:
                        text=text[index+2:]
                except:
                        text=""
                textnew.append(template)
        textnew.append([0, text])
        for q in range(len(textnew)):
                i=textnew[q]
                if i[0]!=0:
                        if i[3]=="":
                                prefix="en"
                        else:
                                prefix=i[3]
                        if i[4]=="":
                                intername=i[1]
                        else:
                                intername=i[4]
                        intername=intername.split()
                        intername="_".join(intername)
                        request="https://"+prefix+".wikipedia.org/w/api.php?action=query&titles="+intername+"&prop=langlinks&lllimit=500&format=json"
                        try:
                                request2=requests.get("https://"+prefix+".wikipedia.org/wiki/"+intername)
                                if request2.status_code!=404:
                                        try:
                                                #json with interwikis
                                                jwi=requests.get(request).json()
                                                interwiki=""
                                                for z in jwi['query']['pages'].keys():
                                                        for j in jwi['query']['pages'][z]['langlinks']:
                                                                if j['lang']=='ru':
                                                                        interwiki=j['*']
                                                try:
                                                        inter=interwiki
                                                        if inter!="" and i[2]=="":
                                                                textnew[q]=[0,"[["+inter+"|"+i[1]+"]]"]
                                                        elif inter!="":
                                                                textnew[q]=[0, "[["+inter+"|"+i[2]+"]]"]
                                                except:
                                                        pass
                                        except:
                                                pass
                                else:
                                        if i[2]!="":
                                                textnew[q]=[0, "[["+i[1]+"]]"]
                                        else:
                                                textnew[q]=[0, "[["+i[2]+"|"+i[1]+"]]"]
                        except:
                                pass
        text=""
        for i in textnew:
                if i[0]==0:
                        text+=i[1]
                else:
                        text+="{{"+i[0]+"|"+i[1]+"|"+i[2]+"|"+i[3]+"|"+i[4]+"}}"
        if text!=page.text:
                page.text=text
                page.save(u"Проверено, не переведены ли ссылки.")
if __name__=="__main__":
        articles=pywikibot.pagegenerators.CategorizedPageGenerator(pywikibot.Category(pywikibot.Site(), u'Категория:Статьи'), recurse=True)
        while True:
            try:
                main(next(articles))
            except:
                break
