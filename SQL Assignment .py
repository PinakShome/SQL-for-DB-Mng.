#!/usr/bin/env python
# coding: utf-8

# # SQL Assignment

# In[2]:


import pandas as pd
import sqlite3

from IPython.display import display, HTML


# In[3]:


conn = sqlite3.connect("/Users/pinakshome/Downloads/Db-IMDB-Assignment.db")
cur=conn.cursor()


# #### Overview of all tables

# In[4]:


tables = pd.read_sql_query("SELECT NAME AS 'Table_Name' FROM sqlite_master WHERE type='table'",conn)
tables = tables["Table_Name"].values.tolist()


# In[4]:


for table in tables:
    query = "PRAGMA TABLE_INFO({})".format(table)
    schema = pd.read_sql_query(query,conn)
    print("Schema of",table)
    display(schema)
    print("-"*100)
    print("\n")


# In[74]:


pd.read_sql_query('''SELECT Name FROM Person where trim(Name) Like 'Yash Chopra' ''' ,conn)


# In[5]:


pd.read_sql_query('SELECT COUNT(*) FROM Person',conn)


# <h3> Preprocessing year in movies

# In[6]:


pd.read_sql_query('SELECT year FROM Movie',conn)


# <h2> we will use the cast substring when selecting year from now 

# <h2> We will use trim(whatever column name) to remove trailing spaces

# ## Useful tips:
# 
# 1. the year column in 'Movie' table, will have few chracters other than numbers which you need to be preprocessed, you need to get a substring of last 4 characters, its better if you convert it as int type, ex: CAST(SUBSTR(TRIM(m.year),-4) AS INTEGER)
# 
# 2. For almost all the TEXT columns we have show, please try to remove trailing spaces, you need to use TRIM() function
# 
# 3. When you are doing count(coulmn) it won't consider the "NULL" values, you might need to explore other alternatives like Count(*)

# ## Q1 --- List all the directors who directed a 'Comedy' movie in a leap year. (You need to check that the genre is 'Comedy’ and year is a leap year) Your query should return director name, the movie name, and the year.

# <h4>To determine whether a year is a leap year, follow these steps:</h4>
# 
# <ul>
#     <li><b>STEP-1:</b> If the year is evenly divisible by 4, go to step 2. Otherwise, go to step 5.</li>
#     <li><b>STEP-2:</b> If the year is evenly divisible by 100, go to step 3. Otherwise, go to step 4.</li>
#     <li><b>STEP-3:</b> If the year is evenly divisible by 400, go to step 4. Otherwise, go to step 5.</li>
#     <li><b>STEP-4:</b> The year is a leap year (it has 366 days).</li>
#     <li><b>STEP-5:</b> The year is not a leap year (it has 365 days).</li>
# </ul>
# 
# Year 1900 is divisible by 4 and 100 but it is not divisible by 400, so it is not a leap year.

# In[7]:


get_ipython().run_cell_magic('time', '', "def grader_1(q1):\n    q1_results  = pd.read_sql_query(q1,conn)\n    print(q1_results.head(10))\n    assert (q1_results.shape == (232,3))\n\nquery1= '''SELECT p.Name,m.title,m.year FROM Person p JOIN M_Director md ON p.PID=md.PID join Movie m on m.MID=md.MID\n         WHERE m.MID IN (SELECT m.MID FROM Movie m JOIN M_Genre mg on m.MID=mg.MID where ((SUBSTR(m.year,-4,4)%4=0\n         and SUBSTR(m.year,-4,4)%100!=0) or SUBSTR(m.year,-4,4)%400=0) AND mg.GID IN (SELECT g.GID FROM\n         Genre g JOIN M_genre mg on g.GID=mg.GID WHERE g.Name LIKE '%Comedy%'))'''\n    \ngrader_1(query1)\n\n")


# ## Q2 --- List the names of all the actors who played in the movie 'Anand' (1971)

# In[8]:


