
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union
from datetime import datetime, timedelta
import random
import json
import asyncio
import aiohttp
import logging
import hashlib
import hmac
import base64
import time
import re
from urllib.parse import urlencode, quote

from models import (
    User, ChatConfig, AdminLevel, ModLog, Business, CryptoAsset,
    StockAsset, UserPortfolio, Miner, Auction, Clan, ClanWar,
    Tournament, Pet, ShopItem, UserInventory, Achievement,
    Transaction, GameSession, Report, GlobalEconomy, Earth,
    Vehicle, House, Insurance, BlacklistEntry, ChatStats,
    WorldEvent, GameType, ModActionType, TransactionType,
    generate_id, SUPER_ADMIN_ID, SUPER_ADMIN_LEVEL,
    CRYPTO_ASSETS_CONFIG, STOCK_ASSETS_CONFIG,
)

from services import DataStore, EconomyService, BankService, BusinessService, MarketService
from game_logic import CasinoService, AuctionService, CrimeService, ModerationService
from game_logic import ClanService, MarriageService, AchievementService, InsuranceService, ReputationService


# ============================================================
# БАЗОВЫЙ КЛАСС ДЛЯ ВНЕШНИХ API
# ============================================================

class BaseAPIClient:
    def __init__(self, base_url: str, api_key: str = "", timeout: int = 30):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self.session: Optional[aiohttp.ClientSession] = None
        self.logger = logging.getLogger(self.__class__.__name__)

    async def ensure_session(self) -> aiohttp.ClientSession:
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.timeout),
                headers={"User-Agent": "FableBot/2.0", "X-API-Key": self.api_key},
            )
        return self.session

    async def close(self) -> None:
        if self.session and not self.session.closed:
            await self.session.close()
            self.session = None

    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None,
                  headers: Optional[Dict[str, str]] = None) -> Optional[Dict[str, Any]]:
        try:
            session = await self.ensure_session()
            url = f"{self.base_url}/{endpoint.lstrip('/')}"
            merged_headers = {**({"X-API-Key": self.api_key} if self.api_key else {}), **(headers or {})}

            async with session.get(url, params=params, headers=merged_headers) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 429:
                    self.logger.warning(f"Rate limit exceeded for {url}")
                    await asyncio.sleep(5)
                    return await self.get(endpoint, params, headers)
                else:
                    self.logger.error(f"API GET error: {response.status} for {url}")
                    text = await response.text()
                    self.logger.debug(f"Response: {text[:500]}")
                    return None
        except asyncio.TimeoutError:
            self.logger.error(f"Timeout for {endpoint}")
            return None
        except aiohttp.ClientError as e:
            self.logger.error(f"Client error for {endpoint}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error for {endpoint}: {e}")
            return None

    async def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None,
                   json_data: Optional[Dict[str, Any]] = None,
                   headers: Optional[Dict[str, str]] = None) -> Optional[Dict[str, Any]]:
        try:
            session = await self.ensure_session()
            url = f"{self.base_url}/{endpoint.lstrip('/')}"
            merged_headers = {**({"X-API-Key": self.api_key} if self.api_key else {}), **(headers or {})}

            async with session.post(url, data=data, json=json_data, headers=merged_headers) as response:
                if response.status in (200, 201, 202):
                    return await response.json()
                elif response.status == 429:
                    self.logger.warning(f"Rate limit exceeded for {url}")
                    await asyncio.sleep(5)
                    return await self.post(endpoint, data, json_data, headers)
                else:
                    self.logger.error(f"API POST error: {response.status} for {url}")
                    text = await response.text()
                    self.logger.debug(f"Response: {text[:500]}")
                    return None
        except asyncio.TimeoutError:
            self.logger.error(f"Timeout for {endpoint}")
            return None
        except aiohttp.ClientError as e:
            self.logger.error(f"Client error for {endpoint}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error for {endpoint}: {e}")
            return None

    async def put(self, endpoint: str, json_data: Optional[Dict[str, Any]] = None,
                  headers: Optional[Dict[str, str]] = None) -> Optional[Dict[str, Any]]:
        try:
            session = await self.ensure_session()
            url = f"{self.base_url}/{endpoint.lstrip('/')}"
            merged_headers = {**({"X-API-Key": self.api_key} if self.api_key else {}), **(headers or {})}

            async with session.put(url, json=json_data, headers=merged_headers) as response:
                if response.status in (200, 201, 202):
                    return await response.json()
                elif response.status == 429:
                    self.logger.warning(f"Rate limit exceeded for {url}")
                    await asyncio.sleep(5)
                    return await self.put(endpoint, json_data, headers)
                else:
                    self.logger.error(f"API PUT error: {response.status} for {url}")
                    return None
        except asyncio.TimeoutError:
            self.logger.error(f"Timeout for {endpoint}")
            return None
        except aiohttp.ClientError as e:
            self.logger.error(f"Client error for {endpoint}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error for {endpoint}: {e}")
            return None

    async def delete(self, endpoint: str, headers: Optional[Dict[str, str]] = None) -> Optional[Dict[str, Any]]:
        try:
            session = await self.ensure_session()
            url = f"{self.base_url}/{endpoint.lstrip('/')}"
            merged_headers = {**({"X-API-Key": self.api_key} if self.api_key else {}), **(headers or {})}

            async with session.delete(url, headers=merged_headers) as response:
                if response.status in (200, 202, 204):
                    if response.status == 204:
                        return {"status": "deleted"}
                    return await response.json()
                elif response.status == 429:
                    self.logger.warning(f"Rate limit exceeded for {url}")
                    await asyncio.sleep(5)
                    return await self.delete(endpoint, headers)
                else:
                    self.logger.error(f"API DELETE error: {response.status} for {url}")
                    return None
        except asyncio.TimeoutError:
            self.logger.error(f"Timeout for {endpoint}")
            return None
        except aiohttp.ClientError as e:
            self.logger.error(f"Client error for {endpoint}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error for {endpoint}: {e}")
            return None


# ============================================================
# TELEGRAM BOT API КЛИЕНТ
# ============================================================

