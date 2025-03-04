# 声明：本代码仅供学习和研究目的使用。使用者应遵守以下原则：  
# 1. 不得用于任何商业用途。  
# 2. 使用时应遵守目标平台的使用条款和robots.txt规则。  
# 3. 不得进行大规模爬取或对平台造成运营干扰。  
# 4. 应合理控制请求频率，避免给目标平台带来不必要的负担。   
# 5. 不得用于任何非法或不当的用途。
#   
# 详细许可条款请参阅项目根目录下的LICENSE文件。  
# 使用本代码即表示您同意遵守上述原则和LICENSE中的所有条款。  


import asyncio
from typing import Optional

from playwright.async_api import BrowserContext, Page

import config
from base.base_crawler import AbstractLogin
from tools import utils


class XiaoHongShuLogin(AbstractLogin):

    def __init__(self,
                 browser_context: BrowserContext,
                 context_page: Page,
                 cookie_str: str = ""
                 ):
        self.browser_context = browser_context
        self.context_page = context_page
        self.cookie_str = cookie_str

    async def begin(self):
        """Start login xiaohongshu"""
        utils.logger.info("[XiaoHongShuLogin.begin] Begin login xiaohongshu ...")
        await self.login_by_cookies()

    async def login_by_cookies(self):
        """login xiaohongshu website by cookies"""
        utils.logger.info("[XiaoHongShuLogin.login_by_cookies] Begin login xiaohongshu by cookie ...")
        for key, value in utils.convert_str_cookie_to_dict(self.cookie_str).items():
            if key != "web_session":  # only set web_session cookie attr
                continue
            await self.browser_context.add_cookies([{
                'name': key,
                'value': value,
                'domain': ".xiaohongshu.com",
                'path': "/"
            }])
