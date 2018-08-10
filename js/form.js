//

var symptomsProblemAreas = {
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

	SPA_INTP: "Intimacy problems",
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