class TelegramBotClient(BaseAPIClient):
    def __init__(self, bot_token: str):
        super().__init__(base_url=f"https://api.telegram.org/bot{bot_token}")
        self.bot_token = bot_token
        self.logger = logging.getLogger("TelegramBotClient")

    async def send_message(self, chat_id: int, text: str,
                           parse_mode: str = "HTML",
                           reply_to_message_id: Optional[int] = None,
                           reply_markup: Optional[Dict[str, Any]] = None,
                           disable_web_page_preview: bool = True,
                           disable_notification: bool = False) -> Optional[Dict[str, Any]]:
        data = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode,
            "disable_web_page_preview": disable_web_page_preview,
            "disable_notification": disable_notification,
        }
        if reply_to_message_id:
            data["reply_to_message_id"] = reply_to_message_id
        if reply_markup:
            data["reply_markup"] = json.dumps(reply_markup)

        return await self.post("sendMessage", json_data=data)

    async def send_photo(self, chat_id: int, photo: str,
                          caption: str = "",
                          parse_mode: str = "HTML",
                          reply_to_message_id: Optional[int] = None,
                          reply_markup: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        data = {
            "chat_id": chat_id,
            "photo": photo,
            "caption": caption,
            "parse_mode": parse_mode,
        }
        if reply_to_message_id:
            data["reply_to_message_id"] = reply_to_message_id
        if reply_markup:
            data["reply_markup"] = json.dumps(reply_markup)

        return await self.post("sendPhoto", json_data=data)

    async def send_document(self, chat_id: int, document: str,
                             caption: str = "",
                             parse_mode: str = "HTML",
                             reply_to_message_id: Optional[int] = None) -> Optional[Dict[str, Any]]:
        data = {
            "chat_id": chat_id,
            "document": document,
            "caption": caption,
            "parse_mode": parse_mode,
        }
        if reply_to_message_id:
            data["reply_to_message_id"] = reply_to_message_id

        return await self.post("sendDocument", json_data=data)

    async def send_sticker(self, chat_id: int, sticker: str,
                            reply_to_message_id: Optional[int] = None) -> Optional[Dict[str, Any]]:
        data = {
            "chat_id": chat_id,
            "sticker": sticker,
        }
        if reply_to_message_id:
            data["reply_to_message_id"] = reply_to_message_id

        return await self.post("sendSticker", json_data=data)

    async def send_animation(self, chat_id: int, animation: str,
                              caption: str = "",
                              parse_mode: str = "HTML",
                              reply_to_message_id: Optional[int] = None) -> Optional[Dict[str, Any]]:
        data = {
            "chat_id": chat_id,
            "animation": animation,
            "caption": caption,
            "parse_mode": parse_mode,
        }
        if reply_to_message_id:
            data["reply_to_message_id"] = reply_to_message_id

        return await self.post("sendAnimation", json_data=data)

    async def send_video(self, chat_id: int, video: str,
                          caption: str = "",
                          parse_mode: str = "HTML",
                          reply_to_message_id: Optional[int] = None) -> Optional[Dict[str, Any]]:
        data = {
            "chat_id": chat_id,
            "video": video,
            "caption": caption,
            "parse_mode": parse_mode,
        }
        if reply_to_message_id:
            data["reply_to_message_id"] = reply_to_message_id

        return await self.post("sendVideo", json_data=data)

    async def send_audio(self, chat_id: int, audio: str,
                          caption: str = "",
                          parse_mode: str = "HTML",
                          reply_to_message_id: Optional[int] = None) -> Optional[Dict[str, Any]]:
        data = {
            "chat_id": chat_id,
            "audio": audio,
            "caption": caption,
            "parse_mode": parse_mode,
        }
        if reply_to_message_id:
            data["reply_to_message_id"] = reply_to_message_id

        return await self.post("sendAudio", json_data=data)

    async def send_voice(self, chat_id: int, voice: str,
                          caption: str = "",
                          reply_to_message_id: Optional[int] = None) -> Optional[Dict[str, Any]]:
        data = {
            "chat_id": chat_id,
            "voice": voice,
            "caption": caption,
        }
        if reply_to_message_id:
            data["reply_to_message_id"] = reply_to_message_id

        return await self.post("sendVoice", json_data=data)

    async def send_video_note(self, chat_id: int, video_note: str,
                               reply_to_message_id: Optional[int] = None) -> Optional[Dict[str, Any]]:
        data = {
            "chat_id": chat_id,
            "video_note": video_note,
        }
        if reply_to_message_id:
            data["reply_to_message_id"] = reply_to_message_id

        return await self.post("sendVideoNote", json_data=data)

    async def send_media_group(self, chat_id: int, media: List[Dict[str, Any]],
                                reply_to_message_id: Optional[int] = None) -> Optional[Dict[str, Any]]:
        data = {
            "chat_id": chat_id,
            "media": json.dumps(media),
        }
        if reply_to_message_id:
            data["reply_to_message_id"] = reply_to_message_id

        return await self.post("sendMediaGroup", json_data=data)

    async def send_location(self, chat_id: int, latitude: float, longitude: float,
                             reply_to_message_id: Optional[int] = None) -> Optional[Dict[str, Any]]:
        data = {
            "chat_id": chat_id,
            "latitude": latitude,
            "longitude": longitude,
        }
        if reply_to_message_id:
            data["reply_to_message_id"] = reply_to_message_id

        return await self.post("sendLocation", json_data=data)

    async def send_venue(self, chat_id: int, latitude: float, longitude: float,
                          title: str, address: str,
                          reply_to_message_id: Optional[int] = None) -> Optional[Dict[str, Any]]:
        data = {
            "chat_id": chat_id,
            "latitude": latitude,
            "longitude": longitude,
            "title": title,
            "address": address,
        }
        if reply_to_message_id:
            data["reply_to_message_id"] = reply_to_message_id

        return await self.post("sendVenue", json_data=data)

    async def send_contact(self, chat_id: int, phone_number: str, first_name: str,
                            reply_to_message_id: Optional[int] = None) -> Optional[Dict[str, Any]]:
        data = {
            "chat_id": chat_id,
            "phone_number": phone_number,
            "first_name": first_name,
        }
        if reply_to_message_id:
            data["reply_to_message_id"] = reply_to_message_id

        return await self.post("sendContact", json_data=data)

    async def send_poll(self, chat_id: int, question: str, options: List[str],
                         is_anonymous: bool = True,
                         allows_multiple_answers: bool = False,
                         reply_to_message_id: Optional[int] = None) -> Optional[Dict[str, Any]]:
        data = {
            "chat_id": chat_id,
            "question": question,
            "options": json.dumps(options),
            "is_anonymous": is_anonymous,
            "allows_multiple_answers": allows_multiple_answers,
        }
        if reply_to_message_id:
            data["reply_to_message_id"] = reply_to_message_id

        return await self.post("sendPoll", json_data=data)

    async def send_dice(self, chat_id: int, emoji: str = "🎲",
                         reply_to_message_id: Optional[int] = None) -> Optional[Dict[str, Any]]:
        data = {
            "chat_id": chat_id,
            "emoji": emoji,
        }
        if reply_to_message_id:
            data["reply_to_message_id"] = reply_to_message_id

        return await self.post("sendDice", json_data=data)

    async def send_chat_action(self, chat_id: int, action: str) -> Optional[Dict[str, Any]]:
        data = {
            "chat_id": chat_id,
            "action": action,
        }
        return await self.post("sendChatAction", json_data=data)

    async def delete_message(self, chat_id: int, message_id: int) -> Optional[Dict[str, Any]]:
        data = {
            "chat_id": chat_id,
            "message_id": message_id,
        }
        return await self.post("deleteMessage", json_data=data)

    async def edit_message_text(self, chat_id: Optional[int], message_id: int,
                                 text: str, parse_mode: str = "HTML",
                                 inline_message_id: Optional[str] = None,
                                 reply_markup: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        data = {
            "message_id": message_id,
            "text": text,
            "parse_mode": parse_mode,
        }
        if chat_id:
            data["chat_id"] = chat_id
        if inline_message_id:
            data["inline_message_id"] = inline_message_id
        if reply_markup:
            data["reply_markup"] = json.dumps(reply_markup)

        return await self.post("editMessageText", json_data=data)

    async def edit_message_caption(self, chat_id: Optional[int], message_id: int,
                                    caption: str, parse_mode: str = "HTML",
                                    inline_message_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        data = {
            "message_id": message_id,
            "caption": caption,
            "parse_mode": parse_mode,
        }
        if chat_id:
            data["chat_id"] = chat_id
        if inline_message_id:
            data["inline_message_id"] = inline_message_id

        return await self.post("editMessageCaption", json_data=data)

    async def edit_message_reply_markup(self, chat_id: Optional[int], message_id: int,
                                         reply_markup: Dict[str, Any],
                                         inline_message_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        data = {
            "message_id": message_id,
            "reply_markup": json.dumps(reply_markup),
        }
        if chat_id:
            data["chat_id"] = chat_id
        if inline_message_id:
            data["inline_message_id"] = inline_message_id

        return await self.post("editMessageReplyMarkup", json_data=data)

    async def stop_poll(self, chat_id: int, message_id: int,
                         reply_markup: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        data = {
            "chat_id": chat_id,
            "message_id": message_id,
        }
        if reply_markup:
            data["reply_markup"] = json.dumps(reply_markup)

        return await self.post("stopPoll", json_data=data)

    async def pin_chat_message(self, chat_id: int, message_id: int,
                                disable_notification: bool = False) -> Optional[Dict[str, Any]]:
        data = {
            "chat_id": chat_id,
            "message_id": message_id,
            "disable_notification": disable_notification,
        }
        return await self.post("pinChatMessage", json_data=data)

    async def unpin_chat_message(self, chat_id: int,
                                  message_id: Optional[int] = None) -> Optional[Dict[str, Any]]:
        data = {"chat_id": chat_id}
        if message_id:
            data["message_id"] = message_id
        return await self.post("unpinChatMessage", json_data=data)

    async def ban_chat_member(self, chat_id: int, user_id: int,
                               until_date: Optional[int] = None,
                               revoke_messages: bool = True) -> Optional[Dict[str, Any]]:
        data = {
            "chat_id": chat_id,
            "user_id": user_id,
            "revoke_messages": revoke_messages,
        }
        if until_date:
            data["until_date"] = until_date

        return await self.post("banChatMember", json_data=data)

    async def unban_chat_member(self, chat_id: int, user_id: int,
                                 only_if_banned: bool = True) -> Optional[Dict[str, Any]]:
        data = {
            "chat_id": chat_id,
            "user_id": user_id,
            "only_if_banned": only_if_banned,
        }
        return await self.post("unbanChatMember", json_data=data)

    async def restrict_chat_member(self, chat_id: int, user_id: int,
                                    permissions: Dict[str, bool],
                                    until_date: Optional[int] = None) -> Optional[Dict[str, Any]]:
        data = {
            "chat_id": chat_id,
            "user_id": user_id,
            "permissions": json.dumps(permissions),
        }
        if until_date:
            data["until_date"] = until_date

        return await self.post("restrictChatMember", json_data=data)

    async def promote_chat_member(self, chat_id: int, user_id: int,
                                   can_manage_chat: bool = True,
                                   can_delete_messages: bool = True,
                                   can_restrict_members: bool = True,
                                   can_promote_members: bool = False,
                                   can_change_info: bool = True,
                                   can_invite_users: bool = True,
                                   can_pin_messages: bool = True,
                                   can_post_stories: bool = False,
                                   can_edit_stories: bool = False,
                                   can_delete_stories: bool = False,
                                   can_manage_topics: bool = False,
                                   is_anonymous: bool = False) -> Optional[Dict[str, Any]]:
        data = {
            "chat_id": chat_id,
            "user_id": user_id,
            "can_manage_chat": can_manage_chat,
            "can_delete_messages": can_delete_messages,
            "can_restrict_members": can_restrict_members,
            "can_promote_members": can_promote_members,
            "can_change_info": can_change_info,
            "can_invite_users": can_invite_users,
            "can_pin_messages": can_pin_messages,
            "can_post_stories": can_post_stories,
            "can_edit_stories": can_edit_stories,
            "can_delete_stories": can_delete_stories,
            "can_manage_topics": can_manage_topics,
            "is_anonymous": is_anonymous,
        }
        return await self.post("promoteChatMember", json_data=data)

    async def set_chat_permissions(self, chat_id: int,
                                    permissions: Dict[str, bool]) -> Optional[Dict[str, Any]]:
        data = {
            "chat_id": chat_id,
            "permissions": json.dumps(permissions),
        }
        return await self.post("setChatPermissions", json_data=data)

    async def export_chat_invite_link(self, chat_id: int) -> Optional[Dict[str, Any]]:
        data = {"chat_id": chat_id}
        return await self.post("exportChatInviteLink", json_data=data)

    async def create_chat_invite_link(self, chat_id: int,
                                       name: str = "",
                                       expire_date: Optional[int] = None,
                                       member_limit: Optional[int] = None,
                                       creates_join_request: bool = False) -> Optional[Dict[str, Any]]:
        data = {
            "chat_id": chat_id,
            "name": name,
            "creates_join_request": creates_join_request,
        }
        if expire_date:
            data["expire_date"] = expire_date
        if member_limit:
            data["member_limit"] = member_limit

        return await self.post("createChatInviteLink", json_data=data)

    async def set_chat_photo(self, chat_id: int, photo: str) -> Optional[Dict[str, Any]]:
        data = {
            "chat_id": chat_id,
            "photo": photo,
        }
        return await self.post("setChatPhoto", json_data=data)

    async def delete_chat_photo(self, chat_id: int) -> Optional[Dict[str, Any]]:
        data = {"chat_id": chat_id}
        return await self.post("deleteChatPhoto", json_data=data)

    async def set_chat_title(self, chat_id: int, title: str) -> Optional[Dict[str, Any]]:
        data = {
            "chat_id": chat_id,
            "title": title,
        }
        return await self.post("setChatTitle", json_data=data)

    async def set_chat_description(self, chat_id: int,
                                    description: str) -> Optional[Dict[str, Any]]:
        data = {
            "chat_id": chat_id,
            "description": description,
        }
        return await self.post("setChatDescription", json_data=data)

    async def leave_chat(self, chat_id: int) -> Optional[Dict[str, Any]]:
        data = {"chat_id": chat_id}
        return await self.post("leaveChat", json_data=data)

    async def get_chat(self, chat_id: int) -> Optional[Dict[str, Any]]:
        data = {"chat_id": chat_id}
        return await self.post("getChat", json_data=data)

    async def get_chat_administrators(self, chat_id: int) -> Optional[List[Dict[str, Any]]]:
        data = {"chat_id": chat_id}
        result = await self.post("getChatAdministrators", json_data=data)
        if result and "result" in result:
            return result["result"]
        return None

    async def get_chat_member_count(self, chat_id: int) -> Optional[int]:
        data = {"chat_id": chat_id}
        result = await self.post("getChatMemberCount", json_data=data)
        if result and "result" in result:
            return result["result"]
        return None

    async def get_chat_member(self, chat_id: int, user_id: int) -> Optional[Dict[str, Any]]:
        data = {
            "chat_id": chat_id,
            "user_id": user_id,
        }
        result = await self.post("getChatMember", json_data=data)
        if result and "result" in result:
            return result["result"]
        return None

    async def answer_callback_query(self, callback_query_id: str,
                                     text: str = "",
                                     show_alert: bool = False,
                                     url: str = "",
                                     cache_time: int = 0) -> Optional[Dict[str, Any]]:
        data = {
            "callback_query_id": callback_query_id,
            "text": text,
            "show_alert": show_alert,
            "cache_time": cache_time,
        }
        if url:
            data["url"] = url

        return await self.post("answerCallbackQuery", json_data=data)

    async def answer_inline_query(self, inline_query_id: str,
                                   results: List[Dict[str, Any]],
                                   cache_time: int = 300,
                                   is_personal: bool = True,
                                   next_offset: str = "",
                                   switch_pm_text: str = "",
                                   switch_pm_parameter: str = "") -> Optional[Dict[str, Any]]:
        data = {
            "inline_query_id": inline_query_id,
            "results": json.dumps(results),
            "cache_time": cache_time,
            "is_personal": is_personal,
        }
        if next_offset:
            data["next_offset"] = next_offset
        if switch_pm_text:
            data["switch_pm_text"] = switch_pm_text
            data["switch_pm_parameter"] = switch_pm_parameter

        return await self.post("answerInlineQuery", json_data=data)

    async def set_webhook(self, url: str, certificate: Optional[str] = None,
                           max_connections: int = 40,
                           allowed_updates: Optional[List[str]] = None) -> Optional[Dict[str, Any]]:
        data = {
            "url": url,
            "max_connections": max_connections,
        }
        if certificate:
            data["certificate"] = certificate
        if allowed_updates:
            data["allowed_updates"] = json.dumps(allowed_updates)

        return await self.post("setWebhook", json_data=data)

    async def delete_webhook(self, drop_pending_updates: bool = False) -> Optional[Dict[str, Any]]:
        data = {"drop_pending_updates": drop_pending_updates}
        return await self.post("deleteWebhook", json_data=data)

    async def get_webhook_info(self) -> Optional[Dict[str, Any]]:
        return await self.post("getWebhookInfo")

    async def get_me(self) -> Optional[Dict[str, Any]]:
        return await self.post("getMe")

    async def log_out(self) -> Optional[Dict[str, Any]]:
        return await self.post("logOut")

    async def close_bot(self) -> Optional[Dict[str, Any]]:
        return await self.post("close")

    def create_inline_keyboard(self, buttons: List[List[Dict[str, str]]]) -> Dict[str, Any]:
        return {"inline_keyboard": buttons}

    def create_reply_keyboard(self, buttons: List[List[Dict[str, str]]],
                               resize_keyboard: bool = True,
                               one_time_keyboard: bool = False) -> Dict[str, Any]:
        return {
            "keyboard": buttons,
            "resize_keyboard": resize_keyboard,
            "one_time_keyboard": one_time_keyboard,
        }

    def create_force_reply(self, input_field_placeholder: str = "",
                            selective: bool = False) -> Dict[str, Any]:
        return {
            "force_reply": True,
            "input_field_placeholder": input_field_placeholder,
            "selective": selective,
        }

    def create_reply_keyboard_remove(self, selective: bool = False) -> Dict[str, Any]:
        return {
            "remove_keyboard": True,
            "selective": selective,
        }


# ============================================================
# DEEPSEEK AI КЛИЕНТ
# ============================================================

class DeepSeekClient(BaseAPIClient):
    def __init__(self, api_key: str, model: str = "deepseek-chat"):
        super().__init__(base_url="https://api.deepseek.com/v1", api_key=api_key)
        self.model = model
        self.logger = logging.getLogger("DeepSeekClient")
        self.conversation_history: Dict[int, List[Dict[str, str]]] = {}
        self.max_history_length = 50

    async def chat(self, user_id: int, message: str,
                   system_prompt: str = "",
                   temperature: float = 0.7,
                   max_tokens: int = 2000) -> Optional[str]:
        try:
            if user_id not in self.conversation_history:
                self.conversation_history[user_id] = []

            history = self.conversation_history[user_id]

            if len(history) == 0 and system_prompt:
                history.append({"role": "system", "content": system_prompt})

            history.append({"role": "user", "content": message})

            if len(history) > self.max_history_length:
                if history[0]["role"] == "system":
                    history = [history[0]] + history[-(self.max_history_length - 1):]
                else:
                    history = history[-self.max_history_length:]
                self.conversation_history[user_id] = history

            payload = {
                "model": self.model,
                "messages": history,
                "temperature": temperature,
                "max_tokens": max_tokens,
            }

            result = await self.post("chat/completions", json_data=payload)

            if result and "choices" in result and len(result["choices"]) > 0:
                response_text = result["choices"][0].get("message", {}).get("content", "")
                history.append({"role": "assistant", "content": response_text})
                self.conversation_history[user_id] = history
                return response_text

            return None

        except Exception as e:
            self.logger.error(f"DeepSeek chat error: {e}")
            return None

    def clear_history(self, user_id: int) -> None:
        if user_id in self.conversation_history:
            del self.conversation_history[user_id]

    def get_history(self, user_id: int) -> List[Dict[str, str]]:
        return self.conversation_history.get(user_id, [])

    async def analyze_sentiment(self, text: str) -> Optional[Dict[str, float]]:
        try:
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": "Проанализируй тональность текста и верни JSON: {\"positive\": float, \"negative\": float, \"neutral\": float, \"toxic\": float}. Сумма должна быть 1.0."
                    },
                    {"role": "user", "content": text},
                ],
                "temperature": 0.1,
                "max_tokens": 100,
                "response_format": {"type": "json_object"},
            }

            result = await self.post("chat/completions", json_data=payload)

            if result and "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0].get("message", {}).get("content", "{}")
                return json.loads(content)

            return None

        except Exception as e:
            self.logger.error(f"DeepSeek sentiment analysis error: {e}")
            return None

    async def generate_text(self, prompt: str, max_tokens: int = 500,
                             temperature: float = 0.8) -> Optional[str]:
        try:
            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": temperature,
                "max_tokens": max_tokens,
            }

            result = await self.post("chat/completions", json_data=payload)

            if result and "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0].get("message", {}).get("content", "")

            return None

        except Exception as e:
            self.logger.error(f"DeepSeek text generation error: {e}")
            return None

    async def translate(self, text: str, target_language: str) -> Optional[str]:
        try:
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": f"Переведи следующий текст на {target_language}. Верни только перевод, без пояснений."
                    },
                    {"role": "user", "content": text},
                ],
                "temperature": 0.3,
                "max_tokens": 2000,
            }

            result = await self.post("chat/completions", json_data=payload)

            if result and "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0].get("message", {}).get("content", "")

            return None

        except Exception as e:
            self.logger.error(f"DeepSeek translation error: {e}")
            return None

    async def summarize(self, text: str, max_length: int = 200) -> Optional[str]:
        try:
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": f"Сделай краткую сводку текста на русском языке, не более {max_length} символов."
                    },
                    {"role": "user", "content": text},
                ],
                "temperature": 0.5,
                "max_tokens": max_length,
            }

            result = await self.post("chat/completions", json_data=payload)

            if result and "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0].get("message", {}).get("content", "")

            return None

        except Exception as e:
            self.logger.error(f"DeepSeek summarization error: {e}")
            return None


