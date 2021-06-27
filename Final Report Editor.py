import tkinter as tk
from tkinter import *
from tkinter import messagebox
import youtrack
import requests
from youtrack import *
from youtrack.connection import Connection as YouTrack
import pdfExample
from pdfExample import *
from testrail import *

client = APIClient('https://testrail.interne.urgotech.xyz/')
client.user = 'ohassani@urgotech.fr'
client.password = 'Testtest123!'


# YouTack authentication request with permanent token
yt = YouTrack('https://youtrack.interne.urgotech.xyz', token='perm:bWNvcXVlcnk=.NDktNQ==.glnCuKTPiNpRWOZ6eh39KCckGYvMpo')

def getSortedIssues(sprint='None',os='None',v='version',u=True,us=True) :
    Issues=yt.getAllIssues()
    versions=[]
    lists={}
    for card in Issues:

        if u :
            if card.projectShortName == os:
                if card.Type != 'User Story':
                    if sprint in card.Sprints or os=='None':
                        if type(card.Swimlane)==list:
                            for swim in card.Swimlane:
                                if not swim in versions:
                                    versions.append(swim)
                                    lists[swim]=[card]
                                    ##Rentrer dans version 1.3.5 et avant d'ajouter la version à la liste checker que c'est description ou 1.3.5 + qqchose
                                else :
                                    lists[swim].append(card)
                        else:
                            swim=card.Swimlane
                            if not swim in versions:
                                versions.append(swim)
                                lists[swim]=[card]
                            else :
                                lists[swim].append(card)

        else :
            if card.projectShortName == os:
                if card.Type != 'User Story':
                    if sprint in card.Sprints or sprint==card.Sprints:
                        if card.Swimlane != 'Uncategorized cards':
                            if type(card.Swimlane)==list:
                                i=0
                                for swim in card.Swimlane:
                                    n=len(v)
                                    if swim[:n]==v or swim=='Description':
                                        if not swim in versions:
                                            versions.append(swim)
                                            if i==0:
                                                lists[swim]=[card]
                                            else:
                                                lists[swim]=[]

                                        else :
                                            if i==0:
                                                lists[swim].append(card)
                                    i+=1
                            else:
                                swim=card.Swimlane
                                n=len(v)
                                if swim[:n]==v or swim=='Description':
                                    if not swim in versions:
                                        versions.append(swim)
                                        lists[swim]=[card]
                                    else :
                                        lists[swim].append(card)
    return(lists,sorted(versions))

def getUnscheduledIssues(sprint='None',os='None') :
    Issues=yt.getAllIssues()
    versions=[]
    lists={'Unscheduled':[]}
    for card in Issues:
        if card.projectShortName == os :
            if card.Type != 'User Story':
                if sprint in card.Sprints or os=='None':
                    lists[sprint].append(card)
    return(lists,sorted(versions))

def Algorithm(sprint='None',version='None') :
    Issues=yt.getAllIssues()
    count=0
    k=0
    l=0
    m=0
    for card in Issues:
        if card.projectShortName != 'TO' or os=='None':         #choix du projet
            if card.Type != 'User Story':                      #enlever les tickets swimlane
                    if card.Sprint == sprint or os=='None':     #choix sprint
                        if card.Swimlane == version:
                            priority=card.Priority
                            if priority=='Minor': #wording, mini design, 3
                                k+=1
                            if priority=='Normal': #des que visible par utilisateur moyennement concentré, 2 normaux
                                l+=1
                            if priority=='Major': # bloquant, crash, update etc mais juste sur qq utilisateurs, 1 max
                                m+=1
                            if priority=='Critical':
                                count+=1
    if k>3 or l>2 or m>1 or count>0 :
        return('Validated')
    else:
        return('Refused')


#Définition des paramètres (inutiles mais sert de legende pour coder)
d='date'
n='tester name'
s='sprint number'
sd='sprint date'
o='os'
v='version'
u=True
verdict='validation?'
us=True

