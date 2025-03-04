// 等待DOM加载完成
document.addEventListener('DOMContentLoaded', function() {
    // 选项卡切换功能
    const tabItems = document.querySelectorAll('.tab-item');
    const tabPanes = document.querySelectorAll('.tab-pane');
    
    tabItems.forEach(item => {
        item.addEventListener('click', function() {
            // 移除所有选项卡的active类
            tabItems.forEach(tab => tab.classList.remove('active'));
            tabPanes.forEach(pane => pane.classList.remove('active'));
            
            // 添加当前选项卡的active类
            this.classList.add('active');
            const tabId = `${this.dataset.tab}-tab`;
            document.getElementById(tabId).classList.add('active');
        });
    });
    
    // URL列表管理
    const urlList = document.getElementById('url-list');
    const addUrlBtn = document.getElementById('add-url-btn');
    const clearUrlsBtn = document.getElementById('clear-urls-btn');
    const urlModal = document.getElementById('url-modal');
    const urlInput = document.getElementById('url-input');
    const confirmUrlBtn = document.getElementById('confirm-url-btn');
    const closeBtn = document.querySelector('.close-btn');
    
    // 存储URL列表
    let urls = [];
    
    // 从localStorage加载已保存的URL
    function loadUrls() {
        const savedUrls = localStorage.getItem('xhsNoteUrls');
        if (savedUrls) {
            urls = JSON.parse(savedUrls);
            renderUrlList();
        }
    }
    
    // 保存URL到localStorage
    function saveUrls() {
        localStorage.setItem('xhsNoteUrls', JSON.stringify(urls));
    }
    
    // 渲染URL列表
    function renderUrlList() {
        urlList.innerHTML = '';
        
        if (urls.length === 0) {
            const emptyMessage = document.createElement('div');
            emptyMessage.className = 'empty-message';
            emptyMessage.textContent = '暂无URL，请点击"添加URL"按钮添加';
            urlList.appendChild(emptyMessage);
            return;
        }
        
        urls.forEach((url, index) => {
            const urlItem = document.createElement('div');
            urlItem.className = 'url-item';
            
            const urlText = document.createElement('div');
            urlText.className = 'url-text';
            urlText.title = url;
            urlText.textContent = url;
            
            const deleteBtn = document.createElement('span');
            deleteBtn.className = 'delete-url';
            deleteBtn.innerHTML = '&times;';
            deleteBtn.title = '删除';
            deleteBtn.addEventListener('click', () => {
                urls.splice(index, 1);
                saveUrls();
                renderUrlList();
            });
            
            urlItem.appendChild(urlText);
            urlItem.appendChild(deleteBtn);
            urlList.appendChild(urlItem);
        });
    }
    
    // 添加URL按钮点击事件
    addUrlBtn.addEventListener('click', () => {
        urlInput.value = '';
        urlModal.style.display = 'block';
    });
    
    // 确认添加URL
    confirmUrlBtn.addEventListener('click', () => {
        const url = urlInput.value.trim();
        if (url) {
            if (!urls.includes(url)) {
                urls.push(url);
                saveUrls();
                renderUrlList();
            }
            urlModal.style.display = 'none';
        } else {
            alert('请输入有效的URL');
        }
    });
    
    // 清空URL列表
    clearUrlsBtn.addEventListener('click', () => {
        if (confirm('确定要清空所有URL吗？')) {
            urls = [];
            saveUrls();
            renderUrlList();
        }
    });
    
    // 关闭模态框
    closeBtn.addEventListener('click', () => {
        urlModal.style.display = 'none';
    });
    
    // 点击模态框外部关闭
    window.addEventListener('click', (event) => {
        if (event.target === urlModal) {
            urlModal.style.display = 'none';
        }
    });
    
    // 状态消息更新
    const statusMessage = document.getElementById('status-message');
    
    // 更新状态消息
    function updateStatusMessage(message, isError = false) {
        statusMessage.textContent = message;
        statusMessage.className = isError ? 'status-error' : 'status-info';
    }
    
    // 执行按钮点击事件
    const executeBtn = document.getElementById('execute-btn');
    
    executeBtn.addEventListener('click', function() {
        // 收集配置数据
        const config = {};
        
        // 获取所有配置输入
        document.querySelectorAll('.config-panel input, .config-panel select, .config-panel textarea').forEach(input => {
            let value;
            
            if (input.type === 'checkbox') {
                value = input.checked;
            } else if (input.type === 'number') {
                value = parseInt(input.value, 10);
            } else {
                value = input.value;
            }
            
            config[input.name] = value;
        });
        
        // 获取当前选项卡中的配置
        const activeTabPane = document.querySelector('.tab-pane.active');
        if (activeTabPane) {
            activeTabPane.querySelectorAll('input, select, textarea').forEach(input => {
                let value;
                
                if (input.type === 'checkbox') {
                    value = input.checked;
                } else if (input.type === 'number') {
                    value = parseInt(input.value, 10);
                } else {
                    value = input.value;
                }
                
                config[input.name] = value;
            });
        }
        
        // 根据当前选中的选项卡设置拉取类型
        const activeTab = document.querySelector('.tab-item.active').dataset.tab;
        config.CRAWLER_TYPE = activeTab;  // 保留原字段名，后端仍然使用这个字段
        
        // 如果是detail类型，添加URL列表
        if (activeTab === 'detail') {
            config.XHS_SPECIFIED_NOTE_URL_LIST = urls;
        }
        
        // 禁用执行按钮，防止重复点击
        executeBtn.disabled = true;
        executeBtn.textContent = '执行中...';
        
        // 更新状态消息
        updateStatusMessage('正在执行拉取任务，请稍候...');
        
        // 发送配置到服务器
        fetch('/api/start_pull', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(config)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                updateStatusMessage(data.message || '拉取任务执行完成');
            } else {
                updateStatusMessage(data.message || '拉取任务执行失败', true);
            }
        })
        .catch(error => {
            console.error('执行拉取任务出错:', error);
            updateStatusMessage('执行拉取任务出错: ' + error.message, true);
        })
        .finally(() => {
            // 恢复执行按钮
            executeBtn.disabled = false;
            executeBtn.textContent = '执行';
        });
    });
    
    // 加载保存的URL
    loadUrls();
    
    // 从配置文件加载默认值
    function loadDefaultConfig() {
        // 通过API获取默认配置
        fetch('/api/config')
            .then(response => response.json())
            .then(config => {
                // 设置表单默认值
                for (const [key, value] of Object.entries(config)) {
                    // 查找所有具有该name的输入元素
                    const elements = document.querySelectorAll(`[name="${key}"]`);
                    
                    elements.forEach(element => {
                        if (element.type === 'checkbox') {
                            element.checked = Boolean(value);
                        } else if (element.tagName === 'SELECT') {
                            // 查找匹配的选项并设置为选中
                            const option = Array.from(element.options).find(opt => opt.value === value);
                            if (option) {
                                option.selected = true;
                            }
                        } else {
                            element.value = value;
                        }
                    });
                }
                
                updateStatusMessage('已加载默认配置');
            })
            .catch(error => {
                console.error('加载默认配置失败:', error);
                updateStatusMessage('加载默认配置失败，请刷新页面重试', true);
            });
    }
    
    // 加载默认配置
    loadDefaultConfig();
});
