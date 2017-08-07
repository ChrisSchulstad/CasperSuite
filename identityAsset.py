import subprocess

# Uses subprocess to run a curl
def runCurl(myString):
        p = subprocess.Popen(curl_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = p.stdout.read()
        return output

# Must specify Casper Suite login credentials
username = ""
password = ""
domain = ""

# Create CSV Header
print "identity,prefix,nick,first,last,suffix,email,phone,phone2,managedBy,priority,bunit,category,watchlist,startDate,endDate,work_city,work_country,work_lat,work_long"

# Curl command to grab all user ids
curl_cmd = "curl -s -k -u \'" + username + ":" + password + "\' https://" + domain + "/JSSResource/users | tr \'>\' \"\\n\" | grep \"</id\" | cut -f1 -d\'<\'"
output = runCurl(curl_cmd)

# Creates and populates a dynamic list with user ids
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

#Curl each user id for user info
for id in myIDs:
        curl_cmd = "curl -s -k -u \'" + username + ":" + password + "\' https://" + domain + "/JSSResource/users/id/" + id + " | tr \'>\' \"\\n\" | egrep \"</name|</full_name|</email_address|</phone_number|</position\" | cut -f1 -d\'<\' | tr \"\n\" \",\""
        output = runCurl(curl_cmd)

        #Parses the user info for csv format
        name = ""
        last = ""
        first = ""
        email = ""
        phone = ""
        bunit = ""
        index = 0
        for char in output:
                if char == ',':
                        index += 1
                else:
                        if index == 0:
                                name += char
                        elif index == 1:
                                last += char
                        elif index == 2:
                                if char != ' ':
                                        first += char
                        elif index == 3:
                                email += char
                        elif index == 4:
                                phone += char
                        else:
                                bunit += char

        output = "" + name + ", , ," + first + "," + last + ", ," + email + "," + phone + ", , , ," + bunit + ", , , , , , , , "
        print output
