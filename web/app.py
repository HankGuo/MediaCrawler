# 声明：本代码仅供学习和研究目的使用。使用者应遵守以下原则：  
# 1. 不得用于任何商业用途。  
# 2. 使用时应遵守目标平台的使用条款和robots.txt规则。  
# 3. 不得进行大规模爬取或对平台造成运营干扰。  
# 4. 应合理控制请求频率，避免给目标平台带来不必要的负担。   
# 5. 不得用于任何非法或不当的用途.
#   
# 详细许可条款请参阅项目根目录下的LICENSE文件。  
# 使用本代码即表示您同意遵守上述原则和LICENSE中的所有条款。  

import os
import sys
import logging
import uuid
import datetime
from typing import Dict, Any

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
import db
from base.base_crawler import AbstractCrawler
from media_platform.xhs import XiaoHongShuCrawler

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    force=True  # 强制应用配置
)
logger = logging.getLogger(__name__)

app = FastAPI()

# 挂载静态文件
app.mount("/static", StaticFiles(directory="web/static"), name="static")

# 设置模板
templates = Jinja2Templates(directory="web/templates")

# 拉取工厂类
class CrawlerFactory:
    CRAWLERS = {
        "xhs": XiaoHongShuCrawler
    }

    @staticmethod
    def create_crawler(platform: str) -> AbstractCrawler:
        crawler_class = CrawlerFactory.CRAWLERS.get(platform)
        if not crawler_class:
            raise ValueError("无效的媒体平台，目前仅支持 xhs")
        return crawler_class()

# 获取默认配置
def get_default_config():
    default_config = {}
    # 从config模块获取所有大写的配置项
    for key in dir(config):
        if key.isupper():
            default_config[key] = getattr(config, key)
    
    # 添加数据库配置
    from config import db_config
    for key in dir(db_config):
        if key.isupper():
            default_config[key] = getattr(db_config, key)
    
    return default_config

# 主页路由
@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    default_config = get_default_config()
    return templates.TemplateResponse("index.html", {"request": request, "config": default_config})

# 获取配置API
@app.get("/api/config")
async def get_config():
    return get_default_config()

# 执行拉取任务API
@app.post("/api/start_pull")
async def start_pull(config_data: Dict[str, Any]):
    try:
        # 检查是否有正在执行的任务
        if config.SAVE_DATA_OPTION == "db":
            logger.info("初始化数据库连接")
            await db.init_db()
            
            # 检查是否有正在执行的任务
            query = "SELECT * FROM xhs_task WHERE status = '执行中' LIMIT 1"
            result = await db.fetch_one(query)
            if result:
                logger.warning("存在正在执行的任务，不允许启动新任务")
                await db.close()
                return JSONResponse(content={"status": "error", "message": "存在正在执行的任务，请等待当前任务完成后再试"}, status_code=400)
            
            # 创建新任务记录
            task_code = f"TASK_{uuid.uuid4().hex[:8]}_{int(datetime.datetime.now().timestamp())}"
            task_type = config_data.get("CRAWLER_TYPE", "unknown")
            
            # 插入任务记录
            query = """
            INSERT INTO xhs_task (task_code, task_type, start_time, status) 
            VALUES (:task_code, :task_type, :start_time, :status)
            """
            values = {
                "task_code": task_code,
                "task_type": task_type,
                "start_time": datetime.datetime.now(),
                "status": "执行中"
            }
            await db.execute(query, values)
            
            # 将任务编号添加到配置中
            config_data["TASK_CODE"] = task_code
        else:
            # 如果不使用数据库，生成一个任务编号但不记录
            task_code = f"TASK_{uuid.uuid4().hex[:8]}_{int(datetime.datetime.now().timestamp())}"
            config_data["TASK_CODE"] = task_code
        
        # 更新配置
        for key, value in config_data.items():
            if hasattr(config, key):
                setattr(config, key, value)
        
        logger.info(f"拉取任务开始执行，任务编号: {task_code}")
        
        try:
            # 创建并启动拉取
            logger.info(f"正在创建{config.PLATFORM}平台拉取器")
            crawler = CrawlerFactory.create_crawler(platform=config.PLATFORM)
            logger.info("开始执行拉取任务")
            await crawler.start()
            logger.info("拉取任务执行完成")
            
            # 更新任务状态为已完成
            if config.SAVE_DATA_OPTION == "db":
                query = """
                UPDATE xhs_task SET status = :status, end_time = :end_time
                WHERE task_code = :task_code
                """
                values = {
                    "status": "已完成",
                    "end_time": datetime.datetime.now(),
                    "task_code": task_code
                }
                await db.execute(query, values)
            
            return JSONResponse(content={"status": "success", "message": "拉取任务执行完成", "task_code": task_code})
            
        except Exception as e:
            error_msg = f"拉取执行出错: {str(e)}"
            logger.error(error_msg)
            
            # 更新任务状态为已失败
            if config.SAVE_DATA_OPTION == "db":
                query = """
                UPDATE xhs_task SET status = :status, end_time = :end_time, remark = :remark
                WHERE task_code = :task_code
                """
                values = {
                    "status": "已失败",
                    "end_time": datetime.datetime.now(),
                    "remark": error_msg[:1000],  # 限制错误信息长度
                    "task_code": task_code
                }
                await db.execute(query, values)
            
            return JSONResponse(content={"status": "error", "message": error_msg, "task_code": task_code}, status_code=500)
        
        finally:
            # 关闭数据库连接（如果需要）
            if config.SAVE_DATA_OPTION == "db":
                logger.info("关闭数据库连接")
                await db.close()
            
    except Exception as e:
        error_msg = f"任务启动失败: {str(e)}"
        logger.error(error_msg)
        return JSONResponse(content={"status": "error", "message": error_msg}, status_code=500)

# 启动服务器
if __name__ == "__main__":
    uvicorn.run("web.app:app", host="0.0.0.0", port=8000, reload=True)
