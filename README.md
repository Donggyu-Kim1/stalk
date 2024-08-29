# 스톡(Stalk) 

## 1. 목표와 기능

1.1 목표
- 미국 주식 투자를 위한 기본적인 기업 정보 제공
- 기업별(미국에 상장된)로 사용자들끼리 블로그 형식의 정보 공유 공간 제공

1.2 주요 기능
- 주식 정보
    - 주가 차트
    - 재무 정보
    - 기업 소개
    - 기업 관련 뉴스(yahoo finance)

- 토론방
    - 글 작성
    - 조회수, 추천, 즐겨찾기, 댓글 기능
    - (주식은 내일? - 찬반 토론방)


## 2. URL 구조

#### Main URL
| **App** | **URL** | **Views Function** | **HTML File Name** | **Note** |
| -- | -- | -- | -- | -- |
| **Main** | / | Main_view | base.html | 메인 페이지 |


#### Stocks URL
| **App** | **URL** | **Views Function** | **HTML File Name** | **Note** |
| -- | -- | -- | -- | -- |
| **stocks** | /stocks/search/ | search | stocks/stocks_search.html | 주식 검색 창 |
| **stocks** | /stocks/detail/str:pk/ | detail | stocks/stocks_detail.html | 주식 소개 글, 차트, 뉴스, 재무정보 |

#### Accounts URL
| **App** | **URL** | **Views Function** | **HTML File Name** | **Note** |
| -- | -- | -- | -- | -- |
| **accounts** | /accounts/signup/ | signup | accounts/signup.html | 회원가입 |
| **accounts** | /accounts/login/ | login | accounts/login.html | 로그인 |
| **accounts** | /accounts/profile/ | profile | accounts/profile.html | 프로필 설정 |
| **accounts** | /accounts/profile/edit/ | edit_profile | accounts/edit_profile.html | 프로필 수정 |

#### Forum URL
| **App** | **URL** | **Views Function** | **HTML File Name** | **Note** |
| -- | -- | -- | -- | -- |
| **forum** | /forum/str:ticker/ | forum_list | forum/forum_list.html | 글 리스트 |
| **forum** | /forum/str:ticker/create/ | post_create | forum/post_create.html | 글 작성 |
| **forum** | /forum/str:ticker/int:post_id/ | post_read | forum/post_read.html | 글 읽기, 댓글 작성 |
| **forum** | /forum/str:ticker/int:post_id/update/ | post_update | forum/post_update.html | 글 수정 |
| **forum** | /forum/str:ticker/int:post_id/delete/ | post_delete | forum/post_delete.html | 글 삭제 |
| **forum** | /forum/str:ticker/int:post_id/comments/ | post_comment_list | forum/post_comment_list.html | 댓글 리스트 |
| **forum** | /forum/str:ticker/int:post_id/comments/int:comment_id/update | post_comment_update | forum/post_comment_update.html | 댓글 수정 |
| **forum** | /forum/str:ticker/int:post_id/comments/int:comment_id/delete | post_comment_delete | forum/post_comment_delete.html | 댓글 삭제 |

## 3. 기능 명세서
1. 사용자 등록 기능
    - 회원가입 : 아이디, 비밀번호
    - 로그인
    - 사용자 정보 변경

2. 주식 정보
    - 기업 소개 : 기업 소개 글
    - 기업 관련 뉴스 : Yahoo Finance 뉴스
    - 주가 차트 : 주가 차트 제공 기능 구현
    - 재무 정보 : 기본 재무 정보

3. 게시글 + 댓글
    - 게시글
        - CRUD
        - 사진 첨부 기능
        - 좋아요, 조회수
        - 유효성 검사 : 광고, 악성 글 차단 
    - 댓글
        - CRUD
        - 댓글
    

| 대분류 | 중분류 | 소분류 | 설명 | 완성 여부 |
|--------|--------|--------|------| :--: |
| 기획 | 아이디어 기획 | - | 핵심 기능 설계 | ㅇ |
| | WBS 작성 | - | mermaid로 프로젝트 단계 세분화 | ㅇ |
| | ERD 그리기 | - | DB, 앱 flow 그리기 | ㅇ |
| | 와이어프레임 | - | 앱 UI 설계 및 그리기 | x |
| 1. 사용자 등록 | 회원가입 | 기본 | 아이디, 비밀번호, 이름, 이메일 | ㅇ |
| | 로그인 | - | 로그인 기능 | ㅇ |
| | 로그아웃 | - | 사용자 세션 종료 | ㅇ |
| | 프로필 관리 | | 사용자 프로필 수정 | ㅇ |
| 2. 주식 정보 | 주식 정보 BD 구축 | - | 기업 이름 검색 | ㅇ |
| | 기업 소개 | - | 기업에 대한 소개글 제공 | ㅇ |
| | 기업 관련 뉴스 | 뉴스 크롤링 | Yahoo Finance에서 최신 뉴스 크롤링 | ㅇ |
| | 주가 차트 | - | 주식의 가격 변동 차트 제공 | ㅇ |
| | 재무 정보 | 기본 재무 정보 | 주요 재무 정보 표로 제공 | ㅇ |
| | 번역 | - | stocks_detail 부분 영어 -> 한국어 번역 | ㅇ |
| 3. 게시글 + 댓글 | 게시글 | CRUD | 게시글 생성, 조회, 수정, 삭제 기능 | ㅇ |
| | | 사진 | 사진 첨부 기능 | ㅇ |
| | | 좋아요 | 게시글 좋아요 기능 | x |
| | | 조회수 | 게시글 조회수 기능 | ㅇ |
| | | 유효성 검사 | 광고, 악성 글 차단 | x |
| | 댓글 | CRUD | 댓글 생성, 조회, 수정, 삭제 | ㅇ |
| 4. 마무리 | 구현 영상 | - | - | x |
| | README 파일 작성 | - | - | x |
| | 배포 | - | - | x |
    