# ============================================================
# GROK AI КЛИЕНТ
# ============================================================

class GrokClient(BaseAPIClient):
    def __init__(self, api_key: str, model: str = "grok-2"):
        super().__init__(base_url="https://api.x.ai/v1", api_key=api_key)
        self.model = model
        self.logger = logging.getLogger("GrokClient")
        self.conversation_history: Dict[int, List[Dict[str, str]]] = {}
        self.max_history_length = 40

    async def chat(self, user_id: int, message: str,
                   system_prompt: str = "",
                   temperature: float = 0.8,
                   max_tokens: int = 2000) -> Optional[str]:
        try:
            if user_id not in self.conversation_history:
                self.conversation_history[user_id] = []

            history = self.conversation_history[user_id]

            if len(history) == 0 and system_prompt:
                history.append({"role": "system", "content": system_prompt})

            history.append({"role": "user", "content": message})

            if len(history) > self.max_history_length:
                if history[0]["role"] == "system":
                    history = [history[0]] + history[-(self.max_history_length - 1):]
                else:
                    history = history[-self.max_history_length:]
                self.conversation_history[user_id] = history

            payload = {
                "model": self.model,
                "messages": history,
                "temperature": temperature,
                "max_tokens": max_tokens,
            }

            result = await self.post("chat/completions", json_data=payload)

            if result and "choices" in result and len(result["choices"]) > 0:
                response_text = result["choices"][0].get("message", {}).get("content", "")
                history.append({"role": "assistant", "content": response_text})
                self.conversation_history[user_id] = history
                return response_text

            return None

        except Exception as e:
            self.logger.error(f"Grok chat error: {e}")
            return None

    def clear_history(self, user_id: int) -> None:
        if user_id in self.conversation_history:
            del self.conversation_history[user_id]

    def get_history(self, user_id: int) -> List[Dict[str, str]]:
        return self.conversation_history.get(user_id, [])

    async def generate_image_prompt(self, description: str, style: str = "") -> Optional[str]:
        try:
            prompt = f"Создай детальный промпт для генерации изображения по описанию: {description}"
            if style:
                prompt += f" в стиле {style}"
            prompt += ". Верни только промпт на английском языке."

            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.9,
                "max_tokens": 500,
            }

            result = await self.post("chat/completions", json_data=payload)

            if result and "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0].get("message", {}).get("content", "")

            return None

        except Exception as e:
            self.logger.error(f"Grok image prompt generation error: {e}")
            return None

    async def generate_joke(self, topic: str = "") -> Optional[str]:
        try:
            prompt = "Придумай смешную шутку"
            if topic:
                prompt += f" на тему: {topic}"
            prompt += " на русском языке."

            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 1.0,
                "max_tokens": 200,
            }

            result = await self.post("chat/completions", json_data=payload)

            if result and "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0].get("message", {}).get("content", "")

            return None

        except Exception as e:
            self.logger.error(f"Grok joke generation error: {e}")
            return None

    async def creative_response(self, message: str, character: str = "саркастичный") -> Optional[str]:
        try:
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": f"Ты отвечаешь в {character} стиле. Будь остроумным, дерзким и креативным. Отвечай на русском."
                    },
                    {"role": "user", "content": message},
                ],
                "temperature": 1.0,
                "max_tokens": 1000,
            }

            result = await self.post("chat/completions", json_data=payload)

            if result and "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0].get("message", {}).get("content", "")

            return None

        except Exception as e:
            self.logger.error(f"Grok creative response error: {e}")
            return None


