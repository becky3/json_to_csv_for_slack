# json_to_csv_for_slack
Convert to csv from exported json data in slack service.

Qiitaに日本語でも記事を書いています
https://qiita.com/beckyJPN/items/4c94a35587d51a0fba0c

# Environment

- OS: macOS Monterey (12.5)
- python: 3.10.5

# Export json file

check for [official site](https://slack.com/intl/ja-jp/help/articles/201658943-%E3%83%AF%E3%83%BC%E3%82%AF%E3%82%B9%E3%83%9A%E3%83%BC%E3%82%B9%E3%81%AE%E3%83%87%E3%83%BC%E3%82%BF%E3%82%92%E3%82%A8%E3%82%AF%E3%82%B9%E3%83%9D%E3%83%BC%E3%83%88%E3%81%99%E3%82%8B).

# How to use

Because there is a file called `converter.py`
In the terminal, 
specify the top folder of the exported data expanded by slack 
with the full path in the first argument as shown below, 
and execute it with python.

```sh
$ python converter.ph /Users/username/Desktop/my_workspace
```

After execution, a folder name slack_csv_output will be created in parallel with the specified folder.
A file called `channel_name.csv` is created in it.
If there is already a folder with the same name, an error will occur, so delete it in advance.

Columns are created in each csv with the following correspondence, and each message is converted as a row.
`date` > Post date (obtained from file name)
`name` > full name or display name
`text` > Posted message
`files` > URL of attached file (If there are multiple attachments, display them with line breaks)
