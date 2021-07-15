from colorama import Style, init, Fore, Back
from time import sleep
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os, pyttsx3 as p3, datetime as dt, speech_recognition as sc,wikipedia as wk, smtplib as sm, getpass as gt, webbrowser as wb, pyautogui as pa, psutil as ps

__name = 'ayer'
__prop = 'diego'
__acco = 'identifiedbyOOO@gmail.com'

init()
print(Fore.RED) #color rojo de texto en consola
engine = p3.init()#iniciamos el motor de voz
voices =  engine.getProperty('voices')#carga de voz 
engine.setProperty('voices', voices[2].id) #modificamos tipo de voz
newVoiceRate = 185 #velocidad de reproduccion de voz
engine.setProperty('rate', newVoiceRate) #modificamos propiedades del motor de voz
command = sc.Recognizer()#reconocimiento de voz a texto 
#------------------------------------------------------- 
def superior(param):
    engine.say(param)
    engine.runAndWait()    

def voiceToCommand():
    with sc.Microphone() as resource:
        command.pause_threshold = True
        audio = command.listen(resource)
    try:
        query = command.recognize_google(audio,language="es-ES").lower()
        print(query)
    except Exception: #esta bien retroceder en modulos y verificar el error que da en el audio
        superior("Señor, no reconozco la instrucción")
        return None        
    return query
    
def wellcome ():
    hours = dt.datetime.now().hour
    if (hours >= 6 and hours <12):
        engine.say("Buenos días señor")
        engine.runAndWait()
    elif(hours >= 12 and hours <18):
        engine.say("Buenas tardes señor")
        engine.runAndWait()
    elif(hours >= 18 and hours <=24):
        engine.say("Buenas noches señor")
        engine.runAndWait()
        dt.time(2)
        superior("Estamos en línea")
    superior("¿En que puedo apoyarlo?")
        
def seeyou():
    engine.say("Nos vemos pronto")
    engine.runAndWait()   
    
def hour():
    timy = dt.datetime.now().strftime("La hora actual es " + "%I:%M:%S")
    engine.say(timy)
    engine.runAndWait()
    
def date():
    dat = dt.datetime.now().date()
    engine.say(dat)
    engine.runAndWait()
    
def createFile():
    superior("Señor, solicito un nombre para el archivo")
    sleep(1)
    try:
        namefile = voiceToCommand()
        #superior("Extensión del archivo")    
        extefile = voiceToCommand()
        doc = open ("documentsIA/"+namefile+".txt", "w") #estaria bien listar la lista de contenido y validar la 'ya' existencia de una archivo
        superior("Archivo creado satisfactoriamente")
        doc.close()
    except ValueError as ve:
        print("exception : " + (ve))
        
def __saveRecordatorio():
    superior("Señor, que desea que guarde para recordarle")
    msg = voiceToCommand()
    try:
        fileRecordatorio = open ('documentsIA/fileRecordatorio.txt','r')
        with fileRecordatorio as fr:
            if (sum (1 for _ in fr)>0):
                fileRecordatorio = open('documentsIA/fileRecordatorio.txt','a')
                fileRecordatorio.write("\n"+msg)    
                fileRecordatorio.close()
            else:
                fileRecordatorio = open ('documentsIA/fileRecordatorio.txt','w')
                fileRecordatorio.write(msg)
                fileRecordatorio.close()
    except FileNotFoundError:
        superior('Señor, tengo inconvenientes con guardar el contenido en el archivo')

def saveRecordatorio():
    __saveRecordatorio()

def __readRemainder():
    newVoiceRate = 140
    try:
        fileRead = open ('documentsIA/fileRecordatorio.txt','r')
        contentFile = fileRead.readlines()
        superior("Señor recuerde que : ")
        for i in contentFile:
            superior(i)
    except Exception as e:
        print("Señor, tengo errores en la lectura del recordatorio")
        
def readRemainder():
    __readRemainder()
    
