import re,os
#group
class Group:
    def __init__(self, seq, level):
        self.seq = seq
        self.level = level
        self.storageList = []
    def __str__(self):
        return "%s"%(self.seq)
#storage
class Storage:
    def __init__(self, seq, ip, port):
        self.seq = seq
        self.ip = ip
        self.port = port

group=Group(-1, -1)
groupList=[]

file_path = r'/tmp/monitor.log'
file = open(file_path, 'r')
lines = file.readlines()
#line group name = group1
emRegex = re.compile(r"^(.*)=(\D*)(\d+)$")
#line Storage 1:
storageNRegex = re.compile(r"^(\D*)(\d+)([:].*)$")
#IP
ipRegex = re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b")

for ii in lines :
    #get level
    line = re.sub(r"[\n|\r]+", '', ii)
    level = len(line)-len(line.lstrip())
    if level == 0:
        if re.match('group name', line):
            mo = emRegex.search(line)
            seq = mo.group(3).strip()
            print('group' + seq)
            group = Group(seq, level)
            groupList.append(group)
    elif level == 1:
        mo = storageNRegex.search(line)
        seq = mo.group(2)
        storage = Storage(seq, '', '')
        group.storageList.append(storage)
        print(seq)
    elif level == 2:
        if re.match('ip_addr', line.lstrip()):
            ipaddr = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", line)
            storage.ip = ipaddr[0]
            print(ipaddr[0])
        elif re.match('storage_http_port', line.lstrip()):
            port = re.findall(r"\b(?:\d+)\b", line)
            storage.port = port[0]
            print(port[0])

file.close()

#output
file_name = '/nginx_conf/conf.d/tracker.conf'
if os.path.exists(file_name):
    os.remove(file_name)
f = open(file_name, 'w')

##########
for g in groupList:
    f.write('upstream fdfs_group' + g.seq + ' {\n')
    for s in g.storageList:
        f.write('\tserver ' + s.ip + ':' + s.port + ' weight=1 max_fails=2 fail_timeout=30s;\n')
    f.write('}\n')

f.write('server {\n')
f.write('\tlisten       8000;\n')
f.write('\tserver_name  localhost;\n')
f.write('\n')
for g in groupList:
    f.write('\tlocation /group' + g.seq + '/M00 {\n')
    f.write('\t\tproxy_pass http://fdfs_group' + g.seq + ';\n')
    f.write('\t}\n')
f.write('}\n')
##########
f.close()