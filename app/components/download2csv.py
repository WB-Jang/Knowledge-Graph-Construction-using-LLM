from neo4j import GraphDatabase
import pandas as pd

# 1. 연결 설정
uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))

# 2. 데이터 가져오기 함수
def get_data(tx):
    query = "MATCH (n:User) RETURN n.id AS id, n.name AS name"
    result = tx.run(query)
    return [record.data() for record in result]

# 3. 실행 및 CSV 저장
with driver.session() as session:
    data = session.read_transaction(get_data)
    df = pd.read_json(json.dumps(data)) # 또는 바로 DataFrame 생성
    df = pd.DataFrame(data)
    df.to_csv("output.csv", index=False, encoding='utf-8-sig')

driver.close()
