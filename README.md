# JPEGフィルターのプロトタイプ
単純にJPEGを受け取り、フィルターをかけ、JPEGを送信する。

## PyAudioの準備
PyAudioの準備

### Macの場合

```bash
brew install portaudio
```

### Ubuntuの場合

```bash
sudo apt-get install portaudio19-dev
```

## 環境構築


poetryをインストールしておく

```bash
poetry install
```

## 環境変数

`pyproject.toml`と同じ階層に`.env`を置く

```
# filter.pyで待ち受けるアドレス
FILTER_MY_IP="127.0.0.1"
FILTER_MY_PORT="5005"
# filter.pyからの送信先アドレス
FILTER_YOUR_IP="127.0.0.1"
FILTER_YOUR_PORT="5006"
# filter.pyで使うJPEGの品質
FILTER_JPEG_QUALITY="80"

# sender.pyでファイルから読み込むか？
FILTER_FROM_FILE="1"
# sender.pyやfilter.pyでつかうVIDEOのINDEX
FILTER_VIDEO_INDEX="0"
# filter.pyでつかうAUDIOのINDEX
FILTER_AUDIO_INDEX="0"
# sender.pyの画像幅
FILTER_IMAGE_WIDTH="480"
# sender.pyの画像高さ
FILTER_IMAGE_HEIGHT="270"
# sender.pyのFPS
FILTER_FPS="30"

# receiver.pyでファイルへ書き込むか？
FILTER_TO_FILE="1"

```

## 実行

最後から順番に実行する。

```bash
poetry run python ./jpeg_filter_prototype/receiver.py
```

cannyの場合
```bash
poetry run python ./jpeg_filter_prototype/filter_canny.py
```

```bash
poetry run python ./jpeg_filter_prototype/sender.py
```
