dir_id="${args[dir_id]}"

echo "Exporting CSV from Paperpile..."

python download_paperpile_dir.py --username $GOOGLE_MAIL --password $GOOGLE_PWD --folder_id $dir_id

echo "Done!"