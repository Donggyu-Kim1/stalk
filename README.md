# 스톡(Stalk) 

## 1. 목표와 기능

1.1 목표
- 미국 주식 투자를 위한 기업 정보 제공
- 기업별(미국에 상장된)로 사용자들끼리 게시판 형식의 정보 공유 공간 제공
- 주식 포트폴리오 만들기

1.2 주요 기능
- 주식 정보(yfinance)
    - 기업 소개
    - 주가 차트
    - 기업 관련 뉴스
    - 재무 정보

- 토론방
    - 글 작성
    - 조회수, 댓글 기능

- 포트폴리오
    - 포트폴리오 생성
    - 포트폴리오 수익률

## 2. URL 구조

#### Main URL
| **App** | **URL** | **Views Function** | **HTML File Name** | **Note** |
| -- | -- | -- | -- | -- |
| **Main** | / | Index_view | base.html | 메인 페이지 |

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
| **accounts** | /accounts/logout/ | logout | | 로그아웃 |
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

#### Portfolio URL
| **App** | **URL** | **Views Function** | **HTML File Name** | **Note** |
| -- | -- | -- | -- | -- |
| **portfolio** | /portfolio/list/ | portfolio_list | portfolio/portfolio_list.html | 포트폴리오 리스트 |
| **portfolio** | /portfolio/create/ | portfolio_create | portfolio/portfolio_create.html | 포트폴리오 만들기 |
| **portfolio** | /portfolio/int:pk/ | portfolio_read | portfolio/portfolio_read.html | 포트폴리오 결과 |
| **portfolio** | /portfolio/delete/int:pk/ | portfolio_delete | portfolio/portfolio_delete.html | 포트폴리오 삭제 |


## 3. 기능 명세서
1. 사용자 등록 기능
    - 회원가입 : 아이디, 비밀번호
    - 로그인
    - 사용자 정보 변경

2. 주식 정보
    - 기업 소개
    - 기업 관련 뉴스
    - 주가 차트
    - 재무 정보

3. 게시글 + 댓글
    - 게시글
        - CRUD
        - 사진 첨부 기능
        - 조회수

    - 댓글
        - CRUD
        - 대댓글(답글)

4. 포트폴리오
    - 나의 주식 포트폴리오
        - CRD
        - 포트폴리오 수익률
    

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
|   │   ├── forum/
|   │   │   ├── forum_list.html       # 글 리스트
|   │   │   ├── post_create.html      # 글 작성
|   │   │   ├── post_read.html        # 글 읽기, 댓글 작성
|   │   │   ├── post_update.html      # 글 수정
|   │   │   ├── post_delete.html      # 글 삭제
|   │   │   ├── post_comment_list.html     # 댓글 리스트
|   │   │   ├── post_comment_update.html   # 댓글 수정
|   |   │   └── post_comment_delete.html   # 댓글 삭제
|   |   │
│   │   └── portfolio/
│   │       ├── portfolio_list.html    # 포트폴리오 리스트
│   │       ├── portfolio_create.html    # 포트폴리오 생성
│   │       ├── portfolio_read.html     # 포트폴리오 결과
│   │       └── portfolio_delete.html   # 포트폴리오 삭제
│   │
│   └── base.html   # 기본 템플릿
|
├── stock_community/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── views.py
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
├── forum/
│   ├── migrations/
│   |   ├── __init__.py
│   |   ├── 0001_initial.py
│   |   ├── 0002_post_image.py
|   |   └── 0003_comment_parent.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
└── portfolio/
    ├── migrations/
    |   ├── __init__.py
    |   └── 0001_initial.py
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
    dateFormat  YYYY-MM-DD

    section 기획
    아이디어 기획      :2024-08-26, 1d
    WBS 작성          :2024-08-26, 1d
    ERD 그리기         :2024-08-26, 1d
    와이어프레임        :2024-08-31, 1d

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
    대댓글             :2024-08-29, 1d
    
    section 4. 포트폴리오
    포트폴리오 리스트        :2024-08-29, 2d
    포트폴리오 CUD       :2024-08-29, 2d
    포트폴리오 결과         :2024-08-29, 3d

    section 5. 마무리
    UI                :2024-08-31, 1d
    구현 영상          :2024-08-31, 1d
    README 파일 작성   :2024-09-01, 1d
