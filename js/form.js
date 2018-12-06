//

var PITextArray = [
	"name", //ro
	"dob", //ro
	"insurance", //ro
	"patient_id", //ro
	"diag",
	"diag_code",
	"diag_2",
	"diag_2_code"
]; // 6

var SICheckArray = [
	"no_new_issue",
]; // 1

var SITextArray = [
	"date",
	"seshNo", //ro
	"modality",
	"new_issue",
]; // 4

var RACheckArray = [
	"RA_none",

	"RA_self_idea",
	"RA_self_plan",
	"RA_self_att",

	"RA_others_idea",
	"RA_others_plan",
	"RA_others_att",

	"RA_prop_idea",
	"RA_prop_plan",
	"RA_prop_att",
]; // 10

var TITextArray = [
	"TI_other_txt",
]; // 1

var GCheckArray = [
	"G_1_impr",
	"G_1_decr",
	"G_2_impr",
	"G_2_decr",
	"G_3_impr",
	"G_3_decr",
	"G_cop_skills",
	"G_sc_skills",
	"G_id_res",
	"G_expr",
	"G_verb",
]; // 9

var GTextArray = [
	"G_1_impr_txt",
	"G_1_decr_txt",
	"G_2_impr_txt",
	"G_2_decr_txt",
	"G_3_impr_txt",
	"G_3_decr_txt",
	"G_other_txt",
]; // 5

var SPATextArray = [
	"SPA_other_txt",
]; // 1

var notesArray = [
	"notes",
]; // 1

var ASSTextArray = [
	"ASS_CONST",
	"ASS_INSIG",
	"ASS_EFFRT",
	"ASS_OR",
	"ASS_present",
	"ASS_present_txt",
	"ASS_ABLE",
	"ASS_COOP",
	"ASS_other_txt",
]; // 9

var PLNCheckArray = [
	"PLN_PSY",
]; //1

var PLNTextArray = [
	"PLN_CONT",
	"PLN_FREQ",
	"PLN_NXT",
	"PLN_other_txt",
]; // 4

// utility functions to build the form

/*
if check, text is clear
if text != "", uncheck
*/
function associateCheckText(chk, txt){
	$('input[name="'+chk+'"]').change(function(){
		if (this.checked){
			$('input[name="'+txt+'"]').val("")
		}
	})
	$('input[name="'+txt+'"]').change(function(){
		if (this.value==""){
			document.getElementsByName(chk)[0].checked = true;
		}
		else {
			document.getElementsByName(chk)[0].checked = false;
		}
	})
}

/*
if text != "", check
*/
function linkTextCheck(chk, txt){
	$('input[name="'+txt+'"]').change(function(){
		document.getElementsByName(chk)[0].checked = (this.value != "");
	})	
}

function addOtherToList(selection, name){
	selection.append('li')
		.classed('list-group-item',true)
		.text('Other')
		.append('input')
		.attr('type','text')
		.attr('name',name)
		.attr('id',name)
		.classed('form-control',true)
}

function createFormSectionArr(id, data){
	d3.select(id)//.select('ul')
	  .selectAll('li')
	  .data(data)
	  .enter()
	  .append('li')
	  .classed('list-group-item',true)
	  .append('input')
	  .attr('type','checkbox')
	  .attr('disabled',true)
	  .attr('name', (d) => d[0]);
	d3.select(id)
	  .selectAll('li')
	  .data(data)
	  .append('span')
	  .text((d) => (" " + d[1]));
}