#uso: 
#gnuplot -e "titleparam='Evolution of the error during the training process. Sigmoid activation';BRAFmut='log/ERR-BRAFmut.txt';NRASmut='log/ERR-NRASmut.txt'" error-evolution.plot
#set term pdf color solid enhanced
#set output "log/error-evolution.pdf"
set terminal png
set output 'out-plot.png'

set grid
set style data lines 

set yrange [-1:]
set ylabel "error in %"
set xlabel "epoch"

if (!exists("titleparam")) titleparam = "Evolution of the error during the training process"
set title titleparam

if (!exists("file1")) file1 = "log/ERR-BRAFmut.txt"
if (!exists("file2")) file2 = "log/ERR-NRASmut.txt"

plot BRAFmut using 0:9, NRASmut using 0:9
#plot BRAFmut using 0:9

pause -1 "Press ENTER to finish ... "
