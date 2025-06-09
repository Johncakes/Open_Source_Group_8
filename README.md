
# 🎬 오픈소스 8조

Django 기반 영화 리뷰 웹 애플리케이션입니다.

**팀원**: 심혁, 김진환, 이재원, 허승우  

---

## 🚀 Getting started

> 이 프로젝트는 Python 패키지 매니저로 [`uv`](https://github.com/astral-sh/uv)를 사용합니다. `uv`는 ultra-fast 설치 속도와 캐싱을 제공하며, `pip`과 `virtualenv`를 대체합니다.

### 1. uv 설치

[공식문서](https://docs.astral.sh/uv/getting-started/installation/)를 참고해주세요.

### 2. Project Clone
```bash
$ git clone https://github.com/Johncakes/Open_Source_Group_8.git
$ cd Open_Source_Group_8
```

### 3. Database Migration
```bash
$ uv run python manage.py migrate
```

### 4. 영화 데이터 Import
```bash
$ uv run python movie/scripts/import_genres.py
$ uv run python movie/scripts/import_movies.py
```

## ⚙️ 개발 서버 실행

### 1. 📝 환경변수 설정
`.env.sample` 을 참고하여 `.env` 를 생성합니다.

### 2. 개발 서버 실행
```bash
$ uv run python manage.py runserver
```

## 🗂 ERD
```mermaid
erDiagram

    USER ||--o{ REVIEW : writes
    MOVIE ||--o{ REVIEW : has
    MOVIE ||--o{ MOVIECAST : has
    MOVIE ||--o{ MOVIECREW : has
    MOVIE }o--o{ GENRE : categorized_as

    USER {
        int id PK "사용자 ID"
        string username "아이디"
        string email "이메일"
        string password "비밀번호"
    }

    REVIEW {
        int id PK "리뷰 ID"
        int movie_id FK "Foreign Key to Movie"
        int user_id FK "Foreign Key to User"
        string username "작성자 이름 (익명 포함)"
        text content "리뷰 본문"
        float rating "평점 (0.5 단위, 0~5)"
        datetime created_at "작성일"
    }

    MOVIE {
        int id PK "TMDB 영화 ID"
        string title "한글 제목"
        string original_title "원제"
        text overview "줄거리"
        string poster_path "포스터 이미지"
        string backdrop_path "배경 이미지"
        date release_date "개봉일"
        int runtime "상영 시간(분)"
        float popularity "인기도 점수"
        string origin_country "제작 국가 코드"
        string production_company "제작사"
    }

    GENRE {
        int id PK
        string name "장르 이름"
    }

    MOVIECAST {
        int id PK
        int movie_id FK
        string name "배우 이름"
        string character "역할 이름"
        string profile_path "프로필 이미지"
    }

    MOVIECREW {
        int id PK
        int movie_id FK
        string name "스태프 이름"
        string job "직책 (예: 감독, 작곡)"
        string profile_path "프로필 이미지"
    }
```