for file in data/corriere.it/dizionario_italiano.json : do
  mv $file $file.old
done

scrapy crawl dizionario_italiano_corriere -t jsonlines -o data/corriere.it/dizionario_italiano.json
