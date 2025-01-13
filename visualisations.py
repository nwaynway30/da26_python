import pandas as pd
import streamlit as st


# Barchart
def bar_chart(data: pd.DataFrame, column: str) -> None:
    st.write("Think of this as a bar chart")
    st.write(data)


# Line chart with categories (time as the x-axis)
def line_chart(data: pd.DataFrame, column: str):
    pass


# Donut chart
def donut_chart(data: pd.DataFrame, column: str):
    pass

# 转换chart_week为datetime
    chart_positions['chart_week'] = pd.to_datetime(chart_positions['chart_week'])
    
    # 添加季节列
    chart_positions['season'] = chart_positions['chart_week'].dt.month.map({
        12: 'Winter', 1: 'Winter', 2: 'Winter',
        3: 'Spring', 4: 'Spring', 5: 'Spring',
        6: 'Summer', 7: 'Summer', 8: 'Summer',
        9: 'Fall', 10: 'Fall', 11: 'Fall'
    })
    
    # 添加年份和月份
    chart_positions['year'] = chart_positions['chart_week'].dt.year
    chart_positions['month'] = chart_positions['chart_week'].dt.month
    
    return audio_features, chart_positions, artists, tracks, tracks_artists

def main():
    st.title("音乐数据多维度分析")
    
    # 加载数据
    audio_features, chart_positions, artists, tracks, tracks_artists = load_data()
    
    # 侧边栏
    st.sidebar.title("分析选项")
    analysis_type = st.sidebar.selectbox(
        "选择分析类型",
        ["季节性趋势", "时间趋势分析", "音乐特征分析", "热门艺术家分析", "曲目类型分析"]
    )
    
    if analysis_type == "季节性趋势":
        st.header("音乐季节性趋势分析")
        
        tab1, tab2 = st.tabs(["排名趋势", "音乐特征"])
        
        with tab1:
            # 按季节统计平均排名
            seasonal_chart = chart_positions.groupby('season')['list_position'].mean().reset_index()
            
            # 创建季节性排名趋势图
            fig_seasonal = px.bar(
                seasonal_chart,
                x='season',
                y='list_position',
                title='各季节歌曲平均排名',
                labels={'list_position': '平均排名', 'season': '季节'}
            )
            st.plotly_chart(fig_seasonal)
            
            # 显示具体数据
            st.write("各季节平均排名：")
            st.write(seasonal_chart.round(2))
        
        with tab2:
            # 合并音频特征和季节数据
            seasonal_features = pd.merge(
                chart_positions[['track_id', 'season']],
                audio_features,
                on='track_id'
            )
            
            # 选择要分析的音频特征
            feature = st.selectbox(
                "选择音频特征",
                ['danceability', 'energy', 'valence', 'tempo']
            )
            
            # 创建音频特征的季节性分布图
            fig_features = px.box(
                seasonal_features,
                x='season',
                y=feature,
                title=f'{feature.capitalize()} 在不同季节的分布'
            )
            st.plotly_chart(fig_features)
            
            # 显示季节均值
            st.write(f"各季节 {feature} 平均值：")
            season_means = seasonal_features.groupby('season')[feature].mean().round(3)
            st.write(season_means)

    elif analysis_type == "时间趋势分析":
        st.header("音乐特征时间趋势分析")
        
        # 合并数据
        time_features = pd.merge(
            chart_positions[['track_id', 'year', 'month']],
            audio_features,
            on='track_id'
        )
        
        # 按年度统计
        yearly_stats = time_features.groupby('year').agg({
            'danceability': 'mean',
            'energy': 'mean',
            'valence': 'mean',
            'tempo': 'mean'
        }).reset_index()
        
        # 选择特征
        feature = st.selectbox(
            "选择要分析的特征",
            ['danceability', 'energy', 'valence', 'tempo']
        )
        
        # 创建时间趋势图
        fig_time = px.line(
            yearly_stats,
            x='year',
            y=feature,
            title=f'{feature.capitalize()} 随时间的变化趋势'
        )
        st.plotly_chart(fig_time)
        
        # 显示年度统计
        st.write("年度均值统计：")
        st.write(yearly_stats.round(3))
        
    elif analysis_type == "音乐特征分析":
        st.header("音乐特征相关性分析")
        
        # 选择要分析的特征
        feature_x = st.selectbox("X轴特征", ['danceability', 'energy', 'valence', 'tempo'])
        feature_y = st.selectbox("Y轴特征", ['danceability', 'energy', 'valence', 'tempo'])
        
        # 计算相关系数
        correlation = audio_features[feature_x].corr(audio_features[feature_y])
        
        # 创建散点图
        fig_scatter = px.scatter(
            audio_features,
            x=feature_x,
            y=feature_y,
            title=f'{feature_x.capitalize()} vs {feature_y.capitalize()} (相关系数: {correlation:.3f})',
            opacity=0.6
        )
        st.plotly_chart(fig_scatter)
        
        # 显示基本统计信息
        st.write("特征统计信息：")
        stats_df = audio_features[[feature_x, feature_y]].describe().round(3)
        st.write(stats_df)
        
    elif analysis_type == "热门艺术家分析":
        st.header("热门艺术家分析")
        
        tab1, tab2 = st.tabs(["Top艺术家", "粉丝分布"])
        
        with tab1:
            # 显示最受欢迎的艺术家
            top_artists = artists.nlargest(10, 'popularity')[['name', 'popularity', 'followers']]
            
            fig_popular = px.bar(
                top_artists,
                x='name',
                y='popularity',
                title='最受欢迎的艺术家 Top 10'
            )
            st.plotly_chart(fig_popular)
            
            # 显示具体数据
            st.write("Top 10 艺术家详细信息：")
            st.write(top_artists)
            
        with tab2:
            # 创建粉丝数分布图
            fig_followers = px.histogram(
                artists,
                x='followers',
                title='艺术家粉丝数分布',
                nbins=50
            )
            fig_followers.update_layout(xaxis_title="粉丝数", yaxis_title="艺术家数量")
            st.plotly_chart(fig_followers)
            
            # 显示粉丝数统计
            st.write("粉丝数统计信息：")
            followers_stats = artists['followers'].describe().round(2)
            st.write(followers_stats)
    
    else:  # 曲目类型分析
        st.header("曲目类型分析")
        
        # 合并tracks和audio_features
        track_analysis = pd.merge(
            tracks[['track_id', 'explicit', 'album_type']],
            audio_features,
            on='track_id'
        )
        
        # 按专辑类型分析
        st.subheader("不同专辑类型的音乐特征")
        
        # 选择特征
        feature = st.selectbox(
            "选择要比较的特征",
            ['danceability', 'energy', 'valence', 'tempo']
        )
        
        # 创建专辑类型特征对比图
        fig_album = px.box(
            track_analysis,
            x='album_type',
            y=feature,
            title=f'不同专辑类型的 {feature.capitalize()} 分布'
        )
        st.plotly_chart(fig_album)
        
        # 显示均值统计
        st.write(f"各专辑类型 {feature} 均值：")
        album_means = track_analysis.groupby('album_type')[feature].mean().round(3)
        st.write(album_means)

if __name__ == "__main__":
    main()