dir_id="${args[dir_id]}"
db_id="${args[db_id]}"
config="${args[--config]}"
input_dir="${args[--input_dir]}"

echo "Exporting CSV from Paperpile..."

python download_paperpile_dir.py --username $GOOGLE_MAIL --password $GOOGLE_PWD --folder_id $dir_id

input_file=$(find "${input_dir}" -name '*.csv' -print0 | xargs -r -0 ls -1 -t | head -1)

echo "Updating Notion Database..."

python update_notion_db.py --input "${input_file}" --config $config --database $db_id --token $NOTION_API_KEY

rm "${input_file}"