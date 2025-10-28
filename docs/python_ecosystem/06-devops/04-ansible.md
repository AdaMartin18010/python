# Ansible 自动化运维

**Python应用自动化部署和配置管理**

---

## 📋 概述

Ansible是基于Python的自动化运维工具，使用YAML编写配置，无需agent，通过SSH管理远程服务器。

### 核心特性

- 📝 **声明式** - YAML配置文件
- 🔓 **无Agent** - SSH远程执行
- 🎯 **幂等性** - 多次执行结果一致
- 📦 **模块化** - 丰富的内置模块
- 🔄 **可重用** - Roles和Playbooks

---

## 🚀 快速开始

### 安装

```bash
uv add ansible
# 或系统包管理器
sudo apt-get install ansible
```

### Inventory配置

```ini
# inventory.ini
[webservers]
web1.example.com ansible_user=deploy
web2.example.com ansible_user=deploy

[databases]
db1.example.com ansible_user=deploy
db2.example.com ansible_user=deploy

[all:vars]
ansible_python_interpreter=/usr/bin/python3
```

### 基础命令

```bash
# 测试连接
ansible all -i inventory.ini -m ping

# 执行命令
ansible webservers -i inventory.ini -m shell -a "uptime"

# 获取信息
ansible all -i inventory.ini -m setup
```

---

## 📝 Playbook编写

### 基础Playbook

```yaml
# deploy.yml
---
- name: 部署Python应用
  hosts: webservers
  become: yes
  
  vars:
    app_name: myapp
    app_version: "1.0.0"
    app_path: /opt/{{ app_name }}
  
  tasks:
    - name: 更新APT缓存
      apt:
        update_cache: yes
      when: ansible_os_family == "Debian"
    
    - name: 安装系统依赖
      apt:
        name:
          - python3
          - python3-pip
          - nginx
        state: present
    
    - name: 创建应用目录
      file:
        path: "{{ app_path }}"
        state: directory
        owner: www-data
        group: www-data
        mode: '0755'
    
    - name: 复制应用文件
      copy:
        src: ./dist/
        dest: "{{ app_path }}"
        owner: www-data
        group: www-data
    
    - name: 安装Python依赖
      pip:
        requirements: "{{ app_path }}/requirements.txt"
        virtualenv: "{{ app_path }}/venv"
        virtualenv_python: python3
    
    - name: 配置systemd服务
      template:
        src: templates/myapp.service.j2
        dest: /etc/systemd/system/{{ app_name }}.service
      notify: 重启应用
    
    - name: 启动应用服务
      systemd:
        name: "{{ app_name }}"
        state: started
        enabled: yes
        daemon_reload: yes
  
  handlers:
    - name: 重启应用
      systemd:
        name: "{{ app_name }}"
        state: restarted
```

---

## 🎯 模板系统

### Jinja2模板

```jinja2
# templates/myapp.service.j2
[Unit]
Description={{ app_name }} Application
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory={{ app_path }}
Environment="PATH={{ app_path }}/venv/bin"
ExecStart={{ app_path }}/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

### Nginx配置

```jinja2
# templates/nginx.conf.j2
server {
    listen 80;
    server_name {{ domain_name }};
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    
    location /static {
        alias {{ app_path }}/static;
    }
}
```

---

## 📦 Roles组织

### Role结构

```
roles/
└── python_app/
    ├── tasks/
    │   ├── main.yml
    │   ├── install.yml
    │   └── configure.yml
    ├── handlers/
    │   └── main.yml
    ├── templates/
    │   ├── app.service.j2
    │   └── nginx.conf.j2
    ├── files/
    │   └── app.tar.gz
    ├── vars/
    │   └── main.yml
    ├── defaults/
    │   └── main.yml
    └── meta/
        └── main.yml
```

### Role主任务

```yaml
# roles/python_app/tasks/main.yml
---
- name: 包含安装任务
  include_tasks: install.yml

- name: 包含配置任务
  include_tasks: configure.yml

- name: 确保服务运行
  systemd:
    name: "{{ app_name }}"
    state: started
    enabled: yes