def Report(d,n,s,sd,o,v,u,verdict,us,lists, versions):

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

    def sym(X,x1):
        x,y=X
        return((x1-(x-x1),y))

    def oval(canvas,h=0, debug=1, fill=0):

        curves = [
    (332.5, h), (475, h), (520, h),
    (550, h), (550, h-20), (520, h-20),
    (490, h-20), (332.5, h-20), (332.5, h-20),
    sym((332.5, h-20),332.5), sym((332.5, h-20),332.5), sym((490, h-20),332.5),
    sym((520, h-20),332.5),sym((520, h-20),332.5),sym((520, h-20),332.5),
    sym((550, h-20),332.5),sym((550, h),332.5), sym((520, h),332.5),
    sym((475, h),332.5),sym((332.5, h),332.5),sym((332.5, h),332.5)
    ]

        from reportlab.lib.units import inch
        if debug: canvas.setLineWidth(6)
        (startx, starty) = (332.5,h)
        p = canvas.beginPath()
        p.moveTo(startx, starty)
        ccopy = list(curves)
        while ccopy:
            [(x1,y1), (x2,y2), (x3,y3)] = ccopy[:3]
            del ccopy[:3]
            p.curveTo(x1,y1,x2,y2,x3,y3)
        p.close()
        canvas.drawPath(p, fill=fill)
        if debug:
            from reportlab.lib.colors import red, green
            (lastx, lasty) = (startx, starty)
            ccopy = list(curves)
            while ccopy:
                [(x1,y1), (x2,y2), (x3,y3)] = ccopy[:3]
                del ccopy[:3]
                canvas.setStrokeColor(red)
                canvas.line(lastx,lasty, x1,y1)
                canvas.setStrokeColor(green)
                canvas.line(x2,y2, x3,y3)
                (lastx,lasty) = (x3,y3)

    def oval2(canvas,h=0, debug=1, fill=0):

        curves = [
    (332.5, h), (475, h), (520, h),
    (550, h), (550, h-20), (520, h-20),
    (490, h-20), (332.5, h-20), (332.5, h-20),
    sym((332.5, h-20),332.5), sym((332.5, h-20),332.5), sym((490, h-20),332.5),
    sym((520, h-20),332.5),sym((520, h-20),332.5),sym((520, h-20),332.5),
    sym((550, h-20),332.5),sym((550, h),332.5), sym((520, h),332.5),
    sym((475, h),332.5),sym((332.5, h),332.5),sym((332.5, h),332.5)
    ]

        curves2=[]
        for curve in curves:
            x,y=curve
            if x==332.5:
                curves2.append((145,y))
            elif x>332.5:
                curves2.append((x/3.1,y))
            else:
                curves2.append((x,y))

        from reportlab.lib.units import inch
        if debug: canvas.setLineWidth(6)
        (startx, starty) = (145,h)
        p = canvas.beginPath()
        p.moveTo(startx, starty)
        ccopy = list(curves2)
        while ccopy:
            [(x1,y1), (x2,y2), (x3,y3)] = ccopy[:3]
            del ccopy[:3]
            p.curveTo(x1,y1,x2,y2,x3,y3)
        p.close()
        canvas.drawPath(p, fill=fill)

    def oval3(canvas,h=0, debug=1, fill=0):

        curves=[(145, h), (151, h), (165, h),
        (175, h), (175, h-20), (165, h-20),
        (155, h-20), (145, h-20), (145, h-20)]

        from reportlab.lib.units import inch
        if debug: canvas.setLineWidth(6)
        (startx, starty) = (145,h)
        p = canvas.beginPath()
        p.moveTo(startx, starty)
        ccopy = list(curves)
        while ccopy:
            [(x1,y1), (x2,y2), (x3,y3)] = ccopy[:3]
            del ccopy[:3]
            p.curveTo(x1,y1,x2,y2,x3,y3)
        p.close()
        canvas.drawPath(p, fill=fill)

    # ###################################
    # Content
    fileName = 'Report.pdf'
    documentTitle = 'Document title!'
    title = 'TEST REPORT'
    subTitle = v+' scope'
    image = 'logo4.png'


    # ###################################
    # 0) Create document
    from reportlab.pdfgen import canvas
    pdf = canvas.Canvas(fileName)
    pdf.setTitle(documentTitle)

    #drawMyRuler(pdf) #REPERE (X,Y)

    # ###################################
    #  1) Draw a image
    pdf.drawInlineImage(image, 480, 800)

    # 2) Title :: Set fonts
    #
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfbase import pdfmetrics

    pdf.setFont("Helvetica-Bold", 24)
    pdf.drawCentredString(300, 770, title)
    pdfmetrics.registerFont(TTFont('abc', 'Arial.ttf'))
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


    #Découpage du titre en lignes
    def AdjustText1(card):
        k=66
        a=len(card)//k
        b=len(card)%k
        text=[]
        if a==0 or (a==1 and b==0):
            return([card])
        else:
            for i in range (0,a):
                if card[((i+1)*a)+1] != ' ':
                    text.append(card[i*k:(i+1)*k]+'-')
                else :
                    text.append(card[i*k:(i+1)*k])
            text.append(card[a*k:])
            return(text)

    #Clean texte
    def Clean1(description):
        result=[]
        k=0
        for i in range(1,len(description)):
            if description[i] == '\n':
                if description[k:i]!='':
                    Decoupage=AdjustText1(description[k:i])
                    for cut in Decoupage :
                        result.append(cut)
                k=i+1
        lastPart=AdjustText1(description[k:])
        L=['',' ','  ']
        for cut in lastPart :
            if cut not in L:
                result.append(cut)
        return(result)

    #Découpage de la description en lignes
    def AdjustText2(card):
        k=60
        a=len(card)//k
        b=len(card)%k
        text=[]
        if a==0 or (a==1 and b==0):
            return([card])
        else:
            for i in range (0,a):
                if card[((i+1)*a)+1] != ' ':
                    text.append(card[i*k:(i+1)*k]+'-')
                else :
                    text.append(card[i*k:(i+1)*k])
            text.append(card[a*k:])
            return(text)

    #Clean description
    def Clean2(description):
        result=[]
        k=0
        for i in range(1,len(description)):
            if description[i] == '\n':
                if description[k:i]!='':
                    Decoupage=AdjustText2(description[k:i])
                    for cut in Decoupage :
                        result.append(cut)
                k=i+1
        lastPart=AdjustText2(description[k:])
        L=['',' ','  ']
        for cut in lastPart :
            if cut not in L:
                result.append(cut)
        return(result)

    #Changement de page
    def NewPage(y1,l=0):
        if y1<150 :
            pdf.showPage()
            return(800)
        else:
            if l==0:
                return(y1-80)

            elif l==-1:
                return(y1-80)
            else :
                return(y1-(30+13*l))

    #Changement de page (spécial titre de version)
    def NewPage2(y1,l=0):
        if y1<150 :
            pdf.showPage()
            return(700)
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
    ## Description cards

    for card in lists['Description']:
        ticket=card.id
        summary=card.summary
        state=card.State
        description=card.description
        priority=card.Priority
        type=card.Type
        pdf.setFillColorRGB(0, 0, 0)

        textLines = Clean1('['+type+'] '+summary)
        l1=len(textLines)
        textLines2 = Clean2(description)
        l2=len(textLines2)

        if y1-(13*(l1+l2))<=0 :
            y1=800
            pdf.showPage()

        #Titre du ticket
        text = pdf.beginText(120, y1)
        text.setFont('abc', 12)

        for line in textLines:
            text.textLine(line)
        pdf.drawText(text)
        pdf.line(42,y1-5-(13*(l1-1)),550,y1-5-(13*(l1-1)))

        #Description du ticket
        text2 = pdf.beginText(120, y1-(5+13*l1))
        text2.setFont("Courier", 11)


        l=l1+l2
        for line in textLines2:
            text2.textLine(line)
        pdf.drawText(text2)

        #Numéro du Ticket YT
        pdf.setFillColorRGB(0, 0, 0)
        pdf.setFont("abc", 12)
        pdf.drawString(50,y1, ticket)

        #Priorité du Ticket YT
        #ADD COLOR
        pdf.setFillColorRGB(0, 0, 0)
        pdf.setFont("abc", 12)
        pdf.drawString(50,((y1-5-(13*(l1-1))+(y1-(13*l)))/2), priority)



        pdf.line(115,y1+12,115,y1-(13*l))
        Encadrement(42,y1+12,550,y1-(13*l))

        y1=NewPage(y1,l)


    ## Algorithme principal
    Historique=['Description']


    ###début de l'acces à l'API de Testrail, suite après
    #Trouver l'id de projet :
    project_id_TR=0
    if o=='NIOS':
        project_id_TR=1
    elif o=='NIOS':
        project_id_TR=2
    else:
        project_id_TR=4

    #Trouver le numéro de milestone et de run
    requete4='get_milestones/'+str(project_id_TR)
    milestones = client.send_get(requete4)
    milestone_id=100
    for milestone in milestones :
        if milestone["is_completed"]==False:

            if milestone["id"]<milestone_id:
                milestone_id=milestone["id"]
    requete3='get_runs/'+str(project_id_TR)+'/'+str(milestone_id)
    runs=client.send_get(requete3)
    listruns=[]
    for run in runs:
        if run['milestone_id']==milestone_id:
            listruns.append(run['id'])
    listruns.sort()



    #Parcours des versions (sauf Description deja fait)

    for version in versions[1:] :

        y1=NewPage2(y1,0)

        # Affichage du titre
        pdf.setFillColorRGB(0, 0, 0)
        pdf.setFont("abc", 20)

        if version==versions[-1] :
            if verdict=='Validated':
                pdf.drawString(30,y1+40, version+':')
                n=len(version+':')
                pdf.setFillColorRGB(0, 255, 0)
                pdf.setFont("abc", 20)
                pdf.drawString(30+9.5*n,y1+40, 'Validated')

            else:
                pdf.drawString(30,y1+40, version+':')
                n=len(version+':')
                pdf.setFillColorRGB(255, 0, 0)
                pdf.setFont("abc", 20)
                pdf.drawString(30+9.5*n,y1+40, 'Rejected')

        elif version=='Uncategorized cards':
            pdf.drawString(30,y1+40, version)

        else:
            pdf.drawString(30,y1+40, version+':')
            n=len(version+':')
            pdf.setFillColorRGB(255, 0, 0)
            pdf.setFont("abc", 20)
            pdf.drawString(30+9.5*n,y1+40, 'Rejected')



        # Souslignage du titre
        pdf.line(30, y1+30, 575, y1+30)

        ###Historique des versions avec cas de test Testrail

        #Trouver le numéro de run correspondant

        run_id=listruns[0]
        listruns=listruns[1:]
        pdf.linkURL('https://testrail.interne.urgotech.xyz/index.php?/runs/view/'+str(run_id)+'&group_by=cases:section_id&group_order=asc', (30,y1+60,30+9.5*(n+10),y1+40))


        #On parcourt les versions antérieures à la version de la loop
        Historique.append(version)
        for old_version in Historique:

            for card in lists[old_version]:
                ticket=card.id
                summary=card.summary
                state=card.State
                priority=card.Priority
                description=card.description
                type=card.Type
                pdf.setFillColorRGB(0, 0, 0)

                #Titre du ticket
                textLines = Clean1('['+type+'] '+summary)
                l1=len(textLines)
                textLines2 = Clean2(description)
                l2=len(textLines2)

                #Besoin du nombre de cas de test pour voir la place restante sur la page
                requete='get_cases/'+str(project_id_TR)+'&refs='+ticket
                l3=len(client.send_get(requete))

                if y1-(13*(l1+l2)+28*l3)<=0 :
                    y1=800
                    pdf.showPage()
                text = pdf.beginText(120, y1)
                text.setFont('abc', 12)

                for line in textLines:
                    text.textLine(line)
                pdf.drawText(text)
                pdf.line(42,y1-5-(13*(l1-1)),550,y1-5-(13*(l1-1)))

                #Description du ticket
                text2 = pdf.beginText(120, y1-(5+13*l1))
                text2.setFont("Courier", 11)


                l2=len(textLines2)
                l=l1+l2
                for line in textLines2:
                    text2.textLine(line)
                pdf.drawText(text2)

                #Numéro du Ticket YT
                pdf.setFillColorRGB(0, 0, 0)
                pdf.setFont("abc", 12)
                pdf.drawString(50,y1, ticket)


                #Priorité du Ticket YT
                pdf.setFillColorRGB(0, 0, 0)
                pdf.setFont("abc", 12)
                pdf.drawString(50,((y1-5-(13*(l1-1))+(y1-(13*l)))/2), priority)




                pdf.line(115,y1+12,115,y1-(13*l))
                Encadrement(42,y1+12,550,y1-(13*l))


                ##Test cases

                requete='get_cases/'+str(project_id_TR)+'&refs='+ticket

                cases = client.send_get(requete)
                number_fail=0
                test_cases=False
                #New page à appliquer selon la longueur de la liste, gérer les trop longs
                k=y1-13*l
                refk=y1-13*l



                if len(cases)!=0 :
                    test_cases=True
                    for case in cases :
                        #Test case
                        oval(pdf,k-12,0)
                        pdf.setFillColorRGB(0, 0, 0)
                        pdf.setFont("abc", 11)
                        pdf.drawString(170,k-26, case['title'])

                        #Numéro de ticket
                        pdf.bezier(145,k-12, 175,k-12, 175,k-32, 145,k-32)
                        pdf.setFillColorRGB(0, 0, 0)
                        pdf.setFont("abc", 11)
                        pdf.drawString(132,k-26, 'C'+str(case['id']))

                        #Statut
                        pdf.bezier(520,k-12, 490,k-12, 490,k-32, 520,k-32)



                        requete2='get_results_for_case/'+str(run_id)+'/'+str(case['id'])
                        testresult = client.send_get(requete2)
                        if len(testresult)>0:
                            status=testresult[0]['status_id']

                            if status==1:
                                pdf.setFillColorRGB(0, 255, 0)
                                pdf.setFont("abc", 11)
                                pdf.drawString(501,k-26, "Passed")
                            elif status==2:
                                pdf.setFillColorRGB(0, 0, 0)
                                pdf.setFont("abc", 11)
                                pdf.drawString(501,k-26, "Blocked")
                            elif status==3:
                                pdf.setFillColorRGB(0, 0, 0)
                                pdf.setFont("abc", 11)
                                pdf.drawString(501,k-26, "Untested")
                            elif status==4:
                                pdf.setFillColorRGB(0, 0, 0)
                                pdf.setFont("abc", 11)
                                pdf.drawString(501,k-26, "Restest")
                            elif status==5:
                                number_fail+=1
                                pdf.setFillColorRGB(255, 0, 0)
                                pdf.setFont("abc", 11)
                                pdf.drawString(505,k-26, "Failed")

                        else:
                            pdf.setFillColorRGB(0, 255, 0)
                            pdf.setFont("abc", 11)
                            pdf.drawString(501,k-26, "Passed")

                        #Fleches
                        pdf.line(100,refk,100,k-22)
                        pdf.line(100,k-22,123,k-22)
                        y1=y1-28
                        k=k-28

                #Etat du ticket YT

                if version==old_version:
                    if version==versions[-1] and verdict=='Validated':
                        if state=='To Verify' or state=='Done':
                            pdf.setFillColorRGB(255, 0, 0)
                            pdf.setFont("abc", 12)
                            pdf.drawString(475,y1+28*len(cases), 'Rescheduled')

                        else :
                            pdf.setFillColorRGB(255, 0, 0)
                            pdf.setFont("abc", 12)
                            pdf.drawString(475,y1+28*len(cases), 'Rescheduled')
                    else:
                        if state=='To Verify' or state=='Done':
                            pdf.setFillColorRGB(255, 0, 0)
                            pdf.setFont("abc", 12)
                            pdf.drawString(500,y1+28*len(cases), 'Open')

                        else :
                            pdf.setFillColorRGB(255, 0, 0)
                            pdf.setFont("abc", 12)
                            pdf.drawString(500,y1+28*len(cases), 'Open')

                else:
                    if test_cases:
                        if number_fail==0:
                            pdf.setFillColorRGB(0, 255, 0)
                            pdf.setFont("abc", 12)
                            pdf.drawString(500,y1+28*len(cases), 'Solved')

                        else :
                            pdf.setFillColorRGB(255, 0, 0)
                            pdf.setFont("abc", 12)
                            pdf.drawString(500,y1+28*len(cases), 'Rejected')

                    else:
                        if state=='To Verify' or state=='Done':
                            pdf.setFillColorRGB(0, 255, 0)
                            pdf.setFont("abc", 12)
                            pdf.drawString(500,y1+28*len(cases), 'Solved')

                        else :
                            pdf.setFillColorRGB(255, 0, 0)
                            pdf.setFont("abc", 12)
                            pdf.drawString(500,y1+28*len(cases), 'Rejected')

                y1=NewPage(y1,l)








    ## Unscheduled cards

    if us:
        lists, versions=getUnscheduledIssues('Unscheduled',o)
        if y1==800 :
            y1=700
        else:
            pdf.showPage()
            y1=700
        # Affichage du titre
        pdf.setFillColorRGB(0, 0, 0)
        pdf.setFont("abc", 20)
        pdf.drawString(30,y1+40, 'Unscheduled Cards')

        # Souslignage du titre
        pdf.line(30, y1+30, 575, y1+30)

        for card in lists['Unscheduled']:
            ticket=card.id
            summary=card.summary
            state=card.State
            description=card.description
            priority=card.Priority
            type=card.Type
            pdf.setFillColorRGB(0, 0, 0)

            textLines = Clean1('['+type+'] '+summary)
            l1=len(textLines)
            textLines2 = Clean2(description)
            l2=len(textLines2)


            if y1-(13*(l1+l2))<=0 :
                y1=800
                pdf.showPage()
            #Titre du ticket
            text = pdf.beginText(120, y1)
            text.setFont("abc", 12)

            for line in textLines:
                text.textLine(line)
            pdf.drawText(text)
            pdf.line(42,y1-5-(13*(l1-1)),550,y1-5-(13*(l1-1)))

            #Description du ticket
            text2 = pdf.beginText(120, y1-(5+13*l1))
            text2.setFont("Courier", 11)



            l=l1+l2
            for line in textLines2:
                text2.textLine(line)
            pdf.drawText(text2)

            #Numéro du Ticket YT
            pdf.setFillColorRGB(0, 0, 0)
            pdf.setFont("abc", 12)
            pdf.drawString(50,y1, ticket)

            #Priorité du Ticket YT
            #ADD COLOR
            pdf.setFillColorRGB(0, 0, 0)
            pdf.setFont("abc", 12)
            pdf.drawString(50,((y1-5-(13*(l1-1))+(y1-(13*l)))/2), priority)

            #Etat du ticket YT
            if state=='To Verify' or state=='Done':
                pdf.setFillColorRGB(0, 255, 0)
                pdf.setFont("abc", 12)
                pdf.drawString(500,y1, state)

            else :
                pdf.setFillColorRGB(255, 0, 0)
                pdf.setFont("abc", 12)
                pdf.drawString(500,y1, state)


            pdf.line(115,y1+12,115,y1-(13*l))
            Encadrement(42,y1+12,550,y1-(13*l))

            y1=NewPage(y1,l)


    #Mise à jour du pdf
    pdf.save()

