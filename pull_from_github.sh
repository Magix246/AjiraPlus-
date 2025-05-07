#!/data/data/com.termux/files/usr/bin/bash

# Nenda kwenye folder la project
cd ~/AjiraPlus- || {
  echo "📁 Folder AjiraPlus- haipatikani"; exit 1;
}

# Hakikisha kila kitu kiko safi kabla ya pull
git status

# Fanya pull kutoka GitHub main branch
git pull origin main
