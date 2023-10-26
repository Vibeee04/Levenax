from typing import Dict, List, Union

from RiruruMusic.core.mongo import mongodb


userdb = mongodb.userstats
chattopdb = mongodb.chatstats
authuserdb = mongodb.authuser
gbansdb = mongodb.gban
chatsdb = mongodb.chats
blacklist_chatdb = mongodb.blacklistChat
usersdb = mongodb.tgusersdb
playlistdb = mongodb.playlist
blockeddb = mongodb.blockedusers
othersdb = mongodb.others


# Playlist


async def _get_playlists(chat_id: int) -> Dict[str, int]:
    _notes = await playlistdb.find_one({"chat_id": chat_id})
    if _notes:
        return _notes["notes"]
    return {}


async def get_playlist_names(chat_id: int) -> List[str]:
    _notes = []
    for note in await _get_playlists(chat_id):
        _notes.append(note)
    return _notes


async def get_playlist(chat_id: int, name: str) -> Union[bool, dict]:
    _notes = await _get_playlists(chat_id)
    if name in _notes:
        return _notes[name]
    else:
        return False


async def save_playlist(chat_id: int, name: str, note: dict):
    _notes = await _get_playlists(chat_id)
    _notes[name] = note
    await playlistdb.update_one({"chat_id": chat_id}, {"$set": {"notes": _notes}}, upsert=True)


async def delete_playlist(chat_id: int, name: str) -> bool:
    notesd = await _get_playlists(chat_id)
    if name in notesd:
        del notesd[name]
        await playlistdb.update_one({"chat_id": chat_id}, {"$set": {"notes": notesd}}, upsert=True)
        return True
    return False


# Users


async def get_served_users() -> list:
    users_list = []
    async for user in usersdb.find({"_id": {"$gt": 0}}):
        users_list.append(user)
    return users_list


async def add_served_user(user_id: int):
    is_served = await usersdb.find_one({"_id": user_id})
    if is_served:
        return
    return await usersdb.insert_one({"_id": user_id})


# Served Chats


async def get_served_chats() -> list:
    chats_list = []
    async for chat in chatsdb.find({"chat_id": {"$lt": 0}}):
        chats_list.append(chat)
    return chats_list


async def is_served_chat(chat_id: int) -> bool:
    chat = await chatsdb.find_one({"chat_id": chat_id})
    if chat:
        return True
    return False


async def add_served_chat(chat_id: int):
    is_served = await is_served_chat(chat_id)
    if is_served:
        return
    return await chatsdb.insert_one({"chat_id": chat_id})


# Blacklisted Chats


async def blacklisted_chats() -> list:
    chats_list = []
    async for chat in blacklist_chatdb.find({"chat_id": {"$lt": 0}}):
        chats_list.append(chat["chat_id"])
    return chats_list


async def blacklist_chat(chat_id: int) -> bool:
    if not await blacklist_chatdb.find_one({"chat_id": chat_id}):
        await blacklist_chatdb.insert_one({"chat_id": chat_id})
        return True
    return False


async def whitelist_chat(chat_id: int) -> bool:
    if await blacklist_chatdb.find_one({"chat_id": chat_id}):
        await blacklist_chatdb.delete_one({"chat_id": chat_id})
        return True
    return False


# Auth Users DB


async def _get_authusers(chat_id: int) -> Dict[str, int]:
    _notes = await authuserdb.find_one({"chat_id": chat_id})
    if _notes:
        return _notes["notes"]
    return {}


async def get_authuser_names(chat_id: int) -> List[str]:
    _notes = []
    for note in await _get_authusers(chat_id):
        _notes.append(note)
    return _notes


async def get_authuser(chat_id: int, name: str) -> Union[bool, dict]:
    _notes = await _get_authusers(chat_id)
    if name in _notes:
        return _notes[name]
    else:
        return False


async def save_authuser(chat_id: int, name: str, note: dict):
    _notes = await _get_authusers(chat_id)
    _notes[name] = note
    await authuserdb.update_one({"chat_id": chat_id}, {"$set": {"notes": _notes}}, upsert=True)


async def delete_authuser(chat_id: int, name: str) -> bool:
    notesd = await _get_authusers(chat_id)
    if name in notesd:
        del notesd[name]
        await authuserdb.update_one({"chat_id": chat_id}, {"$set": {"notes": notesd}}, upsert=True)
        return True
    return False


