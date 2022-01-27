'''
需要实现的功能：
clone 搞定
add 搞定
submit(commit) 搞定
push
branch
remove 搞定
log 搞定
'''
import time # 用于获取本地时间
import os # 用于获取文件路径和创建文件夹
import shutil # 用于复制粘贴文件
import json # 用于解析JSON
import sys # 用于接收命令行参数
import stat # 用于删除只读文件

# 获取当前时间
def get_time (format = '%Y-%m-%d %H:%M:%S'):
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    return dt

# 自定义输出
def log (*args, **kwargs):
    dt = get_time('%Y/%m/%d %H:%M:%S')
    print (dt, *args, **kwargs )

# 设置cmd中的颜色
def set_color ():
    import ctypes
    # 标准输出的句柄
    STD_OUTPUT_HANDLE = -11
    # 获取句柄
    std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    # 设置颜色
    def set_cmd_text_color(color, handle=std_out_handle):
        Bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
        return Bool
    return set_cmd_text_color

# 输出错误信息
def error (mess, isLog=True):
    # Windows CMD命令行 字体颜色定义 text colors
    FOREGROUND_BLUE = 0x09 # blue.
    FOREGROUND_GREEN = 0x0a # green.
    FOREGROUND_RED = 0x0c # red.
    set_cmd_text_color = set_color ()
    set_cmd_text_color(FOREGROUND_RED)
    #   sys.stdout.write(mess + '\n')
    if isLog:
        log (mess)
    else:
        print (mess)
    # 重置回白色
    set_cmd_text_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)

# 输出警告信息
def warning (mess, isLog=True):
    # Windows CMD命令行 字体颜色定义 text colors
    FOREGROUND_BLUE = 0x09 # blue.
    FOREGROUND_GREEN = 0x0a # green.
    FOREGROUND_RED = 0x0c # red.
    set_cmd_text_color = set_color ()
    set_cmd_text_color(FOREGROUND_RED | FOREGROUND_GREEN)
    #   sys.stdout.write(mess + '\n')
    if isLog:
        log (mess)
    else:
        print (mess)
    # 重置回白色
    set_cmd_text_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)

# 输出警告信息
def success (mess, isLog=True):
    # Windows CMD命令行 字体颜色定义 text colors
    FOREGROUND_BLUE = 0x09 # blue.
    FOREGROUND_GREEN = 0x0a # green.
    FOREGROUND_RED = 0x0c # red.
    set_cmd_text_color = set_color ()
    set_cmd_text_color( FOREGROUND_GREEN)
    #   sys.stdout.write(mess + '\n')
    if isLog:
        log (mess)
    else:
        print (mess)
    # 重置回白色
    set_cmd_text_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)

# 忽略文件
def ignore_file (ignoreRule):
    ignoreList = []
    for ir in ignoreRule:
        ignoreName = ir
        if ir.find('*.') != -1:
            ignoreName = ir.split('*.')[-1]
            log (f'在此文件夹中，需忽略后缀名{ignoreName}')
        elif ir.find('/') != -1:
            ignoreName = ir.split('/')[0]
            log (f'在此文件夹中，需忽略文件夹{ignoreName}')
        elif ir != '':
            log (f'在此文件夹中，需忽略文件{ignoreName}')
        ignoreList.append(ignoreName)
    return ignoreList

# 判断是否要被忽略
def is_ignore (fileName, ignoreList):
    yes_or_no = False
    for ignoreName in ignoreList:
        log (f'判断{fileName}与{ignoreName}')
        # 根据文件名判断
        if ignoreName.find('.') != -1:
            if fileName == ignoreName:
                log (f'{fileName}被忽略')
                yes_or_no = True
                break
        else:
            # 根据后缀名判断
            if fileName.find('.' + ignoreName) != -1:
                log (f'{fileName}被忽略')
                yes_or_no = True
                break
            # 文件夹情况
            elif fileName == ignoreName:
                log (f'{fileName}被忽略')
                yes_or_no = True
                break
    return yes_or_no

# 复制文件：根据忽略规则，把a文件夹中的所有文件复制到b文件夹中
def copy_file (fromPath, toPath, ignoreRule=[]):
    ignoreList = ignore_file(ignoreRule)
    # 获取fromPath下的文件列表并遍历fileName
    pathDir = os.listdir(fromPath)
    for fileName in pathDir:
        if is_ignore(fileName, ignoreList):
            continue
        # .a既可能是文件也可能是文件夹，艹，故不能用if fileName.find('.') != -1
        # 处理文件
        if os.path.isfile(fromPath +'/'+ fileName):
            formFile = os.path.join(fromPath, fileName)
            # 若不存在，则创建目录
            if not os.path.isdir(toPath):
                os.makedirs(toPath)
                success (f'成功创建{toPath}')
            # shutil的copy()是复制到一个新的地方，创建时间、修改时间、访问时间都是新的
            # copy2()则是会创建时间、修改时间、访问时间这些也复制过去
            # 注意：无法拷贝文件元数据，如隐藏文件被复制后就不再是隐藏的了（但只读不会）
            shutil.copy(formFile, toPath)
            success (f'成功复制{formFile}粘贴到{toPath}')
        # 处理文件夹
        else:
            log (f'{fileName}是一个文件夹')
            formFile = os.path.join(fromPath, fileName)
            # 这里要加fileName，否则会放到同一个文件夹下
            # 注意：空文件夹不会复制
            copy_file (formFile, toPath + '/' + fileName, ignoreRule)
            pass

