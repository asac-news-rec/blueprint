# 뉴스 추천 공동 청사진

SKP AI DE 1기 개인화 뉴스 추천 팀의 영역별 청사진이다. `main`에 머지하면 Cloudflare가 1분 안에 팀 전용 주소로 자동 배포한다. 주소는 팀 단톡방에 공유한 링크를 쓰고, 이메일 코드로 로그인한다.

## 누가 어떤 파일을 고치나

| 파일 | 내용 | 담당 |
|---|---|---|
| index.html | 대문 (카드 목록) | 공동 |
| overview.html | 전체 그림·인터페이스 규약 | 공동 (초안 윤모) |
| taewon.html | 뉴스 생성·서비스 | 태원 |
| seho.html | 프론트엔드·행동 수집 | 세호 |
| yoonmo.html | 처리·피처·모델 | 윤모 |
| juhyun.html, infra_v2.png | 청사진 정리·인프라 구성도·툴 카탈로그 | 장주현 |
| wbs.html | 작업 나열표 28개 | 장주현 |

자기 파일만 고쳐서 PR을 올린다. 페이지 사이 링크는 `seho.html`처럼 파일 이름으로 건다.

## 용어

- 공통 규약: `overview.html`의 인터페이스 규약 ①~⑦. 단계마다 주고받는 값과 필드를 번호별 표로 정리한 것이다. `https://blueprint.yoonmo335.workers.dev/overview`에서 번호를 눌러 볼 수 있다.
- 청사진 규약 ③: 그중 뉴스 백엔드 → 로깅 서버의 `served`와 브라우저 → 로깅 서버의 `actions` 필드 표다 (`overview.html#c3`).

## 내려받아 보는 한 파일 버전

```bash
python tools/bundle.py
```

`dist/blueprint_all_in_one.html`이 생긴다. 모든 페이지와 사진이 들어 있어 더블클릭으로 열린다. `dist/`는 저장소와 배포에 포함하지 않는다.

담당과 내용은 팀 합의 전 초안이다.