```

### 使用Role

```yaml
# site.yml
---
- name: 部署应用
  hosts: webservers
  become: yes
  
  roles:
    - role: python_app
      vars:
        app_name: myapp
        app_version: "1.0.0"
```

---

## 🔒 Ansible Vault

### 加密敏感数据

```bash
# 创建加密文件
ansible-vault create secrets.yml

# 编辑加密文件
ansible-vault edit secrets.yml

# 查看加密文件
ansible-vault view secrets.yml

# 加密现有文件
ansible-vault encrypt vars.yml

# 解密文件
ansible-vault decrypt vars.yml
```

### 使用加密变量

```yaml
# secrets.yml (加密后)
---
database_password: "SuperSecretPassword123"
api_key: "sk-1234567890abcdef"
```

```bash
# 运行时提供密码
ansible-playbook deploy.yml --ask-vault-pass

# 使用密码文件
ansible-playbook deploy.yml --vault-password-file ~/.vault_pass
```

---

## 🎨 高级特性

### 条件执行

```yaml
- name: 根据OS安装包
  package:
    name: "{{ item }}"
    state: present
  when: ansible_os_family == "Debian"
  loop:
    - python3
    - python3-pip

- name: 只在生产环境执行
  command: /opt/app/production_setup.sh
  when: environment == "production"
```

### 循环

```yaml
- name: 创建多个用户
  user:
    name: "{{ item.name }}"
    groups: "{{ item.groups }}"
    state: present
  loop:
    - { name: 'alice', groups: 'developers' }
    - { name: 'bob', groups: 'ops' }
    - { name: 'carol', groups: 'developers,ops' }

- name: 从字典循环
  debug:
    msg: "User {{ item.key }} has role {{ item.value }}"
  loop: "{{ users | dict2items }}"
  vars:
    users:
      alice: developer
      bob: admin
```

### 错误处理

```yaml
- name: 尝试操作，失败时继续
  command: /opt/app/risky_operation.sh
  ignore_errors: yes

- name: 捕获失败并执行恢复
  block:
    - name: 尝试升级
      command: /opt/app/upgrade.sh
  rescue:
    - name: 升级失败，回滚
      command: /opt/app/rollback.sh
  always:
    - name: 清理临时文件
      file:
        path: /tmp/upgrade
        state: absent
```

---

## 🔄 滚动更新

```yaml
- name: 滚动更新应用
  hosts: webservers
  serial: 1  # 一次更新一台
  max_fail_percentage: 25  # 失败25%时停止
  
  pre_tasks:
    - name: 从负载均衡器移除
      local_action:
        module: command
        args: lb-remove {{ inventory_hostname }}
  
  tasks:
    - name: 更新应用
      copy:
        src: ./app-{{ version }}.tar.gz
        dest: /opt/app/
    
    - name: 重启服务
      systemd:
        name: myapp
        state: restarted
    
    - name: 健康检查
      uri:
        url: http://{{ inventory_hostname }}:8000/health
        status_code: 200
      retries: 5
      delay: 10
  
  post_tasks:
    - name: 添加回负载均衡器
      local_action:
        module: command
        args: lb-add {{ inventory_hostname }}
