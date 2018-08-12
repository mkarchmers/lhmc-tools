//

var PITextArray = [
	"fname", //ro
	"lname", //ro
	"dob", //ro
	"insurance", //ro
	"patient_id", //ro
	"diag",
	"diag_code",
]; // 7

var SITextArray = [
	"seshdate",
	"seshNo", //ro
	"modality",
	"newIssue",
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


var TICheckDict = {

	TI_refl_listen: "Reflective Listening",
	TI_encour: "Encouragement",
	TI_decis_balnc: "Decisional Balancing",
	TI_prob_solv: "Problem Solving",
	TI_pos_reinforce: "Positive Reinforcemnt",
	TI_explore: "Exploring",
	TI_play_therapy: "Play Therapy",
	TI_valid: "Validation",
	TI_conf_behav: "Confronting of Behaviors",
	TI_real_test: "Reality Testing",
	TI_PSCR: "Provide Safe Consistent Relationship",
	TI_CSB: "Communication Skill Building",
	TI_PSB: "Parenting Skill Building",
	TI_emot_supp: "Emotional Supportiveness",
}; // 14


var TITextArray = [
	"TI_other_txt",
]; // 1

var GCheckArray = [
	"G_1_impr",
	"G_1_decr",
	"G_2_impr",
	"G_2_decr",
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
	"G_other_txt",
]; // 5

var SPACheckDict = {

	SPA_AX: "Anxiousness",
	SPA_EW: "Excessive worry",
	SPA_HV: "Hyper Vigilance",
	SPA_DRT: "Disturbing rememberances of trauma",
	SPA_SM: "Sad mood",
	SPA_DM: "Depressed mood",
	SPA_RRA: "Restricted range of affet",
	
	SPA_ML: "Mood liability",
	SPA_MUT: "Mood upset / tearfulness",
	SPA_S: "Stress",
	SPA_LF: "Lonely feelings",
	SPA_I: "Isolation",
	SPA_LI: "Loss of interest",

	SPA_FA: "Flat affect",
	SPA_MS: "Monotone speech",
	SPA_PS: "Preassured speech",
	SPA_LE: "Low energy",
	SPA_LM: "Low motivation",

	SPA_ANG: "Anger",
	SPA_IRR: "Irritability",
	SPA_ARG: "Argumentative",
	SPA_AGI: "Agitation",
	SPA_FRU: "Frustration",

	SPA_GF: "Guilt feelings",
	SPA_OT: "Obsessive thinking",
	SPA_PER: "Perseveration",
	SPA_INT: "Intellectualization",

	SPA_AHA: "Auditory hallucinations",
	SPA_VHA: "Visual hallucinations",
	SPA_DIT: "Disorganized thinking",

	SPA_PAP: "Poor appetite",
	SPA_PSL: "Poor sleep",
	SPA_PSC: "Poor self care",
	SPA_PHY: "Poor hygiene",

	SPA_INTP: "Interpersonal problems",
	SPA_FDP: "Family dynamic problems",
	SPA_MARC: "Marital conflict",
	SPA_SIDI: "Sibling discord",
	SPA_PACH: "Parental challenges",

	SPA_INTI: "Intimacy problems",
	SPA_PSEC: "Poor self esteem / confidence",
	SPA_HSC: "Harsh self criticism",

	SPA_WPP: "Work performance problems",
	SPA_WSTR: "Work stress",
	SPA_SPP: "School performance problems",
	SPA_SSTR: "School stress",

	SPA_MOTREST: "Motor restlessness",
	SPA_EABOR: "Easily bored",
	SPA_DWF: "Difficulty with focus",
	SPA_IMPU: "Impulsivity",
	SPA_DIFTRAN: "Difficuly transitioning",
	SPA_ACTOUT: "Acting out",

	SPA_ALCHUSE: "Alcohol use",
	SPA_DRGUSE: "Drug use",
	SPA_RECREL: "Recent relapse",
	SPA_URGSUSE: "Urges to use",

	SPA_FINDIF: "Financial Difficulties",
	SPA_MEDDIF: "Medical problems",
	SPA_MEDNC: "Medication non-compliance",
} // 59

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

var PLNTextArray = [
	"PLN_CONT",
	"PLN_FREQ",
	"PLN_PSY",
	"PLN_NXT",
	"PLN_other_txt",
]; // 5



// utility functions to build the form

function associateCheckText(chk, txt){
	$('input[name='+chk+']').change(function(){
		$('input[name='+txt+']').toggle(this.checked);
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

function createFormSection(id, data){
	d3.select(id).select('ul')
	  .selectAll('li')
	  .data(Object.entries(data))
	  .enter()
	  .append('li')
	  .classed('list-group-item',true)
	  .append('input')
	  .attr('type','checkbox')
	  .attr('disabled',true)
	  .attr('name',function(d){return d[0]});
	d3.select(id)
	  .selectAll('li')
	  .data(Object.entries(data))
	  .append('span')
	  .text(function(d){return " " + d[1]});
}