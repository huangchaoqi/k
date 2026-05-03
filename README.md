# 城市二手住宅房价 K 线图

这是一个静态网页，展示城市二手住宅价格指数换算后的估算房价 K 线，并叠加 EMA10、EMA21、SMA50、ATR、ADR 等指标。

当前同口径指数数据覆盖：

- 上海
- 南京
- 成都
- 昆明
- 广州
- 深圳

珠海不在当前 AkShare / 东方财富这个国家统计局 70 城住宅销售价格指数接口的同口径城市序列中，因此页面里暂保留为不可选提示。

## 本地文件

- `index.html`：用于 GitHub Pages / Netlify / Vercel 的默认首页，数据已内嵌。
- `shanghai-house-price-kline-single.html`：单文件分享版，和 `index.html` 内容相同。
- `shanghai-house-price-kline.html`：开发版页面，读取 `shanghai-house-price-data.js`。
- `shanghai-house-price-data.js`：由脚本生成的多城市二手住宅指数数据。
- `build_shanghai_house_price_data.py`：联网抓取并生成数据文件。
- `make_single_file.py`：把数据嵌入 HTML，生成 `index.html` 和单文件版。

## 数据口径

指数数据来自 AkShare 的中国新房价指数接口，源站为东方财富宏观数据并整理自国家统计局 70 个大中城市住宅销售价格指数。

网页中的房价是以页面里的“基准月份 + 基准均价”作为锚点，将指数序列按比例换算得到的估算均价，单位为元/平方米。它不是每个月官方发布的真实成交均价。

## 自动更新

`.github/workflows/update-and-deploy.yml` 会：

1. 每月 20 日 10:30（中国/珀斯时间）自动运行。
2. 安装 Python 依赖。
3. 执行 `build_shanghai_house_price_data.py` 抓取最新数据。
4. 执行 `make_single_file.py` 生成 `index.html`。
5. 如果数据有变化，自动提交回 GitHub。
6. 部署到 GitHub Pages。

也可以在 GitHub 仓库的 **Actions** 页面手动运行 `Update City House Price Chart`。

## 发布到 GitHub Pages

1. 在 GitHub 新建一个仓库。
2. 把本文件夹内容推送到仓库。
3. 进入仓库的 **Settings → Pages**。
4. 在 **Build and deployment** 里选择 **GitHub Actions**。
5. 到 **Actions** 页面手动运行一次 `Update City House Price Chart`。

运行完成后，GitHub Pages 会给出一个公网 URL，手机浏览器可以直接打开。
