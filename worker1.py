import requests
import urllib
import time
import sys
import os
from github import Github
from github import Auth
import datetime

try:
    github_token = sys.argv[1]
    bot_token = sys.argv[2]
    bot_chatID = sys.argv[3]
except IndexError:
    print("not all parameters")
    os._exit(0)
import os
os.system('apt-get update&& apt-get install -y python3-pip python3-setuptools python3-pandas python3-yaml python3-requests&& apt-get install -y git')
dataVersion = requests.get('https://github.com/github/codeql-cli-binaries/releases/latest')
dataVerIns = dataVersion.text.split('<title>Release v')[1].split(' · github/codeql-cli-binaries')[0]

os.system("cd /opt/&&sudo mkdir codeqlmy&&cd codeqlmy&&sudo git clone https://github.com/github/codeql.git codeql-repo") 
os.system("cd /opt/codeqlmy&&sudo wget https://github.com/github/codeql-cli-binaries/releases/download/v"+dataVerIns+"/codeql-linux64.zip&&sudo unzip codeql-linux64.zip&&sudo rm codeql-linux64.zip")

folderName = '/tmp/works/'
fileExitCode = '/tmp/check123'
foldDBtmp = '/tmp/dbtmp/'
resultFile = '/tmp/1.csv'



with open('repoList','r') as flist:
    for j in flist.readlines():
        userName = j.split('_|_')[0]
        repoName = j.splitlines()[0].split('_|_')[1]
        prebuildLine = j.splitlines()[0].split('_|_')[2]

        auth = Auth.Token(github_token)
        g = Github(auth=auth)
        repo = g.get_repo(userName+"/"+repoName)
        gitUrl = 'https://github.com/'+userName+'/'+repoName
        since = datetime.datetime.now() - datetime.timedelta(days=1)
        commits = repo.get_commits(since=since)

        index = 1
        os.system('rm -rf '+folderName)
        os.system("git clone "+gitUrl+' '+folderName)
        for i in commits:
            gitCommit = i.commit.sha[:8]
            os.system('cd '+folderName+'&&git checkout '+gitCommit)
            os.system('cd '+folderName+'&&'+prebuildLine)
            os.system('rm -rf '+foldDBtmp)
            os.system("rm -rf "+folderName+"_lgtm*")
            os.system("sudo echo 321 > "+fileExitCode)
            os.system("timeout 60m /opt/codeqlmy/codeql/codeql database create --language=cpp --source-root="+folderName+" -- "+foldDBtmp+" &&sudo echo $? > "+fileExitCode)
            
            echoCode = open(fileExitCode, 'r').read()
            if echoCode.startswith("0"):
                os.system('rm -rf '+resultFile)
                os.system('/opt/codeqlmy/codeql/codeql database analyze '+foldDBtmp+'  codeql/cpp-queries:codeql-suites/cpp-code-scanning.qls --format=csv --output='+resultFile)
                if os.path.exists(resultFile):
                    num_lines = sum(1 for _ in open(resultFile))
                    os.system('cp '+resultFile+' ./result/'+datetime.date.today().strftime("%d%m%Y")+'_'+userName+'_'+repoName+'_'+gitCommit)
                else:
                    num_lines = 0
                bot_message = 'count detect codeql = '+str(num_lines)+'\n https://github.com/'+userName+'/'+repoName+'/commit/'+gitCommit
                send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
                response = requests.get(send_text)
            else:
                bot_message = 'error build \n https://github.com/'+userName+'/'+repoName+'/commit/'+gitCommit
                send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
                response = requests.get(send_text)
            index+=1
            if index >1:
                break
os.system('echo \"'+datetime.date.today().strftime("%d%m%Y")+'_'+userName+'_'+repoName+'\" >> ./result/tmp')
