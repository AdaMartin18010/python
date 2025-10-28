# Plotly 交互式可视化

**现代交互式数据可视化库**

---

## 📋 概述

Plotly是一个现代化的交互式可视化库，支持Web浏览器交互、动画和导出。

### 核心特性

- 🎨 **交互式** - 缩放、平移、悬停提示
- 📊 **丰富图表** - 40+图表类型
- 🌐 **Web友好** - 基于JavaScript
- 📱 **响应式** - 自适应布局
- 🎬 **动画** - 支持动画效果

---

## 🚀 快速开始

### 安装

```bash
uv add plotly
# 或支持Jupyter
uv add plotly nbformat
```

### 基本绘图

```python
import plotly.express as px
import plotly.graph_objects as go

# 使用Express快速绘图
df = px.data.iris()
fig = px.scatter(df, x='sepal_width', y='sepal_length', 
                 color='species')
fig.show()

# 使用Graph Objects精细控制
fig = go.Figure(data=go.Scatter(x=[1, 2, 3], y=[4, 1, 2]))
fig.update_layout(title='简单折线图')
fig.show()
```

---

## 📊 常用图表

### 1. 散点图

```python
import plotly.express as px

df = px.data.iris()
fig = px.scatter(df, x='sepal_width', y='sepal_length',
                 color='species', size='petal_length',
                 hover_data=['petal_width'])
fig.show()
```

### 2. 折线图

```python
fig = px.line(df, x='date', y='value', color='category',
              title='时间序列')
fig.show()
```

### 3. 柱状图

```python
fig = px.bar(df, x='category', y='value', color='region',
             barmode='group')
fig.show()
```

### 4. 热力图

```python
import numpy as np

z = np.random.randn(20, 20)
fig = px.imshow(z, color_continuous_scale='Viridis')
fig.show()
```

---

## 🎨 高级可视化

### 3D图表

```python
df = px.data.iris()
fig = px.scatter_3d(df, x='sepal_length', y='sepal_width',
                    z='petal_width', color='species')
fig.show()
```

### 地图

```python
df = px.data.gapminder().query("year==2007")
fig = px.scatter_geo(df, locations="iso_alpha",
                     size="pop", color="continent",
                     hover_name="country")
fig.show()
```

### 动画

```python
df = px.data.gapminder()
fig = px.scatter(df, x="gdpPercap", y="lifeExp",
                 animation_frame="year",
                 animation_group="country",
                 size="pop", color="continent",
                 hover_name="country",
                 log_x=True, size_max=55,
                 range_x=[100,100000], range_y=[25,90])
fig.show()
```

---

## 🎯 Dash集成

### 创建交互式仪表板

```python
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

app = Dash(__name__)

app.layout = html.Div([
    html.H1('交互式仪表板'),
    dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': 'GDP', 'value': 'gdpPercap'},
            {'label': '人口', 'value': 'pop'}
        ],
        value='gdpPercap'
    ),
    dcc.Graph(id='graph')
])

@app.callback(
    Output('graph', 'figure'),
    Input('dropdown', 'value')
)
def update_graph(column):
    df = px.data.gapminder()
    fig = px.scatter(df, x=column, y='lifeExp')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
```

---

## 💻 实战示例

### 金融K线图

```python
import plotly.graph_objects as go

fig = go.Figure(data=[go.Candlestick(
    x=df['Date'],
    open=df['Open'],
    high=df['High'],
    low=df['Low'],
    close=df['Close']
)])
fig.update_layout(title='股票K线图')
fig.show()
```

### 子图布局

```python
from plotly.subplots import make_subplots

fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=('散点图', '折线图', '柱状图', '饼图')
)

fig.add_trace(go.Scatter(x=[1, 2, 3], y=[4, 5, 6]), row=1, col=1)
fig.add_trace(go.Scatter(x=[1, 2, 3], y=[2, 1, 3]), row=1, col=2)
fig.add_trace(go.Bar(x=[1, 2, 3], y=[2, 5, 1]), row=2, col=1)
fig.add_trace(go.Pie(labels=['A', 'B', 'C'], values=[30, 20, 50]), row=2, col=2)

fig.update_layout(height=600, showlegend=False)
fig.show()
```

---

## 📈 与Pandas集成

```python
import pandas as pd
import plotly.express as px

df = pd.read_csv('data.csv')

# 直接从DataFrame绘图
fig = px.line(df, x='date', y='price', color='symbol')
fig.show()

# 分组聚合后绘图
summary = df.groupby('category')['value'].mean().reset_index()
fig = px.bar(summary, x='category', y='value')
fig.show()
```

---

## 🎨 样式定制

```python
fig = px.scatter(df, x='x', y='y')

fig.update_layout(
    title='自定义标题',
    xaxis_title='X轴',
    yaxis_title='Y轴',
    template='plotly_dark',  # 主题
    font=dict(size=14),
    hovermode='closest'
)

fig.update_traces(marker=dict(size=10, opacity=0.7))
fig.show()
```

---

## 📚 最佳实践

### 1. 性能优化

```python
# ✅ 对大数据集采样
if len(df) > 10000:
    df_sample = df.sample(10000)
    fig = px.scatter(df_sample, x='x', y='y')

# ✅ 使用Scattergl加速
fig = go.Figure(data=go.Scattergl(x=x, y=y, mode='markers'))
```

### 2. 导出图表

```python
# 保存为HTML
fig.write_html('figure.html')

# 保存为静态图片
fig.write_image('figure.png')
fig.write_image('figure.pdf')
```

---

## 🔗 相关资源

- [官方文档](https://plotly.com/python/)
- [Dash文档](https://dash.plotly.com/)

---

**最后更新**: 2025年10月28日

