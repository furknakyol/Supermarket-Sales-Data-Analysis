import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
import gc
import seaborn as sns
import numpy as np 

# SQL Server bağlantısını kur
SERVER = r"FURKANAKYOL\SQLEXPRESS02"  # Server adınız
DATABASE = "SALES10M"  # Veritabanı adı
conn = pyodbc.connect(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;Timeout=10;"
)
print("Veritabanına başarılı bir şekilde bağlanıldı!")


cursor = conn.cursor()
cursor.execute("SELECT name FROM sys.tables;")
tables = cursor.fetchall()
print("Tablolar:", [table[0] for table in tables])



cursor.execute("SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'SALES';")
columns = cursor.fetchall()
print("Sütunlar:", columns)


##Veriyi parça parça çek ve birleştir. 
query = "SELECT TOP 20000 DATE_, ITEMNAME, TOTALPRICE, AMOUNT, UNITPRICE, USERGENDER, USERBIRTHDATE, REGION, CITY, TOWN, DISTRICT FROM SALES WHERE DATE_ <= '2023-12-31';"
chunk_size = 10000
dataframes = []


print("Veri çekiliyor..")
chunks = pd.read_sql_query(query, conn, chunksize=chunk_size)



for i, chunk in enumerate(chunks):
    print(f"{i+1}.parçayı işliyorum...")
    dataframes.append(chunk)
    del chunk
    gc.collect()
    

##Tüm parçaları birleştir. 
data = pd.concat(dataframes, ignore_index=True)
print("Birleştirilmiş veri:")
print(data.head())

print("Veri Sütunları:")
print(data.columns)


print("En çok satılan ürünler hesaplanıyor..")
most_sold_products = data.groupby("ITEMNAME")["TOTALPRICE"].sum().sort_values(ascending=False)
print("En çok satılan ürünler:")
print(most_sold_products.head(10))



print(data.describe())
print(data["TOTALPRICE"].describe())
##
# Statistics brief for understanding data. 
##

print(data["REGION"].value_counts())
print(data["ITEMNAME"].value_counts().head(10))



data["REGION"].value_counts ().plot(kind="pie", color ="green")
plt.title("Bölgelere göre satış dağılımı")
plt.xlabel("Satış sayısı")
plt.show()

##
#Time dependent variation of sales. 
##


data["DATE_"]= pd.to_datetime(data["DATE_"])
sales_by_date = data.groupby("DATE_")["TOTALPRICE"].sum()

plt.figure(figsize=(12,6))
sales_by_date.plot()
plt.title("Zaman Serisi - Günlük Satışlar")
plt.xlabel("Tarih")
plt.ylabel("Toplam Satış (TL)")
plt.grid()
plt.show()


##
#Gender distribution in the graph.
##

gender_sales = data.groupby("USERGENDER")["TOTALPRICE"].sum()
gender_sales.plot(kind="pie")
plt.title("Cinsiyete Göre Satış Dağılımı")
plt.show()

##
#AGE DISTRIBUTION
## 

data["USERBIRTHDATE"] = pd.to_datetime(data["USERBIRTHDATE"])
data["AGE"] = 2024 - data["USERBIRTHDATE"].dt.year
plt.hist(data["AGE"], bins=20, color="skyblue")
plt.title("Kullanıcıların yaş dağılımı")
plt.xlabel("Yaş")
plt.ylabel("Kullanıcı Sayısı")
plt.show()


regıonal_sales = data.groupby("CITY")["TOTALPRICE"].sum().sort_values(ascending=False)
regıonal_sales.head(10).plot(kind="pie", color="green")
plt.title("Şehirlere Göre Toplam Satışlar")
plt.ylabel("Satış Miktarı")
plt.show()


pivot = pd.pivot_table(data , values="TOTALPRICE", index="REGION", columns="USERGENDER", aggfunc="sum")
print(pivot)
pivot.plot(kind="bar", stacked=True)
plt.title("Bölgelere ve Cinsiyete Göre Satışlar")
plt.show()


correlation = data[["TOTALPRICE", "AMOUNT", 'UNITPRICE']].corr()
print(correlation)
sns.heatmap(correlation, annot=True, cmap="coolwarm")
plt.title("Korelasyon Matrisi")
plt.show()



print(data[data["TOTALPRICE"] <= 0])



