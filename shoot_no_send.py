import time
import re

'''
变量区
可自行调节
'''
restart_permission_level = 4  # 重启所需权限等级
restart_delay = 15  # 重启延迟时间
default_restart_time = 0  # 重启时间

'''
功能区
最好不要乱改
'''

help_msg = r'''awa
ShootKing是大佬
awa
--------------------------------
§b!!shoot help §r- §c显示此帮助信息
§b!!restart [时间] §r- §c定时重启服务器(默认{}秒后关闭服务器,关闭{}秒后重启)
§b聊天中可以使用&代替某个无法正常输入的字符发送彩色字符,使用\&发送&
§b!!shoot setperm <玩家> <等级> §r- §c设置权限等级(需要权限等级4)
--------------------------------'''.format(restart_delay, default_restart_time)


def shoot(server, info):
    if info.content == '!!shoot':
        server.tell(info.player, 'Hello,' + info.player)


def help(server, info):
    if info.content == '!!shoot help':
        for i in help_msg.splitlines():
            server.tell(info.player, i)


def amdyes(server, info):
    if re.search(r'(amd yes+)(!*)(！*)', info.content, re.IGNORECASE) != re.search('a', 'b'):
        for i in range(5):
            server.tell(info.player, '§{}AMD YES!'.format(i + 1))
            time.sleep(1)


def colofultalk(server, info):
    if '&' in info.content and not info.content.startswith('!!') and not info.content.startswith('=='):
        replaced = info.content.replace('&', '§').replace(r'\§', '&')
        server.say(replaced)


def restart(server, info):
    if info.content.startswith('!!restart') and server.get_permission_level(info) >= restart_permission_level:
        args = info.content.split(' ')
        if len(args) == 1:
            server.say('§4服务器即将在{}秒后重启,关闭{}秒后重新启动'.format(
                restart_delay, default_restart_time))
            time.sleep(restart_delay)
            server.stop()
            server.wait_for_start()
            time.sleep(default_restart_time)
            server.start()
        if len(args) == 2:
            try:
                restart_time = int(args[1])
                server.say('§4服务器即将在{}秒后重启,关闭{}秒后重新启动'.format(
                    restart_delay, restart_time))
                time.sleep(restart_delay)
                server.stop()
                server.wait_for_start()
                time.sleep(restart_time)
                server.start()
            except ValueError:
                server.tell(info.player, '§4请输入一个数字！')


def setPermissionLevel(server, info):
    if info.content.startswith('!!shoot setperm') and server.get_permission_level(info) >= 4:
        args = info.content.split(' ')
        if len(args) == 4:
            try:
                server.set_permission_level(args[2], args[3])
                server.say('§e现在§4' + args[2] + '§e的权限等级为§4' + args[3])
            except TypeError:
                server.tell(info.player, '§4输入有误!')


def on_info(server, info):
    restart(server, info)
    setPermissionLevel(server, info)
    if info.is_player == 1:
        shoot(server, info)
        help(server, info)
        amdyes(server, info)
        colofultalk(server, info)


def on_player_made_advancement(server, player, advancement):
    server.say('§d恭喜§4' + player + '§d获得进度：§2§l"' + advancement + '"')


def on_load(server, old_module):
    server.add_help_message('!!shoot help', 'Shoot牌帮助!')