get_ipython().run_cell_magic('time', '', 'def grader_2(q2):\n    q2_results  = pd.read_sql_query(q2,conn)\n    print(q2_results.head(10))\n    assert (q2_results.shape == (17,1))\n\n\nquery2 = """SELECT p.Name FROM M_Cast m JOIN Person p on Trim(m.PID)=Trim(p.PID) where m.MID IN\n             (SELECT m.MID FROM M_Cast m JOIN Movie mm on m.MID=mm.MID WHERE mm.title LIKE \'Anand\')"""\ngrader_2(query2)\n')


# ## Q3 --- List all the actors who acted in a film before 1970 and in a film after 1990. (That is: < 1970 and > 1990.)

# In[9]:


get_ipython().run_cell_magic('time', '', '\ndef grader_3a(query_less_1970, query_more_1990):\n    q3_a = pd.read_sql_query(query_less_1970,conn)\n    print(q3_a.shape)\n    q3_b = pd.read_sql_query(query_more_1990,conn)\n    print(q3_b.shape)\n    return (q3_a.shape == (4942,1)) and (q3_b.shape == (62570,1))\n\nquery_less_1970 =""" \nSelect p.PID from Person p \ninner join \n(\n    select trim(mc.PID) PD, mc.MID from M_cast mc \nwhere mc.MID \nin \n(\n    select mv.MID from Movie mv where CAST(SUBSTR(mv.year,-4) AS Integer)<1970\n)\n) r1 \non r1.PD=p.PID \n"""\nquery_more_1990 =""" \nSelect p.PID from Person p \ninner join \n(\n    select trim(mc.PID) PD, mc.MID from M_cast mc \nwhere mc.MID \nin \n(\n    select mv.MID from Movie mv where CAST(SUBSTR(mv.year,-4) AS Integer)>1990\n)\n) r1 \non r1.PD=p.PID """\nprint(grader_3a(query_less_1970, query_more_1990))\n\n# using the above two queries, you can find the answer to the given question \n')


# In[18]:


get_ipython().run_cell_magic('time', '', "def grader_3(q3):\n    q3_results  = pd.read_sql_query(q3,conn)\n    print(q3_results.head(10))\n    assert (q3_results.shape == (300,1))\n\nquery3 = '''Select p.PID from Person p \ninner join \n(\n    select trim(mc.PID) PD, mc.MID from M_cast mc \nwhere mc.MID \nin \n(\n    select mv.MID from Movie mv where CAST(SUBSTR(mv.year,-4) AS Integer)<1970\n)\n) r1 \non r1.PD=p.PID \n \nINTERSECT\n\nSelect p.PID from Person p \ninner join \n(\n    select trim(mc.PID) PD, mc.MID from M_cast mc \nwhere mc.MID \nin \n(\n    select mv.MID from Movie mv where CAST(SUBSTR(mv.year,-4) AS Integer)>1990\n)\n) r1 \non r1.PD=p.PID''' \n         \n         \n                \ngrader_3(query3)\n")


# #### Q4 --- List all directors who directed 10 movies or more, in descending order of the number of movies they directed. Return the directors' names and the number of movies each of them directed.

# In[10]:


#### %%time

def grader_4a(query_4a):
    query_4a = pd.read_sql_query(query_4a,conn)
    print(query_4a.head(10)) 
    return (query_4a.shape == (1462,2))

query_4a =""" SELECT p.PID, Count(*) FROM M_Director m Join Person p on (m.PID)=p.PID Join Movie 
              mm on mm.MID=m.MID group by p.PID"""
print(grader_4a(query_4a))

# using the above query, you can write the answer to the given question


# In[30]:


get_ipython().run_cell_magic('time', '', 'def grader_4(q4):\n    q4_results  = pd.read_sql_query(q4,conn)\n    print(q4_results.head(10))\n    assert (q4_results.shape == (58,2))\n\nquery4 = """ SELECT p.Name,COUNT(m.PID) Movie_count from Person p\n            join M_Director m on Trim(p.PID)=Trim(m.PID) JOIN\n            Movie mm on mm.MID=m.MID GROUP BY m.PID HAVING Movie_count>=10 ORDER BY Movie_count DESC"""\ngrader_4(query4)\n')