# ============================================================
# ГЕНЕРАТОР ИЗОБРАЖЕНИЙ (STABLE DIFFUSION / DALL-E)
# ============================================================

class ImageGenerationClient(BaseAPIClient):
    def __init__(self, api_key: str, provider: str = "openai"):
        if provider == "openai":
            base_url = "https://api.openai.com/v1"
        elif provider == "stability":
            base_url = "https://api.stability.ai/v1"
        else:
            base_url = "https://api.openai.com/v1"

        super().__init__(base_url=base_url, api_key=api_key)
        self.provider = provider
        self.logger = logging.getLogger("ImageGenerationClient")

    async def generate_image(self, prompt: str, size: str = "1024x1024",
                              style: str = "vivid", n: int = 1) -> Optional[List[str]]:
        try:
            if self.provider == "openai":
                return await self._generate_openai(prompt, size, style, n)
            elif self.provider == "stability":
                return await self._generate_stability(prompt, size, n)
            else:
                return await self._generate_openai(prompt, size, style, n)
        except Exception as e:
            self.logger.error(f"Image generation error: {e}")
            return None

    async def _generate_openai(self, prompt: str, size: str = "1024x1024",
                                style: str = "vivid", n: int = 1) -> Optional[List[str]]:
        payload = {
            "model": "dall-e-3",
            "prompt": prompt,
            "n": min(n, 1),
            "size": size,
            "style": style,
        }

        result = await self.post("images/generations", json_data=payload)

        if result and "data" in result:
            return [img.get("url", "") for img in result["data"]]

        return None

    async def _generate_stability(self, prompt: str, size: str = "1024x1024",
                                   n: int = 1) -> Optional[List[str]]:
        width, height = 1024, 1024
        if "x" in size:
            parts = size.split("x")
            width, height = int(parts[0]), int(parts[1])

        payload = {
            "text_prompts": [{"text": prompt, "weight": 1.0}],
            "cfg_scale": 7,
            "height": height,
            "width": width,
            "samples": min(n, 4),
            "steps": 30,
        }

        headers = {"Content-Type": "application/json"}
        result = await self.post(
            "generation/stable-diffusion-xl-1024-v1-0/text-to-image",
            json_data=payload,
            headers=headers,
        )

        if result and "artifacts" in result:
            return [art.get("base64", "") for art in result["artifacts"]]

        return None

    async def generate_image_variation(self, image_url: str, n: int = 1) -> Optional[List[str]]:
        try:
            payload = {
                "image": image_url,
                "n": min(n, 1),
                "size": "1024x1024",
            }

            result = await self.post("images/variations", json_data=payload)

            if result and "data" in result:
                return [img.get("url", "") for img in result["data"]]

            return None

        except Exception as e:
            self.logger.error(f"Image variation error: {e}")
            return None

    async def edit_image(self, image_url: str, prompt: str,
                          mask_url: Optional[str] = None) -> Optional[List[str]]:
        try:
            payload = {
                "image": image_url,
                "prompt": prompt,
                "n": 1,
                "size": "1024x1024",
            }
            if mask_url:
                payload["mask"] = mask_url

            result = await self.post("images/edits", json_data=payload)

            if result and "data" in result:
                return [img.get("url", "") for img in result["data"]]

            return None

        except Exception as e:
            self.logger.error(f"Image edit error: {e}")
            return None