## 4. 프로젝트 구조와 개발 일정

### 4.1 프로젝트 구조

```
stock_community/
│
├── manage.py
├── templates/
│   │   ├── stocks/
│   │   |   ├── stocks_search.html  # 주식 검색 창
│   │   |   └── stocks_detail.html  # 기업 소개 글, 뉴스, 차트, 재무 정보
|   |   |
│   │   ├── accounts/
│   │   │   ├── signup.html    # 회원가입
│   │   │   ├── login.html     # 로그인
│   │   │   ├── profile.html   # 프로필 설정
│   │   │   └── edit_profile.html   # 프로필 수정
│   │   │
|   │   └── forum/
|   │       ├── forum_list.html       # 글 리스트
|   │       ├── post_create.html      # 글 작성
|   │       ├── post_read.html        # 글 읽기, 댓글 작성
|   │       ├── post_update.html      # 글 수정
|   │       ├── post_delete.html      # 글 삭제
|   │       ├── post_comment_list.html     # 댓글 리스트
|   │       ├── post_comment_update.html   # 댓글 수정
|   |       └── post_comment_delete.html   # 댓글 삭제
|   |
│   └── base.html   # 기본 템플릿
|
├── stock_community/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── stocks/
│   ├── management/
│   |   └── commands/
|   |       └── imports_stocks.py
│   ├── migrations/
|   |   ├── __init__.py
|   |   └── 0001_initial.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── accounts/
│   ├── migrations/
|   |   └── __init__.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
|   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
└── forum/
    ├── migrations/
    |   ├── __init__.py
    |   ├── 0001_initial.py
    |   └── 0002_post_image.py
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── forms.py
    ├── models.py
    ├── tests.py
    ├── urls.py
    └── views.py
```


### 4.2 개발 일정(WBS)
```mermaid
gantt
    title 주식 커뮤니티 프로젝트 WBS
    dateFormat  YYYY-MM-DD HH:mm

    section 기획
    아이디어 기획      :2024-08-26, 1d
    WBS 작성          :2024-08-26, 1d
    ERD 그리기         :2024-08-26, 1d
    와이어프레임        :2024-08-29, 1d

    section 1. 사용자 등록
    회원가입           :2024-08-27, 1d
    로그인             :2024-08-27, 1d
    로그아웃           :2024-08-27, 1d
    프로필 관리         :2024-08-27, 1d

    section 2. 주식 정보
    주식 티커 리스트     :2024-08-28, 1d
    기업 소개          :2024-08-27, 2d
    기업 관련 뉴스      :2024-08-27, 2d
    주가 차트          :2024-08-29, 1d
    재무 정보          :2024-08-27, 2d
    번역 기능          :2024-08-29, 1d

    section 3. 게시글 + 댓글
    게시글 CRUD        :2024-08-28, 1d
    게시글 조회수       :2024-08-28, 1d
    댓글 CRUD          :2024-08-28, 1d
    유효성 검사        :2024-08-29, 1d

    section 4. 마무리
    UI                :2024-08-29, 1d
    구현 영상          :2024-08-30, 1d
    README 파일 작성   :2024-08-30, 1d
    배포              :2024-08-31, 1d
```


## 5 화면 설계

### 5.1 화면 flow

```mermaid
    graph TD
        A[로그인 화면] --> B{로그인 성공?}
        B -->|성공| C[주식 검색 창]
        B -->|실패| A
        C --> D[주식 정보 창]
        D --> E[종목별 게시판]
        E --> F[포스트 글]
        
        subgraph "주식 정보 창 내용"
            D1[기업 소개]
            D2[주가 차트]
            D3[기업 관련 뉴스]
            D4[재무 정보]
        end
        
        D --> D1
        D --> D2
        D --> D3
        D --> D4
```

### 5.2 와이어프레임


## 6. 데이터베이스 구조도(ERD)

```mermaid
erDiagram
    AUTH_USER {
        int id PK "Primary Key"
        string username "아이디"
        string password "비밀번호"
        string first_name "이름"
        string last_name "성"
        string email "이메일"
        boolean is_staff "관리자 여부"
        boolean is_active "활성화 여부"
        boolean is_superuser "슈퍼유저 여부"
        datetime last_login "마지막 로그인 시간"
        datetime date_joined "가입일"
    }

    POST {
        bigint post_id PK "Primary Key"
        int user_id FK "작성자 (auth_user.id)"
        string title "게시글 제목"
        text content "게시글 내용"
        int views "조회수"
        datetime created_at "작성일"
        datetime updated_at "수정일"
        string stock_ticker FK "연결된 종목 (stocks.ticker)"
    }

    COMMENT {
        bigint comment_id PK "Primary Key"
        bigint post_id FK "연결된 게시글"
        int user_id FK "작성자 (auth_user.id)"
        text content "댓글 내용"
        datetime created_at "작성일"
        datetime updated_at "수정일"
    }

    STOCK {
        string ticker PK "Primary Key"
        string company_name "기업 이름"
        string exchange "거래소"
        datetime created_at "등록일"
        datetime updated_at "수정일"
    }

    AUTH_USER ||--o{ POST : "작성"
    AUTH_USER ||--o{ COMMENT : "작성"
    POST ||--o{ COMMENT : "게시글에 달린 댓글"
    STOCK ||--o{ POST : "종목 관련 게시글"
```


## 7. 구현 영상

## 8. 추가적으로 해야할 사항

- 유효성 검사 기능 추가
- 대댓글
- UI 개선
- 추가할 모델 고민해보기
- 와이어 프레임 그리기 / 오늘까지 완료하기
- 리드미 다시 재작성
- 배포