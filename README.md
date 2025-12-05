# Knowledge Graph Construction using LLM

LLM을 활용하여 텍스트에서 지식 그래프(Knowledge Graph)를 자동으로 생성하는 시스템입니다.

## 주요 기능

- **LLM 기반 엔티티 추출**: OpenAI GPT 또는 Google Gemini를 사용하여 텍스트에서 엔티티와 관계 자동 추출
- **임베딩 생성**: Sentence Transformers를 사용한 엔티티 벡터 임베딩
- **Neo4j 저장**: 추출된 지식 그래프를 Neo4j에 저장 및 쿼리
- **GPU 최적화**: RTX-4080 (8GB VRAM) 환경에 최적화
- **Docker 지원**: Docker Container, DevContainer, Docker Compose 완벽 지원
- **Poetry 의존성 관리**: Poetry를 사용한 체계적인 패키지 관리

## 시스템 요구사항

- **하드웨어**: NVIDIA GPU (RTX-4080 8GB VRAM 권장)
- **소프트웨어**:
  - Docker & Docker Compose
  - NVIDIA Docker Runtime
  - Python 3.10 이상 (컨테이너 내부)

## 설치 및 실행

### 1. 저장소 클론

```bash
git clone https://github.com/WB-Jang/Knowledge-Graph-Construction-using-LLM.git
cd Knowledge-Graph-Construction-using-LLM
```

### 2. 환경 변수 설정

`.env.example`을 복사하여 `.env` 파일 생성:

```bash
cp .env.example .env
```

`.env` 파일을 편집하여 API 키 설정:

```bash
# OpenAI 사용 시
OPENAI_API_KEY=your_openai_api_key_here

# 또는 Google Gemini 사용 시
GOOGLE_API_KEY=your_google_api_key_here
```

### 3. Docker Compose로 실행

```bash
# Neo4j와 애플리케이션 컨테이너 시작
docker-compose up -d

# 애플리케이션 컨테이너에 접속
docker-compose exec kg-app bash
```

### 4. 패키지 설치 (컨테이너 내부)

```bash
# Poetry를 사용하여 의존성 설치
poetry install
```

## 사용 방법

### 예제 실행

```bash
# 예제 스크립트 실행
poetry run python app/example.py
```

### 텍스트 파일 처리

```bash
# 텍스트 파일에서 지식 그래프 생성
poetry run python app/main.py --input data/sample.txt --clear-db

# PDF 파일 처리
poetry run python app/main.py --input data/sample.pdf --clear-db
```

### 직접 텍스트 입력

```bash
poetry run python app/main.py --text "OpenAI developed GPT-4, a large language model."
```

### Cypher 쿼리 실행

```bash
# 모든 노드 조회
poetry run python app/main.py --query "MATCH (n) RETURN n LIMIT 10"

# 관계 조회
poetry run python app/main.py --query "MATCH (s)-[r]->(t) RETURN s, r, t LIMIT 10"
```

### Google Gemini 사용

```bash
poetry run python app/main.py \
  --input data/sample.txt \
  --llm-type google \
  --llm-model gemini-1.5-flash \
  --clear-db
```

## VSCode DevContainer 사용

VSCode에서 프로젝트를 열고 "Reopen in Container"를 선택하면 자동으로 개발 환경이 구성됩니다.

## Neo4j 브라우저 접속

Neo4j 브라우저를 통해 생성된 지식 그래프를 시각화할 수 있습니다:

- **URL**: http://localhost:7474
- **Username**: neo4j
- **Password**: password123 (기본값)

### 유용한 Cypher 쿼리

```cypher
// 모든 노드와 관계 시각화
MATCH (n)-[r]->(m) RETURN n, r, m LIMIT 50

// 특정 엔티티와 연결된 노드 찾기
MATCH (n {name: "OpenAI"})-[r]-(m) RETURN n, r, m

// 엔티티 타입별 개수
MATCH (n) RETURN labels(n) as type, count(n) as count

// 관계 타입별 개수
MATCH ()-[r]->() RETURN type(r) as relationship, count(r) as count
```

