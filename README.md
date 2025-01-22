# Angus998.github.io

<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI周报</title>
    <style>
        /* 居中标题的样式 */
        .center-title {
            text-align: center; /* 文本居中对齐 */
            font-size: 24px; /* 根据需要调整字体大小 */
            font-weight: bold; /* 加粗标题 */
            margin-bottom: 20px; /* 标题与内容之间的间距 */
        }

        /* 小标题的样式 */
        .sub-title {
            font-size: 18px; /* 根据需要调整字体大小 */
            font-weight: bold; /* 加粗小标题 */
            margin-top: 15px; /* 小标题与上一个内容之间的间距 */
        }

        /* 可折叠内容的样式 */
        details {
            margin-left: 20px; /* 内容缩进 */
        }
        /* 设置图片容器的样式 */
        .image-container {
            display: flex;           /* 使用 Flexbox 布局 */
            justify-content: center; /* 水平居中 */
            align-items: center;     /* 垂直居中 */
            height: 100vh;           /* 容器高度为视口高度 */
            overflow: hidden;        /* 防止图片超出容器 */
        }

        /* 设置图片的样式 */
        .image-container img {
            max-width: 100%;         /* 图片最大宽度为容器宽度 */
            max-height: 100%;        /* 图片最大高度为容器高度 */
            object-fit: contain;     /* 保持图片的宽高比并填充容器 */
        }
    </style>
</head>
<body>
    <!-- 当前周报 -->
    <h1 class="center-title">AI周报(0118-0124)</h1>
    <div>
        <p class="sub-title">1、XXX</p>
        <details>
            <summary>点击展开内容</summary>
            <!-- 图片容器 -->
            <div class="image-container">
                <img src="./探一下.jpg" alt="描述图片的文字">
            </div>
        </details>
        <p class="sub-title">2、XXX</p>
        <details>
            <summary>点击展开内容</summary>
            <p>xxxx</p>
        </details>
    </div>

    <!-- 往期周报 -->
    <h1 class="center-title">往期周报</h1>
    <div>
        <p class="sub-title">1、AI周报(0110-0117)</p>
        <details>
            <summary>简要内容</summary>
            <p>AI应用——京东健康发布医院全场景应用大模型， 面向患者、医生、医院</p>
            <p>AI应用——阿里推出图生视频应用，面向商家的电商商品视频智造</p>
            <p>AI模型——科大讯飞发布国内首个端到端语音同传大模型，未来赋能翻译行业工作提效</p>
            <p>AI模型——面壁智能再推端侧模型，模型压缩挑战内存、功耗、算力三座大山</p>
        </details>
    </div>
</body>
</html>