```


## 5 화면 설계

### 5.1 화면 flow

```mermaid
graph TD
    A[로그인 화면] --> B{로그인 성공?}
    B -->|성공| C[기본 페이지]
    B -->|실패| A

    C --> D[주식 검색 창]
    C --> G[포트폴리오 창]

    %% 주식 정보 창 흐름
    D --> H[주식 정보 창]
    H --> I[종목별 게시판]
    I --> J[포스트 글]
    
    subgraph "주식 정보 창 내용"
        H1[기업 소개]
        H2[주가 차트]
        H3[기업 관련 뉴스]
        H4[재무 정보]
    end
    
    H --> H1
    H --> H2
    H --> H3
    H --> H4

    %% 포트폴리오 창 흐름
    G --> K[포트폴리오 결과]
```

### 5.2 와이어프레임

#### Main

![main](https://github.com/user-attachments/assets/27c60f3c-2e38-4f4f-a5ef-07fca3f42302)

#### stock

![stock](https://github.com/user-attachments/assets/1057e2ae-6a6e-43af-9aa2-3586c3330b23)

#### profile

![profile](https://github.com/user-attachments/assets/d2c14e89-640a-433f-9ebe-b1d90e3c6cab)

#### portfolio

![portfolio](https://github.com/user-attachments/assets/2b5eaec4-93ad-43f3-946b-23bb30d2491e)


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

    Post {
        bigint post_id PK "Primary Key"
        string title "게시물 제목"
        text content "게시물 내용"
        datetime created_at "작성 시간"
        datetime updated_at "수정 시간"
        int views "조회수"
        string image "이미지 경로"
        string stock_ticker FK "Foreign Key to Stock(ticker)"
        int author_id FK "Foreign Key to AUTH_USER(id)"
    }

    Comment {
        bigint id PK "Primary Key"
        text content "댓글 내용"
        datetime created_at "작성 시간"
        datetime updated_at "수정 시간"
        bigint post_id FK "Foreign Key to Post(post_id)"
        int author_id FK "Foreign Key to AUTH_USER(id)"
        bigint parent_id FK "Self-referencing Foreign Key to Comment(id)"
    }

    Portfolio {
        bigint id PK "Primary Key"
        string name "포트폴리오 이름"
        datetime created_at "생성일"
        int user_id FK "Foreign Key to AUTH_USER(id)"
    }

    PortfolioStock {
        bigint id PK "Primary Key"
        int portfolio_id FK "Foreign Key to Portfolio(id)"
        string stock_ticker FK "Foreign Key to Stock(ticker)"
        int quantity "보유 주식 수량"
        decimal purchase_price "매수 가격"
        datetime created_at "추가된 날짜"
    }

    Stock {
        string ticker PK "Primary Key"
        string company_name "회사 이름"
        string exchange "거래소"
        datetime created_at "생성일"
        datetime updated_at "수정일"
    }

    %% Relationships
    AUTH_USER ||--o{ Post : "작성자"
    AUTH_USER ||--o{ Comment : "작성자"
    AUTH_USER ||--o{ Portfolio : "포트폴리오 소유자"
    Post ||--o{ Comment : "포스트에 작성된 댓글"
    Post ||--o| Stock : "관련 주식"
    Comment ||--o| Comment : "부모 댓글"
    Portfolio ||--o{ PortfolioStock : "포트폴리오에 포함된 주식"
    Stock ||--o{ PortfolioStock : "포트폴리오에 포함된 주식"
```


## 7. 구현 영상

#### 회원가입 & 로그인

![signup](https://github.com/user-attachments/assets/0128094b-6035-41c1-bfa1-b0c8ae60c3f6)

#### 프로필

![profile](https://github.com/user-attachments/assets/b6b88294-2bd0-4038-8661-398afaa79151)

#### 주식 정보

![stock](https://github.com/user-attachments/assets/b5c0070c-3ca0-480a-b296-fd48ff6738d9)

#### 게시판

![go_post](https://github.com/user-attachments/assets/235bba8e-ddd8-4dc6-a748-641588b9cd5b)

![post](https://github.com/user-attachments/assets/bb7a9074-b785-47bb-9172-7dc23ed18d2c)

![comment](https://github.com/user-attachments/assets/649b2c1c-65ff-4e61-bd3d-bba131dca0b8)

#### 포트폴리오

![portfolio](https://github.com/user-attachments/assets/490eb41d-c4fa-4d38-a4e2-76d4f193bd4f)
