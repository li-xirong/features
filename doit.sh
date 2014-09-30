rootpath='./'
collection='toyset'
overwrite=1

python generate_id_path_file.py $collection --overwrite $overwrite --rootpath $rootpath
python docolor64.py             $collection --overwrite $overwrite --rootpath $rootpath