# ============================================================
# СЕРВИС РАССЫЛКИ
# ============================================================

class BroadcastService:
    def __init__(self, store: DataStore, telegram_client: TelegramBotClient):
        self.store = store
        self.tg = telegram_client
        self.logger = logging.getLogger("BroadcastService")

    async def broadcast_to_all_chats(self, sender_id: int, text: str,
                                      pin_message: bool = False) -> Tuple[bool, str, int]:
        if not is_super_admin(sender_id):
            return False, "Только супер-админ может делать рассылку", 0

        chat_ids = list(self.store.chats.keys())
        sent_count = 0
        failed_count = 0

        for chat_id in chat_ids:
            try:
                result = await self.tg.send_message(chat_id, text)
                if result and result.get("ok"):
                    sent_count += 1

                    if pin_message:
                        message_id = result.get("result", {}).get("message_id")
                        if message_id:
                            await self.tg.pin_chat_message(chat_id, message_id)
                else:
                    failed_count += 1

                await asyncio.sleep(0.1)

            except Exception as e:
                self.logger.error(f"Broadcast error for chat {chat_id}: {e}")
                failed_count += 1

        return True, f"Рассылка: отправлено в {sent_count} чатов, ошибок: {failed_count}", sent_count

    async def broadcast_to_chat(self, sender_id: int, chat_id: int,
                                 text: str) -> Tuple[bool, str]:
        if not is_super_admin(sender_id):
            return False, "Только супер-админ может делать рассылку"

        try:
            result = await self.tg.send_message(chat_id, text)
            if result and result.get("ok"):
                return True, "Сообщение отправлено"
            return False, "Ошибка отправки"
        except Exception as e:
            return False, f"Ошибка: {e}"

    async def send_announcement(self, sender_id: int, text: str) -> Tuple[bool, str, int]:
        return await self.broadcast_to_all_chats(sender_id, text, pin_message=True)

    async def send_poll_to_all_chats(self, sender_id: int, question: str,
                                      options: List[str]) -> Tuple[bool, str, int]:
        if not is_super_admin(sender_id):
            return False, "Только супер-админ может создавать опросы", 0

        chat_ids = list(self.store.chats.keys())
        sent_count = 0

        for chat_id in chat_ids:
            try:
                result = await self.tg.send_poll(chat_id, question, options)
                if result and result.get("ok"):
                    sent_count += 1
                await asyncio.sleep(0.1)
            except Exception as e:
                self.logger.error(f"Poll broadcast error for chat {chat_id}: {e}")

        return True, f"Опрос отправлен в {sent_count} чатов", sent_count