## 프로젝트 구조

```
.
├── .devcontainer/          # VSCode DevContainer 설정
│   └── devcontainer.json
├── app/                    # 애플리케이션 코드
│   ├── components/         # 핵심 컴포넌트
│   │   ├── chunking.py     # 텍스트 청킹
│   │   ├── embedder.py     # 임베딩 생성
│   │   ├── extractor.py    # LLM 기반 엔티티/관계 추출
│   │   ├── pipeline.py     # 통합 파이프라인
│   │   └── store_neo4j.py  # Neo4j 저장소
│   ├── example.py          # 예제 스크립트
│   └── main.py             # 메인 애플리케이션
├── data/                   # 데이터 디렉토리
├── Dockerfile              # Docker 이미지 정의
├── docker-compose.yml      # Docker Compose 설정
├── pyproject.toml          # Poetry 프로젝트 설정
└── README.md               # 이 파일
```

## 주요 컴포넌트

### 1. Extractor (extractor.py)
- LLM을 사용하여 텍스트에서 엔티티와 관계를 추출
- OpenAI GPT 및 Google Gemini 지원
- JSON 형식으로 구조화된 출력

### 2. Embedder (embedder.py)
- Sentence Transformers를 사용한 임베딩 생성
- GPU 가속 지원 (RTX-4080 최적화)
- 배치 처리로 효율적인 임베딩 생성

### 3. Neo4jStorage (store_neo4j.py)
- Neo4j에 지식 그래프 저장
- Cypher 쿼리 실행
- 유사도 기반 엔티티 검색

### 4. KnowledgeGraphPipeline (pipeline.py)
- 전체 파이프라인 통합
- 문서 처리부터 저장까지 end-to-end 지원
- PDF, 텍스트 파일 처리

## 개발 환경

### 로컬 개발 (DevContainer)

```bash
# VSCode에서 프로젝트 열기
code .

# Command Palette (Ctrl+Shift+P)에서:
# "Dev Containers: Reopen in Container" 선택
```

### Poetry 명령어

```bash
# 의존성 추가
poetry add package-name

# 개발 의존성 추가
poetry add --group dev package-name

# 의존성 업데이트
poetry update

# 가상환경 활성화
poetry shell
```

### 코드 포맷팅

```bash
# Black으로 코드 포맷
poetry run black app/

# Ruff로 린팅
poetry run ruff check app/
```

## 성능 최적화 (RTX-4080 8GB VRAM)

이 프로젝트는 RTX-4080 (8GB VRAM) 환경에 최적화되어 있습니다:

- **메모리 최적화**: `PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512`
- **경량 임베딩 모델**: all-MiniLM-L6-v2 (기본값)
- **배치 처리**: 메모리 효율적인 배치 크기 사용
- **자동 캐시 정리**: CUDA 캐시 자동 관리

## 문제 해결

### Neo4j 연결 오류
```bash
# Neo4j 컨테이너 상태 확인
docker-compose ps

# Neo4j 로그 확인
docker-compose logs neo4j
```

### GPU 관련 오류
```bash
# NVIDIA Docker Runtime 확인
docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi

# PyTorch CUDA 사용 가능 확인
poetry run python -c "import torch; print(torch.cuda.is_available())"
```

### API 키 오류
- `.env` 파일에 올바른 API 키가 설정되어 있는지 확인
- 컨테이너 재시작: `docker-compose restart kg-app`

## 참고 자료

- [Neo4j Documentation](https://neo4j.com/docs/)
- [LangChain Documentation](https://python.langchain.com/)
- [Sentence Transformers](https://www.sbert.net/)
- [OpenAI API](https://platform.openai.com/docs/)
- [Google Gemini API](https://ai.google.dev/)

## 라이선스

MIT License

## 기여

Issues와 Pull Requests를 환영합니다!

## 작성자

Woobin Jang (eeariorie@gmail.com)
