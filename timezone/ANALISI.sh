python3 ANALISI_ORARIA.py &&
python3 ANALISI_3HR.py &&
python3 ANALISI_6HR.py &&
python3 ANALISI_12HR.py &&
python3 ANALISI_24HR.py &&
python3 ANALISI_4D.py

python3 ANALISI_ORARIA.py 1 &&
python3 ANALISI_3HR.py 1 &&
python3 ANALISI_6HR.py 1 &&
python3 ANALISI_12HR.py 1 &&
python3 ANALISI_24HR.py 1 &&
python3 ANALISI_4D.py 1
mkdir out/homepage_no_ansa
mv ANALISI_*.png out/homepage_no_ansa/

python3 ANALISI_ORARIA.py 2 &&
python3 ANALISI_3HR.py 2 &&
python3 ANALISI_6HR.py 2 &&
python3 ANALISI_12HR.py 2 &&
python3 ANALISI_24HR.py 2 &&
python3 ANALISI_4D.py 2
mkdir out/homepage_no_agi
mv ANALISI_*.png out/homepage_no_agi/

python3 ANALISI_ORARIA.py 2 1 &&
python3 ANALISI_3HR.py 2 1 &&
python3 ANALISI_6HR.py 2 1 &&
python3 ANALISI_12HR.py 2 1 &&
python3 ANALISI_24HR.py 2 1 &&
python3 ANALISI_4D.py 2 1
mkdir out/homepage_no_ita
mv ANALISI_*.png out/homepage_no_ita/