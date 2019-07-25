/*
*
*/
var Codes = function(){
	var codes = {};

    function load_codes(){

      return $.getJSON('/codes',
      //https://clinicaltables.nlm.nih.gov/api/icd10cm/v3/search?sf=code&terms=F3&maxList=500',  
        function(data){

          data['codes'].forEach(function(x){codes[x[0]]=x[1]})
      })
    }

	return {
		codes: codes,
		load: load_codes,
	}
}()
