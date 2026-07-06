import markdown
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Challenge, Settings
from ..services.gemini_web import GeminiAuthError, GeminiWebClient

router = APIRouter(prefix="/api/chatbot")


class SettingsPayload(BaseModel):
    gemini_session_cookie: str
    gemini_cookie_ts: str = ""


class MessagePayload(BaseModel):
    message: str
    conversation_id: str = ""
    parent_message_id: str = ""


def render_md(text: str) -> str:
    # Use standard markdown compilation with fenced_code and tables extensions
    return markdown.markdown(text, extensions=["fenced_code", "tables"])


@router.get("/settings")
def get_settings(db: Session = Depends(get_db)):
    settings = db.execute(select(Settings)).scalar_one_or_none()
    if not settings:
        return {"configured": False}
    
    is_configured = bool(settings.gemini_session_cookie)
    return {
        "configured": is_configured,
        "gemini_session_cookie": settings.gemini_session_cookie or "",
        "gemini_cookie_ts": settings.gemini_cookie_ts or "",
    }


@router.post("/settings")
def update_settings(payload: SettingsPayload, db: Session = Depends(get_db)):
    settings = db.execute(select(Settings)).scalar_one_or_none()
    if not settings:
        settings = Settings()
        db.add(settings)
        
    settings.gemini_session_cookie = payload.gemini_session_cookie.strip()
    settings.gemini_cookie_ts = payload.gemini_cookie_ts.strip()
    db.commit()
    return {"success": True}


@router.post("/autodetect")
def autodetect_cookies(db: Session = Depends(get_db)):
    import browser_cookie3
    
    browsers = [
        ("Chrome", browser_cookie3.chrome),
        ("Edge", browser_cookie3.edge),
        ("Firefox", browser_cookie3.firefox),
    ]
    
    errors = []
    for name, extractor in browsers:
        try:
            cj = extractor(domain_name="google.com")
            psid = ""
            psidts = ""
            for cookie in cj:
                if cookie.name == "__Secure-1PSID":
                    psid = cookie.value
                elif cookie.name == "__Secure-1PSIDTS":
                    psidts = cookie.value
            
            if psid:
                settings = db.execute(select(Settings)).scalar_one_or_none()
                if not settings:
                    settings = Settings()
                    db.add(settings)
                
                settings.gemini_session_cookie = psid.strip()
                settings.gemini_cookie_ts = psidts.strip()
                db.commit()
                
                return {
                    "success": True,
                    "browser": name,
                    "gemini_session_cookie": psid,
                    "gemini_cookie_ts": psidts
                }
        except Exception as e:
            errors.append(f"{name} ({str(e)})")
            
    raise HTTPException(
        status_code=400,
        detail=f"Auto-detection failed. Checked browsers errors: {'; '.join(errors)}. Please configure manually.",
    )



@router.post("/message")
def send_message(payload: MessagePayload, db: Session = Depends(get_db)):
    settings = db.execute(select(Settings)).scalar_one_or_none()
    if not settings or not settings.gemini_session_cookie:
        raise HTTPException(
            status_code=400,
            detail="Gemini Copilot is not configured. Please go to settings and add your session cookies.",
        )
        
    try:
        with GeminiWebClient(
            secure_1psid=settings.gemini_session_cookie,
            secure_1psidts=settings.gemini_cookie_ts,
        ) as client:
            reply_text, conversation_id, parent_message_id = client.send_message(
                prompt=payload.message,
                conversation_id=payload.conversation_id,
                parent_message_id=payload.parent_message_id,
            )

            # Google rotates __Secure-1PSIDTS; persist the fresh value so the
            # stored snapshot doesn't go stale and start returning 401s.
            rotated = client.current_psidts
            if rotated and rotated != settings.gemini_cookie_ts:
                settings.gemini_cookie_ts = rotated
                db.commit()

        return {
            "success": True,
            "reply": reply_text,
            "html": render_md(reply_text),
            "conversation_id": conversation_id,
            "parent_message_id": parent_message_id,
        }
    except GeminiAuthError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/challenge/{slug}")
def get_challenge_details(slug: str, db: Session = Depends(get_db)):
    challenge = db.execute(
        select(Challenge).where(Challenge.slug == slug)
    ).scalar_one_or_none()
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
        
    return {
        "title": challenge.title,
        "prompt_md": challenge.prompt_md,
        "starter_code": challenge.starter_code,
    }