def __webChrome():
    superior("Abriendo navegador Chrome, ¿Qué busco señor??")
    pathChrome = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
    yousearch = voiceToCommand()
    superior('Accediendo a ' + yousearch + '.com')
    wb.get(pathChrome).open_new_tab(yousearch + '.com')
    superior("¿Le puedo ayudar con algo más señor?")
    voiceToCommand()

def webChrome():
    __webChrome()

def __wiki():
    superior("Señor que busco en wikipedia")
    try:
        responseWiki = voiceToCommand()
        querywk = responseWiki.replace('search','')
        response = wk.summary(querywk, sentences = 2)
        superior("¿Señor desea que lea la información?")
        read = voiceToCommand().lower()
        if (('okay' in read) or ('claro' in read) or ('si' in read)):
            newVoiceRate = 160
            superior(response)
        elif (('not' in read) or ('no' in read)):
            superior("Puedo apoyarle con algo más señor??")
            
    except Exception as error:
        superior("lo siento señor, no encuentro esa información")
        
def wiki():
    __wiki()


def __send_mail():
    cont = 0
    #account from and to
    faddress = __prop + '<' + __acco + '>' #from
    taddress = 'AMIGO<identifiedbyOOO@gmail.com>'#to
    #affair from email
    affair = "Asistente IA Yesterday v1.0"
    server = sm.SMTP('smtp.gmail.com:587')
    #cipher
    server.starttls()
    #credentials
    superior("Escriba la contraseña")
    pasw = gt.getpass("password: ")
    try:
        server.login(__acco,pasw)         
        superior("¿Qué escribo en el email? ")
        msg = voiceToCommand()
        superior("¿Esta bien el email señor?")
        print("Contenido del email: " + msg)
        temp = voiceToCommand()
        if (('okay' in temp) or ('yes' in temp) or ('si esta bien' in temp) or ('si' in temp)):
            #debug operations
            server.set_debuglevel(1)
            #header email
            header = MIMEMultipart()
            header['Subject'] = affair #Asunto del email
            header['From'] = faddress
            header['To'] = taddress
            msg = MIMEText(msg, 'html')
            header.attach(msg)
            server.sendmail(faddress,taddress,header.as_string())
            superior("Envío autorizado, ... Enviando...")
            server.quit()
        elif (('no' in temp) or ('not' in temp)):
            superior("Reintegrando email, se solicitará la contraseña nuevamente, es por seguridad señor")
            server.quit()
            __send_mail()
    except Exception as ex:
        print("Error: "+ex.message)
        superior("Lo siento señor, tengo inconvenientes con el envío del correo, asegurese de haber escrito correctamente la contraseña")
        superior("¿desea seguir con el proceso?")
        recept = voiceToCommand()
        if 'yes' in recept:
            superior("Procedo a reeintegrar el email, se solicitará la contraseña nuevamente, es por seguridad señor")
            cont+1
            __send_mail()
        elif (('not' in recept) or ('no' in recept)):
            superior("Cancelando procesos, redirigiendo...")
            voiceToCommand()
        
def send():
    __send_mail()
    
def shutdownMachine():
    """shutdown
        -s : 'Apaga equipo' 
        -h : 'Bloqueo del equipo'
        -r : 'Reinicio de equipo'
        -t : 'Establece tiempo de duradez de instrucción'
        -l : 'Logout del sistena'
        -a : 'Cancela instrucción'
        -c : 'Establece mensaje de la acción sobre el equipo',-> -c 'Apagando equipo'
        -i : 'GUI de gestión de comandos'
    """
    superior("¿Qué acción desea realizar señor?")
    operation = voiceToCommand()
    if ('interface' in operation):
        superior("Abriendo interfaz de gestión manual")
        os.system("shutdown /i")
    elif ('logout' in operation):
        superior("Cerrando sesión")
        os.system("shutdown /l ")
    elif ('turn off' in operation):
        superior("Apagando sistema")
        os.system("shutdown /s /t 3")
    elif ('restart' in operation):
        superior("Reiniciando sistema")
        os.system("shutdown /r /t 3")
    elif ('block' in operation):
        superior("Bloqueando sistema")
        os.system("shutdown /h")
    else:
        superior("Parametro no reconocido")
        shutdownMachine()

