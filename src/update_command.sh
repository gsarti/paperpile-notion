input_dir="${args[--input_dir]}"

cli_paperpile_download_dir_command "$@"

args[input]=$(find "${input_dir}" -name '*.csv' -print0 | xargs -r -0 ls -1 -t | head -1)

cli_notion_update_db_command "$@"