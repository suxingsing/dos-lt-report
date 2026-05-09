#!/usr/bin/env python3
"""
DOS & LT 统计分析周报 — Streamlit 版
生管效率先锋专项组
运行: streamlit run dos_lt_streamlit.py
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="DOS & LT 周报", page_icon="📊", layout="wide")

# ============================================================
# 数据
# ============================================================

DOS_DATA = {
    '惠州龙旗':    {'score5': 93.4, 'score4': 74.4, 'score3': 74.4, 'score2': 81.6, 'score1': 64.8, 'days5': 2.71, 'trend': '↑'},
    '南昌勤胜':    {'score5': 78.6, 'score4': 69.9, 'score3': 50.8, 'score2': 42.3, 'score1': 36.5, 'days5': 4.06, 'trend': '↑'},
    '湘潭蓝思':    {'score5': 86.7, 'score4': 53.5, 'score3': 51.9, 'score2': 28.0, 'score1': 25.8, 'days5': 4.92, 'trend': '↑↑'},
    '集贤比亚迪':  {'score5': 97.1, 'score4': 75.7, 'score3': 79.7, 'score2': 68.8, 'score1': 57.5, 'days5': 2.51, 'trend': '↑'},
    '北京昌数工厂': {'score5': 86.3, 'score4': 67.9, 'score3': 73.3, 'score2': 78.9, 'score1': 90.5, 'days5': 3.30, 'trend': '↓'},
    '惠州光弘':    {'score5': 56.5, 'score4': 36.5, 'score3': 37.6, 'score2': 19.2, 'score1': 24.7, 'days5': 7.80, 'trend': '↑'},
    '昆明立讯':    {'score5': 94.0, 'score4': 82.1, 'score3': 80.7, 'score2': 63.0, 'score1': 54.9, 'days5': 1.77, 'trend': '↑'},
}

LT_DATA = {
    '湘潭蓝思':    {'score4': 0,    'lt4': 14.97, 'score3': 22.4,  'lt3': 10.65, 'score2': 6.8,   'lt2': 11.59, 'score1': 0,     'lt1': 12.57, 'trend': '↓'},
    '惠州光弘':    {'score4': 0,    'lt4': 15.47, 'score3': 17.7,  'lt3': 10.94, 'score2': 0,     'lt2': 14.81, 'score1': 0,     'lt1': 15.0,  'trend': '↓'},
    '北京昌数工厂': {'score4': 0,    'lt4': 12.27, 'score3': 31.4,  'lt3': 10.12, 'score2': 69.9,  'lt2': 7.81,  'score1': 89.0,  'lt1': 6.66,  'trend': '↓↓'},
    '集贤比亚迪':  {'score4': 0,    'lt4': 18.13, 'score3': 8.8,   'lt3': 11.47, 'score2': 100,   'lt2': 5.81,  'score1': 100,   'lt1': 5.16,  'trend': '↓↓'},
    '惠州龙旗':    {'score4': 63.5, 'lt4': 8.19,  'score3': 71.7,  'lt3': 7.70,  'score2': 65.4,  'lt2': 8.08,  'score1': 47.5,  'lt1': 9.15,  'trend': '→'},
    '南昌勤胜':    {'score4': 68.1, 'lt4': 7.91,  'score3': 75.2,  'lt3': 7.49,  'score2': 49.9,  'lt2': 9.00,  'score1': 48.5,  'lt1': 9.09,  'trend': '↑'},
    '昆明立讯':    {'score4': 74.2, 'lt4': 7.55,  'score3': 54.5,  'lt3': 8.73,  'score2': 62.4,  'lt2': 8.26,  'score1': 21.5,  'lt1': 10.71, 'trend': '↑'},
}

DOS_TOP10 = [
    {'factory':'惠州光弘','project':'P12U','series':'—','actual':90540,'std':4.3,'dos':11.86,'score':0},
    {'factory':'北京昌数工厂','project':'P17','series':'Redmi Note','actual':30263,'std':4.3,'dos':7.91,'score':36.6},
    {'factory':'惠州龙旗','project':'O19','series':'Redmi Note','actual':10399,'std':3.5,'dos':6.93,'score':23.7},
    {'factory':'惠州龙旗','project':'SOMALIA','series':'—','actual':65404,'std':3.5,'dos':6.38,'score':36},
    {'factory':'南昌勤胜','project':'C3ZR','series':'—','actual':87828,'std':3.5,'dos':5.64,'score':52.5},
    {'factory':'惠州龙旗','project':'P85','series':'—','actual':40264,'std':4.3,'dos':5.92,'score':71.6},
    {'factory':'惠州龙旗','project':'O17R','series':'—','actual':25536,'std':4.3,'dos':5.87,'score':72.5},
    {'factory':'集贤比亚迪','project':'P82','series':'—','actual':15498,'std':4.3,'dos':5.11,'score':85.8},
    {'factory':'惠州龙旗','project':'P17','series':'Redmi Note','actual':17798,'std':4.3,'dos':4.94,'score':88.7},
    {'factory':'集贤比亚迪','project':'P16U','series':'Redmi Note Pro 防水','actual':30470,'std':4.3,'dos':4.88,'score':89.9},
]

LT_TOP10 = [
    {'factory':'集贤比亚迪','project':'O16U','volume':50101,'std':4.3,'avgLT':99.39,'projLT':99.39,'factLT':9.12},
    {'factory':'集贤比亚迪','project':'O82P','volume':4283,'std':4.3,'avgLT':80.59,'projLT':80.59,'factLT':0.63},
    {'factory':'湘潭蓝思','project':'P1','volume':57092,'std':4.3,'avgLT':32.36,'projLT':32.36,'factLT':1.42},
    {'factory':'湘潭蓝思','project':'O88','volume':18912,'std':4.3,'avgLT':29.03,'projLT':29.03,'factLT':0.42},
    {'factory':'湘潭蓝思','project':'P11U','volume':63824,'std':4.3,'avgLT':19.21,'projLT':19.21,'factLT':0.94},
    {'factory':'惠州龙旗','project':'SOMALIAX','volume':194000,'std':3.5,'avgLT':18.39,'projLT':19.19,'factLT':0.86},
    {'factory':'集贤比亚迪','project':'P16UP','volume':8730,'std':4.3,'avgLT':17.73,'projLT':17.73,'factLT':0.28},
    {'factory':'惠州龙旗','project':'P10','volume':371087,'std':5.6,'avgLT':16.33,'projLT':15.03,'factLT':1.28},
    {'factory':'惠州龙旗','project':'P85X','volume':61750,'std':4.3,'avgLT':12.09,'projLT':12.09,'factLT':0.17},
    {'factory':'北京昌数工厂','project':'P17','volume':105575,'std':4.3,'avgLT':11.88,'projLT':11.88,'factLT':2.16},
]

MONTHS = ['1月', '2月', '3月', '4月', '5月']
LT_MONTHS = ['1月', '2月', '3月', '4月']
ALL_FACTORIES = list(DOS_DATA.keys())
FACTORY_COLORS = {
    '惠州龙旗': '#FF6700', '南昌勤胜': '#1976D2', '湘潭蓝思': '#388E3C',
    '集贤比亚迪': '#D32F2F', '北京昌数工厂': '#7B1FA2', '惠州光弘': '#F57C00', '昆明立讯': '#00796B',
}


# ============================================================
# 标题
# ============================================================

st.title("📊 DOS & LT 统计分析周报")
st.caption("生管效率先锋专项组 — 数据来源：DOS及LT统计及评分规则")
st.caption(f"📅 报告更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')} | DOS最新周：5月3日 | LT最新月：4月")
st.divider()

# ============================================================
# 侧边栏筛选
# ============================================================

with st.sidebar:
    st.header("🔍 筛选条件")
    selected_factory = st.selectbox("🏭 选择工厂", ["全部工厂"] + ALL_FACTORIES)
    filter_factory = None if selected_factory == "全部工厂" else selected_factory

# ============================================================
# 概览指标
# ============================================================

avg_dos = round(sum(DOS_DATA[f]['score5'] for f in ALL_FACTORIES) / len(ALL_FACTORIES), 1)
avg_lt = round(sum(LT_DATA.get(f, {}).get('lt4', 0) for f in ALL_FACTORIES) / len(ALL_FACTORIES), 1)

c1, c2, c3, c4 = st.columns(4)
c1.metric("DOS均分（5月）", f"{avg_dos}")
c2.metric("LT均值天数（4月）", f"{avg_lt}")
c3.metric("监控工厂数", f"{len(ALL_FACTORIES)}")
c4.metric("监控项目数", f"{len(DOS_TOP10)}+")

st.divider()

# ============================================================
# 月度得分趋势
# ============================================================

st.subheader("📈 月度得分趋势")

col1, col2 = st.columns(2)

with col1:
    fig_dos = go.Figure()
    # 均值线
    avg_scores = [round(sum(DOS_DATA[f][f'score{i}'] for f in ALL_FACTORIES) / len(ALL_FACTORIES), 1) for i in range(1, 6)]
    fig_dos.add_trace(go.Scatter(x=MONTHS, y=avg_scores, name='全厂均值', line=dict(color='gray', dash='dash', width=2)))
    if filter_factory:
        fac_scores = [DOS_DATA[filter_factory][f'score{i}'] for i in range(1, 6)]
        fig_dos.add_trace(go.Scatter(x=MONTHS, y=fac_scores, name=filter_factory,
                                     line=dict(color=FACTORY_COLORS[filter_factory], width=3)))
    fig_dos.update_layout(title='DOS 月度得分趋势', yaxis_range=[0, 105], height=350, margin=dict(t=40))
    st.plotly_chart(fig_dos, use_container_width=True)

with col2:
    fig_lt = go.Figure()
    avg_lt_scores = [round(sum(LT_DATA.get(f, {}).get(f'score{i}', 0) for f in ALL_FACTORIES if LT_DATA.get(f, {}).get(f'score{i}') is not None) / max(1, sum(1 for f in ALL_FACTORIES if LT_DATA.get(f, {}).get(f'score{i}') is not None)), 1) for i in range(1, 5)]
    fig_lt.add_trace(go.Scatter(x=LT_MONTHS, y=avg_lt_scores, name='全厂均值', line=dict(color='gray', dash='dash', width=2)))
    if filter_factory:
        fac_lt_scores = [LT_DATA.get(filter_factory, {}).get(f'score{i}', 0) for i in range(1, 5)]
        fig_lt.add_trace(go.Scatter(x=LT_MONTHS, y=fac_lt_scores, name=filter_factory,
                                    line=dict(color=FACTORY_COLORS[filter_factory], width=3)))
    fig_lt.update_layout(title='LT 月度得分趋势', yaxis_range=[0, 105], height=350, margin=dict(t=40))
    st.plotly_chart(fig_lt, use_container_width=True)

# ============================================================
# 天数趋势
# ============================================================

col3, col4 = st.columns(2)

with col3:
    if filter_factory:
        fig_dos_days = go.Figure()
        avg_dos_days = round(sum(DOS_DATA[f]['days5'] for f in ALL_FACTORIES) / len(ALL_FACTORIES), 2)
        fig_dos_days.add_trace(go.Bar(x=[filter_factory], y=[DOS_DATA[filter_factory]['days5']],
                                      name='实际DOS天数', marker_color=FACTORY_COLORS[filter_factory]))
        fig_dos_days.add_trace(go.Scatter(x=[filter_factory], y=[avg_dos_days], name='全厂均值',
                                          mode='lines', line=dict(color='gray', dash='dash', width=2)))
        fig_dos_days.update_layout(title=f'{filter_factory} DOS 天数 vs 全厂均值', height=350, margin=dict(t=40))
    else:
        fig_dos_days = go.Figure()
        avg_dos_days = round(sum(DOS_DATA[f]['days5'] for f in ALL_FACTORIES) / len(ALL_FACTORIES), 2)
        fig_dos_days.add_trace(go.Bar(x=ALL_FACTORIES, y=[DOS_DATA[f]['days5'] for f in ALL_FACTORIES],
                                      name='DOS天数(5月)',
                                      marker_color=[FACTORY_COLORS[f] for f in ALL_FACTORIES]))
        fig_dos_days.add_trace(go.Scatter(x=ALL_FACTORIES, y=[avg_dos_days]*len(ALL_FACTORIES), name='全厂均值',
                                          mode='lines', line=dict(color='gray', dash='dash', width=2)))
        fig_dos_days.update_layout(title='各工厂 DOS 天数（5月3日）', height=350, margin=dict(t=40))
    st.plotly_chart(fig_dos_days, use_container_width=True)

with col4:
    if filter_factory:
        fig_lt_days = go.Figure()
        avg_lt_days = round(sum(LT_DATA.get(f, {}).get('lt4', 0) for f in ALL_FACTORIES) / len(ALL_FACTORIES), 2)
        fig_lt_days.add_trace(go.Bar(x=[filter_factory], y=[LT_DATA.get(filter_factory, {}).get('lt4', 0)],
                                     name='LT天数', marker_color=FACTORY_COLORS[filter_factory]))
        fig_lt_days.add_trace(go.Scatter(x=[filter_factory], y=[avg_lt_days], name='全厂均值',
                                         mode='lines', line=dict(color='gray', dash='dash', width=2)))
        fig_lt_days.update_layout(title=f'{filter_factory} LT 天数 vs 全厂均值', height=350, margin=dict(t=40))
    else:
        fig_lt_days = go.Figure()
        avg_lt_days = round(sum(LT_DATA.get(f, {}).get('lt4', 0) for f in ALL_FACTORIES) / len(ALL_FACTORIES), 2)
        fig_lt_days.add_trace(go.Bar(x=ALL_FACTORIES, y=[LT_DATA.get(f, {}).get('lt4', 0) for f in ALL_FACTORIES],
                                     name='LT天数(4月)',
                                     marker_color=[FACTORY_COLORS[f] for f in ALL_FACTORIES]))
        fig_lt_days.add_trace(go.Scatter(x=ALL_FACTORIES, y=[avg_lt_days]*len(ALL_FACTORIES), name='全厂均值',
                                         mode='lines', line=dict(color='gray', dash='dash', width=2)))
        fig_lt_days.update_layout(title='各工厂 LT 天数（4月）', height=350, margin=dict(t=40))
    st.plotly_chart(fig_lt_days, use_container_width=True)

st.divider()

# ============================================================
# DOS Top10
# ============================================================

st.subheader("🔴 DOS Top10 问题项目（最新周：5月3日）")
st.caption("筛选条件：最终实际 ≥ 5,000 | 按DOS天数降序（越高越差）")

dos_df = pd.DataFrame(DOS_TOP10)
if filter_factory:
    dos_df = dos_df[dos_df['factory'] == filter_factory].head(10)
    if len(dos_df) < 10:
        extra = pd.DataFrame(DOS_TOP10)[~pd.DataFrame(DOS_TOP10)['factory'].eq(filter_factory)].head(10 - len(dos_df))
        dos_df = pd.concat([dos_df, extra])

dos_df.insert(0, '#', range(1, len(dos_df) + 1))
dos_df['actual'] = dos_df['actual'].apply(lambda x: f"{x:,}")
dos_df['状态'] = dos_df['score'].apply(lambda x: '🔴 严重' if x == 0 else ('🟡 警告' if x < 60 else '🟢 正常'))
dos_df = dos_df.rename(columns={'factory': '工厂', 'project': '项目', 'series': '系列', 'actual': '最终实际', 'std': '标准DOS', 'dos': '实际DOS', 'score': 'DOS得分'})
st.dataframe(dos_df[['#', '工厂', '项目', '系列', '最终实际', '标准DOS', '实际DOS', 'DOS得分', '状态']],
             use_container_width=True, hide_index=True)

st.divider()

# ============================================================
# LT Top10
# ============================================================

st.subheader("🟡 LT Top10 问题项目（最新月：4月）")
st.caption("筛选条件：生产量 ≥ 5,000 | 按LT天数降序（越高越差）")

lt_df = pd.DataFrame(LT_TOP10)
if filter_factory:
    lt_df = lt_df[lt_df['factory'] == filter_factory].head(10)
    if len(lt_df) < 10:
        extra = pd.DataFrame(LT_TOP10)[~pd.DataFrame(LT_TOP10)['factory'].eq(filter_factory)].head(10 - len(lt_df))
        lt_df = pd.concat([lt_df, extra])

lt_df.insert(0, '#', range(1, len(lt_df) + 1))
lt_df['volume'] = lt_df['volume'].apply(lambda x: f"{x:,}")
lt_df['状态'] = lt_df['projLT'].apply(lambda x: '🔴 严重' if x > 15 else ('🟡 警告' if x > 10 else '🟢 正常'))
lt_df = lt_df.rename(columns={'factory': '工厂', 'project': '项目', 'volume': '生产量', 'std': '标准',
                               'avgLT': '全流程均值LT', 'projLT': '项目LT', 'factLT': '工厂LT'})
st.dataframe(lt_df[['#', '工厂', '项目', '生产量', '标准', '全流程均值LT', '项目LT', '工厂LT', '状态']],
             use_container_width=True, hide_index=True)

st.divider()

# ============================================================
# 各工厂汇总
# ============================================================

st.subheader("🏭 各工厂得分汇总")

summary_rows = []
for f in ALL_FACTORIES:
    d = DOS_DATA[f]
    l = LT_DATA.get(f, {})
    overall = round((d['score5'] + (l.get('score4', 0) or 0)) / (2 if l.get('score4') is not None else 1), 1)
    summary_rows.append({
        '工厂': f,
        'DOS得分(5月)': d['score5'],
        'DOS趋势': d['trend'],
        'LT得分(4月)': l.get('score4', '—'),
        'LT趋势': l.get('trend', '—'),
        '综合评价': f"{'优秀' if overall >= 80 else '良好' if overall >= 60 else '需改善'} ({overall})",
    })

summary_df = pd.DataFrame(summary_rows)
if filter_factory:
    summary_df = summary_df[summary_df['工厂'] == filter_factory]

st.dataframe(summary_df, use_container_width=True, hide_index=True)

# ============================================================
# 页脚
# ============================================================

st.divider()
st.caption("🦞 生管效率先锋专项组 · DOS & LT 周报 · 自动生成")
