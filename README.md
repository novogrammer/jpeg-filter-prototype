# JPEGフィルターのプロトタイプ
単純にJPEGを受け取り、フィルターをかけ、JPEGを送信する。

## 環境構築
poetryをインストールしておく

```
poetry install
```

## 環境変数

`pyproject.toml`と同じ階層に`.env`を置く

```
# filter.pyで待ち受けるアドレス
FILTER_MY_IP="127.0.0.1"
FILTER_MY_PORT="5000"
# filter.pyからの送信先アドレス
FILTER_YOUR_IP="127.0.0.1"
FILTER_YOUR_PORT="5001"

```

## 実行

最後から順番に実行する。

```
poetry run python ./jpeg_filter_prototype/receiver.py
```
```
poetry run python ./jpeg_filter_prototype/filter.py
```
```
poetry run python ./jpeg_filter_prototype/sender.py
```
