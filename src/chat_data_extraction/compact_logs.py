import gzip


f = open("logs_data/log_paths.txt", "r")
lines = f.readlines()

file_unread_lines=open("logs_data/unread_lines.txt","w")

for l in lines:
    #Put it in windows format file path
    with gzip.open(str(l[1].upper())+':'+l[2:-1], "r") as unzipfile:
        file_content = unzipfile.readlines()
        #print('file read for : '+str(unzipfile.name))
        with open('./logs_data/compact_logs/log-'+unzipfile.name.split('/')[-1].split('.')[0]+str('.txt'),'w') as compact_log:
            for line in file_content:
                try:
                    if line.decode(encoding='unicode_escape',errors='replace').__contains__('[CHAT]'):
                        compact_log.write(line.decode(encoding='unicode_escape',errors='replace')[:-1])
                except:
                    file_unread_lines.write(str(line)+'\n')

print('Done ...')


