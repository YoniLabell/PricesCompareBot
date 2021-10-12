import sqlite3


def sqldb(uname,uid,itemid,itemname,addeletall):
    try:

        con=sqlite3.connect('customer.db')
        c=con.cursor()
        tablename=str(uname)+str(uid)
        try:
            c.execute("CREATE TABLE "+ tablename+" (ID TEXT PRIMARY KEY , NAME CHAR(50));")
        except:
            pass
        if addeletall=="add":
            c.execute('INSERT INTO '+ tablename+'(ID,NAME) VALUES(?,?)',(itemid,itemname))
            con.commit()
            con.close()
            return "הוספתי"

        elif addeletall=="delete":
            c.execute("DELETE FROM "+ tablename+" WHERE ID=(?)",(itemid,))
            con.commit()
            con.close()
            return "מחקתי"

        elif addeletall=="all":
            c.execute("SELECT NAME FROM "+ tablename)
            l=c.fetchall()

            con.commit()
            con.close()
            flat_list = [item for sublist in l for item in sublist]
            str1 = "\n".join(flat_list)
            return(str1+'\n'+"📌")

        elif addeletall=="delall":
            try:
                c.execute("DROP TABLE "+ tablename)
                con.commit()
                con.close()

            finally:
                return "מחקתי"



        elif addeletall=="list":
            c.execute("SELECT ID FROM "+ tablename)
            l=c.fetchall()

            con.commit()
            con.close()
            flat_list = [item for sublist in l for item in sublist]
            str1 = ",".join(flat_list)
            return(str1)

    except:
        return "לא הבנתי"

def users_DB(uid,uname,action,ustor="talp"):
    try:
        con=sqlite3.connect('customer.db')
        c=con.cursor()
        tablename="USERS"
        try:
            c.execute("CREATE TABLE "+ tablename+" (ID TEXT PRIMARY KEY, NAME CHAR(50),STOR CHAR(50));")
        except:
            pass

        if action=="add":
            c.execute('INSERT INTO '+ tablename+'(ID,NAME,STOR) VALUES(?,?,?)',(uid,uname,ustor))
            con.commit()
            con.close()
            return "add"

        elif action=="update_store":
            c.execute("Update USERS set STOR = '"+ustor+"' where ID = '"+uid+"'")
            con.commit()
            con.close()
            return "update"

        elif action=="get_usr_stor":
            c.execute('SELECT STOR FROM USERS WHERE ID ='+uid)
            l=c.fetchall()
            con.commit()
            con.close()
            return str(l[0][0])


        elif action=="selectall":
            c.execute('SELECT * FROM USERS')
            l=c.fetchall()
            con.commit()
            con.close()
            return str(l)



    except:

        return "לא הבנתי"













#test
#print(sqldb("tabl","3456","456","k.hvg","add"))
#print(sqldb("tabl","3456","456","i","all"))
