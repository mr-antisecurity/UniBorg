import html
from uniborg.util import admin_cmd
import sql_helpers.warns_sql as sql


@borg.on(admin_cmd(pattern="warn (.*)")) # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    warn_reason = event.pattern_match.group(1)
    reply_message = await event.get_reply_message()
    limit, soft_warn = sql.get_warn_setting(event.chat_id)
    num_warns, _ = sql.warn_user(reply_message.from_id, event.chat_id, warn_reason)
    if num_warns >= limit:
        sql.reset_warns(reply_message.from_id, event.chat_id)
        if soft_warn:
            logger.info("TODO: kick user")
            reply = "{} warnings, <u><a href='tg://user?id={}'>user</a></u> has been kicked!".format(limit, reply_message.from_id)
        else:
            logger.info("TODO: ban user")
            reply = "{} warnings, <u><a href='tg://user?id={}'>user</a></u> has been banned!".format(limit, reply_message.from_id)
    else:
        reply = "<u><a href='tg://user?id={}'>user</a></u> has {}/{} warnings... watch out!".format(reply_message.from_id, num_warns, limit)
        if warn_reason:
            reply += "\nReason for last warn:\n{}".format(html.escape(warn_reason))
    #
    await event.edit(reply, parse_mode="html")


@borg.on(admin_cmd(pattern="get_warns")) # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    reply_message = await event.get_reply_message()
    result = sql.get_warns(reply_message.from_id, event.chat_id)
    if result and result[0] != 0:
        num_warns, reasons = result
        limit, _ = sql.get_warn_setting(event.chat_id)
        if reasons:
            text = "This user has {}/{} warnings, for the following reasons:".format(num_warns, limit)
            text += "\r\n"
            text += reasons
            await event.edit(text)
        else:
            await event.edit("this user has {} / {} warning, but no reasons for any of them.".format(num_warns, limit))
    else:
        await event.edit("this user hasn't got any warnings!")


@borg.on(admin_cmd(pattern="reset_warns")) # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    reply_message = await event.get_reply_message()
    sql.reset_warns(reply_message.from_id, event.chat_id)
    await event.edit("Warnings have been reset!")