# Sudoers

async def get_sudoers() -> list:
    sudoers = await othersdb.find_one({"_id": "sudo"})
    if sudoers:
        return sudoers["sudoers"]
    return []

async def add_sudo(user_id: int) -> bool:
    sudoers = await get_sudoers()
    sudoers.append(user_id)
    await othersdb.update_one({"_id": "sudo"}, {"$set": {"sudoers": sudoers}}, upsert=True)
    return True


async def remove_sudo(user_id: int) -> bool:
    sudoers = await get_sudoers()
    sudoers.remove(user_id)
    await othersdb.update_one({"_id": "sudo"}, {"$set": {"sudoers": sudoers}}, upsert=True)
    return True


# Total Queries on bot


async def get_queries() -> int:
    mode = await othersdb.find_one({"_id": "queries"})
    if mode:
        return mode["mode"]
    return 0


async def set_queries(mode: int):
    queries = await othersdb.find_one({"_id": "queries"})
    if queries:
        mode = queries["mode"] + mode
    return await othersdb.update_one({"_id": "queries"}, {"$set": {"mode": mode}}, upsert=True)


# Top Chats DB


async def get_top_chats() -> dict:
    results = {}
    async for chat in chattopdb.find({"chat_id": {"$lt": 0}}):
        chat_id = chat["chat_id"]
        total = 0
        for i in chat["vidid"]:
            counts_ = chat["vidid"][i]["spot"]
            if counts_ > 0:
                total += counts_
                results[chat_id] = total
    return results


async def get_global_tops() -> dict:
    results = {}
    async for chat in chattopdb.find({"chat_id": {"$lt": 0}}):
        for i in chat["vidid"]:
            counts_ = chat["vidid"][i]["spot"]
            title_ = chat["vidid"][i]["title"]
            if counts_ > 0:
                if i not in results:
                    results[i] = {}
                    results[i]["spot"] = counts_
                    results[i]["title"] = title_
                else:
                    spot = results[i]["spot"]
                    count_ = spot + counts_
                    results[i]["spot"] = count_
    return results


async def get_particulars(chat_id: int) -> Dict[str, int]:
    ids = await chattopdb.find_one({"chat_id": chat_id})
    if ids:
        return ids["vidid"]
    return {}


async def get_particular_top(chat_id: int, name: str) -> Union[bool, dict]:
    ids = await get_particulars(chat_id)
    if name in ids:
        return ids[name]


async def update_particular_top(chat_id: int, name: str, vidid: dict):
    ids = await get_particulars(chat_id)
    ids[name] = vidid
    await chattopdb.update_one({"chat_id": chat_id}, {"$set": {"vidid": ids}}, upsert=True)


# Top User DB


async def get_userss(chat_id: int) -> Dict[str, int]:
    ids = await userdb.find_one({"chat_id": chat_id})
    if ids:
        return ids["vidid"]
    return {}


async def get_user_top(chat_id: int, name: str) -> Union[bool, dict]:
    ids = await get_userss(chat_id)
    if name in ids:
        return ids[name]


async def update_user_top(chat_id: int, name: str, vidid: dict):
    ids = await get_userss(chat_id)
    ids[name] = vidid
    await userdb.update_one({"chat_id": chat_id}, {"$set": {"vidid": ids}}, upsert=True)


async def get_topp_users() -> dict:
    results = {}
    async for chat in userdb.find({"chat_id": {"$gt": 0}}):
        user_id = chat["chat_id"]
        total = 0
        for i in chat["vidid"]:
            counts_ = chat["vidid"][i]["spot"]
            if counts_ > 0:
                total += counts_
        results[user_id] = total
    return results


# Blocked Users

async def get_banned_users() -> list:
    results = []
    async for user in blockeddb.find({}):
        results.append(user["_id"])
    return results


async def add_banned_user(user_id: int):
    user = await blockeddb.find_one({"_id": user_id})
    if user:
        return
    return await blockeddb.insert_one({"_id": user_id})


async def remove_banned_user(user_id: int):
    user = await blockeddb.find_one({"_id": user_id})
    if user:
        return await blockeddb.delete_one({"_id": user_id})
    return
