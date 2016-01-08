import subprocess, os, shlex, shutil, ctypes, time, threading
from clint.textui import colored, indent, puts

#TODO

dbv = '2232'
bill = 'BILLING'
user = 'RF_User'
world = 'RF_World'
billf = 'RF_RusBill'
billl = 'RF_RusBill_log'
userf = 'RF_User_Data'
userl = 'RF_User_Log'
worldf = 'RF_World'
worldl = 'RF_World_log'
FNULL = open(os.devnull, 'w')

class Whatever(threading.Thread):

    def __init__(self, threadID, name, filename):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.filename = filename

    def run(self):
        if os.path.isfile(self.filename):
            # print "Starting " + self.name
            extract_files(self.filename)
        

def extract_files(file):
    cwd = os.getcwd()
    extractor = 'unrar.exe'
    if os.path.isfile(extractor):
        if file == dbrar:
            args = "unrar x -y 'db{0}.rar' '{1}\\db\\'".format(dbv, cwd)
            lex = shlex.split(args)
            proc = subprocess.Popen(lex)
            proc.wait()
        elif file == serverrar:
            args = "unrar x -y '{0}' '{1}\\'".format(file, cwd)
            lex = shlex.split(args)
            proc = subprocess.Popen(lex)
            raw_input('Press any key to continue...')
        elif file == emulatorrar:
            args = "unrar x -y '{0}' 'C:\\AppServ\\'".format(file)
            lex = shlex.split(args)
            proc = subprocess.Popen(lex)
            proc.wait()
    else:
        print "I can't extract these files...unrar.exe not found!"
        raise SystemExit


def setup_mssql():
    proc = subprocess.Popen('SQL\SQLEXPRWT_x64_ENU.exe /extract: SQL\\a', stdout=FNULL, stderr=FNULL)
    proc.wait()


def create_instance():
    args = "SQL\\a\\Setup.exe /qs /ACTION=Install /FEATURES=SQL,Tools /INSTANCENAME=MSSQLSERVER /SQLSVCACCOUNT=\"NT AUTHORITY\Network Service\" /ADDCURRENTUSERASSQLADMIN /AGTSVCACCOUNT=\"NT AUTHORITY\Network Service\" /SECURITYMODE=SQL /SAPWD=wanker12 /IACCEPTSQLSERVERLICENSETERMS"
    proc = subprocess.Popen(args, stdout=FNULL, stderr=FNULL)
    proc.wait()


def set_path_mssql():
    os.system('set Path="%ProgramFiles%\Microsoft SQL Server\100\Tools\Binn";%Path%')
    os.system('set Path="%ProgramFiles(x86)%\Microsoft SQL Server\100\Tools\Binn";%Path%')


def set_path_python():
    os.system('set Path="C:\Python27";%Path%')
    os.system('set Path="C:\Python27\Scripts";%Path%')


def install_python_modules():
    subprocess.Popen('pip install flask', stdout=FNULL, stderr=FNULL)
    subprocess.Popen('pip install flask-wtf', stdout=FNULL, stderr=FNULL)
    subprocess.Popen('pip install pyodbc', stdout=FNULL, stderr=FNULL)
    subprocess.Popen('pip install passlib', stdout=FNULL, stderr=FNULL)


def create_db(db):
    args = "sqlcmd -S (local) -Q \"create database {0}\"".format(db)
    proc = subprocess.Popen(args, stdout=FNULL, stderr=FNULL)
    return proc


def restore_billing():
    cwd = os.getcwd()
    args = "sqlcmd -S (local) -Q \"RESTORE DATABASE {0} FROM DISK = N'{3}\\db\\{0}.bak'WITH FILE = 1, MOVE N'{1}' TO N'{3}\\db\\{0}.mdf', MOVE N'{2}' TO N'{3}\\db\\{0}.LDF', NOUNLOAD, REPLACE,  STATS = 10\"".format(bill, billf, billl, cwd)
    proc = subprocess.Popen(args, stdout=FNULL, stderr=FNULL)