# ## Q5.a --- For each year, count the number of movies in that year that had only female actors.

# In[3]:


get_ipython().run_cell_magic('time', '', '\n# note that you don\'t need TRIM for person table\n\ndef grader_5aa(query_5aa):\n    query_5aa = pd.read_sql_query(query_5aa,conn)\n    print(query_5aa.head(10)) \n    return (query_5aa.shape == (8846,3))\n\nquery_5aa ="""SELECT c.MID, p.Gender, COUNT(*) AS Count\n                FROM Person p JOIN M_Cast c\n                ON (p.PID) = Trim(c.PID)\n                GROUP BY c.MID, p.Gender"""\nprint(grader_5aa(query_5aa))\n\ndef grader_5ab(query_5ab):\n    query_5ab = pd.read_sql_query(query_5ab,conn)\n    print(query_5ab.head(10)) \n    return (query_5ab.shape == (3469, 3))\n\nquery_5ab ="""SELECT c.MID, p.Gender, COUNT(*) Count\n                FROM M_Cast c INNER JOIN Person p\n                ON (p.PID) = trim(c.PID) where p.Gender=\'Male\' GROUP BY c.MID, p.Gender Having Count>=1"""\n        \nprint(grader_5ab(query_5ab))\n\n\n# using the above queries, you can write the answer to the given question\n')


# In[94]:


get_ipython().run_cell_magic('time', '', "def grader_5a(q5a):\n    q5a_results  = pd.read_sql_query(q5a,conn)\n    print(q5a_results.head(10))\n    assert (q5a_results.shape == (4,2))\n\nquery5a = '''SELECT SUBSTR(year,-4,4), COUNT(MID) FROM Movie where MID NOT IN\n      (SELECT MID FROM (SELECT c.MID, p.Gender, COUNT(*) Count FROM\n                          M_Cast c INNER JOIN Person p\n                          ON (p.PID) = trim(c.PID) where p.Gender='Male' GROUP BY c.MID, p.Gender Having Count>=1))\n                          GROUP BY MID'''\ngrader_5a(query5a)\n")


# ## Q5.b --- Now include a small change: report for each year the percentage of movies in that year with only female actors, and the total number of movies made that year. For example, one answer will be: 1990 31.81 13522 meaning that in 1990 there were 13,522 movies, and 31.81% had only female actors. You do not need to round your answer.

# In[145]:


#source: https://stackoverflow.com/questions/57743348/sql-query-imdb-data-to-count-the-total-movies-with-only-female-cast-per-year

def grader_5b(q5b):
    q5b_results  = pd.read_sql_query(q5b,conn)
    print(q5b_results.head(10))
    assert (q5b_results.shape == (4,3))

query5b = '''SELECT female_count.Year, ((female_count.OnlyF)*100)/total_count.TT,total_count.TT 
FROM

((SELECT SUBSTR(year,-4,4) Year, COUNT(MID) OnlyF FROM Movie where MID NOT IN
      (SELECT MID FROM (SELECT c.MID, p.Gender, COUNT(*) Count FROM
                          M_Cast c INNER JOIN Person p
                          ON (p.PID) = trim(c.PID) where p.Gender='Male' GROUP BY c.MID, p.Gender Having Count>=1))
                          GROUP BY MID) female_count,
 (SELECT Movie.year MM,count(*) TT FROM Movie group by Movie.year) total_count)
WHERE female_count.year=total_count.MM'''
grader_5b(query5b)


# ### Q6 --- Find the film(s) with the largest cast. Return the movie title and the size of the cast. By "cast size" we mean the number of distinct actors that played in that movie: if an actor played multiple roles, or if it simply occurs multiple times in casts, we still count her/him only once.

# In[156]:


