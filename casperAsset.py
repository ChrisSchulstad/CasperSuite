import subprocess

# Uses suprocess to run a curl
def runCurl(myString):
        p = subprocess.Popen(myString, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = p.stdout.read()
        return output

# Must specify Casper Suite login credentials
username = ""
password = ""
domain = ""

# Create CSV Header
print "category,city,country,ip,lat,long,address,owner"

# Curl command to grab all computer ids
curl_cmd = "curl -s -k -u \'" + username + ":" + password + "\' https://" + domain + "/JSSResource/computers/subset/basic | tr \'>\' \"\\n\" | grep \"</id\" | cut -f1 -d\'<\'"
output = runCurl(curl_cmd)

# Creates and populates a dynamic list with computer ids
myIDs = []
index = 0
temp = ""
for char in output:
        if char != '\n':
                temp += char
        else:
                myIDs.append(temp)
                temp = ""
        index += 1

# Curls each computer id for computer info - lat/long/country found with ip lookuptable
for id in myIDs:
        curl_cmd = "curl -s -k -u \'" + username + ":" + password + "\' https://" + domain + "/JSSResource/computers/id/" + id + " | tr \'>\' \"\\n\" | egrep \"</ip_address|</mac_address|</username|</building\" | cut -f1 -d\'<\' | tr \"\n\" \",\""
        output = runCurl(curl_cmd)

        #Parses the computer info for csv format
        mac = ""
        ip = ""
        owner = ""
        city = ""
        index=0
        for char in output:
                if char == ',':
                        index += 1
                else:
                        if index == 0:
                                mac += char
                        elif index == 1:
                                ip += char
                        elif index == 2:
                                owner += char
                        else:
                                city += char

        output = "mac," + city + ",," + ip + ",,," + mac + "," + owner
        print output