def restore_rfuser():
    cwd = os.getcwd()
    args = "sqlcmd -S (local) -Q \"RESTORE DATABASE {0} FROM DISK = N'{3}\\db\\{0}.bak'WITH FILE = 1, MOVE N'{1}' TO N'{3}\\db\\{0}.mdf', MOVE N'{2}' TO N'{3}\\db\\{0}.LDF', NOUNLOAD, REPLACE,  STATS = 10\"".format(user, userf, userl, cwd)
    proc = subprocess.Popen(args, stdout=FNULL, stderr=FNULL)


def restore_rfworld():
    cwd = os.getcwd()
    args = "sqlcmd -S (local) -Q \"RESTORE DATABASE {0} FROM DISK = N'{3}\\db\\{0}.bak'WITH FILE = 1, MOVE N'{1}' TO N'{3}\\db\\{0}.mdf', MOVE N'{2}' TO N'{3}\\db\\{0}.LDF', NOUNLOAD, REPLACE,  STATS = 10\"".format(world, worldf, worldl, cwd)
    proc = subprocess.Popen(args, stdout=FNULL, stderr=FNULL)


def odbcconf():
    subprocess.Popen('ODBCCONF.exe /a { CONFIGDSN "SQL Server" "DSN=bill|SERVER=(local)|Trusted_Connection=Yes|Database=bill"}', stdout=FNULL, stderr=FNULL)
    subprocess.Popen('ODBCCONF.exe /a { CONFIGDSN "SQL Server" "DSN=user|SERVER=(local)|Trusted_Connection=Yes|Database=user"}', stdout=FNULL, stderr=FNULL)
    subprocess.Popen('ODBCCONF.exe /a { CONFIGDSN "SQL Server" "DSN=user|SERVER=(local)|Trusted_Connection=Yes|Database=user"}', stdout=FNULL, stderr=FNULL)


def copy_dll():
    dllfile = 'C:\\AppServ\php5\\ntwdblib.dll'
    exefile = 'RF Online.exe'
    if os.path.isfile(dllfile):
        shutil.copy2('C:\\AppServ\php5\\ntwdblib.dll', 'C:\\Windows')
        shutil.copy2('C:\\AppServ\\php5\\ntwdblib.dll', 'C:\\Windows\\system32')
        shutil.copy2('C:\\AppServ\\php5\\ntwdblib.dll', 'C:\\Windows\\SysWow64')
        if os.path.isfile(exefile):
            shutil.copy2(exefile, 'C:\\Program Files (x86)\\CCR INC\\RFOnline\\')
        else:
            print "File %s not found!" % exefile
    else:
        print "File %s not found!" % dllfile


def restart_mssql():
    args = "net.exe stop \"MSSQLSERVER\" && net.exe start \"MSSQLSERVER\""
    lex = shlex.split(args)
    proc = subprocess.Popen(lex, stdout=FNULL, stderr=FNULL)
    proc.wait()


def restart_apache():
    args = "net.exe stop \"apache2.2\" && net.exe start \"apache2.2\""
    lex = shlex.split(args)
    proc = subprocess.Popen(lex, stdout=FNULL, stderr=FNULL)
    proc.wait()


