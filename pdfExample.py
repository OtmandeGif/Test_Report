# ###################################
# Help
import youtrack
import requests
from youtrack import *
from youtrack.connection import Connection as YouTrack

# changer sprint en sprints et changer les restrictions TO, essayer de juste changer la fonction get
# authentication request with permanent token
yt = YouTrack('https://youtrack.interne.urgotech.xyz', token='perm:bWNvcXVlcnk=.NDktMw==.wQXjKaMl3Dokxi3pd4Tac4X7Ri9Uwp')

def getSortedIssues(sprint='None',os='None',u=True) :
    Issues=yt.getAllIssues()
    versions=[]
    lists={}
    for card in Issues:
        if u :
            if card.projectShortName == 'TO' or os=='None':
                if card.Type != 'User Story':
                    if card.Sprint == sprint or os=='None':
                        swim=card.Swim
                        if not swim in versions:
                            versions.append(swim)
                            lists[swim]=[card]
                        else :
                            lists[swim].append(card)
        else :
            if card.projectShortName == 'TO' or os=='None':
                if card.Type != 'User Story':
                        if card.Sprint == sprint or os=='None':
                            if card.Swim != 'Uncategorized cards':
                                swim=card.Swim
                                if not swim in versions:
                                    versions.append(swim)
                                    lists[swim]=[card]
                                else :
                                    lists[swim].append(card)
    return(lists,sorted(versions))


"""
d='date'
n='tester name'
s='sprint 2'
sd='sprint date'
o='os'
v='version 1.1.31 (2)'
u=True
verdict='Validated'

lists, versions=getSortedIssues(s,o,u)"""

