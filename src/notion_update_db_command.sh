db_id="${args[db_id]}"
input_file="${args[input]}"
config="${args[--config]}"

echo "Updating Notion Database..."

python update_notion_db.py --input "${input_file}" --config $config --database $db_id --token $NOTION_API_KEY