def envoi(lst_entry):
    d=lst_entry[0].get()
    n=lst_entry[1].get()
    s=lst_entry[2].get()
    sd=lst_entry[3].get()
    v=lst_entry[4].get()

    os_choice  = var.get()
    if os_choice == 1:
        o='NIOS'

    elif os_choice == 2:
        o='NA'

    else:
        o='TO'

    ucards_choice  = var2.get()
    if ucards_choice == 1:
        u=True

    elif ucards_choice == 2:
       u=False

    verdict_choice  = var3.get()
    if verdict_choice == 1:
        verdict='Validated'

    elif verdict_choice == 2:
        verdict='Rejected'

    elif verdict_choice == 3:
        verdict=Algorithm(s,v)
    print(verdict,v)
    uscards_choice  = var4.get()
    if uscards_choice == 1:
        us=True

    elif uscards_choice == 2:
        us=False

    lists, versions=getSortedIssues(s,o,v,u,us)
    Report(d,n,s,sd,o,v,u,verdict,us,lists, versions)
    print('Done')
    fenetrePrincipale.destroy()
    #appel à la fonction report(ces parametres)


def viewSelected():
    choice  = var.get()
    if choice == 1:
        o='NIOS'
        output = "iOS"

    elif choice == 2:
        o='NA'
        output =  "Android"

    else:
        o='TO'
        output = "TO"

    print('')