# 版本管理
def zh_git (type, fromPath, projectName, version, ignore=[]):
    # 更新时间（默认为当前时间）
    date = get_time('%Y-%m-%d-%H-%M-%S')
    # 本地存档
    publicPath = 'D:/zzh/versionManage/'
    if type == 'submit':
        toPath = publicPath + projectName + '/' + version + '_' + date
        if os.path.exists(toPath):
            error (f'{toPath}已存在')
        else:
            addPath = publicPath + projectName + '/stage'
            if not os.path.exists(addPath):
                error (f'{addPath}不存在，请先把本地代码提交至stage')
            else:
                copy_file(addPath, toPath, ignore)
                # 这个删除是不走回收站的
                shutil.rmtree(addPath)
                # 更新提交记录
                logPath = publicPath + projectName + '/log.json'
                # 存在则读取，反之则创建
                if os.path.exists(logPath):
                    logList = json.loads(read_file(logPath))
                else:
                    logList = []
                print ('请输入本次提交的说明：', end='')
                msg = input()
                logList.append({
                    'version': version,
                    'date': date,
                    'message': msg
                })
                logStr = json.dumps(logList)
                write_file(logPath, logStr)
    elif type == 'add':
        if publicPath in fromPath:
            error ('您的命令有误，该操作会把{fromPath}复制到{frompublicPathPath}\n如果是想要拉取，请在命令末尾加上clone')
            return
        toPath = publicPath + projectName + '/stage'
        # 若存在，则删除
        if os.path.exists(toPath):
            # shutil.rmtree(toPath)是不能删除只读文件的
            def readonly_handler(func, toPath, execinfo):
                os.chmod(toPath, stat.S_IWRITE)
                func(toPath)
            shutil.rmtree(toPath, onerror=readonly_handler)
        copy_file(fromPath, toPath, ignore)
    elif type == 'clone':
        projectName = fromPath.split('/')[-2]
        # 执行.py的本地路径
        # os.path.abspath(__file__)不准确，打包后调用，会变成C:\Users\ADMINI~1\AppData\Local\Temp\_MEI90962\git.py
        localPath = os.getcwd()
        toPath = localPath
        if "git.py" in toPath:
            toPath = toPath.replace("git.py", projectName, 1)
        else:
            toPath = toPath + '\\' + projectName
        # 若存在，则删除
        if os.path.exists(toPath):
            shutil.rmtree(toPath)
        copy_file(fromPath, toPath, ignore)
    elif type == 'remove':
        toPath = publicPath + projectName
        warning (f'该操作会删除{toPath}整个文件夹，是否继续（Y/N，默认为N）')
        answer = input()
        if str.upper(answer) == 'Y':
            # 若存在，则删除
            if os.path.exists(toPath):
                shutil.rmtree(toPath)
                success (f'成功删除{toPath}')
            else:
                log (f'不存在{toPath}，无需删除')
        else:
            log ('取消操作')
    elif type == 'log':
        toPath = publicPath + projectName + '/log.json'
        if os.path.exists(toPath):
            # log (os.listdir(publicPath + projectName))
            logList = json.loads(read_file(toPath))
            print ('version\t  date\t\t\t message')
            for o in logList:
                print (f'{o["version"]}\t  {o["date"]}\t {o["message"]}')
        else:
            error (f'{toPath}不存在')
        
# 写入文件
def write_file (filePath, text):
    # 以utf-8的编码写入文件
    with open(filePath, 'w', encoding='utf-8') as f:
            f.write(text)
            log (f'成功往{filePath}里写入{text}')

# 读取文件
def read_file (filePath):
    try:
        # 以二进制的方式读取（为了应对图片）
        with open(filePath, 'r') as f:
            log (f'打开{filePath}')
            content = f.read()
    except:
        warning (f'错误：找不到{filePath}')
        content = -1
    finally:
        return content

