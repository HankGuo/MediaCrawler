# 声明：本代码仅供学习和研究目的使用。使用者应遵守以下原则：
# 1. 不得用于任何商业用途。
# 2. 使用时应遵守目标平台的使用条款和robots.txt规则。
# 3. 不得进行大规模爬取或对平台造成运营干扰。
# 4. 应合理控制请求频率，避免给目标平台带来不必要的负担。
# 5. 不得用于任何非法或不当的用途。
#
# 详细许可条款请参阅项目根目录下的LICENSE文件。
# 使用本代码即表示您同意遵守上述原则和LICENSE中的所有条款。


# 基础配置
PLATFORM = "xhs"
KEYWORDS = "转运水晶"  # 关键词搜索配置，以英文逗号分隔
LOGIN_TYPE = "cookie"  # qrcode or phone or cookie
COOKIES = "abRequestId=f57ce515-02b3-51b1-91ce-e042fc16f3d1;a1=18e40ced23b382ti6daos4aoq9n5ugffzwxofjcge30000811176;webId=34393c2af6d1ce6e0174f3372cc71b81;gid=yYd48SdfWSuqyYd48SdfJEVSqDqYJ93Kf0lMCkd40lAjIlq827kiii888YyyyWK8WJ420J42;customerClientId=243236499342074;x-user-id-ark.xiaohongshu.com=6518e6b9000000002402e5db;x-user-id-creator.xiaohongshu.com=60056ad4000000000100b578;access-token-creator.xiaohongshu.com=customer.creator.AT-68c517469998758676156666wzoz3qp4jbt9j8vg;galaxy_creator_session_id=EyihCtuXOmrCkxpBGm0j7HgsYvzmPcajPjMK;galaxy.creator.beaker.session.id=1739244619516054800620;xsecappid=xhs-pc-web;webBuild=4.58.0;acw_tc=0a00d49217406475629751877e208786fef95c0c384140008ccbcf6195d508;web_session=040069b171299c56e52ecc64f5354bff9931c9;unread={%22ub%22:%2267bc7124000000000603a275%22%2C%22ue%22:%2267bfca670000000029027b53%22%2C%22uc%22:28};websectiga=10f9a40ba454a07755a08f27ef8194c53637eba4551cf9751c009d9afb564467;sec_poison_id=dc57f9f9-07fd-4074-a332-796260cad5ce;loadts=1740648379193"
# 具体值参见media_platform.xxx.field下的枚举值，暂时只支持小红书
SORT_TYPE = "popularity_descending"
CRAWLER_TYPE = (
    "detail"  # 爬取类型，search(关键词搜索) | detail(帖子详情)| creator(创作者主页数据)
)
# 自定义User Agent（暂时仅对XHS有效）
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/131.0.0.0'

# 是否开启 IP 代理
ENABLE_IP_PROXY = True

# 未启用代理时的最大爬取间隔，单位秒（暂时仅对XHS有效）
CRAWLER_MAX_SLEEP_SEC = 2

# 代理IP池数量
IP_PROXY_POOL_COUNT = 2

# 代理IP提供商名称
IP_PROXY_PROVIDER_NAME = "kuaidaili"

# 设置为True不会打开浏览器（无头浏览器）
# 设置False会打开一个浏览器
# 小红书如果一直扫码登录不通过，打开浏览器手动过一下滑动验证码
# 抖音如果一直提示失败，打开浏览器看下是否扫码登录之后出现了手机号验证，如果出现了手动过一下再试。
HEADLESS = True

# 是否保存登录状态
SAVE_LOGIN_STATE = True

# 数据保存类型选项配置,支持三种类型：csv、db、json, 最好保存到DB，有排重的功能。
SAVE_DATA_OPTION = "db"  # csv or db or json

# 用户浏览器缓存的浏览器文件配置
USER_DATA_DIR = "%s_user_data_dir"  # %s will be replaced by platform name

# 爬取开始页数 默认从第一页开始
START_PAGE = 1

# 爬取视频/帖子的数量控制
CRAWLER_MAX_NOTES_COUNT = 1

# 并发爬虫数量控制
MAX_CONCURRENCY_NUM = 1

# 是否开启爬图片模式, 默认不开启爬图片
ENABLE_GET_IMAGES = False

# 是否开启爬评论模式, 默认开启爬评论
ENABLE_GET_COMMENTS = True

# 爬取一级评论的数量控制(单视频/帖子)
CRAWLER_MAX_COMMENTS_COUNT_SINGLENOTES = 600

# 是否开启爬二级评论模式, 默认不开启爬二级评论
# 老版本项目使用了 db, 则需参考 schema/tables.sql line 287 增加表字段
ENABLE_GET_SUB_COMMENTS = False

# 指定小红书需要爬虫的笔记URL列表, 目前要携带xsec_token和xsec_source参数
XHS_SPECIFIED_NOTE_URL_LIST = [
    "https://www.xiaohongshu.com/explore/6739e243000000001a037043?xsec_token=AB0OlIe8q16hcEqI21bhLaI10VnHMQsYJkb33DYJntzLI=&xsec_source=pc_search&source=web_search_result_notes"
]

# 指定小红书创作者ID列表
XHS_CREATOR_ID_LIST = [
    "63e36c9a000000002703502b",
    # ........................
]

# 词云相关
# 是否开启生成评论词云图
ENABLE_GET_WORDCLOUD = True
# 自定义词语及其分组
# 添加规则：xx:yy 其中xx为自定义添加的词组，yy为将xx该词组分到的组名。
CUSTOM_WORDS = {
    "零几": "年份",  # 将“零几”识别为一个整体
    "高频词": "专业术语",  # 示例自定义词
}

# 停用(禁用)词文件路径
STOP_WORDS_FILE = "./docs/hit_stopwords.txt"

# 中文字体文件路径
FONT_PATH = "./docs/STZHONGS.TTF"