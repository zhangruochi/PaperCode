#! /bin/sh

echo 'add execute mode for  R files'
cd  $1
cd core

chmod -R  +x *
ls -l 
#cd ..

#echo 'delete old files'
#rm *matrix_table*
#rm *gdm*
#rm *ci*
#ls -l 
