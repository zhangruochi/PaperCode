#!/usr/bin/perl -w
use strict;
my$tline="";
my@tlist=();
my$tempi=0;
my$tempj=0;
my$tempk=0;
my$pline="";
my@plist=();
my$tid=0;
my%tidx=();
my$egDirScript="/home/xynlab/zhouff/work/script_app";
my$egDirGenomes="/db/ncbi-genomes-bacteria/Bacteria";
@ARGV==3 or die""."Error in syntax!\n"."   ./getMCL.all-against-all.pl <sequences.fasta> <FileOut.dat> <DirTemp>\n";
my$egFileIn=$ARGV[0];
my$egFileOut=$ARGV[1];
my$egDirTemp=$ARGV[2];
@tlist=split(/\//,$egFileIn);
$tline=$tlist[@tlist-1];
my$egFileTag="$tline.all-against-all.blastn";
print"Mapping ... ";
if(system("formatdb -p F -i \"$egFileIn\" >/dev/null")or system("blastall -p blastn -d \"$egFileIn\" -i \"$egFileIn\" -o \"$egDirTemp/$egFileTag\" >/dev/null")){die"-Error occured!\n";}print" [done]\n";
print"Clustering ... ";
if(chdir("$egDirTemp")){}else{die"<br>--------------[Directory not changed]------------------------<br>\n";}my$egCmdLine="mclblastline --blast-score=b --blast-bcut=5 --mcl-I=2.5 \"$egFileTag\"";
if(system("$egCmdLine 2>/dev/null 1>/dev/null")){die"~Error occured!\n---[$egCmdLine]---\n";}print" [done]\n";
chdir("..");
my%egName2ID=();
my%egID2Name=();
print"Loading name mapping ... ";
open(efIn,"$egDirTemp/$egFileTag.tab")or die"Error when loading TAB data!\n";
while(<efIn>){$tline=$_;
$tline=~s/[\r\n]//g;
@tlist=split(/\s+/,$tline,2);
if($tline=~/^#/){}elsif((defined$tlist[0])and(defined$tlist[1])){@plist=split(/,/,$tlist[1]);
if(!(defined$plist[0])){$plist[0]="-";}if(!(defined$plist[1])){$plist[1]="-";}if(!(defined$plist[2])){$plist[2]="-";}$egID2Name{"$tlist[0]"}=$tlist[1];
$egName2ID{"$tlist[1]"}=$tlist[0];}}close(efIn);
print" [done] [Number:".(scalar keys%egName2ID)."]\n";
my$egID=-1;
my$egName="";
print"Loading MCL clusters ... ";
my$egFileMCL="$egDirTemp/out.$egFileTag.I25s2";
if(!(-e$egFileMCL)){$egFileMCL="$egDirTemp/out.$egFileTag.I25";}open(efIn,"$egFileMCL")or die"Error when loading [I25s2] MCL clusters [$egFileMCL]!\n";
while(<efIn>){if($_=~/^\(mclmatrix$/){last;}}while(<efIn>){if($_=~/^begin$/){last;}}my%egID2Cluster=();
while(<efIn>){if($_=~/^\)$/){last;}elsif($_=~/^\(mclruninfo$/){last;}elsif($_=~/^(\d+)\s+([\d\s\$]+)$/){lbNextTag:$tid=$1;
$tline=$2;
$tline=~s/[\r\n]//g;
if($tline=~/\$$/){}else{while(<efIn>){$tline=$tline." ".$_;
$tline=~s/[\r\n]//g;
if($_=~/\$$/){last;}elsif($_=~/^(\d+)\s+([\d\s\$]+)$/){if((defined$tid)and($tid>=0)){$tline=~s/\s*\$$//g;
$tline=~s/\s+/ /g;
$tline=~s/^\s+//g;
$tline=~s/\s+$//g;
$egID2Cluster{"$tid"}=$tline;}goto lbNextTag;}}}if((defined$tid)and($tid>=0)){$tline=~s/\s*\$$//g;
$tline=~s/\s+/ /g;
$tline=~s/^\s+//g;
$tline=~s/\s+$//g;
$egID2Cluster{"$tid"}=$tline;}}}close(efIn);
print" [done] [ClusterNum:".(scalar keys%egID2Cluster)."]\n";
my%tMatchedID=();
print"Saving clusters ... ";
if($egFileOut=~/\//){}else{$egFileOut="$egDirTemp/$egFileOut";}open(efOut,">$egFileOut")or die"Error when saving clusters!\n";
print efOut "#ClusterID ID  Org RefSeq\n";
@tlist=keys%egID2Cluster;
for($tempi=0;$tempi<@tlist;$tempi++){@plist=split(/\s+/,$egID2Cluster{"$tlist[$tempi]"});
%tidx=();
for($tempj=0;$tempj<@plist;$tempj++){$tid=$egID2Name{"$plist[$tempj]"};
$tMatchedID{"$plist[$tempj]"}=1;
$tidx{"$tid"}=1;}@plist=keys%tidx;
for($tempj=0;$tempj<@plist;$tempj++){if(!(defined$pline)){print"------------[$plist[$tempj] => [$pline]]------------\n";}my@qlist=split(/,/,$plist[$tempj]);
if(!(defined$qlist[1])){$qlist[1]="-";}if(!(defined$qlist[2])){$qlist[2]="-";}print efOut "$tempi	$qlist[0]	$qlist[1]	$qlist[2]\n";}}@tlist=keys%egID2Name;
for($tempk=0;$tempk<@tlist;$tempk++){if(!(defined$tMatchedID{"$tlist[$tempk]"})){my@qlist=split(/,/,$egID2Name{"$tlist[$tempk]"});
if(!(defined$qlist[1])){$qlist[1]="-";}if(!(defined$qlist[2])){$qlist[2]="-";}print efOut "$tempi	$qlist[0]	$qlist[1]	$qlist[2]\n";
$tempi++;}}close(efOut);
print" [done]\n";