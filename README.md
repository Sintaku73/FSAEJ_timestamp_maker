# FSAEJ-timestamp-maker

学生フォーミュラ日本大会のYouTube配信にタイムスタンプを作成することを補助するツールです。

## Getting Started

### Prerequisites

- [Python](https://www.python.org/)
- [pandas](https://pandas.pydata.org/)

Pythonの環境構築後、下記コマンドで必要なライブラリをインストールしてください。

```bash
pip install pandas
```

本ツールを使用するにあたってYouTube配信に対応する現実の時間を把握する必要があります。必要に応じて[YouTubeLiveClock](https://chromewebstore.google.com/detail/youtubeliveclock/chpodcedholiggcllnmmjlnghllddgmj)などのブラウザ拡張機能をご利用ください。

### Installing

```bash
git clone https://github.com/Sintaku73/FSAEJ-timestamp-maker.git
```

## Usage and Examples

このツールの使い方は下記の通りです。

1. タイムスタンプを作成する種目によって使用するスクリプトを選択してください。以降は選択したスクリプトに対して手順を実行してください。  
   エンデュランス以外→`FSAEJ_timestamp_maker.py`  
   エンデュランス→`FSAEJ_timestamp_maker_endurance.py`
2. 変数`url`に対象種目の公式ライブタイミングURLを指定してください。
3. 変数`reference_timestamp`に対象の配信で基準とするタイムスタンプを指定してください。
4. 変数`reference_time`に基準のタイムスタンプに対応する時刻を指定してください。  
   ブラウザの拡張機能[^ext]などで確認することができます。
5. 変数`live_delay`でライブタイミングに対する配信時刻のずれを補正してください。
6. スクリプトを実行すると`/out`ディレクトリ内に実行結果が保存されます。

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## References

[^ext]: [YouTubeLiveClock](https://chromewebstore.google.com/detail/youtubeliveclock/chpodcedholiggcllnmmjlnghllddgmj)
