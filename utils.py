#Fonte: http://adamlamers.com/post/GRBJUKCDMPOA

def parse_sql(filename):
    data = open(filename, 'r',encoding='utf8').readlines()
    stmts = []
    DELIMITER = ';'
    stmt = ''

    for lineno, line in enumerate(data):
        if not line.strip():
            continue

        if line.startswith('--'):
            continue

        if 'DELIMITER' in line:
            DELIMITER = line.split()[1]
            continue

        if (DELIMITER not in line):
            stmt += line.replace(DELIMITER, ';')
            continue

        if stmt:
            stmt += line
            stmts.append(stmt.strip())
            stmt = ''
        else:
            stmts.append(line.strip())
    return stmts


def run_sql_file(filename, connection):
    '''
    The function takes a filename and a connection as input
    and will run the SQL query on the given connection  
    '''
    #start = time.time()
    
    file = open(filename, 'r',encoding='utf8')
    sql = s = " ".join(file.readlines()).rstrip()
    #print "Start executing: " + filename + " at " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")) + "\n" + sql 
    cursor = connection.cursor()
    cursor.execute(sql)    
    connection.commit()
    
   # end = time.time()
   # print "Time elapsed to run the query:"
    #print str((end - start)*1000) + ' ms'