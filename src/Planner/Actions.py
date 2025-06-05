from __future__ import annotations

import enum
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class _ActionInfo:
    category: str
    desc: str

class RomanceAction(enum.Enum):
    ROOT_ACTION           = _ActionInfo("ROOT", "")

    GREET_WARM            = _ActionInfo("rapport",  "Cheerful hello / emoji wave.")
    GREET_CALLBACK        = _ActionInfo("rapport",  "Open by referencing last chat.")
    ASK_DAY               = _ActionInfo("rapport",  "Quick check-in about their day.")
    INSIDE_JOKE           = _ActionInfo("rapport",  "Shared meme or running gag.")

    COMPLIMENT_APPEARANCE = _ActionInfo("flirt",    "Praise a photo / outfit.")
    COMPLIMENT_PERSONALITY= _ActionInfo("flirt",    "Admire a character trait.")
    COMPLIMENT_SKILL      = _ActionInfo("flirt",    "Admire a talent / hobby.")
    FLIRT_SUBTLE          = _ActionInfo("flirt",    "Hinted attraction, indirect.")
    FLIRT_DIRECT          = _ActionInfo("flirt",    "Explicit attraction line.")
    LIGHT_TEASE           = _ActionInfo("flirt",    "Friendly playful poke.")

    SHARE_PERSONAL_ANECDOTE = _ActionInfo("share",  "Short story from today / past.")
    SHARE_EMOTION           = _ActionInfo("share",  "Reveal current feeling.")
    PERSONAL_DISCLOSURE     = _ActionInfo("share",  "Deeper value / fear / dream.")
    VALIDATE_PARTNER_FEELING= _ActionInfo("share",  "Reflect & affirm their emotion.")
    ENCOURAGE_PARTNER       = _ActionInfo("share",  "Cheer them on / motivate.")

    PLAYFUL_CHALLENGE     = _ActionInfo("humor",    "Friendly competition/rematch.")
    HUMOROUS_GIF_EMOJI    = _ActionInfo("humor",    "Send meme / GIF / emoji bit.")

    SUGGEST_CASUAL_MEET   = _ActionInfo("escalate", "Low-stakes hangout invite.")
    SUGGEST_ACTIVITY_DATE = _ActionInfo("escalate", "Specific activity/date idea.")
    TIME_PROPOSAL         = _ActionInfo("escalate", "Ask about concrete timing.")
    MOVE_TO_CALL_VIDEO    = _ActionInfo("escalate", "Suggest voice/video call.")
    COMMIT_TO_PLAN        = _ActionInfo("escalate", "Confirm/lock logistics.")

    COMFORT_SUPPORT       = _ActionInfo("support",  "Empathise when they’re down.")
    CHECK_BOUNDARIES      = _ActionInfo("support",  "Ask if pace/topic is okay.")
    REFERENCE_PAST_EVENT  = _ActionInfo("momentum", "Recall shared memory.")
    EXPRESS_MISS          = _ActionInfo("momentum", "Say you missed chatting.")
    ACK_DELAY_APOLOGIZE   = _ActionInfo("momentum", "Explain slow response.")
    SWEET_GOODNIGHT       = _ActionInfo("closure",  "Affectionate sign-off.")