```

---

## 📊 实战示例

### 完整部署Playbook

```yaml
# deploy-full.yml
---
- name: 完整Python应用部署
  hosts: webservers
  become: yes
  
  vars:
    app_name: fastapi-app
    app_version: "{{ lookup('env', 'APP_VERSION') | default('latest') }}"
    app_user: www-data
    app_path: /opt/{{ app_name }}
  
  tasks:
    # 1. 系统准备
    - name: 更新系统包
      apt:
        update_cache: yes
        cache_valid_time: 3600
    
    - name: 安装系统依赖
      apt:
        name:
          - python3
          - python3-pip
          - python3-venv
          - nginx
          - supervisor
        state: present
    
    # 2. 应用部署
    - name: 创建应用目录
      file:
        path: "{{ item }}"
        state: directory
        owner: "{{ app_user }}"
        group: "{{ app_user }}"
      loop:
        - "{{ app_path }}"
        - "{{ app_path }}/logs"
        - "{{ app_path }}/static"
    
    - name: 解压应用包
      unarchive:
        src: "dist/{{ app_name }}-{{ app_version }}.tar.gz"
        dest: "{{ app_path }}"
        owner: "{{ app_user }}"
        group: "{{ app_user }}"
    
    - name: 创建虚拟环境
      command: python3 -m venv {{ app_path }}/venv
      args:
        creates: "{{ app_path }}/venv"
    
    - name: 安装Python依赖
      pip:
        requirements: "{{ app_path }}/requirements.txt"
        virtualenv: "{{ app_path }}/venv"
    
    # 3. 配置服务
    - name: 配置supervisor
      template:
        src: templates/supervisor.conf.j2
        dest: /etc/supervisor/conf.d/{{ app_name }}.conf
      notify: 重启supervisor
    
    - name: 配置nginx
      template:
        src: templates/nginx-site.conf.j2
        dest: /etc/nginx/sites-available/{{ app_name }}
      notify: 重启nginx
    
    - name: 启用nginx站点
      file:
        src: /etc/nginx/sites-available/{{ app_name }}
        dest: /etc/nginx/sites-enabled/{{ app_name }}
        state: link
    
    # 4. 数据库迁移
    - name: 运行数据库迁移
      command: "{{ app_path }}/venv/bin/alembic upgrade head"
      args:
        chdir: "{{ app_path }}"
      become_user: "{{ app_user }}"
    
    # 5. 启动服务
    - name: 启动应用
      supervisorctl:
        name: "{{ app_name }}"
        state: restarted
  
  handlers:
    - name: 重启supervisor
      service:
        name: supervisor
        state: restarted
    
    - name: 重启nginx
      service:
        name: nginx
        state: reloaded
```

---

## 🐍 Python集成

### 使用Python API

```python
import ansible_runner

# 运行playbook
r = ansible_runner.run(
    private_data_dir='/tmp/ansible',
    playbook='deploy.yml',
    inventory='inventory.ini',
    extravars={'app_version': '1.0.0'}
)

# 检查结果
print(f"状态: {r.status}")
print(f"返回码: {r.rc}")

# 遍历事件
for event in r.events:
    if event['event'] == 'runner_on_ok':
        print(f"成功: {event['event_data']['task']}")
```

### 自定义模块

```python
#!/usr/bin/python
# library/check_app_health.py

from ansible.module_utils.basic import AnsibleModule
import requests

def main():
    module = AnsibleModule(
        argument_spec=dict(
            url=dict(type='str', required=True),
            timeout=dict(type='int', default=10)
        )
    )
    
    url = module.params['url']
    timeout = module.params['timeout']
    
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            module.exit_json(changed=False, healthy=True)
        else:
            module.fail_json(msg=f"健康检查失败: {response.status_code}")
    except Exception as e:
        module.fail_json(msg=str(e))

if __name__ == '__main__':
    main()
```

使用自定义模块：

```yaml
- name: 检查应用健康
  check_app_health:
    url: "http://{{ inventory_hostname }}:8000/health"
    timeout: 5
```

---

## 📚 最佳实践

### 1. 目录结构

```
ansible/
├── inventory/
│   ├── production
│   └── staging
├── group_vars/
│   ├── all.yml
│   ├── webservers.yml
│   └── databases.yml
├── host_vars/
│   └── web1.example.com.yml
├── roles/
│   ├── common/
│   ├── python_app/
│   └── nginx/
├── playbooks/
│   ├── deploy.yml
│   ├── rollback.yml
│   └── update.yml
├── ansible.cfg
└── requirements.yml
```

### 2. 幂等性

```yaml
# ✅ 幂等
- name: 确保目录存在
  file:
    path: /opt/app
    state: directory

# ❌ 非幂等
- name: 创建目录
  command: mkdir /opt/app
```

### 3. 变量优先级

```
1. 命令行 (-e)
2. role vars
3. play vars
4. host_vars
5. group_vars
6. role defaults
```

---

## 🔗 相关资源

- [Ansible文档](https://docs.ansible.com/)
- [Ansible Galaxy](https://galaxy.ansible.com/)

---

**最后更新**: 2025年10月28日

