import re
import json
import random
import urllib.parse
import httpx

_FRIENDLY_AUTH_MESSAGE = (
    "Gemini session expired or rejected. Open Gemini Copilot settings and "
    "click Auto-detect (or paste fresh cookies from gemini.google.com)."
)


class GeminiAuthError(Exception):
    """Gemini rejected the session cookies (stale/rotated __Secure-1PSIDTS)."""

    def __init__(self, message: str = _FRIENDLY_AUTH_MESSAGE):
        super().__init__(message)


class GeminiWebClient:
    def __init__(
        self,
        secure_1psid: str,
        secure_1psidts: str | None = None,
        transport: httpx.BaseTransport | None = None,
    ):
        self.secure_1psid = secure_1psid
        self.secure_1psidts = secure_1psidts

        # Seed cookies with an explicit .google.com domain so a Set-Cookie
        # rotation from Google overwrites the jar entry instead of adding a
        # conflicting duplicate.
        cookies = httpx.Cookies()
        cookies.set("__Secure-1PSID", secure_1psid, domain=".google.com")
        if secure_1psidts:
            cookies.set("__Secure-1PSIDTS", secure_1psidts, domain=".google.com")

        self.client = httpx.Client(
            transport=transport,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
            },
            cookies=cookies,
            follow_redirects=True,
            timeout=30.0
        )

    @property
    def current_psidts(self) -> str | None:
        """The freshest __Secure-1PSIDTS known — Google rotates this cookie
        via Set-Cookie on page loads; the caller should persist it."""
        for cookie in self.client.cookies.jar:
            if cookie.name == "__Secure-1PSIDTS" and cookie.value != self.secure_1psidts:
                return cookie.value
        return self.secure_1psidts

    def close(self) -> None:
        self.client.close()

    def __enter__(self) -> "GeminiWebClient":
        return self

    def __exit__(self, *exc_info) -> None:
        self.close()

    def extract_tokens(self) -> tuple[str, str, str]:
        """
        Extracts SNlM0e (at), cfb2h (bl), and FdrFJe (sid) from gemini.google.com/app
        """
        resp = self.client.get("https://gemini.google.com/app")
        if resp.status_code in (401, 403):
            raise GeminiAuthError()
        if resp.status_code != 200:
            raise Exception(
                f"Could not reach Gemini (Status {resp.status_code}). Please make sure your cookies are correct."
            )
            
        html = resp.text
        
        # SNlM0e -> at
        at_match = re.search(r'"SNlM0e"\s*:\s*"([^"]+)"', html)
        at = at_match.group(1) if at_match else None
        
        # cfb2h -> bl
        bl_match = re.search(r'"cfb2h"\s*:\s*"([^"]+)"', html)
        bl = bl_match.group(1) if bl_match else None
        
        # FdrFJe -> sid
        sid_match = re.search(r'"FdrFJe"\s*:\s*"([^"]+)"', html)
        sid = sid_match.group(1) if sid_match else ""
        
        if not at or not bl:
            raise GeminiAuthError(
                "Gemini session not found. Please log into gemini.google.com, "
                "extract a fresh __Secure-1PSID cookie, and try again."
            )

        return at, bl, sid

    def send_message(self, prompt: str, conversation_id: str = "", parent_message_id: str = "") -> tuple[str, str, str]:
        """
        Sends a message to Gemini and returns (reply_text, new_conversation_id, new_message_id)

        Retries once on an auth failure: the token-scrape GET usually picks up
        a rotated __Secure-1PSIDTS via Set-Cookie, so the second attempt runs
        with a fresh cookie jar.
        """
        try:
            return self._attempt_send(prompt, conversation_id, parent_message_id)
        except GeminiAuthError:
            return self._attempt_send(prompt, conversation_id, parent_message_id)

    def _attempt_send(self, prompt: str, conversation_id: str, parent_message_id: str) -> tuple[str, str, str]:
        at, bl, sid = self.extract_tokens()
        
        # Format identical to prompt_enhancer's background.ts StreamGenerate call
        inner_req = [
            [prompt, 0, None, None, None, None, 0],
            ["en"],
            [conversation_id or "", parent_message_id or "", "", None, None, None, None, None, None, ""]
        ]
        
        f_req = json.dumps([None, json.dumps(inner_req)])
        req_body = {
            "at": at,
            "f.req": f_req
        }
        
        req_id = random.randint(1000000, 9999999)
        url = (
            f"https://gemini.google.com/_/BardChatUi/data/assistant.lamda.BardFrontendService/StreamGenerate"
            f"?bl={urllib.parse.quote(bl)}"
            f"&f.sid={urllib.parse.quote(sid)}"
            f"&hl=en"
            f"&_reqid={req_id}"
            f"&rt=c"
        )
        
        resp = self.client.post(
            url,
            data=req_body,
            headers={
                "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
            }
        )
        
        if resp.status_code in (401, 403):
            raise GeminiAuthError()
        if resp.status_code != 200:
            raise Exception(f"Gemini returned status {resp.status_code}: {resp.text[:200]}")
            
        reply_text = ""
        new_conv_id = ""
        new_msg_id = ""
        
        # Parse stream response lines
        for line in resp.text.splitlines():
            if line.startswith("[["):
                try:
                    arr = json.loads(line)
                    if (
                        arr 
                        and isinstance(arr, list) 
                        and len(arr) > 0 
                        and arr[0] 
                        and arr[0][0] == 'wrb.fr' 
                        and len(arr[0]) > 2 
                        and arr[0][2]
                    ):
                        inner = json.loads(arr[0][2])
                        # Extract the message contents
                        if (
                            len(inner) > 4 
                            and inner[4] 
                            and len(inner[4]) > 0 
                            and inner[4][0] 
                            and len(inner[4][0]) > 1 
                            and inner[4][0][1] 
                            and len(inner[4][0][1]) > 0
                        ):
                            # The first element is the main markdown content
                            reply_text = inner[4][0][1][0] or reply_text
                        
                        # Extract conversationId & messageId
                        if len(inner) > 1 and inner[1]:
                            if len(inner[1]) > 0 and inner[1][0]:
                                new_conv_id = inner[1][0]
                            if len(inner[1]) > 1 and inner[1][1]:
                                new_msg_id = inner[1][1]
                except Exception:
                    pass
                    
        if not reply_text:
            raise Exception("Received empty response from Gemini. Check if your cookies are expired.")
            
        return reply_text.strip(), new_conv_id, new_msg_id
