import psycopg2
conn = psycopg2.connect("host=ec2-174-129-233-123.compute-1.amazonaws.com dbname=daegvftoc455n user=wogbjubkvafrgx password=42ff2222dd3ae1dfe6f4c4d466666b1e17fe5f610fb12846f8ae53c80ba8182e")
cur = conn.cursor()
with open('/Users/mkauks/Desktop/pset01/project1/books.csv', 'r') as f:
    next(f)
cur.copy_to(f, 'books', sep=',')
conn.commit()