# ============================================================
# СЕРВИС УВЕДОМЛЕНИЙ
# ============================================================

class NotificationService:
    def __init__(self, store: DataStore, telegram_client: TelegramBotClient):
        self.store = store
        self.tg = telegram_client
        self.logger = logging.getLogger("NotificationService")

    async def notify_user(self, user_id: int, text: str) -> bool:
        try:
            result = await self.tg.send_message(user_id, text)
            return result is not None and result.get("ok", False)
        except Exception as e:
            self.logger.error(f"Notification error for user {user_id}: {e}")
            return False

    async def notify_moderation_action(self, target_id: int, action: str,
                                        reason: str, duration: str = "",
                                        chat_title: str = "") -> bool:
        text_parts = [f"🔔 Модерация: {action}"]
        if chat_title:
            text_parts.append(f"Чат: {chat_title}")
        if reason:
            text_parts.append(f"Причина: {reason}")
        if duration:
            text_parts.append(f"Срок: {duration}")

        text = "\n".join(text_parts)
        return await self.notify_user(target_id, text)

    async def notify_unmute_unban(self, target_id: int, action: str,
                                   chat_title: str = "") -> bool:
        text = f"🔓 {action} снят"
        if chat_title:
            text += f" в чате {chat_title}"
        return await self.notify_user(target_id, text)

    async def notify_transaction(self, user_id: int, amount: int,
                                  transaction_type: str, balance: int) -> bool:
        if amount > 0:
            text = f"💰 Зачисление: +{amount} монет\nТип: {transaction_type}\nБаланс: {balance}"
        else:
            text = f"💸 Списание: {amount} монет\nТип: {transaction_type}\nБаланс: {balance}"

        if abs(amount) >= 10000:
            return await self.notify_user(user_id, text)
        return True

    async def notify_insurance_payout(self, user_id: int, amount: int,
                                       reason: str) -> bool:
        text = f"🛡 Страховая выплата: {amount} монет\nПричина: {reason}"
        return await self.notify_user(user_id, text)

    async def notify_achievement(self, user_id: int, achievement_name: str,
                                  reward: int) -> bool:
        text = f"🏆 Новое достижение: {achievement_name}!\nНаграда: {reward} монет"
        return await self.notify_user(user_id, text)

    async def notify_tournament_start(self, user_id: int, tournament_name: str,
                                       starts_in_minutes: int) -> bool:
        text = f"🏟 Турнир '{tournament_name}' начинается через {starts_in_minutes} минут!"
        return await self.notify_user(user_id, text)

    async def notify_clan_war_start(self, user_id: int, opponent_clan: str) -> bool:
        text = f"⚔️ Клановая война против '{opponent_clan}' началась!"
        return await self.notify_user(user_id, text)

    async def notify_super_admin_stats(self, sender_id: int) -> Tuple[bool, str]:
        if not is_super_admin(sender_id):
            return False, "Только супер-админ"

        total_users = self.store.get_total_users()
        total_chats = self.store.get_total_chats()
        active_today = self.store.get_active_users_today()
        total_money = self.store.get_total_money_in_circulation()

        text = (
            f"📊 Статистика бота:\n"
            f"👥 Пользователей: {total_users}\n"
            f"💬 Чатов: {total_chats}\n"
            f"📅 Активных сегодня: {active_today}\n"
            f"💰 Монет в обращении: {total_money:,}\n"
            f"🏢 Бизнесов: {len(self.store.businesses)}\n"
            f"🏘 Кланов: {len(self.store.clans)}\n"
            f"⛏ Майнеров: {len(self.store.miners)}"
        )

        try:
            await self.tg.send_message(sender_id, text)
            return True, "Статистика отправлена в ЛС"
        except Exception as e:
            return False, f"Ошибка отправки: {e}"