def Report(d,n,s,sd,o,v,u,verdict,lists, versions):

    def drawMyRuler(pdf):
        pdf.drawString(100,810, 'x100')
        pdf.drawString(200,810, 'x200')
        pdf.drawString(300,810, 'x300')
        pdf.drawString(400,810, 'x400')
        pdf.drawString(500,810, 'x500')

        pdf.drawString(10,100, 'y100')
        pdf.drawString(10,200, 'y200')
        pdf.drawString(10,300, 'y300')
        pdf.drawString(10,400, 'y400')
        pdf.drawString(10,500, 'y500')
        pdf.drawString(10,600, 'y600')
        pdf.drawString(10,700, 'y700')
        pdf.drawString(10,800, 'y800')



    # ###################################
    # Content
    fileName = 'Report.pdf'
    documentTitle = 'Document title!'
    title = 'Test Report'
    subTitle = 'Description'
    image = 'logo.png'


    # ###################################
    # 0) Create document
    from reportlab.pdfgen import canvas
    pdf = canvas.Canvas(fileName)
    pdf.setTitle(documentTitle)
    """drawMyRuler(pdf)""" #REPERE (X,Y)

    # ###################################
    #  1) Draw a image
    pdf.drawInlineImage(image, 400, 780)

    # 2) Title :: Set fonts
    #
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfbase import pdfmetrics

    pdfmetrics.registerFont(TTFont('abc', 'Arial.ttf'))
    pdf.setFont('abc', 36)
    pdf.drawCentredString(300, 770, title)

    # ###################################
    # 3) Parameters, First Sub Title
    # RGB - Red Green and Blue
    pdf.setFillColorRGB(0, 0, 0)
    pdf.setFont('abc', 12)
    pdf.drawString(30,800, 'by '+n+', '+d)

    pdf.setFillColorRGB(0, 0, 0)
    pdf.setFont("abc", 12)
    pdf.drawString(30,787, s+'('+sd+')')

    pdf.setFillColorRGB(0, 0, 0)
    pdf.setFont("abc", 12)
    pdf.drawString(30,774, v)

    pdf.setFillColorRGB(0, 0, 0)
    pdf.setFont("abc", 20)
    pdf.drawString(30,720, subTitle)

    # ###################################
    # 4) Draw a line for Description

    pdf.line(30, 710, 575, 710)


    # ###################################
        # 5) Fonctions d'encadrement du texte et d'ajustement du texte, changement de page

    #Encadrement des tickets
    def Encadrement(x1,y1,x2,y2):
        pdf.line(x1, y1, x1, y2)
        pdf.line(x1, y1, x2, y1)
        pdf.line(x1, y2, x2,y2)
        pdf.line(x2, y1, x2,y2)

    #Découpage du texte en lignes
    def AdjustText(card):
            k=50
            a=len(card)//k
            b=len(card)%k
            text=[]
            if a==0 :
                return([card])
            for i in range (0,a):
                if card[((i+1)*a)+1] != ' ':
                    text.append(card[i*k:(i+1)*k]+'-')
                else :
                    text.append(card[i*k:(i+1)*k])
            text.append(card[a*k:])
            return(text)

    #Changement de page
    def NewPage(y1,l=0):
        if y1<140 :
            pdf.showPage()
            return(720)
        else:
            if l==0:
                return(y1-80)

            elif l==-1:
                return(y1-80)
            else :
                return(y1-(20+13*l))


    # 6) Set parameters and Display all description cards
    from reportlab.lib import colors

    x1=30
    y1=680

    for card in lists['Description']:
        ticket=card.id
        summary=card.summary
        state=card.State
        description=card.description
        priority=card.Priority
        pdf.setFillColorRGB(0, 0, 0)

        #Titre du ticket
        text = pdf.beginText(120, y1)
        text.setFont("Courier", 12)
        """text.setFillColor(colors.red)""" #si besoin d'une couleur
        textLines = AdjustText(summary)
        l=len(textLines)
        for line in textLines:
            text.textLine(line)
        pdf.drawText(text)

        #Description du ticket
        text2 = pdf.beginText(120, y1-(5+13*l))
        text2.setFont("Courier", 11)

        """text.setFillColor(colors.red)""" #si besoin d'une couleur
        textLines2 = AdjustText(description)
        l2=len(textLines2)
        l=l+l2
        for line in textLines2:
            text2.textLine(line)
        pdf.drawText(text2)

        #Numéro du Ticket YT
        pdf.setFillColorRGB(0, 0, 0)
        pdf.setFont("abc", 12)
        pdf.drawString(50,y1, ticket)

        #Priorrité du Ticket YT
        #ADD COLOR
        pdf.setFillColorRGB(0, 0, 0)
        pdf.setFont("abc", 12)
        pdf.drawString(50,(y1+6-(((13//2)+1)*l)), priority)

        #Etat du ticket YT
        if state=='Fixed' or state=='Verified':
            pdf.setFillColorRGB(0, 255, 0)
            pdf.setFont("abc", 12)
            pdf.drawString(500,y1, state)

        else :
            pdf.setFillColorRGB(255, 0, 0)
            pdf.setFont("abc", 12)
            pdf.drawString(500,y1, state)



        Encadrement(42,y1+12,550,y1-(13*l))
        y1=NewPage(y1,l)
    # Algorithme principal

    for version in versions[1:] :
        y1=NewPage(y1,0)
        # Affichage du titre
        pdf.setFillColorRGB(0, 0, 0)
        pdf.setFont("abc", 20)
        pdf.drawString(30,y1+40, version)

        # Souslignage du titre
        pdf.line(30, y1+30, 575, y1+30)

        for card in lists[version]:
            ticket=card.id
            summary=card.summary
            state=card.State
            priority=card.Priority
            description=card.description
            pdf.setFillColorRGB(0, 0, 0)

            #Titre du ticket
            text = pdf.beginText(120, y1)
            text.setFont("Courier", 12)
            """text.setFillColor(colors.red)""" #si besoin d'une couleur
            textLines = AdjustText(summary)
            l=len(textLines)
            for line in textLines:
                text.textLine(line)
            pdf.drawText(text)

            #Description du ticket
            text2 = pdf.beginText(120, y1-(5+13*l))
            text2.setFont("Courier", 11)

            """text.setFillColor(colors.red)""" #si besoin d'une couleur
            textLines2 = AdjustText(description)
            l2=len(textLines2)
            l=l+l2
            for line in textLines2:
                text2.textLine(line)
            pdf.drawText(text2)

            #Numéro du Ticket YT
            pdf.setFillColorRGB(0, 0, 0)
            pdf.setFont("abc", 12)
            pdf.drawString(50,y1, ticket)

            #Priorrité du Ticket YT
            #ADD COLOR
            pdf.setFillColorRGB(0, 0, 0)
            pdf.setFont("abc", 12)
            pdf.drawString(50,(y1+6-(((13//2)+1)*l)), priority)

            #Etat du ticket YT

            if state=='Fixed' or state=='Verified':
                pdf.setFillColorRGB(0, 255, 0)
                pdf.setFont("abc", 12)
                pdf.drawString(500,y1, state)

            else :
                pdf.setFillColorRGB(255, 0, 0)
                pdf.setFont("abc", 12)
                pdf.drawString(500,y1, state)



            Encadrement(42,y1+12,550,y1-(13*l))
            y1=NewPage(y1,l)

    y1=NewPage(y1,-1)
    if verdict=='Validated':
        pdf.setFillColorRGB(0, 255, 0)
        pdfmetrics.registerFont(TTFont('abc', 'Arial.ttf'))
        pdf.setFont('abc', 25)
        pdf.drawCentredString(300, y1, 'Version '+verdict)
        Encadrement(200,y1+30,400,y1-10)

    else:
        pdf.setFillColorRGB(255, 0, 0)
        pdfmetrics.registerFont(TTFont('abc', 'Arial.ttf'))
        pdf.setFont('abc', 25)
        pdf.drawCentredString(300, y1, 'Version '+verdict)
        Encadrement(200,y1+30,400,y1-10)
    #Mise à jour du pdf
    # DE LA MISE EN FORME ET DES COULEURS
    # INTEGRATION CONFLUENCE
    #Tout unifier
    pdf.save()