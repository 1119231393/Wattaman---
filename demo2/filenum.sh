function funNumfile(){
	find $1 -name "*_gt.json" | wc -l
}

funNumfile ./ss