get_ipython().run_cell_magic('time', '', 'def grader_6(q6):\n    q6_results  = pd.read_sql_query(q6,conn)\n    print(q6_results.head(10))\n    assert (q6_results.shape == (3473, 2))\n\nquery6 = """ Select m.title, Count(*) J from Movie m join M_Cast mc on m.MID=mc.MID Group by m.MID ORDER BY\n             J desc"""\ngrader_6(query6)\n')


# ### Q7 --- A decade is a sequence of 10 consecutive years. 
# ### For example, say in your database you have movie information starting from 1931. 
# ### the first decade is 1931, 1932, ..., 1940,
# ### the second decade is 1932, 1933, ..., 1941 and so on. 
# ### Find the decade D with the largest number of films and the total number of films in D

# In[16]:


get_ipython().run_cell_magic('time', '', "def grader_7a(q7a):\n    q7a_results  = pd.read_sql_query(q7a,conn)\n    print(q7a_results.head(10))\n    assert (q7a_results.shape == (78, 2))\n\nquery7a = '''SELECT distinct(SUBSTR(year,-4,4)), Count(SUBSTR(year,-4,4)) From Movie GROUP BY SUBSTR(year,-4,4)'''\ngrader_7a(query7a)\n\n\n# using the above query, you can write the answer to the given question\n")


# In[42]:


get_ipython().run_cell_magic('time', '', 'def grader_7b(q7b):\n    q7b_results  = pd.read_sql_query(q7b,conn)\n    print(q7b_results.head(10))\n    assert (q7b_results.shape == (713, 4))\n\nquery7b = """SELECT m.Y, m.Z,n.X,n.C from\n            (SELECT year Y, COUNT(*) Z From Movie group by year) m ,  \n            (SELECT year X, COUNT(*) C From Movie group by year) n WHERE\n             n.X<=m.Y+9 and n.X>=m.Y"""\ngrader_7b(query7b)\n# if you see the below results the first movie year is less than 2nd movie year and \n# 2nd movie year is less or equal to the first movie year+9\n\n# using the above query, you can write the answer to the given question\n')


# In[24]:


get_ipython().run_cell_magic('time', '', 'def grader_7(q7):\n    q7_results  = pd.read_sql_query(q7,conn)\n    print(q7_results.head(10))\n    assert (q7_results.shape == (1, 2))\n\nquery7 = """ SELECT (y.year),Count(*) aa FROM\n             (SELECT DISTINCT(year) FROM Movie) y \n              JOIN Movie m on m.year>=y.year and m.year<=y.year+9\n              group by y.year order by aa Desc limit 1"""\ngrader_7(query7)\n# if you check the output we are printinng all the year in that decade, its fine you can print 2008 or 2008-2017\n')


# ## Q8 --- Find all the actors that made more movies with Yash Chopra than any other director.

# In[44]:


get_ipython().run_cell_magic('time', '', 'def grader_8a(q8a):\n    q8a_results  = pd.read_sql_query(q8a,conn)\n    print(q8a_results.head(10))\n    assert (q8a_results.shape == (73408, 3))\n\nquery8a = """ SELECT mm.PID,m.PID,count(*) FROM M_Director mm \n              JOIN M_Cast m on mm.MID=m.MID group by mm.PID,m.PID"""\ngrader_8a(query8a)\n\n# using the above query, you can write the answer to the given question\n')


# In[84]:


get_ipython().run_cell_magic('time', '', "\ndef grader_8(q8):\n    q8_results  = pd.read_sql_query(q8,conn)\n    print(q8_results.head(10))\n    print(q8_results.shape)\n    assert (q8_results.shape == (245, 2))\n\nquery8 = '''SELECT p.Name Actor_Name, mov_cnt Movie_count_with_yash_chopra \n            FROM\n                (SELECT actor act_id, dir_name, movies mov_cnt \n                    FROM\n\n                    (SELECT trim(mc.PID) actor, p.Name dir_name, trim(md.PID) director, COUNT(*) as movies \n                        FROM M_Cast mc\n                        JOIN M_Director md ON trim(mc.MID) = md.MID\n                        JOIN Person p ON director = p.PID\n                        GROUP BY actor,director\n                    ) \n                \n            WHERE (act_id,mov_cnt) IN\n                \n                    (SELECT actor act_id, MAX(movies) \n                        FROM\n                        (SELECT trim(mc.PID) actor, trim(md.PID) director, COUNT(*) as movies \n                            FROM M_Cast mc\n                            JOIN M_Director md ON trim(mc.MID) = md.MID\n                            GROUP BY actor,director\n                        )\n                    GROUP BY act_id\n                    )\n            AND dir_name LIKE '%Yash Chopra%'\n            )\n        JOIN Person p ON act_id = p.PID\n        ORDER BY Movie_count_with_yash_chopra DESC\n               '''\ngrader_8(query8)\n")


