import pandas as pd
import cx_Oracle


sql = "select a.*,b.secucode from jydb.DZ_DailyQuote a inner join jydb.SecuMain b on a.innercode=b.innercode where b.secucode='000002' and b.secucategory=1"
db = cx_Oracle.connect('jydb_read', '7Yv67!Fb#3dC', '84.239.183.27/IRDB')
data = pd.read_sql(sql, db)
db.close()
