LINK=$1
mkdir $LINK 2>/dev/null;
cd $LINK;
mkdir current 2>/dev/null;
mkdir past 2>/dev/null;
cd current/
httrack --continue $LINK >>/dev/null

for file in "*" ; do
  if ! -d $file ; then
    sed -E 's/[0-9]{2}:[0-9]{2}:[0-9]{2}//' $file;
  fi
done
cd ..
DIFFCOUNT=$(diff -r current/ past/ | wc -l)
echo $DIFFCOUNT > current/diffcount.txt

if [ -z past/diffcount.txt ]; then
  DIFFCOUNTPAST=-1;
fi
DIFFCOUNTPAST=$(cat past/diffcount.txt);
DATE=$(date '+%Y-%m-%d');
NUM=0;

if [ $DIFFCOUNT -eq $DIFFCOUNTPAST ]; then
  echo "EQUAL $DIFFCOUNT -eq $DIFFCOUNTPAST"
  echo $DATE,$((NUM+1)) > current/date.txt
elif [ "past/diffcount.txt" -ot "current/diffcount.txt" ]; then
  echo "1 ago $DIFFCOUNT -eq $DIFFCOUNTPAST"
  diff -r current/ past/
  IFS=,
  while read DATES NUMS
  do
  echo $DATES,$((NUMS+1)) > current/date.txt
  done < current/date.txt

  cp -a current/* past/
fi