# ## Q9 --- The Shahrukh number of an actor is the length of the shortest path between the actor and Shahrukh Khan in the "co-acting" graph. That is, Shahrukh Khan has Shahrukh number 0; all actors who acted in the same film as Shahrukh have Shahrukh number 1; all actors who acted in the same film as some actor with Shahrukh number 1 have Shahrukh number 2, etc. Return all actors whose Shahrukh number is 2.

# In[55]:


get_ipython().run_cell_magic('time', '', 'def grader_9a(q9a):\n    q9a_results  = pd.read_sql_query(q9a,conn)\n    print(q9a_results.head(10))\n    print(q9a_results.shape)\n    assert (q9a_results.shape == (2382, 1))\n\nquery9a = """SELECT distinct(p.PID) FROM M_Cast m join Person p on trim(m.PID)=(p.PID) where m.MID IN \n            (SELECT (m.MID) from M_Cast m join Person p on (p.PID)=trim(m.PID) \n            where trim(p.Name) LIKE \'%Shah Rukh Khan%\') AND  trim(p.Name) != \'Shah Rukh Khan\' """\ngrader_9a(query9a)\n# using the above query, you can write the answer to the given question\n\n# selecting actors who acted with srk (S1)\n# selecting all movies where S1 actors acted, this forms S2 movies list\n# selecting all actors who acted in S2 movies, this gives us S2 actors along with S1 actors\n# removing S1 actors from the combined list of S1 & S2 actors, so that we get only S2 actors \n')


# In[79]:


get_ipython().run_cell_magic('time', '', 'def grader_9(q9):\n    q9_results  = pd.read_sql_query(q9,conn)\n    print(q9_results.head(10))\n    print(q9_results.shape)\n    assert (q9_results.shape == (25698, 1))\n\nquery9 = """ WITH S1_act AS \n\n            (SELECT distinct(p.PID) a1 FROM M_Cast m join Person p on trim(m.PID)=(p.PID) where m.MID IN \n            (SELECT (m.MID) from M_Cast m join Person p on (p.PID)=trim(m.PID) \n             where trim(p.Name) LIKE \'%Shah Rukh Khan%\') AND  trim(p.Name) != \'Shah Rukh Khan\'),\n            \n             S1_mov AS\n             \n             (SELECT distinct(m.MID) M1 from M_Cast m join Person p on (p.PID)=trim(m.PID) \n             where trim(p.PID) IN  (SELECT distinct(p.PID) a1 FROM M_Cast m join Person p on trim(m.PID)=(p.PID) where m.MID IN \n            (SELECT (m.MID) from M_Cast m join Person p on (p.PID)=trim(m.PID) \n             where trim(p.Name) LIKE \'%Shah Rukh Khan%\') AND  trim(p.Name) != \'Shah Rukh Khan\')  and m.MID NOT IN (SELECT (m.MID) from M_Cast m join Person p on (p.PID)=trim(m.PID) \n             where trim(p.Name) LIKE \'%Shah Rukh Khan%\'))\n             \n             \n             SELECT S2.a2 from (SELECT distinct(p.PID) a2 FROM M_Cast m join Person p on trim(m.PID)=(p.PID) \n             where m.MID IN S1_mov) S2 where S2.a2 Not in S1_act\n        \n             \n             \n             \n             \n             \n             \n             \n             \n             \n             """\ngrader_9(query9)\n')