def start_server():
    checkpath = os.path.dirname(os.path.realpath(__file__)) + '\Server2232'
    loginpath = os.path.dirname(os.path.realpath(__file__)) + '\Server2232\Account and Login\RF_Bin'
    zonepath = os.path.dirname(os.path.realpath(__file__)) + '\Server2232\Zone Server\RF_Bin'
    os.chdir(loginpath)
    if os.path.isdir(checkpath):
        print "Starting AccountServer..."
        time.sleep(5)
        args1 = loginpath + '\AccountServerSD.exe'
        p1 =subprocess.Popen(args1)
        print "Starting BillingAgent..."
        time.sleep(5)
        args2 = loginpath + '\BillingAgentSD.exe'
        p2 = subprocess.Popen(args2)
        print "Starting LoginServer..."
        time.sleep(5)
        args3 = loginpath + '\LoginServerSD.exe'
        p3 = subprocess.Popen(args3)
        # [subprocess.Popen(args) for args in args1, args2, args3]
        path = zonepath
        os.chdir(path)
        print "Starting ZoneServer..."
        time.sleep(5)
        args4 = zonepath + '\ZoneServerUD_x64.exe'
        with indent(4, quote='>>>'):
            puts(colored.red('Important: ') + 'Type /open to LoginServer to enable normal account login.')
            subprocess.Popen(args4)
            time.sleep(20)
    else:
        print "Run Server Setup first."


def start_web():
    try:
        checkpath = os.path.dirname(os.path.realpath(__file__)) + '\\Web\\'
        if os.path.isdir(checkpath):
            app = 'app.py'
            args = 'python2 {0}{1}'.format(checkpath, app)
            subprocess.Popen(args)
            with indent(4, quote='>>>'):
                puts(colored.green('Success: ') + 'Visit this link to register http://127.0.0.1:8666/gm')
        else:
            print "Run Server Setup first."
    except:
        print "Run Server Setup first."


def start_game():
    try:
        path = "C:\Program Files (x86)\CCR INC\RFOnline" 
        os.chdir(path)
        if os.path.isdir(path):
            with indent(4, quote='>>>'):
                subprocess.Popen(path + 'RF Online.exe')
                puts(colored.green('Success: ') + 'Enjoy!')
                time.sleep(20)
        else:
            p1 = subprocess.Popen('2232-PlayRF\RFOnline_Setup.exe')
            p1.wait()
            if p1.returncode == 0:
                p2 = subprocess.Popen('dependencies\RF Account & Login.msi')
                p2.wait()
                if p2.returncode == 0:
                    p3 = subprocess.Popen('dependencies\RF World & Login.msi')
    except:
        print "Install RF Client first!"


def welcome():
    with indent(1, quote=' '):
        puts('================================================================')
        puts('=                    *Installation-Menu*                       =')
        puts('=  ==========================================================  =')
        puts('=  = #Choose from 1-4                                       =  =')
        puts('=  =  1. Start Server Setup                                 =  =')
        puts('=  =  2. Start Game Server                                  =  =')
        puts('=  =  3. Start Web Control Panel                            =  =')
        puts('=  =  4. Start Game                                         =  =')
        puts('=  ==========================================================  =')
        puts('=                      by : jjan                               =')
        puts('================================================================')


if __name__ == '__main__':
    welcome()
    input = int(raw_input("Input:  ") or "1")
    if input == 1:
        dbrar = 'db2232.rar'
        emulatorrar = 'Emulator.rar'
        serverrar = '2232.rar'
        thread1 = Whatever(1, "Worker#1", dbrar)
        thread2 = Whatever(2, "Worker#2", serverrar)
        thread3 = Whatever(3, "Worker#3", emulatorrar)
        thread1.start()
        thread2.start()
        thread3.start()
        raw_input('Press any key to continue...')
        copy_dll()

        #Configure MSSQL
        print "Configuring MSSQL..."
        db1 = bill
        db2= user
        db3 = world
        setup_mssql()
        create_instance()
        set_path_mssql()
        create_db(db1)
        create_db(db2)
        create_db(db3)
        restore_billing()
        restore_rfuser()
        restore_rfworld()
        odbcconf()
        raw_input('Press any key to continue...')

        #Configure Web CPANEL
        print "Configuring Web CPANEL..."
        set_path_python()
        install_python_modules()
        # restart_mssql()
        # restart_apache()
        with indent(4, quote='>>>'):
            puts(colored.green('Success: ') + 'Installation Complete!')
            time.sleep(10)

    elif input == 2:
        start_server()

    elif input == 3:
        start_web()

    elif input == 4:
        start_game()
