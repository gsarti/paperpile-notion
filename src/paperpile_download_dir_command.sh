dir_id="${args[dir_id]}"
cookies_path="${args[--cookies_path]}"

echo "Exporting CSV from Paperpile..."

if [ -z ${COOKIES_PWD+x} ]; then
    python download_paperpile_dir.py --username $GOOGLE_MAIL --password $GOOGLE_PWD --folder_id $dir_id --cookies_path "${cookies_path}"
else
    python download_paperpile_dir.py --username $GOOGLE_MAIL --password $GOOGLE_PWD --folder_id $dir_id --cookies_path "${cookies_path}" --cookies_pwd $COOKIES_PWD
fi