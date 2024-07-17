import utils

def main():
    utils.init_colors()
    utils.clear()
    utils.print_logo()
    if not utils.app_is_admin():
        utils.log(utils.get_translate('needAdmin'))
        return utils.exit()
    steam_path = utils.get_steam_path()
    if steam_path == '':
        steam_path = 'C:/Program Files (x86)/Steam'
    utils.log(utils.get_translate('steamDetected') + steam_path)
    utils.log(utils.get_translate('steamKill'))
    utils.kill_steam()
    utils.log(utils.get_translate('steamKillSuccess'))
    utils.log('')
    utils.log(utils.get_translate('sure'))
    input('    ' + utils.get_translate('enter') + ' ')
    t = utils.run_script(steam_path)
    utils.log('')
    utils.log(utils.get_translate('success') + f''' ({t}s)''')
    utils.log('')
    ans = input('    ' + utils.get_translate('restart'))
    if 'yes' in ans.lower():
        utils.restart()
    return utils.exit()

if __name__ == '__main__':
    main()