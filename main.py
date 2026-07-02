from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles as StarletteStaticFiles

app = FastAPI(title="헬로비디디 포트폴리오")

STATIC_DIR = Path("static")


class NoCacheStaticFiles(StarletteStaticFiles):
    async def get_response(self, path: str, scope):
        response = await super().get_response(path, scope)
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        return response


def static_version() -> int:
    candidates = [
        STATIC_DIR / "css" / "style.css",
        STATIC_DIR / "js" / "main.js",
        Path("templates/index.html"),
        Path(__file__),
    ]
    return int(max(path.stat().st_mtime for path in candidates if path.exists()))


app.mount("/static", NoCacheStaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ── 실적 수치 ──────────────────────────────────────────────────
KMONG_RATING = {"value": "5.0", "numeric": 5.0}

STATS_OVERVIEW = [
    {"label": "총 작업 수", "value": "235", "unit": "건", "desc": "크몽 누적 납품", "numeric": 235},
    {"label": "고객 만족도", "value": "100", "unit": "%", "desc": "크몽 만족도 기록", "numeric": 100},
    {
        "label": "평균 평점",
        "value": KMONG_RATING["value"],
        "unit": "점",
        "desc": "리뷰 137건 기준",
        "numeric": KMONG_RATING["numeric"],
    },
    {"label": "평균 응답", "value": "10", "unit": "분", "desc": "문의 후 응답 시간", "numeric": 10},
]

KMONG_PROFILE = {
    "name": "HelloBDD",
    "url": "https://kmong.com/@HelloBDD",
    "level": 3,
    "rating": KMONG_RATING["value"],
    "rating_numeric": KMONG_RATING["numeric"],
    "reviews": 137,
    "tasks": 235,
    "satisfaction": 100,
    "response_time": "10분 이내",
    "contact_hours": "10시 ~ 23시",
    "location": "인천",
    "tax_invoice": "세금계산서 발행 가능",
}

CAPABILITIES = [
    {
        "id": "naver",
        "num": "01",
        "tab": "N사·플레이스",
        "goal": "검색·플레이스 마케팅을 자동화합니다",
        "headline": "N사 검색·플레이스 데이터 수집·모니터링이 가능합니다",
        "desc": "키워드, 순위, 리뷰, 경쟁사 데이터를 자동 수집합니다. 로직 변화에 즉각 대응하는 마케팅 프로그램을 구축합니다.",
        "tags": ["N사 검색", "플레이스", "순위 모니터링", "하이랭크"],
    },
    {
        "id": "medical",
        "num": "02",
        "tab": "병·의원",
        "goal": "의료·뷰티 플랫폼 업무를 자동화합니다",
        "headline": "병·의원 플랫폼 마케팅 프로그램 개발이 가능합니다",
        "desc": "미용·의료 정보 플랫폼 데이터 수집, 노출 분석, 반복 업무 자동화까지 대행사·병원 맞춤으로 개발합니다.",
        "tags": ["의료 플랫폼", "노출 분석", "다이노픽"],
    },
    {
        "id": "ai",
        "num": "03",
        "tab": "AI·데이터",
        "goal": "AI 생성·분석으로 마케팅을 자동화합니다",
        "headline": "AI 생성·분석·활용 프로그램 개발이 가능합니다",
        "desc": "AI 게시글·콘텐츠 생성, 여론·감정 분석, 데이터 분석 등 AI를 사용·활용하는 마케팅 프로그램을 구축합니다. 크롤링 수집부터 실행까지 자동화합니다.",
        "tags": ["AI 생성", "AI 분석", "AI 활용", "크롤링"],
    },
    {
        "id": "custom",
        "num": "04",
        "tab": "맞춤 개발",
        "goal": "소통·자동화·바이럴까지 맞춤 대응합니다",
        "headline": "소통 작업·자동화 작업 개발이 가능합니다",
        "desc": "메신저·커뮤니티 소통 자동화, 반복 업무 자동화, 바이럴 마케팅 프로그램까지 대행사·브랜드 요청에 맞춰 구축합니다. 테더링·프록시 인프라도 지원합니다.",
        "tags": ["소통 작업", "자동화 작업", "바이럴 프로그램", "맞춤 개발"],
    },
]

HERO_EYEBROW = "B2B DEVELOPMENT PARTNER"
HERO_TITLE_MAIN = "대행사의 상상을 기술로 구현합니다"
HERO_TITLE_SUB = "서버 직접 통신 기반 무차단 자동화 & AI 솔루션"

HERO_PLATFORM_LINES = [
    ["카페", "블로그", "플레이스", "검색·포털", "병·의원", "뷰티·메디컬"],
    ["커뮤니티", "SNS", "쇼핑몰", "지도·리뷰", "메신저", "커머스", "앱·웹", "여론·리뷰"],
]
HERO_PLATFORMS_NOTE = "모든 플랫폼 개발 가능"

HERO_KEYWORDS = [
    "서버 직접 통신",
    "무차단 자동화",
    "데이터 동기화 엔진",
    "메디컬/포털 최적화",
    "AI 여론 분석",
]

PRODUCTS = [
    {
        "name": "하이랭크",
        "url": "https://www.hirank.kr",
        "display_url": "www.hirank.kr",
        "desc": "N사 포털·플레이스 로직 대응, 검색·순위 알고리즘 변화 선제 대응",
    },
    {
        "name": "다이노픽",
        "url": "https://www.dainopick.com",
        "display_url": "www.dainopick.com",
        "desc": "메디컬 플랫폼 데이터 분석·노출 최적화 SaaS",
    },
]

CASE_STATS = [
    {
        "client": "C 마케팅 대행사",
        "platform": "N사 플레이스",
        "metric_label": "수동 작업 절감",
        "metric_value": "—",
        "metric_unit": "%",
        "metric_numeric": None,
        "before_label": "수동 모니터링",
        "after_label": "API 자동화",
        "before_pct": 100,
        "after_pct": 10,
        "before_text": "—시간/일",
        "after_text": "—분/일",
    },
    {
        "client": "A 의료 마케팅 대행사",
        "platform": "뷰티 플랫폼",
        "metric_label": "업무 효율 향상",
        "metric_value": "—",
        "metric_unit": "%",
        "metric_numeric": None,
        "before_label": "수동 수집",
        "after_label": "자동 수집",
        "before_pct": 100,
        "after_pct": 5,
        "before_text": "—시간/일",
        "after_text": "—분/일",
    },
    {
        "client": "B 병원 그룹",
        "platform": "여론 모니터링",
        "metric_label": "감지 응답",
        "metric_value": "—",
        "metric_unit": "시간",
        "metric_numeric": None,
        "before_label": "수동 확인",
        "after_label": "AI 실시간",
        "before_pct": 100,
        "after_pct": 100,
        "before_text": "—시간 지연",
        "after_text": "실시간",
    },
]

TREND_DATA = [
    {"month": "1월", "value": 0},
    {"month": "2월", "value": 0},
    {"month": "3월", "value": 0},
    {"month": "4월", "value": 0},
    {"month": "5월", "value": 0},
    {"month": "6월", "value": 0},
]


def _with_trend_heights(data: list[dict]) -> list[dict]:
    max_val = max((item["value"] for item in data), default=0)
    result = []
    for item in data:
        if max_val <= 0 or item["value"] <= 0:
            height = 8
        else:
            height = max(12, round(item["value"] / max_val * 100))
        result.append({**item, "height_pct": height})
    return result

CONTACT_HERO = {
    "eyebrow": "CONTACT",
    "title": "문의하기",
    "desc": "구상 중이신 아이디어를 현실로 만들어 드립니다. 개발 및 자동화 구축 문의는 아래 링크로 편하게 남겨주세요.",
    "points": ["평균 응답 10분 이내", "10시 ~ 23시 상담", "세금계산서 발행 가능"],
    "highlights": [
        {
            "title": "100% 맞춤형 제작",
            "desc": "원하시는 사양대로 모두 구현이 가능합니다.",
        },
        {
            "title": "지속적인 유지보수",
            "desc": "개발만 하고 유지보수를 하지 않는 타 업체와 달리, 각 플랫폼 변화에 맞춰 지속적인 업데이트가 가능합니다.",
        },
    ],
}

CONTACT_CHANNELS = [
    {
        "id": "kakao",
        "label": "카카오톡",
        "value": "헬로비디디 - 개발문의",
        "url": "https://open.kakao.com/o/sBrSfcCi",
        "hint": "가장 빠른 상담",
        "action": "카톡으로 문의",
        "primary": True,
    },
    {
        "id": "telegram",
        "label": "텔레그램",
        "value": "@bedogdog",
        "url": "https://t.me/bedogdog",
        "hint": "해외·대용량 파일",
        "action": "텔레그램 문의",
        "primary": False,
    },
    {
        "id": "email",
        "label": "이메일",
        "value": "hellobdd0409@gmail.com",
        "url": "mailto:hellobdd0409@gmail.com",
        "hint": "제안서·견적 요청",
        "action": "메일 보내기",
        "primary": False,
    },
]


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    response = templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "company": "헬로비디디",
            "static_v": static_version(),
            "slogan": "서버 직접 통신 기반 마케팅 인프라 자동화 & AI 솔루션",
            "hero_eyebrow": HERO_EYEBROW,
            "hero_title_main": HERO_TITLE_MAIN,
            "hero_title_sub": HERO_TITLE_SUB,
            "hero_platform_lines": HERO_PLATFORM_LINES,
            "hero_platforms_note": HERO_PLATFORMS_NOTE,
            "hero_keywords": HERO_KEYWORDS,
            "stats_overview": STATS_OVERVIEW,
            "case_stats": CASE_STATS,
            "trend_data": _with_trend_heights(TREND_DATA),
            "contact_channels": CONTACT_CHANNELS,
            "contact_hero": CONTACT_HERO,
            "kmong": KMONG_PROFILE,
            "capabilities": CAPABILITIES,
            "products": PRODUCTS,
        },
    )
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    return response


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import socket
    import uvicorn

    def find_available_port(start: int = 8000, end: int = 8010) -> int:
        for port in range(start, end):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                try:
                    sock.bind(("127.0.0.1", port))
                    return port
                except OSError:
                    continue
        raise RuntimeError(f"사용 가능한 포트가 없습니다 ({start}~{end - 1})")

    port = find_available_port()
    print(f"서버 시작: http://127.0.0.1:{port}")
    uvicorn.run("main:app", host="127.0.0.1", port=port, reload=False)
