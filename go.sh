for file in data/corriere.it/dizionario_italiano.json : do
  mv $file $file.old
done

wget http://www.istat.it/it/files/2011/01/Elenco-codici-statistici-e-denominazioni-al-01_07_2016.csv

scrapy crawl dizionario_italiano_corriere -t jsonlines -o data/corriere.it/dizionario_italiano.json
