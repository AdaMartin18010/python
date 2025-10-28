# 日期时间处理

**Python日期时间工具**

---

## 📋 标准库datetime

### 基本使用

```python
from datetime import datetime, date, time, timedelta

# 当前时间
now = datetime.now()
today = date.today()

# 创建时间
dt = datetime(2025, 10, 28, 15, 30, 0)

# 时间计算
tomorrow = today + timedelta(days=1)
next_week = now + timedelta(weeks=1)

# 格式化
formatted = now.strftime('%Y-%m-%d %H:%M:%S')

# 解析
parsed = datetime.strptime('2025-10-28', '%Y-%m-%d')
```

---

## ⏰ Arrow - 人性化时间

### 安装

```bash
uv add arrow
```

### 使用

```python
import arrow

# 当前时间
now = arrow.now()

# 人性化表示
print(now.humanize())  # 'just now'
print(now.shift(hours=-1).humanize())  # 'an hour ago'

# 时区转换
utc = arrow.utcnow()
beijing = utc.to('Asia/Shanghai')

# 解析
a = arrow.get('2025-10-28')
a = arrow.get('2025-10-28T15:30:00+08:00')

# 格式化
formatted = now.format('YYYY-MM-DD HH:mm:ss')
```

---

## 🌍 Pendulum - 时区处理

### 安装

```bash
uv add pendulum
```

### 使用

```python
import pendulum

# 创建时间（自动处理时区）
now = pendulum.now('Asia/Shanghai')

# 时区转换
tokyo = now.in_timezone('Asia/Tokyo')

# 时间计算
tomorrow = now.add(days=1)
next_month = now.add(months=1)

# 人性化
print(now.diff_for_humans())  # '刚刚'

# 时期
period = now.diff(tomorrow)
print(period.in_days())
```

---

## 📅 dateutil

```bash
uv add python-dateutil
```

```python
from dateutil import parser, rrule
from datetime import datetime

# 智能解析
dt = parser.parse('2025-10-28')
dt = parser.parse('Oct 28, 2025')

# 相对时间
from dateutil.relativedelta import relativedelta
next_month = datetime.now() + relativedelta(months=1)

# 重复规则
# 每周一重复
rule = rrule.rrule(
    rrule.WEEKLY,
    byweekday=rrule.MO,
    dtstart=datetime.now(),
    count=10
)
for dt in rule:
    print(dt)
```

---

## 📚 最佳实践

### 1. 始终使用UTC存储

```python
import pendulum

# ✅ 存储UTC
utc_time = pendulum.now('UTC')
db.save(utc_time)

# ✅ 显示时转换
local_time = utc_time.in_timezone('Asia/Shanghai')
```

### 2. 时区感知

```python
# ✅ 时区感知
aware = pendulum.now('Asia/Shanghai')

# ❌ 时区无关
naive = datetime.now()
```

### 3. ISO 8601格式

```python
# ✅ 使用ISO格式
iso_str = datetime.now().isoformat()
# '2025-10-28T15:30:00+08:00'
```

---

## 🔗 相关资源

- [datetime文档](https://docs.python.org/3/library/datetime.html)
- [Arrow](https://arrow.readthedocs.io/)
- [Pendulum](https://pendulum.eustace.io/)

---

**最后更新**: 2025年10月28日