def viewSelected2():
    choice  = var2.get()
    if choice == 1:
        u=True
        output = "SD"

    elif choice == 2:
       u=False
       output =  "V"

    else:
        output = "Invalid selection"


    print('')

def viewSelected3():
    choice  = var3.get()
    if choice == 1:
        verdict='Validated'
        output = "Validated"

    elif choice == 2:
        verdict='Rejected'
        output =  "Rejected"

    print('')

fenetrePrincipale = Tk()


Date = tk.Label(fenetrePrincipale, text = "Date").grid(row = 0, column = 0)
Name = tk.Label(fenetrePrincipale, text = "Tester name").grid(row = 1, column = 0)
Sprint = tk.Label(fenetrePrincipale, text = "Sprint number").grid(row = 2, column = 0)
SprintDate = tk.Label(fenetrePrincipale, text = "Sprint date").grid(row = 3, column = 0)
os = tk.Label(fenetrePrincipale, text = "os").grid(row = 4, column = 0)
VersionNumber = tk.Label(fenetrePrincipale, text = "Version number").grid(row = 5, column = 0)
Uncat = tk.Label(fenetrePrincipale, text = "Add Uncategorized cards?").grid(row = 6, column = 0)
Version = tk.Label(fenetrePrincipale, text = "Version").grid(row = 7, column = 0)
Uncat = tk.Label(fenetrePrincipale, text = "Add Unscheduled cards?").grid(row = 8, column = 0)

