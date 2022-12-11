"""
2022/12/10  streamlitのテストように作ってみた
"""
import streamlit as st
import pandas as pd

st.title('test app')

# 初期値を読み込む
df = pd.read_csv('data.csv', header=None, index_col=0)

# ボタンフレームを作る
with st.form(key='form'):
    st.write('streamlitをどう思う?')
    # 押されたボタンによって加算
    df.loc[0][1] += st.form_submit_button('使ってみたい')
    df.loc[1][1] += st.form_submit_button('いらない')
    df.loc[2][1] += st.form_submit_button('検討してみる')
    reset  = st.form_submit_button('リセット')
    if reset  == True : df.loc[0][1],df.loc[1][1],df.loc[2][1] = 0,0,0
    st.write('使ってみたい:',df.loc[0][1],'いらない:',df.loc[1][1],'検討してみる:',df.loc[2][1])

# 結果を書き込む
df.to_csv("data.csv", header=None)

# 結果を表形式とグラフで表示
data = pd.DataFrame({
    'index': ['1:使ってみたい','2:いらない','3:検討してみる'],
    '投票数': [df.loc[0][1],df.loc[1][1],df.loc[2][1]],
     }).set_index('index')
st.write(data)
st.bar_chart(data)