# ============================================================
# ПЛАНИРОВЩИК ЗАДАЧ
# ============================================================

class TaskScheduler:
    def __init__(self, store: DataStore,
                 market_service: MarketService,
                 clan_service: ClanService,
                 achievement_service: AchievementService,
                 notification_service: NotificationService):
        self.store = store
        self.market = market_service
        self.clan = clan_service
        self.achievements = achievement_service
        self.notifications = notification_service
        self.logger = logging.getLogger("TaskScheduler")
        self.tasks: List[asyncio.Task] = []
        self.running = False

    async def start(self) -> None:
        self.running = True
        self.logger.info("Task scheduler started")

        self.tasks = [
            asyncio.create_task(self._crypto_update_loop()),
            asyncio.create_task(self._stock_update_loop()),
            asyncio.create_task(self._dividend_loop()),
            asyncio.create_task(self._mining_loop()),
            asyncio.create_task(self._bank_interest_loop()),
            asyncio.create_task(self._auction_check_loop()),
            asyncio.create_task(self._clan_war_check_loop()),
            asyncio.create_task(self._world_event_loop()),
            asyncio.create_task(self._insurance_expiry_loop()),
            asyncio.create_task(self._loan_check_loop()),
            asyncio.create_task(self._jail_release_loop()),
            asyncio.create_task(self._warn_expiry_loop()),
            asyncio.create_task(self._mute_expiry_loop()),
            asyncio.create_task(self._pet_status_loop()),
            asyncio.create_task(self._data_save_loop()),
        ]

    async def stop(self) -> None:
        self.running = False
        for task in self.tasks:
            task.cancel()
        self.tasks.clear()
        self.logger.info("Task scheduler stopped")

    async def _crypto_update_loop(self) -> None:
        while self.running:
            try:
                self.market.update_crypto_prices()
                self.logger.debug("Crypto prices updated")
            except Exception as e:
                self.logger.error(f"Crypto update error: {e}")
            await asyncio.sleep(CRYPTO_UPDATE_INTERVAL_MINUTES * 60)

    async def _stock_update_loop(self) -> None:
        while self.running:
            try:
                self.market.update_stock_prices()
                self.logger.debug("Stock prices updated")
            except Exception as e:
                self.logger.error(f"Stock update error: {e}")
            await asyncio.sleep(STOCK_UPDATE_INTERVAL_MINUTES * 60)

    async def _dividend_loop(self) -> None:
        while self.running:
            try:
                for user_id in list(self.store.users.keys()):
                    self.market.process_dividends(user_id)
                self.logger.debug("Dividends processed")
            except Exception as e:
                self.logger.error(f"Dividend processing error: {e}")
            await asyncio.sleep(DIVIDEND_INTERVAL_HOURS * 3600)

    async def _mining_loop(self) -> None:
        while self.running:
            try:
                for miner_id, miner in list(self.store.miners.items()):
                    if miner.owner_id in self.store.users:
                        self.market.process_mining(miner.owner_id)
                self.logger.debug("Mining processed")
            except Exception as e:
                self.logger.error(f"Mining processing error: {e}")
            await asyncio.sleep(3600)

    async def _bank_interest_loop(self) -> None:
        while self.running:
            try:
                bank_service = BankService(self.store)
                for user_id in list(self.store.users.keys()):
                    bank_service.process_interest(user_id)
                self.logger.debug("Bank interest processed")
            except Exception as e:
                self.logger.error(f"Bank interest error: {e}")
            await asyncio.sleep(3600)

    async def _auction_check_loop(self) -> None:
        while self.running:
            try:
                auction_service = AuctionService(self.store, EconomyService(self.store))
                now = datetime.now()
                for auction_id, auction in list(self.store.auctions.items()):
                    if auction.status == AuctionStatus.ACTIVE and auction.ends_at <= now:
                        auction_service.finalize_auction(auction_id)
                self.logger.debug("Auctions checked")
            except Exception as e:
                self.logger.error(f"Auction check error: {e}")
            await asyncio.sleep(60)

    async def _clan_war_check_loop(self) -> None:
        while self.running:
            try:
                now = datetime.now()
                for war_id, war in list(self.store.clan_wars.items()):
                    if war.status == ClanWarStatus.ACTIVE and war.ends_at <= now:
                        self.clan.finalize_war(war_id)
                self.logger.debug("Clan wars checked")
            except Exception as e:
                self.logger.error(f"Clan war check error: {e}")
            await asyncio.sleep(60)

    async def _world_event_loop(self) -> None:
        while self.running:
            try:
                now = datetime.now()

                for event_id, event in list(self.store.world_events.items()):
                    if event.active and event.ends_at and event.ends_at <= now:
                        event.active = False

                if random.random() < 0.1:
                    self._trigger_random_world_event()

                self.logger.debug("World events checked")
            except Exception as e:
                self.logger.error(f"World event error: {e}")
            await asyncio.sleep(300)

    def _trigger_random_world_event(self) -> None:
        event_config = random.choice(WORLD_EVENTS_POOL)
        event = WorldEvent(
            name=event_config["name"],
            description=event_config.get("description", ""),
            affect_stocks=event_config["affect_stocks"],
            affect_crypto=event_config["affect_crypto"],
            affect_business=event_config["affect_business"],
            stock_impact_percent=event_config["stock_impact"],
            crypto_impact_percent=event_config["crypto_impact"],
            business_impact_percent=event_config["business_impact"],
            duration_hours=event_config["duration_hours"],
            active=True,
            started_at=datetime.now(),
            ends_at=datetime.now() + timedelta(hours=event_config["duration_hours"]),
        )
        self.store.world_events[event.event_id] = event
        self.logger.info(f"World event triggered: {event.name}")

    async def _insurance_expiry_loop(self) -> None:
        while self.running:
            try:
                now = datetime.now()
                for insurance_id, insurance in list(self.store.insurances.items()):
                    if insurance.active and insurance.expires_at <= now:
                        insurance.active = False
                        user = self.store.get_user(insurance.user_id)
                        user.insurance_active = False
                        user.insurance_expires = None
                self.logger.debug("Insurance expiry checked")
            except Exception as e:
                self.logger.error(f"Insurance expiry error: {e}")
            await asyncio.sleep(3600)

    async def _loan_check_loop(self) -> None:
        while self.running:
            try:
                now = datetime.now()
                for user_id, user in list(self.store.users.items()):
                    if user.loan_amount > 0 and user.loan_due_date and user.loan_due_date <= now:
                        if user.balance >= user.loan_amount:
                            user.balance -= user.loan_amount
                            user.loan_amount = 0
                            user.loan_due_date = None
                        else:
                            user.loan_amount = int(user.loan_amount * 1.5)
                            user.loan_due_date = now + timedelta(days=7)
                self.logger.debug("Loans checked")
            except Exception as e:
                self.logger.error(f"Loan check error: {e}")
            await asyncio.sleep(3600)

    async def _jail_release_loop(self) -> None:
        while self.running:
            try:
                now = datetime.now()
                for user_id, user in list(self.store.users.items()):
                    if user.jailed_until and user.jailed_until <= now:
                        user.jailed_until = None
                self.logger.debug("Jail releases checked")
            except Exception as e:
                self.logger.error(f"Jail release error: {e}")
            await asyncio.sleep(60)

    async def _warn_expiry_loop(self) -> None:
        while self.running:
            try:
                now = datetime.now()
                for log in self.store.mod_logs:
                    if (log.action == ModActionType.WARN and log.is_active
                            and log.expires_at and log.expires_at <= now):
                        log.is_active = False
                self.logger.debug("Warn expiry checked")
            except Exception as e:
                self.logger.error(f"Warn expiry error: {e}")
            await asyncio.sleep(3600)

    async def _mute_expiry_loop(self) -> None:
        while self.running:
            try:
                now = datetime.now()
                for user_id, user in list(self.store.users.items()):
                    if user.muted_until and user.muted_until <= now:
                        user.muted_until = None
                for log in self.store.mod_logs:
                    if (log.action == ModActionType.MUTE and log.is_active
                            and log.expires_at and log.expires_at <= now):
                        log.is_active = False
                self.logger.debug("Mute expiry checked")
            except Exception as e:
                self.logger.error(f"Mute expiry error: {e}")
            await asyncio.sleep(60)

    async def _pet_status_loop(self) -> None:
        while self.running:
            try:
                now = datetime.now()
                for pet_id, pet in list(self.store.pets.items()):
                    hours_since_fed = (now - pet.last_fed).total_seconds() / 3600
                    if hours_since_fed > 24:
                        pet.hunger = min(100, pet.hunger + 10)
                        pet.health = max(0, pet.health - 2)
                        if pet.hunger > 50:
                            pet.mood = PetMood.HUNGRY
                        if pet.health < 20:
                            pet.mood = PetMood.SICK

                    hours_since_played = (now - pet.last_played).total_seconds() / 3600
                    if hours_since_played > 48:
                        pet.mood = PetMood.SAD

                self.logger.debug("Pet statuses updated")
            except Exception as e:
                self.logger.error(f"Pet status error: {e}")
            await asyncio.sleep(1800)

    async def _data_save_loop(self) -> None:
        while self.running:
            try:
                self.store.save_to_disk("data/state.json")
                self.logger.debug("Data saved to disk")
            except Exception as e:
                self.logger.error(f"Data save error: {e}")
            await asyncio.sleep(300)


print("Интеграции + внешние вызовы загружены успешно.")
print(f"BaseAPIClient: CRUD методы")
print(f"TelegramBotClient: 40+ методов")
print(f"DeepSeekClient: 6 методов")
print(f"GrokClient: 5 методов")
print(f"ImageGenerationClient: 4 метода")
print(f"BroadcastService: 4 метода")
print(f"NotificationService: 10 методов")
print(f"TaskScheduler: 15 циклов")