e1 = tk.Entry(fenetrePrincipale)
e1.grid(row = 0, column = 1)
e2 = tk.Entry(fenetrePrincipale)
e2.grid(row = 1, column = 1)
e3 = tk.Entry(fenetrePrincipale)
e3.grid(row = 2, column = 1)
e4 = tk.Entry(fenetrePrincipale)
e4.grid(row = 3, column = 1)
e7 = tk.Entry(fenetrePrincipale)
e7.grid(row = 5, column = 1)
entries=[e1,e2,e3,e4,e7]

var = IntVar()
o1 = Radiobutton(fenetrePrincipale, text = "IOS", variable=var, value = '1', command=viewSelected).grid(row = 4, column = 1)
o2 = Radiobutton(fenetrePrincipale, text = "ANDROID", variable=var, value = '2', command=viewSelected).grid(row = 4, column = 2)
o3 = Radiobutton(fenetrePrincipale, text = "TO", variable=var, value = '3', command=viewSelected).grid(row = 4, column = 3)

var2 = IntVar()
s1 = Radiobutton(fenetrePrincipale, text = "Yes", variable=var2, value = '1', command=viewSelected2).grid(row = 6, column = 1)
s2 = Radiobutton(fenetrePrincipale, text = "No", variable=var2, value = '2', command=viewSelected2).grid(row = 6, column = 2)

var3 = IntVar()
rb1 = Radiobutton(fenetrePrincipale, text = "Validated", variable=var3, value = '1', command=viewSelected3).grid(row = 7, column = 1)
rb2 = Radiobutton(fenetrePrincipale, text = "Rejected", variable=var3, value = '2', command=viewSelected3).grid(row = 7, column = 2)
rb3 = Radiobutton(fenetrePrincipale, text = "Use algorithm", variable=var3, value = '3', command=viewSelected3).grid(row = 7, column = 3)


var4 = IntVar()
u1 = Radiobutton(fenetrePrincipale, text = "Yes", variable=var4, value = '1', command=viewSelected3).grid(row = 8, column = 1)
u2 = Radiobutton(fenetrePrincipale, text = "No", variable=var4, value = '2', command=viewSelected3).grid(row = 8, column = 2)




fenetrePrincipale.bind("<Return>", lambda event: envoi(entries))
fenetrePrincipale.mainloop()