def listenToMusic():
    try:
        
        item = 1
        musicpath = 'C:/Users/lenovo/Music/' #path of folder content of Music
        songs = os.listdir(musicpath)
        #print(type(song))
        superior("Listando canciones disponibles... ")
        for song in songs:
            print('\n' + str(item) + ".- " + song)
            if 'desktop.ini' in song:
                item-=1
            item+=1
        superior("Señor, ingrese número de canción que desea escuchar...")
        responseSong = int(input("\nIngrese número de canción: "))
        os.startfile(os.path.join(musicpath,songs[responseSong]))
        sleep(3)
        superior("¿Le puedo ayudar con algo más señor?")
        pausesong = voiceToCommand()
        """if 'pause music' in pausesong:
            os.pause(os.path.join(musicpath,songs[responseSong]))"""
    except FileNotFoundError as ffe:
        superior("Señor no encuentro la ruta la música")    

def screenshot():
    takeScreen = pa.screenshot()
    nameScreen = "picture"
    try:
        list_files = os.listdir("C:/Users/lenovo/Desktop/yesterday/imgs/") #Devuelve lista de objS
        contScren = 1
    
        for i in list_files:# Bucle define total de objs en el directorio
           contScren+=1
    
        if contScren==0:
            takeScreen.save("imgs/" + nameScreen + str(contScren) + ".png")
        else:
            takeScreen.save("imgs/" + nameScreen + str(contScren) + ".png")
        
        superior("Guardando imagen")
    except Exception as tp:
        print(tp)
        superior("Señor, tengo inconvenientes al guardar la imagen")
        
def __screenshot():
    screenshot()

def virtualMachine():
    pathVM = os.listdir('C:/')
    for i in pathVM:
        print(i)
                    
def __principal():
    wellcome()
    while True:
        query = voiceToCommand()
        if(__name in query):
            superior('¿En qué puedo ayudarle señor? ')
        elif (('Cual es tu nombre' in query) or ('dime tu nombre' in query)):
            superior("Mi nombre es " + __name)
        elif (('cual es la hora'in query) or ('dime la hora' in query)):
            hour()
        elif (('qué día es hoy' in query) or ('hoy es' in query) or ('el dia de hoy es' in query)):
            date()
        elif (('abre wikipedia' in query) or ('wikipedia' in query)):
            wiki()
        elif (('envia un correo' in query) or ('correo' in query) or ('envia un email' in query)):
            send()          
        elif (('a dormir' in query) or ('descansa' in query) or ('ve a descansar' in query)):
            superior("Señor, fue un placer atenderle")
            seeyou()
            quit()
        elif (('abre chrome' in query) or ('busca en chrome' in query)):
            webChrome()             
        elif (('shutdown' in query) or ('apaga ordenador' in query)):
            superior("Entrando a parametros del comando shutdown")#shutdown - comando que gestiona 
            shutdownMachine()
        elif ('reproduce música' in query):
            listenToMusic()
        elif ('crea un archivo' in query):
            createFile()
        elif (('guardame un recordatorio' in query) or ('puedes guardarme algo' in query)):
            saveRecordatorio()
        elif (('recuerdame' in query) or ('que tengo pendiente' in query)):
            readRemainder()
        elif ('yesterday'in query):
            superior("Digame Señor")
        elif ('presentación' in query):
            superior("Soy Yesterday, asistente oficial virtual de " + __prop + ", trabajo con módulos creados por inteligencia humana, fui creada en el año 2021, actualmente estoy en constante actualización, ¡Saludos!")
        elif ('screenshot' in query):
            screenshot()
            

def executes():
    __principal()

superior("Cargando...")
executes()