# 获取配置：读取项目文件夹中的zhconfig.json，若不存在会自动创建
def read_config (type, fromPath):
    def get_projectName (fromPath):
        projectName = fromPath
        if fromPath.find('/') != -1:
            projectName = fromPath.split('/')[-1]
        if fromPath.find('\\') != -1:
            projectName = fromPath.split('\\')[-1]
        return projectName
    
    # 读取配置文件
    def get_config (configPath):
        configStr = read_file(configPath)
        configJson = {}
        # 防止configStr为空
        try:
            configJson = json.loads(configStr)
        except:
            warning (f'{configStr}不能被解析成JSON')
        return configJson

    # 版本号（默认为V1.0.0）
    def get_version (configJson):
        version = 'V1.0.0'
        if ('version' in configJson):
            version = configJson['version']
        else: 
            warning ('zhconfig.json中没有version')
        return version
    
    # 忽略规则，如a.txt *.ini dir
    def get_ignore (configJson):
        ignore = []
        if ('ignore' in configJson):
            ignore = configJson['ignore']
        else: 
            warning ('zhconfig.json中没有ignore')
        return ignore
    
    projectName = get_projectName(fromPath)
    if type == 'log':
        # 生成配置
        config = dict(
            # 待复制的文件夹名称
            fromPath = fromPath,
            # 待粘贴的文件夹名称
            projectName = projectName,
            version = '',
            # 待忽略的文件列表
            ignore = []
        )
        return config
    else:
        configPath = fromPath + '/zhconfig.json'
        configJson = get_config(configPath)
        version = get_version(configJson)
        ignore = get_ignore (configJson)
        # 生成配置
        config = dict(
            # 待复制的文件夹名称
            fromPath = fromPath,
            # 待粘贴的文件夹名称
            projectName = projectName,
            version = version,
            # 待忽略的文件列表
            ignore = ignore
        )
        # 更新配置文件
        if (not 'ignore' in configJson or not 'version' in configJson):
            configJson['version'] = version
            configJson['ignore'] = ignore
            newConfig = json.dumps(configJson)
            write_file (configPath, newConfig)
        # 返回
        return config

# 接收参数：获取"python git.py project -r"中的project项目名和-r命令类型
def receive_Param (args):
    # 项目名
    target = ''
    try:
        target = args[0][1]
    except:
        error ('错误：target为空')
    # 判断命令的类型
    type = 'add'
    if len(args[0]) > 2:
        param = str.lower(args[0][2])
        if param == 'submit' or param == '-s' :
            type = 'submit'
        elif param == 'clone' or param == '-c':
            type = 'clone'
        elif param == 'remove' or param == '-r':
            type = 'remove'
        elif param == 'log' or param == '-l':
            type = 'log'
        elif param == 'help' or param == '-h':
            type = 'help'
    # 帮助手册
    help = str.lower(target)
    if help == 'help' or help == '-h' or type == 'help':
        print ('------------------------------------------------------------')
        print ('命令 \t\t 含义\n')
        print ('空/-a/add \t 把目标文件夹复制到库中的stage缓存文件夹中（需读取zhconfig.json，不存在会自动创建）')
        print ('-s/sumbit \t 把库中的stage缓存文件夹移动到形如V1.0.0_2022-1-22-13-24-56的自动命名文件夹中')
        print ('-l/log \t\t 打印sumbit的记录（包含版本号、时间和提交说明）')
        print ('-r/remove \t 删除某个库（本地需存在同名文件夹，否则不需删除）')
        print ('-h/help \t 查看帮助手册\n')
        print ('格式: zh 项目文件夹所在路径 命令类型')
        print ('注: -h不需要项目文件夹所在路径\n')
        print ('例如: 在project所在是文件夹下打开cmd（命令行）')
        print ('输入命令(暂存)：zh project')
        print ('输入命令(提交)：zh project -s')
        print ('输入命令(记录)：zh project -l')
        print ('输入命令(拉取)：zh project/V1.0.0_2022-1-22-13-24-56 -c')
        print ('输入命令(删库)：zh project -r\n')
        success ('绿色提示：成功进行文件操作，如复制、删除等', False)
        warning ('黄色提示：程序出错，但不影响运行', False)
        error ('红色提示：程序出错，不能运行', False)
        print ('白色提示：剩下的统统都是白色提示')
        print ('------------------------------------------------------------')
        sys.exit()
    if type == 'clone':
        # 补全路径
        publicPath = 'D:/zzh/versionManage/'
        if not publicPath in target:
            target = publicPath + target
    if type == 'log':
        pass
    else:
        if not os.path.exists(target):
            if type == 'remove':
                error (f'当前路径下不存在{target}，故不允许删除库（否则无法恢复）')
            else:
                error (f'找不到{target}文件夹，本次上传失败')
            # 打包后exit()用不了，只能用sys.exit()
            sys.exit()
    return (target, type)

# 主函数入口：接收参数后读取配置并进行版本管理
def main (*args):
    # 执行.py的本地路径
    localPath = os.getcwd()
    print (localPath, args)
    # 接收命令行参数
    options = receive_Param (args)
    target = options[0]
    type = options[1]
    # 读取配置文件（只要填项目文件夹）
    config = read_config(type, target)
    log (f'配置项{config}')
    # 上传版本
    zh_git(type, **config)

# 只有在被直接执行时才启动（被import时不调用）
if __name__ == '__main__':
    main (sys.argv)
